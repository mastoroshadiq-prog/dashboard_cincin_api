import pandas as pd
import json

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Critical blocks
critical_blocks = ['D001A', 'D003A', 'D004A', 'E001A', 'E002A', 'E003A', 'E005A', 'E006A']

# Production (Ton) columns - Real data
# Each year has pattern: Real (Ton col), Potensi, Real vs Potensi
# Row 5 shows units, 3rd column in each year group is "Ton"
production_cols = {
    2023: 152,  # 2023 Real production (Ton) - calculated as col 150 + 2
    2024: 161,  # 2024 Real production (Ton) - calculated as col 159 + 2  
    2025: 170,  # 2025 Real production (Ton) - calculated as col 168 + 2
}

# Verify by checking a sample
print("Verifying column structure:")
for year, col in production_cols.items():
    print(f"{year} - Col {col}: Row3={df.iloc[3, col-2]} | Row4={df.iloc[4, col-2]} | Row5={df.iloc[5, col]}")

# Extract historical yield data
historical_data = {}

for block in critical_blocks:
    block_rows = df[df[0] == block]
    if len(block_rows) == 0:
        print(f"❌ Block {block} not found!")
        continue
        
    row_idx = block_rows.index[0]
    
    # Get area (column 11)
    luas_ha = df.iloc[row_idx, 11]
    if pd.isna(luas_ha) or luas_ha == 0:
        print(f"⚠️  {block}: No area data")
        continue
    
    luas_ha = float(luas_ha)
    
    yields = {}
    for year, col in production_cols.items():
        total_ton = df.iloc[row_idx, col]
        if pd.notna(total_ton):
            try:
                ton_ha = float(total_ton) / luas_ha
                yields[year] = round(ton_ha, 2)
            except:
                yields[year] = None
        else:
            yields[year] = None
    
    print(f"\n{block} (Luas: {luas_ha} Ha):")
    for year, yld in sorted(yields.items()):
        if yld:
            print(f"  {year}: {yld:.2f} Ton/Ha")
    
    # Calculate trend
    if yields.get(2023) and yields.get(2025):
        trend_pct = ((yields[2025] - yields[2023]) / yields[2023] * 100)
        print(f"  📊 Trend (2023→2025): {trend_pct:+.1f}%")
    
    historical_data[block] = {
        'luas_ha': luas_ha,
        'yields': yields
    }

# Save to JSON
with open('data/output/historical_yield_data.json', 'w') as f:
    json.dump(historical_data, f, indent=2)

print("\n" + "="*60)
print("✅ Saved to: data/output/historical_yield_data.json")
print("="*60)
