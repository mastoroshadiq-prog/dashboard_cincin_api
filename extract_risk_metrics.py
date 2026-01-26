import pandas as pd
import json

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(file_path, header=None, skiprows=8)
    
    risk_data = {}
    
    # Mapping Index (Verified by debug_risk_data.py)
    # Col 0: Block Code
    # Col 66: Populasi (Pokok)
    # Col 68: SPH
    # Col 55: Serangan Ganoderma (Pokok)
    
    for _, row in df.iterrows():
        block_code = row[0]
        if pd.isna(block_code) or not isinstance(block_code, str):
            continue
            
        try:
            pokok = float(row[66]) if pd.notna(row[66]) else 0
            sph = float(row[68]) if pd.notna(row[68]) else 0
            infected = float(row[55]) if pd.notna(row[55]) else 0
            
            # Hitung Attack Rate %
            attack_rate = 0
            if pokok > 0:
                attack_rate = (infected / pokok) * 100
                
            risk_data[block_code] = {
                "sph": round(sph, 2),
                "total_infected": int(infected),
                "attack_rate": round(attack_rate, 2),
                "loss_value_juta": 0 # Sementara 0 dulu, nanti logic JS bisa estimasi
            }
        except Exception as ex:
             # print(f"Error {block_code}: {ex}")
             continue
             
    # Simpan JSON
    with open(r'data\output\risk_metrics_real.json', 'w') as f:
        json.dump(risk_data, f, indent=4)
        
    print(f"Sukses mengekstrak Risk Metrics untuk {len(risk_data)} blok.")
    
except Exception as e:
    print(f"Error: {e}")
