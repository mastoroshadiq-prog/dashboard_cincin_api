import pandas as pd
import json
import sys

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Read the Excel file
file_path = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\poac_sim\data\input\data_gabungan.xlsx'

print("Reading Excel file...")
df = pd.read_excel(file_path)

print(f"\n[DATA] Total rows: {len(df)}")
print(f"[COLS] Columns: {list(df.columns)}\n")

# Check for TBM status
print("=" * 60)
print("🔍 ANALYZING TBM BLOCKS")
print("=" * 60)

# Look for status or TBM-related columns
status_cols = [col for col in df.columns if 'status' in col.lower() or 'tbm' in col.lower()]
print(f"\nStatus-related columns: {status_cols}")

# Check unique values in status column if exists
if status_cols:
    for col in status_cols:
        print(f"\n📌 Column: {col}")
        print(f"Unique values: {df[col].unique()}")
        print(f"Value counts:")
        print(df[col].value_counts())

# Look for blocks with production = 0
prod_cols = [col for col in df.columns if 'prod' in col.lower() or 'produksi' in col.lower()]
print(f"\n\n📈 Production-related columns: {prod_cols}")

if prod_cols:
    for col in prod_cols[:3]:  # Check first 3 production columns
        print(f"\n📌 Column: {col}")
        zero_prod = df[df[col] == 0]
        print(f"Blocks with zero production: {len(zero_prod)}")

# Check for tahun_tanam (planting year)
tanam_cols = [col for col in df.columns if 'tanam' in col.lower() or 'tahun' in col.lower()]
print(f"\n\n🌱 Planting-related columns: {tanam_cols}")

# Display sample of data
print("\n\n📋 SAMPLE DATA (first 5 rows):")
print(df.head())

# Find TBM blocks (assuming they have production = 0 and recent planting year)
print("\n\n" + "=" * 60)
print("🎯 IDENTIFYING TBM BLOCKS")
print("=" * 60)

# Try to find blocks planted in 2023-2025 with zero production
if 'tahun_tanam' in df.columns:
    recent_plant = df[(df['tahun_tanam'].notna()) & 
                      (df['tahun_tanam'] >= 2023) & 
                      (df['tahun_tanam'] <= 2025)]
    print(f"\n🌱 Blocks planted 2023-2025: {len(recent_plant)}")
    if len(recent_plant) > 0:
        print(recent_plant[['block_code', 'tahun_tanam']].head(10))
    
    # Check if they have zero production
    if 'prod_2025' in df.columns:
        tbm_blocks = recent_plant[recent_plant['prod_2025'] == 0]
        print(f"\n🟡 TBM blocks (planted 2023-2025, prod=0): {len(tbm_blocks)}")
        if len(tbm_blocks) > 0:
            print(tbm_blocks[['block_code', 'tahun_tanam', 'prod_2025']].head(10))

# Export sample TBM data
if 'tahun_tanam' in df.columns and len(recent_plant) > 0:
    sample_tbm = recent_plant.head(20).to_dict('records')
    with open('tbm_sample_data.json', 'w') as f:
        json.dump(sample_tbm, f, indent=2, default=str)
    print("\n✅ Sample TBM data exported to: tbm_sample_data.json")

print("\n" + "=" * 60)
print("Analysis complete!")
