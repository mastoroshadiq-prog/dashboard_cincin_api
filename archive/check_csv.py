import pandas as pd

# Baca CSV
df = pd.read_csv('poac_sim/data/input/tabelNDREnew.csv')

print("Columns in tabelNDREnew.csv:")
print(df.columns.tolist())

# Filter F008A
f008a = df[df['blok_baru'] == 'F008A']
d001a = df[df['blok_baru'] == 'D001A']

print("\n" + "="*60)
print("F008A DATA:")
print("="*60)
print(f"Total pohon: {len(f008a)}")
if len(f008a) > 0:
    print(f"TT (Tahun Tanam): {f008a['tt'].iloc[0]}")
    if 'sisip' in df.columns:
        sisip_count = f008a['sisip'].sum()
        print(f"Tanaman Sisip (sisip=1): {sisip_count}")
        print(f"Tanaman Normal: {len(f008a) - sisip_count}")

print("\n" + "="*60)
print("D001A DATA:")
print("="*60)
print(f"Total pohon: {len(d001a)}")
if len(d001a) > 0:
    print(f"TT (Tahun Tanam): {d001a['tt'].iloc[0]}")
    if 'sisip' in df.columns:
        sisip_count = d001a['sisip'].sum()
        print(f"Tanaman Sisip (sisip=1): {sisip_count}")
        print(f"Tanaman Normal: {len(d001a) - sisip_count}")
