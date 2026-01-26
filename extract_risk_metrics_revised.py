import pandas as pd
import json

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    risk_data = {}
    
    # REVISI INDEX BERDASARKAN AUDIT (Ground Truth User)
    # Col 0: Block Code
    # Col 53: Pokok Sensus (Aktual)
    # Col 54: SPH Sensus (Aktual) - TARGET USER
    # Col 55: Serangan Ganoderma (Pokok)
    
    for _, row in df.iterrows():
        block_code = row[0]
        if pd.isna(block_code) or not isinstance(block_code, str):
            continue
            
        try:
            pokok_sensus = float(row[53]) if pd.notna(row[53]) else 0
            sph_sensus = float(row[54]) if pd.notna(row[54]) else 0
            infected = float(row[55]) if pd.notna(row[55]) else 0
            
            # Hitung Attack Rate %
            attack_rate = 0
            if pokok_sensus > 0:
                attack_rate = (infected / pokok_sensus) * 100
            elif sph_sensus > 0: # Fallback jika pokok 0 tapi sph ada
                 pass
                 
            risk_data[block_code] = {
                "sph": round(sph_sensus, 2),
                "total_infected": int(infected),
                "attack_rate": round(attack_rate, 2),
                "loss_value_juta": 0
            }
        except Exception as ex:
             # print(f"Error {block_code}: {ex}")
             continue
             
    # Simpan JSON
    with open(r'data\output\risk_metrics_real.json', 'w') as f:
        json.dump(risk_data, f, indent=4)
        
    print(f"Sukses mengekstrak REVISED Risk Metrics (Index 53, 54, 55) untuk {len(risk_data)} blok.")
    
except Exception as e:
    print(f"Error: {e}")
