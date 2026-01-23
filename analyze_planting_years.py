import pandas as pd
import json
from collections import Counter

# Read the Excel file
file_path = r'poac_sim\data\input\data_gabungan.xlsx'

# Read with simple header from row 6
df = pd.read_excel(file_path, header=6)

print("=== PLANTING YEAR ANALYSIS ===")
print(f"\nTotal blocks: {len(df)}")

# Column K001 is block code, K002 is planting year
block_col = 'K001'
year_col = 'K002'

print(f"\nBlock code column: {block_col}")
print(f"Planting year column: {year_col}")

# Get planting year distribution
planting_years = df[year_col].dropna()
year_counts = Counter(planting_years)

print(f"\n=== PLANTING YEAR DISTRIBUTION ===")
print(f"Total blocks with year data: {len(planting_years)}")
print(f"Blocks without year data: {df[year_col].isna().sum()}")

print("\nYear distribution (sorted):")
for year in sorted(year_counts.keys()):
    count = year_counts[year]
    print(f"  {int(year)}: {count} blocks")

# Focus on 2023-2025 as requested
recent_years = {2023: 0, 2024: 0, 2025: 0}
for year in planting_years:
    if year in recent_years:
        recent_years[int(year)] += 1

print(f"\n=== BLOCKS PLANTED 2023-2025 ===")
for year in [2023, 2024, 2025]:
    print(f"  {year}: {recent_years[year]} blocks")

# Show sample blocks with planting years
print(f"\n=== SAMPLE BLOCKS WITH PLANTING YEARS ===")
sample = df[[block_col, year_col]].head(20)
print(sample.to_string(index=False))

# Export to JSON for dashboard integration
planting_data = []
for idx, row in df.iterrows():
    block_code = row[block_col]
    planting_year = row[year_col]
    
    if pd.notna(block_code) and pd.notna(planting_year):
        planting_data.append({
            'block_code': str(block_code),
            'planting_year': int(planting_year)
        })

output_file = 'planting_year_data.json'
with open(output_file, 'w') as f:
    json.dump(planting_data, f, indent=2)

print(f"\n✓ Exported {len(planting_data)} blocks to {output_file}")

# Create summary for dashboard
summary = {
    'total_blocks': len(planting_data),
    'year_distribution': {int(k): v for k, v in year_counts.items()},
    'recent_years_2023_2025': recent_years,
    'earliest_year': int(min(year_counts.keys())),
    'latest_year': int(max(year_counts.keys()))
}

summary_file = 'planting_year_summary.json'
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✓ Exported summary to {summary_file}")
