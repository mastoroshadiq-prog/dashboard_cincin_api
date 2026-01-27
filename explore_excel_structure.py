import pandas as pd

# Load Excel to check structure
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

print("\n=== EXCEL FILE STRUCTURE ===\n")
print(f"Total Rows: {len(df)}")
print(f"Total Columns: {len(df.columns)}")

print("\n=== FIRST 200 COLUMNS ===\n")
for i in range(min(200, len(df.columns))):
    col = df.columns[i]
    # Show non-null count to understand data density
    non_null = df[col].notna().sum()
    print(f"{i:4d}: {str(col)[:60]:<60} (non-null: {non_null})")

print("\n=== CHECKING AROUND INDEX 170 (known 2025 columns) ===\n")
for i in range(160, min(185, len(df.columns))):
    col = df.columns[i]
    print(f"{i:4d}: {col}")
