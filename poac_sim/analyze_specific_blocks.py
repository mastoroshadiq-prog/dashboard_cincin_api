
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent dir to path to find src
sys.path.insert(0, '.')
try:
    from src.ingestion import load_and_clean_data
except ImportError:
    # If run from poac_sim folder
    sys.path.insert(0, '..')
    from src.ingestion import load_and_clean_data

def get_detailed_block_stats(df_ndre, target_blocks):
    """
    Calculate detailed stats (Red, Orange, Yellow) for specific blocks.
    Using Standard Preset: z_core=-1.5, z_neighbor=-1.0, min=3
    """
    z_core = -1.5
    z_neighbor = -1.0
    min_neighbors = 3
    
    results = []
    
    # Filter for target blocks
    if 'BLOK' in df_ndre.columns: df_ndre['Blok'] = df_ndre['BLOK']
    df_ndre['Blok'] = df_ndre['Blok'].astype(str).str.strip().str.upper()
    
    print(f"Total Unique Blocks: {len(df_ndre['Blok'].unique())}")
    a_blocks = [b for b in df_ndre['Blok'].unique() if 'A00' in b]
    print(f"Blocks with 'A00': {a_blocks[:20]}")
    
    target_df = df_ndre[df_ndre['Blok'].isin(target_blocks)]
    print(f"Filtered Rows: {len(target_df)}")
    
    for blok, group in target_df.groupby('Blok'):
        # 1. Z-Score
        ndvi = group['NDRE125']
        mean_val = ndvi.mean()
        std_val = ndvi.std()
        
        group = group.copy()
        if std_val != 0:
            group['z'] = (group['NDRE125'] - mean_val) / std_val
        else:
            group['z'] = 0
        
        # 2. Build Map
        tree_map = {}
        for _, row in group.iterrows():
            key = f"{int(row['N_POKOK'])},{int(row['N_BARIS'])}"
            tree_map[key] = {'z': row['z'], 'status': 'GREEN'} # Default Green
            
        # 3. Logic
        offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        keys = list(tree_map.keys())
        
        # Step 3a: Identify Cores (MERAH)
        cores = set()
        for k in keys:
            node = tree_map[k]
            if node['z'] < z_core:
                # Check neighbors
                x, y = map(int, k.split(','))
                count = 0
                for o in offsets:
                    nk = f"{x+o[0]},{y+o[1]}"
                    if nk in tree_map and tree_map[nk]['z'] < z_neighbor:
                        count += 1
                
                if count >= min_neighbors:
                    tree_map[k]['status'] = 'MERAH'
                    cores.add(k)
        
        # Step 3b: Identify Ring of Fire (ORANYE)
        queue = list(cores)
        visited = set(cores)
        
        while queue:
            curr_key = queue.pop(0)
            cx, cy = map(int, curr_key.split(','))
            
            for o in offsets:
                nx, ny = cx + o[0], cy + o[1]
                nk = f"{nx},{ny}"
                
                if nk in tree_map and nk not in visited:
                    idx_z = tree_map[nk]['z']
                    curr_status = tree_map[nk]['status']
                    
                    if idx_z < z_neighbor:
                        if curr_status != 'MERAH':
                            tree_map[nk]['status'] = 'ORANYE'
                        visited.add(nk)
                        queue.append(nk)
                        
        # Step 3c: Identify Suspects (KUNING)
        for k in keys:
            if tree_map[k]['status'] == 'GREEN':
                if tree_map[k]['z'] < z_neighbor:
                    tree_map[k]['status'] = 'KUNING'

        # 4. Count
        counts = {'MERAH': 0, 'ORANYE': 0, 'KUNING': 0, 'HIJAU': 0}
        total = len(group)
        for k in keys:
            s = tree_map[k]['status']
            if s == 'GREEN': counts['HIJAU'] += 1
            else: counts[s] += 1
            
        results.append({
            'Blok': blok,
            'Estate': group['ESTATE'].iloc[0] if 'ESTATE' in group.columns else 'AME 001', # Default to AME001 if unknown
            'Tree_Count': total,
            'Merah': counts['MERAH'],
            'Merah_Pct': (counts['MERAH']/total)*100,
            'Oranye': counts['ORANYE'],
            'Oranye_Pct': (counts['ORANYE']/total)*100,
            'Kuning': counts['KUNING'],
            'Kuning_Pct': (counts['KUNING']/total)*100,
            'Trench_Criticality': "SANGAT PERLU (Prioritas Tinggi)" if counts['MERAH'] > 20 else "PERLU PENGAWASAN"
        })
        
    return results

def main():
    print("Running detailed analysis for A004A and A005A...")
    # Try AME_IV.csv
    path_ndre = Path('data/input/AME_IV.csv')
    if not path_ndre.exists(): path_ndre = Path('../data/input/AME_IV.csv')
    
    print(f"Loading from: {path_ndre}")
    df_ndre = load_and_clean_data(path_ndre)
    stats = get_detailed_block_stats(df_ndre, ['A004A', 'A005A'])
    
    with open('analysis_output_utf8.txt', 'w', encoding='utf-8') as f:
        for s in stats:
            f.write(f"\nBLOCK: {s['Blok']} (Estate: {s['Estate']})\n")
            f.write(f"Total Trees: {s['Tree_Count']}\n")
            f.write(f"🔴 Merah (Infected): {s['Merah']} ({s['Merah_Pct']:.1f}%)\n")
            f.write(f"🟠 Oranye (Ring)   : {s['Oranye']} ({s['Oranye_Pct']:.1f}%)\n")
            f.write(f"🟡 Kuning (Suspect): {s['Kuning']} ({s['Kuning_Pct']:.1f}%)\n")
            f.write(f"KRUSIALITAS PARIT  : {s['Trench_Criticality']}\n")
    print("Analysis complete. Saved to analysis_output_utf8.txt")

main()
