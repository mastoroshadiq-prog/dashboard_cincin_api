import pandas as pd
import json

# Read the Excel file
print("Reading data_gabungan.xlsx...")
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print(f"\nFile shape: {df.shape}")
print("\n=== Exploring Structure ===")

# Check row 6 which seems to have block codes
print("\nRow 6 (Block codes):")
print(df.iloc[6, :20].tolist())

# Check if there are year columns in row 3 or 4
print("\nRow 3 (possible year headers):")
print(df.iloc[3, :50].tolist())

print("\nRow 4 (possible column labels):")
print(df.iloc[4, :50].tolist())

print("\nRow 5:")
print(df.iloc[5, :50].tolist())

# Find D003A row
d003a_rows = df[df[0] == 'D003A']
if len(d003a_rows) > 0:
    print("\n=== D003A Data ===")
    row_idx = d003a_rows.index[0]
    print(f"Found at row {row_idx}")
    print("\nAll data for D003A:")
    print(d003a_rows.iloc[0, :80].tolist())
    
# Check columns around 30-80 where production data might be
print("\n=== Checking for production data columns ===")
print("Columns 30-50 headers (row 4):")
for i in range(30, min(50, len(df.columns))):
    val = df.iloc[4, i]
    if pd.notna(val):
        print(f"Col {i}: {val}")

# Look for "Ton" or "TBS" keywords
print("\n=== Searching for 'Ton' or 'Produksi' keywords ===")
for row in range(10):
    for col in range(min(100, len(df.columns))):
        val = str(df.iloc[row, col]).lower()
        if 'ton' in val or 'produksi' in val or 'real' in val:
            print(f"Row {row}, Col {col}: {df.iloc[row, col]}")
