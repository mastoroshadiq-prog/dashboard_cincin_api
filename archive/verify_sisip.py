import pandas as pd

# Baca Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', sheet_name=0)

# Kolom AY = index 50, AZ = index 51
col_tanam = 50
col_sisip = 51

print("Mencari semua baris yang mengandung 'F008' atau 'D001':")
print("="*80)

# Cari di semua kolom
for idx in range(len(df)):
    row = df.iloc[idx]
    row_str = ' '.join([str(x) for x in row[:10] if pd.notna(x)])
    
    if 'F008' in row_str or 'D001' in row_str:
        print(f"\nRow {idx}:")
        print(f"  Col 0: {row.iloc[0]}")
        print(f"  Col 1: {row.iloc[1]}")
        print(f"  Col 2: {row.iloc[2]}")
        print(f"  Total Tanam (AY/col{col_tanam}): {row.iloc[col_tanam]}")
        print(f"  Total Sisip (AZ/col{col_sisip}): {row.iloc[col_sisip]}")
        
        # Cek apakah ini F008A atau D001A
        for col_idx in range(min(10, len(row))):
            val = str(row.iloc[col_idx])
            if 'F008A' in val:
                print(f"  >>> FOUND F008A in column {col_idx}")
            if 'D001A' in val:
                print(f"  >>> FOUND D001A in column {col_idx}")
