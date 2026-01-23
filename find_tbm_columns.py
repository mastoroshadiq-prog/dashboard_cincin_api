import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    # Baca header lagi untuk mencari kolom TBM spesifik
    df = pd.read_excel(file_path, header=6, nrows=0)
    cols = df.columns.tolist()
    
    print("=== MENCARI KOLOM TBM (2023-2025) ===")
    
    # Keyword pencarian
    keywords = ['tbm', 'pokok', 'jlh', 'jumlah', 'populasi', 'stand', 'palms']
    
    found_cols = []
    for i, col in enumerate(cols):
        col_lower = str(col).lower()
        if any(k in col_lower for k in keywords):
            found_cols.append(f"Index {i}: {col}")
            
    print("\nKandidat Kolom Ditemukan:")
    for c in found_cols:
        print(c)
        
    # Cek level header di atasnya jika header utama kurang jelas
    # Kadang info tahun ada di merge header baris ke-4 atau 5
    print("\n--- Cek Multi-Header ---")
    df_multi = pd.read_excel(file_path, header=[3, 4, 5, 6], nrows=0)
    print("Sample Multi-Header columns:")
    print(df_multi.columns[:20])

except Exception as e:
    print(f"Error: {e}")
