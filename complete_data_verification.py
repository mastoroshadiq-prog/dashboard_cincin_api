import pandas as pd
import json

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Critical blocks
critical_blocks = ['D001A', 'D003A', 'D004A', 'E001A', 'E002A', 'E003A', 'E005A', 'E006A']

# Year data structure (found from investigation)
# Each year has: BJR Kg, Jum JJg, Ton (Real), BJR Kg, Jum JJg, Ton (Potensi), BJR Kg, Jum JJg, Ton (Real vs Potensi)
year_data = {
    2023: {
        'real_bjr': 150,
        'real_jjg': 151,
        'real_ton': 152,
        'poten_bjr': 153,
        'poten_jjg': 154,
        'poten_ton': 155,
    },
    2024: {
        'real_bjr': 159,
        'real_jjg': 160,
        'real_ton': 161,
        'poten_bjr': 162,
        'poten_jjg': 163,
        'poten_ton': 164,
    },
    2025: {
        'real_bjr': 168,
        'real_jjg': 169,
        'real_ton': 170,
        'poten_bjr': 171,
        'poten_jjg': 172,
        'poten_ton': 173,
    }
}

print("=" * 100)
print("COMPLETE DATA EXTRACTION & VERIFICATION FOR ALL 8 CRITICAL BLOCKS (2023-2025)")
print("=" * 100)

all_data = {}

for block in critical_blocks:
    block_rows = df[df[0] == block]
    
    if len(block_rows) == 0:
        print(f"\n❌ {block}: NOT FOUND IN EXCEL")
        continue
    
    row_idx = block_rows.index[0]
    
    # Get area
    luas_ha = df.iloc[row_idx, 11]
    year_planted = df.iloc[row_idx, 1]
    
    print(f"\n{'='*100}")
    print(f"BLOCK: {block} | Year Planted: {year_planted} | Luas: {luas_ha} Ha | Row: {row_idx}")
    print(f"{'='*100}")
    
    block_data = {
        'block_code': block,
        'row_index': int(row_idx),
        'year_planted': int(year_planted) if pd.notna(year_planted) else None,
        'luas_ha': float(luas_ha) if pd.notna(luas_ha) else None,
        'years': {}
    }
    
    for year, cols in year_data.items():
        # Extract raw values
        real_ton_total = df.iloc[row_idx, cols['real_ton']]
        poten_ton_total = df.iloc[row_idx, cols['poten_ton']]
        real_bjr = df.iloc[row_idx, cols['real_bjr']]
        real_jjg = df.iloc[row_idx, cols['real_jjg']]
        
        # Calculate Ton/Ha
        real_ton_ha = None
        poten_ton_ha = None
        gap_ton_ha = None
        gap_pct = None
        
        if pd.notna(real_ton_total) and pd.notna(luas_ha) and luas_ha > 0:
            real_ton_ha = round(float(real_ton_total) / float(luas_ha), 2)
        
        if pd.notna(poten_ton_total) and pd.notna(luas_ha) and luas_ha > 0:
            poten_ton_ha = round(float(poten_ton_total) / float(luas_ha), 2)
        
        if real_ton_ha and poten_ton_ha:
            gap_ton_ha = round(poten_ton_ha - real_ton_ha, 2)
            gap_pct = round((gap_ton_ha / poten_ton_ha) * 100, 1)
        
        print(f"\n--- YEAR {year} ---")
        print(f"  📊 RAW DATA FROM EXCEL:")
        print(f"     Col {cols['real_ton']}: Total Ton (Real)    = {real_ton_total}")
        print(f"     Col {cols['poten_ton']}: Total Ton (Potensi) = {poten_ton_total}")
        print(f"     Col {cols['real_bjr']}: BJR Kg (Real)      = {real_bjr}")
        print(f"     Col {cols['real_jjg']}: Jum JJg (Real)     = {real_jjg}")
        
        print(f"\n  🧮 CALCULATED VALUES:")
        print(f"     Realisasi: {real_ton_total} Ton / {luas_ha} Ha = {real_ton_ha} Ton/Ha")
        print(f"     Potensi:   {poten_ton_total} Ton / {luas_ha} Ha = {poten_ton_ha} Ton/Ha")
        print(f"     Gap:       {gap_ton_ha} Ton/Ha ({gap_pct}%)")
        
        block_data['years'][year] = {
            'real_ton_total': float(real_ton_total) if pd.notna(real_ton_total) else None,
            'poten_ton_total': float(poten_ton_total) if pd.notna(poten_ton_total) else None,
            'real_ton_ha': real_ton_ha,
            'poten_ton_ha': poten_ton_ha,
            'gap_ton_ha': gap_ton_ha,
            'gap_pct': gap_pct
        }
    
    all_data[block] = block_data

# Save to JSON for verification
with open('data/output/verified_historical_data_2023_2025.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print("\n" + "=" * 100)
print("✅ SAVED TO: data/output/verified_historical_data_2023_2025.json")
print("=" * 100)

# Create summary table
print("\n" + "=" * 100)
print("SUMMARY TABLE - REALISASI (Ton/Ha)")
print("=" * 100)
print(f"{'Block':<10} {'Luas Ha':<10} {'2023':<12} {'2024':<12} {'2025':<12} {'Trend':<15}")
print("-" * 100)

for block, data in all_data.items():
    luas = data['luas_ha']
    y2023 = data['years'].get(2023, {}).get('real_ton_ha', '-')
    y2024 = data['years'].get(2024, {}).get('real_ton_ha', '-')
    y2025 = data['years'].get(2025, {}).get('real_ton_ha', '-')
    
    if all([isinstance(y, (int, float)) for y in [y2023, y2024, y2025]]):
        trend = f"{y2025 - y2023:+.2f}"
    else:
        trend = "-"
    
    print(f"{block:<10} {luas:<10.1f} {str(y2023):<12} {str(y2024):<12} {str(y2025):<12} {trend:<15}")

print("\n" + "=" * 100)
print("⚠️  PLEASE VERIFY THIS DATA AGAINST YOUR SOURCE SPREADSHEET!")
print("=" * 100)
