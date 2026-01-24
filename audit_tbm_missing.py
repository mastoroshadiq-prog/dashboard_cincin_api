import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    targets = ['B006D', 'C003A', 'C004F']
    print(f"=== AUDIT BLOK TBM BERMASALAH: {targets} ===")
    
    for code in targets:
        row = df[df[0] == code]
        if not row.empty:
            print(f"\nBlok: {code}")
            vals = row.iloc[0].tolist()
            
            # Cek Tahun Tanam (Index 1)
            print(f"Tahun Tanam (Index 1): {vals[1]}")
            
            # Dump semua kolom yang punya nilai angka signifikan (> 0) di range 30 - 60
            print("Nilai Angka di Range Index 30-60:")
            has_data = False
            for i in range(30, 60):
                try:
                    num = float(vals[i])
                    if num > 0:
                        print(f"  Index {i}: {num}")
                        has_data = True
                except:
                    pass
            
            if not has_data:
                print("  (Tidak ada data angka > 0 di range 30-60)")
                
        else:
            print(f"Blok {code} tidak ditemukan.")

except Exception as e:
    print(f"Error: {e}")
