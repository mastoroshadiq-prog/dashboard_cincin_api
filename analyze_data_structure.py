import pandas as pd

try:
    # Membaca header file excel untuk memahami struktur data
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    # Membaca baris ke-7 (index 6) yang sepertinya header utama berdasarkan sesi sebelumnya
    df = pd.read_excel(file_path, header=6, nrows=0)
    
    print("=== STRUKTUR DATA (DATA GABUNGAN) ===")
    print(f"Total Kolom: {len(df.columns)}")
    print("\nSampel Header Kolom Utama:")
    # Menampilkan kolom-kolom kunci untuk identifikasi
    cols = df.columns.tolist()
    print(cols[:10])  # Identitas Blok
    
    # Mencari pola kolom penting
    yield_cols = [c for c in cols if 'real' in str(c).lower() or 'ton' in str(c).lower()]
    risk_cols = [c for c in cols if 'sph' in str(c).lower() or 'pokok' in str(c).lower() or 'serangan' in str(c).lower()]
    year_cols = [c for c in cols if 'tahun' in str(c).lower() or 'tanam' in str(c).lower()]
    
    print("\nKelompok Data Teridentifikasi:")
    print(f"- Kolom Produksi/Yield: {len(yield_cols)} kolom")
    print(f"- Kolom Risiko (SPH/Serangan): {len(risk_cols)} kolom")
    print(f"- Kolom Tahun Tanam: {len(year_cols)} kolom")
    
except Exception as e:
    print(f"Error reading Excel: {e}")
