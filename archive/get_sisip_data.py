import pandas as pd

# Baca Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', sheet_name=0)

# Baris 86 = D001A, Baris 92 = F008A (0-indexed: 85 dan 91)
# Kolom SISIP adalah sekitar C046-C049 (index 45-48)

print("D001A (row 86, index 85):")
d001a_row = df.iloc[85]
print(f"Block identifier (col 0): {d001a_row.iloc[0]}")

# Cek kolom 45-50 untuk SISIP
print("\nChecking columns 45-50 for SISIP data:")
for i in range(45, 51):
    val = d001a_row.iloc[i] if i < len(d001a_row) else 'N/A'
    print(f"  Column {i}: {val}")

print("\n" + "="*60)
print("F008A (row 92, index 91):")
f008a_row = df.iloc[91]
print(f"Block identifier (col 0): {f008a_row.iloc[0]}")

print("\nChecking columns 45-50 for SISIP data:")
for i in range(45, 51):
    val = f008a_row.iloc[i] if i < len(f008a_row) else 'N/A'
    print(f"  Column {i}: {val}")

# Coba cari kolom header di baris pertama
print("\n" + "="*60)
print("Headers around column 45-50:")
for i in range(45, 51):
    header = df.columns[i]
    val_row0 = df.iloc[0, i]
    val_row1 = df.iloc[1, i]
    print(f"  Column {i} header='{header}', row0={val_row0}, row1={val_row1}")
