"""
Explore data_gabungan.xlsx to find:
1. Stadium 1, 2, 3 columns (jumlah pohon terinfeksi)
2. Total trees for calculating attack rate
"""
import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*70)
print("EXPLORING DATA_GABUNGAN.XLSX FOR STADIUM DATA")
print("="*70)

# Search for Stadium-related columns
print("\nSearching for 'STADIUM' in headers (rows 0-10):")
for col in range(df.shape[1]):
    for row in range(10):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'STAD' in val.upper() or 'GANO' in val.upper():
            print(f"  Row {row}, Col {col}: {val}")

# Search for total trees columns
print("\nSearching for tree count columns:")
for col in range(df.shape[1]):
    for row in range(10):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'PKK' in val.upper() or 'POKOK' in val.upper() or 'JML' in val.upper() or 'TOTAL' in val.upper():
            print(f"  Row {row}, Col {col}: {val}")

# Show header structure for potential stadium columns (around col 60+)
print("\nHeader structure for cols 55-75:")
for col in range(55, min(75, df.shape[1])):
    header_parts = []
    for row in range(7):
        val = df.iloc[row, col]
        if pd.notna(val):
            header_parts.append(f"R{row}:{str(val)[:20]}")
    if header_parts:
        print(f"Col {col}: {header_parts}")
