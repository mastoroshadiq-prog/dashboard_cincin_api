
import pandas as pd
import json
import re

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    # OUTPUT FORMAT
    # "BLOCK_CODE": { "year": 2023, "tanam_2023": 100, "tanam_2024": 50, "tanam_2025": 0, "total_tbm_3th": 150 }
    
    tbm_data = {}
    
    for _, row in df.iterrows():
        block_code = row[0]
        if pd.isna(block_code) or not isinstance(block_code, str):
            continue
            
        # Index Mapping
        # Tahun Tanam: Index 1 (Col B)
        # Realisasi Tanam (Pokok) - REVISED AUDIT 2026-01-25 (Header Row Check)
        # 2023: Index 40 (Col 41)
        # 2024: Index 43 (Col 44)
        # 2025: Index 47 (Col 48)
        
        try:
            thn_tanam = int(row[1]) if pd.notna(row[1]) and str(row[1]).replace('.','').isdigit() else 0
            
            t23 = float(row[40]) if pd.notna(row[40]) else 0
            t24 = float(row[43]) if pd.notna(row[43]) else 0
            t25 = float(row[47]) if pd.notna(row[47]) else 0
            
            total_3th = t23 + t24 + t25
            
            # FILTER KETAT:
            # Hanya blok yang PUNYA aktivitas tanam atau TBM baru (>= 2021)
            # Jika thn_tanam 0 dan total 0 -> SKIP
            
            is_valid_tbm = False
            if total_3th > 0:
                is_valid_tbm = True
            elif thn_tanam >= 2021:
                is_valid_tbm = True
                
            if is_valid_tbm:
                tbm_data[block_code] = {
                    "year": thn_tanam,
                    "tanam_2023": int(t23),
                    "tanam_2024": int(t24),
                    "tanam_2025": int(t25),
                    "total_tbm_3th": int(total_3th)
                }
                
        except Exception as ex:
             continue

    # Simpan JSON
    output_path = r'data\output\tbm_stats_real.json'
    with open(output_path, 'w') as f:
        json.dump(tbm_data, f, indent=4)
        
    print(f"Sukses mengekstrak TBM Data (Filtered) untuk {len(tbm_data)} blok.")
    
except Exception as e:
    print(f"Error: {e}")
