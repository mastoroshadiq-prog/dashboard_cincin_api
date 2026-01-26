
import pandas as pd
import numpy as np

try:
    print("--- DIAGNOSTIK DATA MATCHING ---\n")

    # 1. Load Data Drone (tabelNDREnew.csv)
    # Ini sumber data visualisasi Cincin Api
    df_ndre = pd.read_csv('data/input/tabelNDREnew.csv')
    # Normalisasi lowercase agar fair comparison
    df_ndre.columns = df_ndre.columns.str.lower()
    
    # Cari kolom blok di drone
    col_blok_ndre = 'blok' if 'blok' in df_ndre.columns else df_ndre.columns[1] # Asumsi col 2
    
    unique_drone = sorted(df_ndre[col_blok_ndre].dropna().astype(str).unique().tolist())
    print(f"[DRONE DATA] Total Blok Unik: {len(unique_drone)}")
    print(f"Sample (First 15): {unique_drone[:15]}")
    
    # 2. Load Data Cost Control (data_baru.csv)
    # Ini sumber data Ghost Tree
    df_cost = pd.read_csv('data/input/data_baru.csv', header=4)
    
    # Cari kolom blok di cost control (BARU.2 / Index 2)
    # Gunakan logic yang sama dengan dashboard v8.2
    blok_col_cost = None
    for c in df_cost.columns:
        if 'BARU.2' in c or 'BLOK' in c.upper():
             sample = df_cost[c].dropna().astype(str).unique()
             if len(sample) > 5:
                 blok_col_cost = c
                 break
    if not blok_col_cost: blok_col_cost = df_cost.columns[2] # Fallback index 2
    
    unique_cost = sorted(df_cost[blok_col_cost].dropna().astype(str).unique().tolist())
    
    # Clean cost data (remove spaces) like in script
    unique_cost_clean = sorted([s.replace(" ", "").upper() for s in unique_cost])
    
    print(f"\n[COST DATA] Total Blok Unik: {len(unique_cost)}")
    print(f"Col used: {blok_col_cost}")
    print(f"Sample Raw (First 15): {unique_cost[:15]}")
    print(f"Sample Clean (First 15): {unique_cost_clean[:15]}")
    
    # 3. Intersection Analysis
    set_drone = set([s.upper().replace(" ", "") for s in unique_drone])
    set_cost = set(unique_cost_clean)
    
    matches = set_drone.intersection(set_cost)
    
    print("\n--- HASIL MATCHING ---")
    print(f"Jumlah Match: {len(matches)}")
    print(f"Persentase Match: {len(matches)/len(set_drone)*100:.1f}% dari data Drone")
    
    if len(matches) == 0:
        print("\n❌ TIDAK ADA MATCH SAMA SEKALI!")
        print("Saran: Perhatikan perbedaan format di atas.")
        print("Dugaan: Apakah Blok di Drone pakai 'C006' tapi di Cost 'C06'?")
    else:
        print(f"Review Match: {list(matches)[:10]}")
        
except Exception as e:
    print(f"Error: {e}")
