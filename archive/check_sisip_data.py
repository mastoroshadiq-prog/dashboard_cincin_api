import pandas as pd

# Baca file Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

# Filter data F008A
f008a = df[df['blok'] == 'F008A']
d001a = df[df['blok'] == 'D001A']

print("="*60)
print("F008A DATA:")
print("="*60)
print(f"Total pohon: {len(f008a)}")
if len(f008a) > 0:
    print(f"TT (Tahun Tanam): {f008a['tt'].iloc[0]}")
    if 'sisip' in f008a.columns:
        sisip_count = f008a['sisip'].sum()
        print(f"Tanaman Sisip: {sisip_count}")
    else:
        print("Column 'sisip' tidak ditemukan")

print()
print("="*60)
print("D001A DATA:")
print("="*60)
print(f"Total pohon: {len(d001a)}")
if len(d001a) > 0:
    print(f"TT (Tahun Tanam): {d001a['tt'].iloc[0]}")
    if 'sisip' in d001a.columns:
        sisip_count = d001a['sisip'].sum()
        print(f"Tanaman Sisip: {sisip_count}")
    else:
        print("Column 'sisip' tidak ditemukan")

print()
print("="*60)
print("AVAILABLE COLUMNS:")
print("="*60)
print(list(df.columns))
