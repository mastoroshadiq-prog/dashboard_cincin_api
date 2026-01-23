import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca header baris ke-7 (index 6) dimana kode C038, C041 berada
    df = pd.read_excel(file_path, header=6, nrows=0)
    cols = df.columns.tolist()
    
    print("=== MAPPING HEADER TAHUN TANAM ===")
    
    target_codes = ['C038', 'C039', 'C040', 'C041', 'C042', 'C043', 'C044', 'C045', 'C046', 'C047']
    
    found_map = {}
    for code in target_codes:
        if code in cols:
            idx = cols.index(code)
            print(f"Kode {code} ditemukan di Index: {idx}")
            found_map[code] = idx
            
    # Verifikasi label parent (THN 2023 dll)
    # Baca header baris 5 (index 4) untuk melihat label tahun
    df_years = pd.read_excel(file_path, header=None, skiprows=4, nrows=1)
    row_years = df_years.iloc[0].tolist()
    
    print("\n=== VERIFIKASI LABEL TAHUN (Baris 5) ===")
    for code, idx in found_map.items():
        if idx < len(row_years):
            print(f"Index {idx} ({code}) label atasnya: {row_years[idx]}")

except Exception as e:
    print(f"Error: {e}")
