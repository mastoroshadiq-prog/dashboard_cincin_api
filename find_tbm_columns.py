import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    # Cari blok dengan Tahun Tanam (Col 1) >= 2023
    print("=== MENCARI BLOK TANAM BARU (>= 2023) ===")
    
    target_blocks = []
    
    for i, row in df.iterrows():
        try:
            year = int(row[1])
            if year >= 2023:
                target_blocks.append(row)
                if len(target_blocks) >= 3: break # Ambil 3 sampel
        except:
            pass
            
    if not target_blocks:
        print("Tidak ada blok tanam >= 2023 ditemukan. Cek Index 1.")
    
    for row in target_blocks:
        block = row[0]
        print(f"\nBlok: {block} (Tahun {row[1]})")
        
        # Dump nilai kolom 30 - 60
        for j in range(30, 60):
            val = row[j]
            try:
                if float(val) > 0:
                    print(f"Index {j}: {val}")
            except:
                pass
                
    # Baca header lagi untuk memastikan label
    df_head = pd.read_excel(file_path, header=None, nrows=10)
    # Cek baris header yang mungkin mengandung "REALISASI TANAM"
    # Baris 3, 4, 5, 6, 7?
    
    print("\n=== HEADER LABELS ===")
    for r in range(2, 8): # Baris 3 sampai 8
        row_vals = df_head.iloc[r]
        # Cari text yang mengandung "TANAM" atau "REAL"
        found_txt = []
        for c in range(30, 60):
            txt = str(row_vals[c])
            if "REAL" in txt.upper() or "TANAM" in txt.upper() or "POKOK" in txt.upper():
                found_txt.append(f"Col {c}: {txt}")
        
        if found_txt:
            print(f"Row {r+1}: {found_txt[:5]} ...")

except Exception as e:
    print(f"Error: {e}")
