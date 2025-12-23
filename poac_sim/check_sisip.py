
import pandas as pd
from pathlib import Path

def check_sisip_variation(filepath, name, col_blok, col_tahun):
    print(f"\n--- ANALISIS VARIASI TAHUN TANAM: {name} ---")
    try:
        if name == 'AME IV':
            df = pd.read_csv(filepath, sep=';')
            # Mapping AME IV issues (re-using logic from dashboard_v7)
            # T_TANAM -> Blok, N_BARIS -> Tahun
            df['BLOK_REAL'] = df['T_TANAM'] 
            df['TAHUN_REAL'] = pd.to_numeric(df['N_BARIS'], errors='coerce')
        else:
            df = pd.read_csv(filepath)
            df.columns = df.columns.str.lower()
            df['BLOK_REAL'] = df[col_blok]
            df['TAHUN_REAL'] = pd.to_numeric(df[col_tahun], errors='coerce')

        sisip_blocks = 0
        total_blocks = 0
        
        for blok, group in df.groupby('BLOK_REAL'):
            total_blocks += 1
            years = group['TAHUN_REAL'].dropna().unique()
            if len(years) > 1:
                sisip_blocks += 1
                counts = group['TAHUN_REAL'].value_counts()
                major_year = counts.idxmax()
                minor_years = [y for y in years if y != major_year]
                count_sisip = group[group['TAHUN_REAL'].isin(minor_years)].shape[0]
                
                if sisip_blocks <= 5: # Show sample
                    print(f"Blok {blok}: Mayoritas {int(major_year)} ({counts[major_year]}), Sisip {minor_years} ({count_sisip} pohon)")
        
        print(f"KESIMPULAN {name}: {sisip_blocks} dari {total_blocks} blok memiliki data sisip (beda tahun).")
            
    except Exception as e:
        print(f"Error {name}: {e}")

# Check AME II
check_sisip_variation('data/input/tabelNDREnew.csv', 'AME II', 'blok', 't_tanam')

# Check AME IV
check_sisip_variation('data/input/AME_IV.csv', 'AME IV', 'T_TANAM', 'N_BARIS')
