import pandas as pd
import json

# Read the Excel file
file_path = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\poac_sim\data\input\data_gabungan.xlsx'

print("Reading Excel file...")
df = pd.read_excel(file_path)

print(f"\nTotal rows: {len(df)}")
print(f"\nFirst 10 columns: {list(df.columns[:10])}")

# Check for TBM status
print("\n" + "=" * 60)
print("ANALYZING TBM BLOCKS")
print("=" * 60)

# Look for status or TBM-related columns
status_cols = [col for col in df.columns if 'status' in str(col).lower() or 'tbm' in str(col).lower()]
print(f"\nStatus-related columns: {status_cols}")

# Check unique values in status column if exists
if status_cols:
    for col in status_cols:
        print(f"\nColumn: {col}")
        print(f"Unique values: {df[col].unique()}")
        print(f"\nValue counts:")
        print(df[col].value_counts())

# Look for blocks with production = 0
prod_cols = [col for col in df.columns if 'prod' in str(col).lower()]
print(f"\n\nProduction-related columns found: {len(prod_cols)}")
if len(prod_cols) > 0:
    print(f"Sample: {prod_cols[:5]}")

# Check for tahun_tanam (planting year)
tanam_cols = [col for col in df.columns if 'tanam' in str(col).lower() or 'tahun' in str(col).lower()]
print(f"\nPlanting-related columns: {tanam_cols}")

# Look for division and block code
print(f"\nLooking for division/afdeling columns...")
div_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['div', 'afdeling', 'block', 'blok'])]
print(f"Found: {div_cols[:5]}")

# Display first few rows with key columns
print("\n" + "=" * 60)
print("SAMPLE DATA")
print("=" * 60)
key_cols = [c for c in df.columns if any(x in str(c).lower() for x in ['block', 'blok', 'div', 'afd', 'prod', 'status', 'tanam'])]
print(f"\nKey columns: {key_cols[:10]}")
if len(key_cols) > 0:
    print("\nFirst 5 rows:")
    print(df[key_cols[:10]].head())

# Save column list for reference
with open('excel_columns.txt', 'w', encoding='utf-8') as f:
    for i, col in enumerate(df.columns):
        f.write(f"{i+1}. {col}\n")
print("\nColumn list saved to: excel_columns.txt")

print("\nAnalysis complete!")
