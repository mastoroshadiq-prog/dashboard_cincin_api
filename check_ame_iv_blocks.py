"""
Quick script to check AME IV blocks from NDRE CSV
"""
import pandas as pd

# Read AME IV NDRE data
df = pd.read_csv('data/input/AME_IV.csv', sep=';', encoding='utf-8')

print("Columns:", df.columns.tolist())
print(f"\nTotal trees: {len(df)}")

if 'Blok' in df.columns or 'BLOK_B' in df.columns:
    block_col = 'Blok' if 'Blok' in df.columns else 'BLOK_B'
    blocks = sorted(df[block_col].dropna().unique())
    print(f"\nAME IV Blocks ({len(blocks)} total):")
    for b in blocks:
        count = len(df[df[block_col] == b])
        print(f"  {b}: {count} trees")
else:
    print("\nBlock column not found!")
    print("Sample data:")
    print(df.head())
