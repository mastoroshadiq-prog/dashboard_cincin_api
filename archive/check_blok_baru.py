import pandas as pd

# Baca file Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

print("="*60)
print("MENCARI KOLOM 'BLOK BARU' DAN 'SISIP':")
print("="*60)

# Cari kolom yang mengandung kata 'blok' atau 'baru'
blok_col = None
sisip_col = None
tt_col = None

for col in df.columns:
    col_lower = str(col).lower()
    if 'baru' in col_lower and 'blok' in col_lower:
        blok_col = col
        print(f"✓ Found 'blok baru' column: {col}")
    elif 'sisip' in col_lower:
        sisip_col = col
        print(f"✓ Found 'sisip' column: {col}")
    elif col_lower in ['tt', 'tahun tanam', 'tahun_tanam']:
        tt_col = col
        print(f"✓ Found 'tt' column: {col}")

if blok_col:
    # Filter F008A
    f008a = df[df[blok_col] == 'F008A']
    d001a = df[df[blok_col] == 'D001A']
    
    print("\n" + "="*60)
    print("F008A DATA:")
    print("="*60)
    print(f"Total pohon: {len(f008a)}")
    
    if len(f008a) > 0 and tt_col:
        print(f"TT (Tahun Tanam): {f008a[tt_col].iloc[0]}")
    
    if len(f008a) > 0 and sisip_col:
        # Hitung tanaman sisip (nilai 1 = sisip)
        sisip_count = (f008a[sisip_col] == 1).sum()
        print(f"Tanaman Sisip: {sisip_count}")
        print(f"Tanaman Normal: {len(f008a) - sisip_count}")
    
    print("\n" + "="*60)
    print("D001A DATA:")
    print("="*60)
    print(f"Total pohon: {len(d001a)}")
    
    if len(d001a) > 0 and tt_col:
        print(f"TT (Tahun Tanam): {d001a[tt_col].iloc[0]}")
    
    if len(d001a) > 0 and sisip_col:
        sisip_count = (d001a[sisip_col] == 1).sum()
        print(f"Tanaman Sisip: {sisip_count}")
        print(f"Tanaman Normal: {len(d001a) - sisip_count}")
else:
    print("\nKolom 'blok baru' tidak ditemukan!")
    print("\nMenampilkan 20 kolom pertama:")
    for i, col in enumerate(df.columns[:20]):
        print(f"{i+1}. {col}")
