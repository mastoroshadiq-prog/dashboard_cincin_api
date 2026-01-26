import pandas as pd
import numpy as np
import json

print('='*80)
print('🔥 EXTRACT CORRECT CINCIN API STATS - USING V8 ALGORITHM')
print('='*80)

# Load NDRE data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = df.columns.str.strip()

# Convert ndre125 to numeric
df['ndre125'] = pd.to_numeric(df['ndre125'], errors='coerce')

# V8 Algorithm Parameters (from dashboard_v8_interactive.py line 195-196)
z_core = -1.5  # sim_z_core
z_neighbor = -1.0  # sim_z_neighbor
min_neighbors = 3  # sim_min

print(f'\nAlgorithm Parameters (Standard Preset):')
print(f'  z_core: {z_core}')
print(f'  z_neighbor: {z_neighbor}')
print(f'  min_neighbors: {min_neighbors}')

results = {}

for blok_code, blok_name in [('F08', 'F008A'), ('D01', 'D001A')]:
    print(f'\n{"="*80}')
    print(f'📊 PROCESSING BLOK: {blok_name} ({blok_code})')
    print('='*80)
    
    # Filter data
    df_blok = df[df['blok'] == blok_code].copy()
    total_trees = len(df_blok)
    
    print(f'\nTotal trees: {total_trees}')
    
    # Calculate Z-scores
    mean_ndre = df_blok['ndre125'].mean()
    std_ndre = df_blok['ndre125'].std()
    
    print(f'Mean NDRE: {mean_ndre:.3f}')
    print(f'Std NDRE: {std_ndre:.3f}')
    
    # Z-score normalization (from v8 line 172-174)
    if std_ndre > 0:
        df_blok['z_score'] = (df_blok['ndre125'] - mean_ndre) / std_ndre
    else:
        df_blok['z_score'] = 0
    
    # Create tree map for neighbor lookup
    tree_map = {}
    trees = []
    
    for _, row in df_blok.iterrows():
        x = int(row['n_pokok'])
        y = int(row['n_baris'])
        z = row['z_score']
        
        tree = {
            'x': x,
            'y': y,
            'z': z,
            'status': 'HIJAU'
        }
        trees.append(tree)
        tree_map[f"{x},{y}"] = tree
    
    print(f'\nBuilt tree map with {len(trees)} trees')
    
    # V8 Algorithm (from line 207-221)
    # Step 1: Identify potential MERAH (core infection) candidates
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    
    merah_count = 0
    for tree in trees:
        if tree['z'] < z_core:
            # Check neighbors
            neighbors = 0
            for offset in offsets:
                neighbor_key = f"{tree['x']+offset[0]},{tree['y']+offset[1]}"
                if neighbor_key in tree_map and tree_map[neighbor_key]['z'] < z_neighbor:
                    neighbors += 1
            
            # If has enough stressed neighbors, mark as MERAH
            if neighbors >= min_neighbors:
                tree['status'] = 'MERAH'
                merah_count += 1
    
    print(f'\n🔴 MERAH (Core Infection): {merah_count} trees')
    
    # Step 2: Identify ORANYE (Ring of Fire) - neighbors of MERAH
    oranye_count = 0
    merah_trees = [t for t in trees if t['status'] == 'MERAH']
    
    for merah_tree in merah_trees:
        for offset in offsets:
            neighbor_key = f"{merah_tree['x']+offset[0]},{merah_tree['y']+offset[1]}"
            if neighbor_key in tree_map:
                neighbor = tree_map[neighbor_key]
                if neighbor['status'] != 'MERAH' and neighbor['status'] != 'ORANYE':
                    neighbor['status'] = 'ORANYE'
                    oranye_count += 1
    
    print(f'🔥 ORANYE (Ring of Fire): {oranye_count} trees')
    
    # Step 3: Identify KUNING (Suspect) - stressed but not MERAH or ORANYE
    kuning_count = 0
    for tree in trees:
        if tree['status'] == 'HIJAU' and tree['z'] < z_core:
            tree['status'] = 'KUNING'
            kuning_count += 1
    
    print(f'🟡 KUNING (Suspect): {kuning_count} trees')
    
    # Step 4: Count HIJAU (Healthy)
    hijau_count = sum(1 for t in trees if t['status'] == 'HIJAU')
    
    print(f'🟢 HIJAU (Healthy): {hijau_count} trees')
    
    # Calculate attack rate
    attack_rate = ((merah_count + oranye_count) / total_trees) * 100
    
    print(f'\n📈 ATTACK RATE: {attack_rate:.1f}%')
    
    # Store results
    results[blok_name] = {
        'blok_code': blok_code,
        'total_trees': total_trees,
        'merah': merah_count,
        'oranye': oranye_count,
        'kuning': kuning_count,
        'hijau': hijau_count,
        'attack_rate': round(attack_rate, 1),
        'mean_ndre': round(mean_ndre, 3),
        'std_ndre': round(std_ndre, 3)
    }

# Save results
with open('data/output/cincin_api_stats_v8_algorithm.json', 'w') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*80)
print('✅ SUMMARY')
print('='*80)

for blok_name, stats in results.items():
    print(f'\n{blok_name}:')
    print(f'  🔴 Merah: {stats["merah"]}')
    print(f'  🔥 Oranye: {stats["oranye"]}')
    print(f'  🟡 Kuning: {stats["kuning"]}')
    print(f'  🟢 Hijau: {stats["hijau"]}')
    print(f'  📈 Attack Rate: {stats["attack_rate"]}%')

print(f'\n📁 Saved to: data/output/cincin_api_stats_v8_algorithm.json')
