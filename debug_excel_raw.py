import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca 10 baris pertama tanpa header untuk melihat struktur raw
    print("=== INSPEKSI RAW HEADER (Baris 0-10) ===")
    df_raw = pd.read_excel(file_path, header=None, nrows=10)
    
    # Tampilkan baris demi baris, tapi hanya kolom 0-50 agar tidak banjir
    # Kita cari perpotongan "Pokok" atau "TBM" dengan "2023/2024/2025"
    for idx, row in df_raw.iterrows():
        row_str = " | ".join([str(x) for x in row[:50] if pd.notna(x)])
        print(f"Baris {idx}: {row_str}")

except Exception as e:
    print(f"Error: {e}")
