import pandas as pd
import json

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    # Baca data, header di baris 7 (index 6, tapi skiprows=7 agar kolom P005 (pokok) jadi header, eh tunggu
    # Header excel agak berantakan.
    # Baris 3 (index 2) ada 'POKOK' di kolom 66.
    # Baris 7 (index 6) adalah baris data pertama? Tidak, baris 8 (index 7) data pertama.
    
    # Mari baca tanpa header lalu slice manual biar aman
    df = pd.read_excel(file_path, header=None, skiprows=8) # Mulai baca dari baris data A001A
    
    tbm_data = {}
    
    for _, row in df.iterrows():
        block_code = row[0] # Kolom A
        planting_year = row[1] # Kolom B
        pokok_count = row[66] # Kolom BO (66)
        
        # Validasi data
        if pd.notna(block_code) and isinstance(block_code, str):
            # Clean data
            try:
                pokok = int(pokok_count) if pd.notna(pokok_count) else 0
                year = int(planting_year) if pd.notna(planting_year) else 0
                
                tbm_data[block_code] = {
                    "year": year,
                    "pokok": pokok
                }
            except:
                continue
                
    # Simpan ke JSON file
    with open(r'data\output\tbm_stats_data.json', 'w') as f:
        json.dump(tbm_data, f, indent=4)
        
    print(f"Sukses mengekstrak data TBM untuk {len(tbm_data)} blok.")
    
except Exception as e:
    print(f"Error: {e}")
