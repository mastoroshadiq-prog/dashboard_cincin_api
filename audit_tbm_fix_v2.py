import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    blocks_to_check = ["B012D", "F025E", "B006D"]
    print(f"=== AUDIT RAW DATA SPECIFIC BLOCKS: {blocks_to_check} ===")
    
    for code in blocks_to_check:
        row = df[df[0] == code]
        if not row.empty:
            print(f"\nBlok: {code}")
            vals = row.iloc[0].tolist()
            
            # 1. Cek Tahun Tanam (Index 1)
            print(f"Index 1 (Tahun Tanam): {vals[1]}")
            
            # 2. Cek Kolom yang KITA PAKAI SEKARANG (36, 40, 44)
            # 2023: 36, 2024: 40, 2025: 44
            print(f"Current Logic -> 2023(36): {vals[36]}, 2024(40): {vals[40]}, 2025(44): {vals[44]}")
            
            # 3. SCAN SELURUH KOLOM MENCARI ANGKA 149 (Untuk B012D) atau angka > 0 lainnya
            found_cols = []
            for i, val in enumerate(vals):
                try:
                    num = float(val)
                    if num == 149.0:
                        print(f"!!! FOUND 149.0 at Index {i} !!!")
                    if 0 < num < 3000 and i > 2: # Filter angka tahun dan angka basic
                        found_cols.append((i, num))
                except:
                    pass
            
            # Tampilkan 10 data non-0 pertama untuk clue
            print("Data Non-Zero (Index > 2):")
            for idx, val in found_cols[:15]:
                print(f"  idx {idx}: {val}")
                
            # Cek range 30-60 detail
            print("Range 30-60 Detail:")
            for j in range(30, 60):
                print(f"  {j}: {vals[j]}")
                
        else:
            print(f"Blok {code} tidak ditemukan.")

except Exception as e:
    print(f"Error: {e}")
