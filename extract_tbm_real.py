import pandas as pd
import json

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca data skip header 8 baris (row 8 adalah data pertama A001A)
    # Header tidak penting karena kita pakai index kolom langsung
    # Index 40 (Col 40) = C038 (Tanam 2023)
    # Index 43 (Col 43) = C041 (Tanam 2024)
    # Index 47 (Col 47) = C045 (Tanam 2025)
    
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    tbm_stats = {}
    
    for _, row in df.iterrows():
        block_code = row[0] # Kolom A
        planting_year = row[1] # Kolom B
        
        # Validasi
        if pd.isna(block_code) or not isinstance(block_code, str):
            continue
            
        try:
            # Ambil data Tanam per tahun
            tanam_2023 = int(row[40]) if pd.notna(row[40]) else 0
            tanam_2024 = int(row[43]) if pd.notna(row[43]) else 0
            tanam_2025 = int(row[47]) if pd.notna(row[47]) else 0
            
            # Tahun tanam
            p_year = int(planting_year) if pd.notna(planting_year) else 0
            
            # Hitung total 3 tahun (indikator aktivitas TBM aktif)
            total_3th = tanam_2023 + tanam_2024 + tanam_2025
            
            # Hanya simpan blok yang punya aktivitas tanam di 3 tahun terakhir ATAU tahun tanam >= 2022
            # Atau simpan semua untuk safety map
            
            tbm_stats[block_code] = {
                "year": p_year,
                "tanam_2023": tanam_2023,
                "tanam_2024": tanam_2024,
                "tanam_2025": tanam_2025,
                "total_tbm_3th": total_3th
            }
            
        except Exception as ex:
            # print(f"Skip {block_code}: {ex}")
            continue

    # Simpan JSON
    with open(r'data\output\tbm_stats_real.json', 'w') as f:
        json.dump(tbm_stats, f, indent=4)
        
    print(f"Sukses mengekstrak Data TBM REAL 2023-2025 untuk {len(tbm_stats)} blok.")
    
except Exception as e:
    print(f"Error: {e}")
