import pandas as pd

# Baca Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', sheet_name=0)

# Cari baris dengan F008A dan D001A di kolom pertama
print("Searching for F008A and D001A in column 0...")
print()

# Kolom AY = index 50 (0-based), AZ = index 51
col_tanam = 50  # AY - Total Tanam
col_sisip = 51  # AZ - Total Sisip

print(f"Column AY (index {col_tanam}): {df.columns[col_tanam]}")
print(f"Column AZ (index {col_sisip}): {df.columns[col_sisip]}")
print()

# Cari baris F008A dan D001A
for idx, row in df.iterrows():
    block_id = str(row.iloc[0]).strip()
    if 'F008A' in block_id or 'D001A' in block_id:
        total_tanam = row.iloc[col_tanam]
        total_sisip = row.iloc[col_sisip]
        
        print("="*60)
        print(f"BLOK: {block_id} (Row {idx})")
        print("="*60)
        print(f"Total Tanam (AY): {total_tanam}")
        print(f"Total Sisip (AZ): {total_sisip}")
        print(f"Tanaman Normal: {total_tanam - total_sisip if pd.notna(total_tanam) and pd.notna(total_sisip) else 'N/A'}")
        print()
