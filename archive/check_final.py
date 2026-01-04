import pandas as pd

# Baca CSV
df = pd.read_csv('poac_sim/data/input/tabelNDREnew.csv')

print("Columns:")
print(df.columns.tolist())

# Filter F008A (gunakan blok_b)
f008a = df[df['blok_b'] == 'F008A']
d001a = df[df['blok_b'] == 'D001A']

print("\n" + "="*60)
print("F008A DATA:")
print("="*60)
print(f"Total pohon: {len(f008a)}")
if len(f008a) > 0:
    print(f"TT (Tahun Tanam): {f008a['t_tanam'].iloc[0] if 't_tanam' in df.columns else 'N/A'}")
    if 'sisip' in df.columns:
        sisip_count = f008a['sisip'].sum()
        print(f"Tanaman Sisip: {sisip_count}")
        print(f"Tanaman Normal: {len(f008a) - sisip_count}")
    else:
        print("Column 'sisip' not found")

print("\n" + "="*60)
print("D001A DATA:")
print("="*60)
print(f"Total pohon: {len(d001a)}")
if len(d001a) > 0:
    print(f"TT (Tahun Tanam): {d001a['t_tanam'].iloc[0] if 't_tanam' in df.columns else 'N/A'}")
    if 'sisip' in df.columns:
        sisip_count = d001a['sisip'].sum()
        print(f"Tanaman Sisip: {sisip_count}")
        print(f"Tanaman Normal: {len(d001a) - sisip_count}")
    else:
        print("Column 'sisip' not found")
