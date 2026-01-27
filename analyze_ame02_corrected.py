"""
AME02 PILOT ANALYSIS - CORRECTED VERSION
Menggunakan column index yang sudah di-verify: 170 (Real), 173 (Potensi), 176 (Gap)

Metrics:
1. Gap Yield = Potensi - Realisasi (dalam Ton)
2. Loss/Kerugian = Gap Yield (KG) × Harga TBS
3. Avg Attack Rate Ganoderma
4. Avg Yield per blok
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_FILE = Path("poac_sim/data/output/ame02_analysis.json")

# Fixed column indices (verified)
DIVISI_COL_IDX = 5          # Unnamed: 5
BLOK_COL_IDX = 8            # Unnamed: 8
GANO_STADIUM_12_IDX = 55    # Stadium 1&2
GANO_STADIUM_34_IDX = 56    # Stadium 3&4
GANO_TOTAL_IDX = 57         # Total Ganoderma
GANO_PCT_IDX = 58           # % Serangan

# 2025 Production columns (VERIFIED from KI)
REAL_TON_2025_IDX = 170     # Real Ton 2025
POT_TON_2025_IDX = 173      # Potensi Ton 2025
GAP_TON_2025_IDX = 176      # Gap (already calculated in Excel)

# SPH (Stand Per Hectare) column
SPH_COL_IDX = 54            # SPH (after PKK)

# SPH Standard range for oil palm
SPH_STANDARD_MIN = 130
SPH_STANDARD_MAX = 143

DEFAULT_TBS_PRICE = 2500    # Rupiah per KG

def format_currency(value):
    """Format Rupiah"""
    if value >= 1_000_000_000:
        return f"Rp {value/1_000_000_000:.2f} Miliar"
    elif value >= 1_000_000:
        return f"Rp {value/1_000_000:.2f} Juta"
    else:
        return f"Rp {value:,.0f}"

def analyze_ame02_pilot(tbs_price=DEFAULT_TBS_PRICE):
    """
    Analisa PILOT untuk AME02:
    - Gap Yield (Potensi - Realisasi)
    - Financial Loss
    - Ganoderma Attack Rate
    - Average Yield
    """
    
    print("=" * 80)
    print("ANALISA AME II (AME02) - PILOT PROJECT")
    print("=" * 80)
    
    # Load Excel
    print(f"\n[1/5] Loading data...")
    df = pd.read_excel(INPUT_FILE)
    print(f"      Total rows: {len(df)}, Total columns: {len(df.columns)}")
    
    # Filter AME02 (skip header rows - first 3 rows are headers)
    print(f"\n[2/5] Filtering AME02 data...")
    divisi_col = df.columns[DIVISI_COL_IDX]
    blok_col = df.columns[BLOK_COL_IDX]
    
    # Skip first 3 rows (headers) then filter
    ame02_data = df[df[divisi_col] == 'AME02'].copy()
    
    print(f"      AME02 blocks found: {len(ame02_data)}")
    
    if len(ame02_data) == 0:
        print("\n[ERROR] No AME02 data found!")
        return None
    
    # Extract production data
    print(f"\n[3/5] Extracting 2025 production data...")
    real_col = df.columns[REAL_TON_2025_IDX]
    pot_col = df.columns[POT_TON_2025_IDX]
    gap_col = df.columns[GAP_TON_2025_IDX]
    
    print(f"      Real Ton column: {real_col} (index {REAL_TON_2025_IDX})")
    print(f"      Potensi Ton column: {pot_col} (index {POT_TON_2025_IDX})")
    print(f"      Gap column: {gap_col} (index {GAP_TON_2025_IDX})")
    
    # Convert to numeric
    ame02_data['real_ton_2025'] = pd.to_numeric(ame02_data[real_col], errors='coerce').fillna(0)
    ame02_data['pot_ton_2025'] = pd.to_numeric(ame02_data[pot_col], errors='coerce').fillna(0)
    ame02_data['gap_ton_2025'] = pd.to_numeric(ame02_data[gap_col], errors='coerce').fillna(0)
    
    # Calculate gap: pot - real
    # User definition: positive gap = LOSS/DEFICIT (potensi > realisasi)
    ame02_data['gap_final'] = ame02_data['pot_ton_2025'] - ame02_data['real_ton_2025']
    
    # Calculate loss in Rupiah
    ame02_data['gap_kg'] = ame02_data['gap_final'] * 1000
    ame02_data['loss_rp'] = ame02_data['gap_kg'] * tbs_price
    
    # Aggregate metrics
    total_real_ton = ame02_data['real_ton_2025'].sum()
    total_pot_ton = ame02_data['pot_ton_2025'].sum()
    total_gap_ton = ame02_data['gap_final'].sum()
    total_gap_kg = total_gap_ton * 1000
    total_loss_rp = ame02_data['loss_rp'].sum()
    
    print(f"\n[4/5] Calculating Ganoderma & SPH metrics...")
    
    # Ganoderma - detailed breakdown
    gano_pct_col = df.columns[GANO_PCT_IDX]
    gano_stad_12_col = df.columns[GANO_STADIUM_12_IDX]
    gano_stad_34_col = df.columns[GANO_STADIUM_34_IDX]
    gano_total_col = df.columns[GANO_TOTAL_IDX]
    
    ame02_data['gano_pct'] = pd.to_numeric(ame02_data[gano_pct_col], errors='coerce').fillna(0)
    ame02_data['gano_stad_12'] = pd.to_numeric(ame02_data[gano_stad_12_col], errors='coerce').fillna(0)
    ame02_data['gano_stad_34'] = pd.to_numeric(ame02_data[gano_stad_34_col], errors='coerce').fillna(0)
    ame02_data['gano_total'] = pd.to_numeric(ame02_data[gano_total_col], errors='coerce').fillna(0)
    
    avg_attack_rate = ame02_data['gano_pct'].mean() * 100  # to percentage
    blocks_with_gano = (ame02_data['gano_pct'] > 0).sum()
    total_gano_stad_12 = ame02_data['gano_stad_12'].sum()
    total_gano_stad_34 = ame02_data['gano_stad_34'].sum()
    total_gano_all = ame02_data['gano_total'].sum()
    
    # SPH Analysis
    sph_col = df.columns[SPH_COL_IDX]
    ame02_data['sph'] = pd.to_numeric(ame02_data[sph_col], errors='coerce').fillna(0)
    
    avg_sph = ame02_data['sph'].mean()
    min_sph = ame02_data['sph'].min()
    max_sph = ame02_data['sph'].max()
    
    # SPH categories
    blocks_below_standard = (ame02_data['sph'] < SPH_STANDARD_MIN).sum()
    blocks_within_standard = ((ame02_data['sph'] >= SPH_STANDARD_MIN) & (ame02_data['sph'] <= SPH_STANDARD_MAX)).sum()
    blocks_above_standard = (ame02_data['sph'] > SPH_STANDARD_MAX).sum()
    
    print(f"\n[5/5] Compiling results...")
    
    # Build result object
    results = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'division': 'AME02',
        'division_name': 'AME II',
        'total_blocks': len(ame02_data),
        'tbs_price_per_kg': tbs_price,
        'metrics': {
            'production': {
                'total_real_ton': float(total_real_ton),
                'total_pot_ton': float(total_pot_ton),
                'avg_real_per_block_ton': float(total_real_ton / len(ame02_data)),
                'avg_pot_per_block_ton': float(total_pot_ton / len(ame02_data)),
                'yield_efficiency_pct': float((total_real_ton / total_pot_ton * 100) if total_pot_ton > 0 else 0)
            },
            'gap_yield': {
                'total_gap_ton': float(total_gap_ton),
                'total_gap_kg': float(total_gap_kg),
                'avg_gap_per_block_ton': float(total_gap_ton / len(ame02_data)),
                'avg_gap_per_block_kg': float(total_gap_kg / len(ame02_data))
            },
            'financial_loss': {
                'tbs_price_rp_per_kg': tbs_price,
                'total_loss_rp': float(total_loss_rp),
                'total_loss_juta': float(total_loss_rp / 1_000_000),
                'total_loss_miliar': float(total_loss_rp / 1_000_000_000),
                'avg_loss_per_block_rp': float(total_loss_rp / len(ame02_data))
            },
            'ganoderma': {
                'avg_attack_rate_pct': float(avg_attack_rate),
                'blocks_with_ganoderma': int(blocks_with_gano),
                'blocks_clean': int(len(ame02_data) - blocks_with_gano),
                'infection_rate_pct': float((blocks_with_gano / len(ame02_data) * 100)),
                'total_trees_stadium_12': int(total_gano_stad_12),
                'total_trees_stadium_34': int(total_gano_stad_34),
                'total_trees_infected': int(total_gano_all),
                'severity_ratio_34_vs_12': float(total_gano_stad_34 / total_gano_stad_12) if total_gano_stad_12 > 0 else 0
            },
            'sph': {
                'avg_sph': float(avg_sph),
                'min_sph': float(min_sph),
                'max_sph': float(max_sph),
                'standard_range': f"{SPH_STANDARD_MIN}-{SPH_STANDARD_MAX}",
                'blocks_below_standard': int(blocks_below_standard),
                'blocks_within_standard': int(blocks_within_standard),
                'blocks_above_standard': int(blocks_above_standard),
                'status': 'Below Standard' if avg_sph < SPH_STANDARD_MIN else ('Above Standard' if avg_sph > SPH_STANDARD_MAX else 'Within Standard')
            }
        }
    }
    
    # Save JSON
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {OUTPUT_FILE}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("HASIL ANALISA AME II (AME02) - PILOT")
    print("=" * 80)
    
    print(f"\n📊 JUMLAH BLOK: {len(ame02_data)} blok")
    
    print(f"\n1️⃣ PRODUKSI 2025:")
    print(f"   Realisasi Total     : {total_real_ton:,.2f} Ton")
    print(f"   Potensi Total       : {total_pot_ton:,.2f} Ton")
    print(f"   Avg Realisasi/Blok  : {total_real_ton/len(ame02_data):,.2f} Ton")
    print(f"   Avg Potensi/Blok    : {total_pot_ton/len(ame02_data):,.2f} Ton")
    print(f"   Yield Efficiency    : {(total_real_ton/total_pot_ton*100) if total_pot_ton > 0 else 0:.2f}%")
    
    print(f"\n2️⃣ GAP YIELD (Deficit/Loss):")
    print(f"   Total Gap (Loss)    : {total_gap_ton:,.2f} Ton ({total_gap_kg:,.0f} KG)")
    print(f"   Avg Gap per Blok    : {total_gap_ton/len(ame02_data):,.2f} Ton")
    print(f"   Status              : {'✅ SURPLUS' if total_gap_ton < 0 else '❌ DEFICIT (Underperform)'}")
    
    print(f"\n3️⃣ KERUGIAN FINANCIAL:")
    print(f"   Harga TBS           : Rp {tbs_price:,}/KG")
    print(f"   Total Loss          : {format_currency(total_loss_rp)}")
    print(f"   Avg Loss per Blok   : {format_currency(total_loss_rp/len(ame02_data))}")
    
    print(f"\n4️⃣ GANODERMA ATTACK:")
    print(f"   Avg Attack Rate     : {avg_attack_rate:.2f}%")
    print(f"   Blok Terserang      : {blocks_with_gano} / {len(ame02_data)} ({blocks_with_gano/len(ame02_data)*100:.1f}%)")
    print(f"   Blok Bersih         : {len(ame02_data) - blocks_with_gano}")
    print(f"   Total Pohon Terinfeksi: {total_gano_all:,.0f} pohon")
    print(f"   Stadium 1 & 2 (Ringan): {total_gano_stad_12:,.0f} pohon")
    print(f"   Stadium 3 & 4 (Parah) : {total_gano_stad_34:,.0f} pohon")
    if total_gano_stad_12 > 0:
        severity_ratio = total_gano_stad_34 / total_gano_stad_12
        print(f"   Severity Ratio (3&4/1&2): {severity_ratio:.2f}x")
    
    print(f"\n5️⃣ SPH (STAND PER HECTARE):")
    print(f"   Avg SPH             : {avg_sph:.2f} pohon/Ha")
    print(f"   Range               : {min_sph:.0f} - {max_sph:.0f} pohon/Ha")
    print(f"   Standard Range      : {SPH_STANDARD_MIN}-{SPH_STANDARD_MAX} pohon/Ha")
    print(f"   Status              : ", end="")
    if avg_sph < SPH_STANDARD_MIN:
        print(f"⚠️ BELOW STANDARD")
    elif avg_sph > SPH_STANDARD_MAX:
        print(f"⚠️ ABOVE STANDARD")
    else:
        print(f"✅ WITHIN STANDARD")
    print(f"   Blok < Standard     : {blocks_below_standard} ({blocks_below_standard/len(ame02_data)*100:.1f}%)")
    print(f"   Blok dalam Standard : {blocks_within_standard} ({blocks_within_standard/len(ame02_data)*100:.1f}%)")
    print(f"   Blok > Standard     : {blocks_above_standard} ({blocks_above_standard/len(ame02_data)*100:.1f}%)")
    
    print("\n" + "=" * 80)
    print("✅ ANALISA SELESAI!")
    print("=" * 80)
    
    return results

def main():
    try:
        results = analyze_ame02_pilot()
        
        if results:
            print(f"\n✅ SUCCESS!")
            print(f"📄 JSON Output: {OUTPUT_FILE}")
        else:
            print("\n❌ FAILED!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
