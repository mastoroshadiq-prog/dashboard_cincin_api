import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca data tanpa header dulu untuk mapping posisi
    df_raw = pd.read_excel(file_path, header=None, skiprows=8)
    
    targets = ['B019A', 'A012C']
    
    print(f"=== AUDIT DATA MENTAH: {targets} ===")
    
    for code in targets:
        row = df_raw[df_raw[0] == code]
        if not row.empty:
            print(f"\nBlok: {code}")
            vals = row.iloc[0].tolist()
            # Loop semua kolom, cari yang nilainya mendekati angka target
            # B019A Target: 116.17
            # A012C Target: 136.66
            
            for i, val in enumerate(vals):
                try:
                    num = float(val)
                    print(f"Index {i}: {num}")
                except:
                    pass # Skip non-numeric
        else:
            print(f"Blok {code} tidak ditemukan")

except Exception as e:
    print(f"Error: {e}")
