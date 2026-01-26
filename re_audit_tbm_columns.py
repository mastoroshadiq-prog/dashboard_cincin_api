import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca semua data
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    print("=== MENCARI SAMPEL DATA TANAM YANG VALID ===")
    
    # Kita cari baris yang punya nilai > 10 di range kolom 30-50
    # Ini indikasi jumlah pokok tanam
    
    found_sample = False
    
    for i, row in df.iterrows():
        block = row[0]
        # Scan kolom 30 sampai 60
        potential_cols = []
        for col_idx in range(30, 60):
            val = row[col_idx]
            try:
                num = float(val)
                if num > 10: # Asumsi ada > 10 pokok ditanam
                    potential_cols.append((col_idx, num))
            except:
                pass
        
        if len(potential_cols) > 2: # Jika ada minimal 2 kolom tanam terisi
            print(f"\nSAMPEL DITEMUKAN: Blok {block}")
            print(f"Values Found: {potential_cols}")
            
            # Mari lihat header untuk indeks ini
            # Sayangnya dataframe ini tanpa header, saya harus baca header terpisah
            found_sample = True
            break
            
    if found_sample:
        # Baca Header Baris 7 (Index 6)
        df_head = pd.read_excel(file_path, header=None, nrows=10)
        header_row = df_head.iloc[6] # Baris 7
        
        print("\n=== HEADER MAPPING (Baris 7) ===")
        # Tampilkan header untuk kolom yang ditemukan tadi
        for col_idx, _ in potential_cols:
             label = header_row[col_idx]
             print(f"Index {col_idx}: {label}")
             
        # Cek kolom sekitar
        print("\n--- Pengecekan Area Sekitar ---")
        for j in range(35, 50):
             print(f"Idx {j}: {header_row[j]}")

except Exception as e:
    print(f"Error: {e}")
