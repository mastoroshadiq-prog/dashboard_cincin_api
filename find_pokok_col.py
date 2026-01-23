import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df_raw = pd.read_excel(file_path, header=None, nrows=5)
    
    # Cari indeks kolom yang mengandung kata "POKOK" atau "SPH" di Baris 3
    header_row = df_raw.iloc[3]
    
    found_cols = []
    print("=== MENCARI KOLOM 'POKOK' DI BARIS 3 ===")
    for i, val in enumerate(header_row):
        if pd.notna(val) and ('POKOK' in str(val).upper() or 'SPH' in str(val).upper()):
             print(f"Kolom {i}: {val}")
             found_cols.append(i)
    
    if found_cols:
        # Baca 5 baris data untuk kolom-kolom tersebut
        print("\n=== SAMPEL DATA KOLOM POKOK ===")
        df_sample = pd.read_excel(file_path, header=None, skiprows=6, nrows=5, usecols=[0] + found_cols)
        print(df_sample)

except Exception as e:
    print(f"Error: {e}")
