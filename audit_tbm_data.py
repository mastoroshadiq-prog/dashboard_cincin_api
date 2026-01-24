import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca data tanpa header
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    target = 'A012D'
    row = df[df[0] == target]
    
    print(f"=== AUDIT DATA TBM BLOK {target} ===")
    
    if not row.empty:
        vals = row.iloc[0].tolist()
        
        # Mapping Index (Berdasarkan temuan sebelumnya):
        # Index 1: Tahun Tanam
        # Index 37: Realisasi Tanam 2023 (Pokok) ?
        # Index 41: Realisasi Tanam 2024 (Pokok) ?
        # Index 45: Realisasi Tanam 2025 (Pokok) ?
        
        # Mari kita dump range activity tanam
        print(f"Index 1 (Tahun Tanam): {vals[1]}")
        print(f"Index 9 (Tahun Tanam Alternatif): {vals[9]}")
        
        print("\n--- Data Tanam & Sisip (Index 30-50) ---")
        for i in range(30, 51):
            val = vals[i]
            # Coba format float
            try:
                val_float = float(val)
                print(f"Index {i}: {val_float}")
            except:
                print(f"Index {i}: {val} (Nan/String)")
                
    else:
        print(f"Blok {target} TIDAK DITEMUKAN di Excel.")

except Exception as e:
    print(f"Error: {e}")
