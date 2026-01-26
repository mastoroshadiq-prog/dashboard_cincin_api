import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

print("F008A (Row 92):")
print(f"  Total Tanam col50 (AY): {df.iloc[92, 50]}")
print(f"  Total Sisip col51 (AZ): {df.iloc[92, 51]}")
print(f"  Expected total from CSV: 3770")
print()

print("D001A (Row 86):")
print(f"  Total Tanam col50 (AY): {df.iloc[86, 50]}")
print(f"  Total Sisip col51 (AZ): {df.iloc[86, 51]}")
print(f"  Expected total from CSV: 3486")
print()

# Coba cek beberapa kolom sekitar AY/AZ
print("Checking columns around 48-54 for F008A (row 92):")
for i in range(48, 54):
    print(f"  Col {i}: {df.iloc[92, i]}")

print()
print("Checking columns around 48-54 for D001A (row 86):")
for i in range(48, 54):
    print(f"  Col {i}: {df.iloc[86, i]}")
