import pandas as pd
import json

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Critical blocks
critical_blocks = ['D001A', 'D003A', 'D004A', 'E001A', 'E002A', 'E003A', 'E005A', 'E006A']

# Year column mapping (from exploration)
year_cols = {
    2019: 32,
    2020: 34,
    2021: 36,
    2022: 38,
    2023: 40,
    2024: 43,
    2025: 47
}

# Extract historical yield data
historical_data = {}

for block in critical_blocks:
    block_rows = df[df[0] == block]
    if len(block_rows) > 0:
        row_idx = block_rows.index[0]
        
        yields = {}
        for year, col in year_cols.items():
            val = df.iloc[row_idx, col]
            if pd.notna(val):
                try:
                    yields[year] = float(val)
                except:
                    yields[year] = None
            else:
                yields[year] = None
        
        # Also get current year (2025) data
        luas_ha = df.iloc[row_idx, 11]  # Column 11 seems to be area
        
        print(f"\n{block}:")
        print(f"  Luas Ha: {luas_ha}")
        print(f"  Yields:")
        for year, yld in sorted(yields.items()):
            if yld:
                print(f"    {year}: {yld:.2f} Ton/Ha")
        
        historical_data[block] = {
            'luas_ha': float(luas_ha) if pd.notna(luas_ha) else None,
            'yields': yields
        }

# Save to JSON
with open('data/output/historical_yield_data.json', 'w') as f:
    json.dump(historical_data, f, indent=2)

print("\n✅ Saved to: data/output/historical_yield_data.json")

# Calculate 3-year average for 2023-2025
print("\n=== 3-Year Trend (2023-2025) ===")
for block, data in historical_data.items():
    y2023 = data['yields'].get(2023)
    y2024 = data['yields'].get(2024)
    y2025 = data['yields'].get(2025)
    
    if all([y2023, y2024, y2025]):
        print(f"\n{block}:")
        print(f"  2023: {y2023:.2f} Ton/Ha")
        print(f"  2024: {y2024:.2f} Ton/Ha")
        print(f"  2025: {y2025:.2f} Ton/Ha")
        trend = ((y2025 - y2023) / y2023 * 100)
        print(f"  Trend: {trend:+.1f}% (3 years)")
