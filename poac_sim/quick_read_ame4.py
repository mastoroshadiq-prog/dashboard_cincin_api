
import pandas as pd
import numpy as np
from pathlib import Path

def calculate_status(path):
    print(f"Reading {path}...")
    try:
        df = pd.read_csv(path, sep=';')
    except:
        df = pd.read_csv(path) # try default
        
    print(f"Columns: {df.columns.tolist()}")
    
    # Normalize col names
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Inspect BLOK_B
    if 'blok_b' in df.columns:
        print(f"Sample BLOK_B: {df['blok_b'].unique()[:10]}")
        df['blok'] = df['blok_b'].astype(str).str.strip().str.upper()
    else:
        df['blok'] = df['blok'].astype(str).str.strip().str.upper()

    targets = ['A004A', 'A005A']
    target_df = df[df['blok'].isin(targets)]
    
    print(f"Found {len(target_df)} rows for targets.")
    
    if len(target_df) == 0:
        print(f"Unique blocks: {df['blok'].unique()[:10]}")
        return

    # Logic
    z_core = -1.5
    z_neighbor = -1.0
    min_neighbors = 3
    
    for blok, group in target_df.groupby('blok'):
        # 1. Z-Score
        # Clean numeric
        group['ndre125'] = pd.to_numeric(group['ndre125'].astype(str).str.replace(',', '.'), errors='coerce')
        
        ndvi = group['ndre125']
        mean_val = ndvi.mean()
        std_val = ndvi.std()
        
        group = group.copy()
        if std_val != 0:
            group['z'] = (group['ndre125'] - mean_val) / std_val
        else:
            group['z'] = 0
            
        # Map
        tree_map = {}
        for _, row in group.iterrows():
            key = f"{int(row['n_pokok'])},{int(row['n_baris'])}"
            tree_map[key] = {'z': row['z'], 'status': 'GREEN'}

        offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        keys = list(tree_map.keys())
        
        # Red
        cores = set()
        for k in keys:
            node = tree_map[k]
            if node['z'] < z_core:
                x, y = map(int, k.split(','))
                c = 0
                for o in offsets:
                    nk = f"{x+o[0]},{y+o[1]}"
                    if nk in tree_map and tree_map[nk]['z'] < z_neighbor:
                        c += 1
                if c >= min_neighbors:
                    tree_map[k]['status'] = 'MERAH'
                    cores.add(k)
                    
        # Orange
        queue = list(cores)
        visited = set(cores)
        while queue:
            k = queue.pop(0)
            cx, cy = map(int, k.split(','))
            for o in offsets:
                nk = f"{cx+o[0]},{cy+o[1]}"
                if nk in tree_map and nk not in visited:
                    if tree_map[nk]['z'] < z_neighbor:
                        if tree_map[nk]['status'] != 'MERAH':
                             tree_map[nk]['status'] = 'ORANYE'
                        visited.add(nk)
                        queue.append(nk)
        
        # Yellow
        for k in keys:
            if tree_map[k]['status'] == 'GREEN' and tree_map[k]['z'] < z_neighbor:
                tree_map[k]['status'] = 'KUNING'
                
        # Count
        counts = {'MERAH': 0, 'ORANYE': 0, 'KUNING': 0, 'GREEN': 0}
        total = len(group)
        for k in keys:
             counts[tree_map[k]['status']] += 1
             
        print(f"\nBLOCK {blok}")
        print(f"Red: {counts['MERAH']} ({counts['MERAH']/total:.1%})")
        print(f"Orange: {counts['ORANYE']} ({counts['ORANYE']/total:.1%})")
        print(f"Yellow: {counts['KUNING']} ({counts['KUNING']/total:.1%})")

path = Path('../data/input/AME_IV.csv')
if not path.exists(): path = Path('data/input/AME_IV.csv')

calculate_status(path)
