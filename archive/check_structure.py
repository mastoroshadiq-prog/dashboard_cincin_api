import pandas as pd

# Baca file Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

print("="*60)
print("STRUCTURE OF FILE:")
print("="*60)
print(f"Total rows: {len(df)}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

# Coba cari kolom yang mengandung 'blok' atau 'F008' atau 'D001'
print("\n" + "="*60)
print("SEARCHING FOR BLOCK IDENTIFIERS:")
print("="*60)
for col in df.columns:
    if 'blok' in col.lower() or 'block' in col.lower():
        print(f"Found column: {col}")
        print(f"Unique values: {df[col].unique()[:10]}")
