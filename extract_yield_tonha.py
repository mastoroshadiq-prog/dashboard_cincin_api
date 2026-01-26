import pandas as pd
import json

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Critical blocks
critical_blocks = ['D001A', 'D003A', 'D004A', 'E001A', 'E002A', 'E003A', 'E005A', 'E006A']

# Columns based on exploration
# Row 3 has years, Row 4 has "Real", Row 5 has "Ton"
# Production (Ton) columns - these are "Real" Ton columns
production_cols = {
    #2019: 71,   # THN 2019 Real Ton
    #2020: 80,   # THN 2020 Real Ton
    2021: 89,   # THN 2021 Real Ton   
    2022: 98,   # THN 2022 Real Ton
    2023: 107,  # THN 2023 Real Ton
    2024: 116,  # THN 2024 Real Ton
    # 2025 might be in a different column - let me find it
}

# Check what years are in row 3
print("Checking year headers in row 3:")
for i in range(60, 150):
    val = df.iloc[3, i]
    if pd.notna(val) and ('201' in str(val) or '202' in str(val)):
        print(f"Col {i}: {val}")

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
    
    historical_data[block] = {
        'luas_ha': luas_ha,
        'yields': yields
    }

# Save to JSON
with open('data/output/historical_yield_data.json', 'w') as f:
    json.dump(historical_data, f, indent=2)

print("\n✅ Saved to: data/output/historical_yield_data.json")
