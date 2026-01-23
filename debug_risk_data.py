import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca header baris 3 (index 2) dimana SPH ditemukan sebelumnya
    df_head = pd.read_excel(file_path, header=None, nrows=5)
    row_3 = df_head.iloc[3] # Baris yang punya 'POKOK', 'SPH'
    
    print("=== PENCARIAN KOLOM RISIKO (Baris 3) ===")
    risk_keywords = ['SERANGAN', 'ATTACK', 'INFECTED', 'SENSUS', 'GANODERMA', 'STADIUM']
    
    found_cols = {}
    for i, val in enumerate(row_3):
        if pd.notna(val):
            val_str = str(val).upper()
            if any(k in val_str for k in risk_keywords):
                print(f"Index {i}: {val}")
                found_cols[i] = val
                
    # Tambah pencarian 'SPH' lagi untuk konfirmasi
    for i, val in enumerate(row_3):
        if pd.notna(val) and 'SPH' in str(val).upper():
             print(f"Index {i}: {val} (SPH)")
             found_cols[i] = val

    if not found_cols:
        print("Tidak ditemukan keyword risiko di Baris 3. Coba Baris 7 (Header Utama Table).")
        # Fallback ke baris 7
        df_head7 = pd.read_excel(file_path, header=6, nrows=0)
        for i, col in enumerate(df_head7.columns):
            if any(k in str(col).upper() for k in risk_keywords):
                 print(f"Header Row 7 - Index {i}: {col}")

    # Cek Data Blok A012C secara spesifik
    print("\n=== MENGECEK DATA BLOK A012C ===")
    # Baca seluruh data (skip 8 baris awal)
    df_data = pd.read_excel(file_path, header=None, skiprows=8)
    
    # Cari baris dengan A012C di kolom 0
    target_row = df_data[df_data[0] == 'A012C']
    
    if not target_row.empty:
        print("Data Raw A012C ditemukan:")
        # Tampilkan nilai di kolom-kolom risiko yang ditemukan tadi
        for col_idx, col_name in found_cols.items():
            val = target_row.iloc[0, col_idx]
            print(f"- {col_name} (Col {col_idx}): {val}")
    else:
        print("Blok A012C TIDAK ditemukan di Excel.")

except Exception as e:
    print(f"Error: {e}")
