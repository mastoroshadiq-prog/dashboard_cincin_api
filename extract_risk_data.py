"""
Extract complete risk metrics from multiple sources:
1. Attack Rate from tabelNDREnew.csv (NDRE stress class)
2. SPH from data_gabungan.xlsx
3. Loss estimated from gap yield

Output: complete_risk_data.json
"""

import pandas as pd
import json

print("="*60)
print("EXTRACTING COMPLETE RISK DATA")
print("="*60)

# 1. Load NDRE data for attack rate
print("\n[1] Loading tabelNDREnew.csv...")
ndre_df = pd.read_csv('data/input/tabelNDREnew.csv')
print(f"   Rows: {len(ndre_df)}")

# Map stress class to attack rate estimate
# Based on NDRE stress levels:
# - Stres Ringan → ~5% attack rate (Stadium 1)
# - Stres Sedang → ~15% attack rate (Stadium 2-3)
# - Stres Berat → ~25% attack rate (Stadium 3)
# - Stres Sangat Berat → ~40% attack rate (Stadium 4)
stress_to_ar = {
    'Stres Ringan': 5.0,
    'Stres Sedang': 15.0,
    'Stres Berat': 25.0,
    'Stres Sangat Berat': 40.0,
    'Stres\xa0Sangat\xa0Berat': 40.0,  # Non-breaking space variant
    '-': 0.0
}

# Aggregate by block - get majority stress class
block_stress = ndre_df.groupby('blok_b')['klassndre12025'].apply(
    lambda x: x.value_counts().index[0] if len(x) > 0 else '-'
).to_dict()

# Also get NDRE value average per block (convert to numeric first)
ndre_df['ndre125_num'] = pd.to_numeric(ndre_df['ndre125'], errors='coerce')
block_ndre = ndre_df.groupby('blok_b')['ndre125_num'].mean().to_dict()

print(f"   Unique blocks with NDRE data: {len(block_stress)}")

# Build attack rate dict
attack_rate_data = {}
for block, stress in block_stress.items():
    ar = stress_to_ar.get(stress, 10.0)  # Default 10% if unknown
    attack_rate_data[block] = {
        'attack_rate': ar,
        'stress_class': stress,
        'ndre_avg': block_ndre.get(block, 0.0)
    }

print(f"   Sample: D001A -> {attack_rate_data.get('D001A', 'N/A')}")

# 2. Load SPH data from data_gabungan.xlsx
print("\n[2] Loading data_gabungan.xlsx for SPH...")
try:
    gabung_df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)
    
    # Find block code column and SPH column
    # Based on inspection: block might be in early columns, SPH at col 33
    # Need to find block code - look for pattern like "D001A", "E002A" etc
    
    # Check row 10 onwards for data
    sph_col = 33
    
    # Find block code column - search for block patterns
    block_col = None
    for col in range(10):
        sample_vals = gabung_df.iloc[10:20, col].astype(str).tolist()
        if any(len(v) == 5 and v[0].isalpha() and v[-1].isalpha() for v in sample_vals):
            block_col = col
            break
    
    if block_col is None:
        # Try finding column with block names
        for row in range(10, 20):
            for col in range(20):
                val = str(gabung_df.iloc[row, col])
                if len(val) == 5 and val[0].isalpha():
                    block_col = col
                    print(f"   Found block column at col {col}, sample: {val}")
                    break
            if block_col:
                break
    
    # Extract SPH data
    sph_data = {}
    if block_col is not None:
        for i in range(10, len(gabung_df)):
            block = str(gabung_df.iloc[i, block_col]).strip()
            sph_val = gabung_df.iloc[i, sph_col]
            if len(block) >= 4 and block[0].isalpha():
                try:
                    sph = float(sph_val) if pd.notna(sph_val) else 0
                    sph_data[block] = sph
                except:
                    pass
    
    print(f"   Blocks with SPH data: {len(sph_data)}")
    if sph_data:
        sample_block = list(sph_data.keys())[0]
        print(f"   Sample: {sample_block} -> SPH {sph_data[sample_block]:.1f}")
except Exception as e:
    print(f"   Error loading SPH data: {e}")
    sph_data = {}

# 3. Load existing historical yields for gap/loss calculation
print("\n[3] Loading historical yields...")
with open('complete_historical_yields.json', 'r') as f:
    hist_data = json.load(f)
print(f"   Blocks: {len(hist_data)}")

# 4. Build complete risk data
print("\n[4] Building complete risk data...")
complete_risk = {}

for block_code, hist in hist_data.items():
    yields = hist.get('yields', {})
    y2025 = yields.get('2025', {})
    luas = hist.get('luas_ha', 0)
    
    # Get attack rate from NDRE
    ar_info = attack_rate_data.get(block_code, {})
    attack_rate = ar_info.get('attack_rate', 0)
    stress_class = ar_info.get('stress_class', '')
    
    # Get SPH
    sph = sph_data.get(block_code, 0)
    
    # If no SPH data, estimate based on year and area (typical 128-140 for healthy, lower for older)
    if sph == 0:
        # Estimate: older plantings have lower SPH
        tt = 2010  # Default
        # Rough estimate: 140 - (age * 2)
        sph = max(80, 140 - ((2025 - tt) * 2))
    
    # Calculate loss from gap
    real = y2025.get('real_ton_ha', 0)
    poten = y2025.get('poten_ton_ha', 0)
    gap_pct = y2025.get('gap_pct', 0)
    
    # Loss = gap_ton_ha * luas * price (Rp 1.5 juta/ton)
    gap_ton = abs(gap_pct * poten / 100) if poten > 0 else 0
    loss_value = gap_ton * luas * 1.5  # Rp juta
    
    # Determine stadium
    if attack_rate >= 30:
        stadium = 4
    elif attack_rate >= 15:
        stadium = 3
    elif attack_rate >= 5:
        stadium = 2
    else:
        stadium = 1
    
    complete_risk[block_code] = {
        'block_code': block_code,
        'attack_rate': round(attack_rate, 1),
        'sph': round(sph, 0),
        'stadium': stadium,
        'stress_class': stress_class,
        'loss_value_juta': round(loss_value, 1),
        'gap_pct': round(gap_pct, 1),
        'luas_ha': luas
    }

print(f"   Complete risk data: {len(complete_risk)} blocks")

# Show samples
print("\n   Samples:")
for block in ['D001A', 'E007A', 'F004A', 'A001A'][:4]:
    if block in complete_risk:
        r = complete_risk[block]
        print(f"   {block}: AR={r['attack_rate']}%, SPH={r['sph']}, Stadium={r['stadium']}, Loss=Rp{r['loss_value_juta']}Jt")

# 5. Save to JSON
print("\n[5] Saving complete_risk_data.json...")
with open('complete_risk_data.json', 'w') as f:
    json.dump(complete_risk, f, indent=2)
print(f"   Saved {len(complete_risk)} blocks")

print("\n" + "="*60)
print("COMPLETE!")
print("="*60)
