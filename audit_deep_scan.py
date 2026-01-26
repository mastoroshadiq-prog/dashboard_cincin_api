import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    print("=== CEK DUPLIKASI & DATA TERSEMBUNYI ===")
    
    # COUNT C003A
    c003a_count = len(df[df[0] == 'C003A'])
    print(f"Jumlah Baris Blok C003A: {c003a_count}")
    
    # SCAN FULL B006D
    b006d = df[df[0] == 'B006D']
    if not b006d.empty:
        print("\n--- DATA LENGKAP B006D (Semua Kolom > 0) ---")
        vals = b006d.iloc[0].tolist()
        for i, val in enumerate(vals):
            try:
                num = float(val)
                if num > 0:
                    print(f"Index {i}: {num}")
            except:
                pass
                
except Exception as e:
    print(f"Error: {e}")
