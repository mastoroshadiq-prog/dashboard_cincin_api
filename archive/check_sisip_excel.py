import pandas as pd

# Baca Excel - coba beberapa kemungkinan sheet
xl = pd.ExcelFile('poac_sim/data/input/data_gabungan.xlsx')
print(f"Sheet names: {xl.sheet_names}")

# Baca sheet pertama
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', sheet_name=0)

print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Cari kolom SISIP (C046 based on header image, which is column index 45 in 0-based)
# Cari kolom yang mengandung 'F008A' or 'D001A'
print("\nSearching for SISIP column (around column 45-50):")
for i in range(44, min(60, len(df.columns))):
    col = df.columns[i]
    print(f"Column {i} ({col}): {df.iloc[0:3, i].tolist()}")

# Cari baris yang mengandung F008A atau D001A
print("\nSearching for rows with F008A or D001A:")
for col in df.columns[:30]:
    if df[col].astype(str).str.contains('F008A|D001A', na=False).any():
        print(f"Found in column: {col}")
        print(df[df[col].astype(str).str.contains('F008A|D001A', na=False)][col].head())
        break
