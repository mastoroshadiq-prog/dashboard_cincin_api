import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

# D001A row 86, F008A row 92
# Tapi mari cek semua kemungkinan lokasi data sisip

print("="*70)
print("MENCARI DATA SISIP UNTUK D001A (Total pohon expected: 3486)")
print("="*70)

# Cek berbagai kolom di sekitar row 86 (D001A)
row_d001a = df.iloc[86]
print(f"D001A Row 86 - Checking columns 48-56:")
for i in range(48, 56):
    val = row_d001a.iloc[i]
    if pd.notna(val) and val > 0:
        print(f"  Col {i}: {val}")
        # Cek apakah ini bisa jadi sisip
        if val < 500:  # Sisip seharusnya kecil
            remaining = 3486 - val
            print(f"    -> Jika ini sisip, normal = {remaining}")

print("\n" + "="*70)
print("CROSSCHECK: Cari nilai yang mendekati 3486 (total D001A)")
print("="*70)
for i in range(48, 80):
    val = row_d001a.iloc[i]
    if pd.notna(val) and 3400 < val < 3600:
        print(f"  Col {i}: {val} <- Mendekati total 3486!")
        # Cek kolom sebelah/sesudahnya untuk sisip
        if i > 0:
            sisip_before = row_d001a.iloc[i-1]
            print(f"    Col {i-1} (before): {sisip_before} <- Possible SISIP?")
        if i < len(row_d001a) - 1:
            sisip_after = row_d001a.iloc[i+1]
            print(f"    Col {i+1} (after): {sisip_after}")

print("\n" + "="*70)
print("SUMMARY DATA:")
print("="*70)
print(f"F008A (row 92): Total 3770, Sisip 142 (dari col 51)")
print(f"D001A (row 86): Total 3486, Sisip = ???")
