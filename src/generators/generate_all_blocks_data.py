"""
Generate comprehensive JSON data for ALL blocks in AME II
For interactive dashboard dropdown
"""
import pandas as pd
import numpy as np
import json
import math
from pathlib import Path

print("="*70)
print("🔥 GENERATING ALL BLOCKS DATA FOR INTERACTIVE DASHBOARD")
print("="*70)

# Load NDRE data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = [c.upper().strip() for c in df.columns]

# Convert NDRE to numeric
df['NDRE125'] = pd.to_numeric(df['NDRE125'].astype(str).str.replace(',', '.'), errors='coerce')

# Process coordinates
for col in ['N_POKOK', 'N_BARIS']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Get unique blocks
if 'BLOK_B' in df.columns:
    df['Blok'] = df['BLOK_B']
elif 'BLOK' in df.columns:
    df['Blok'] = df['BLOK']

df['Blok'] = df['Blok'].astype(str).str.strip().str.upper()
unique_blocks = sorted(df['Blok'].unique())

print(f"\n📊 Found {len(unique_blocks)} unique blocks")

# Load sisip and production data if available
try:
    df_gabungan = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')
    has_gabungan = True
    print("✅ Loaded data_gabungan.xlsx for sisip/production")
except:
    has_gabungan = False
    print("⚠️  data_gabungan.xlsx not found - sisip/production will be null")

# Load production data
try:
    with open('data/output/all_36_blocks_production_data.json', 'r') as f:
        production_data_json = json.load(f)
    print(f"✅ Loaded production data for {len(production_data_json)} blocks")
except FileNotFoundError:
    production_data_json = {}
    print("⚠️  all_36_blocks_production_data.json not found - production stats will be missing")

def calculate_v8_stats(df_block):
    """Calculate V8 algorithm statistics for a block"""
    if len(df_block) == 0:
        return None
    
    # Calculate z-scores
    mean_v = df_block['NDRE125'].mean()
    std_v = df_block['NDRE125'].std()
    
    if std_v == 0 or pd.isna(std_v):
        return None
    
    df_block = df_block.copy()
    df_block['z'] = (df_block['NDRE125'] - mean_v) / std_v
    
    # Build tree map
    tree_map = {}
    for _, row in df_block.iterrows():
        if pd.isna(row['N_POKOK']) or pd.isna(row['N_BARIS']):
            continue
        x, y = int(row['N_POKOK']), int(row['N_BARIS'])
        tree_map[f"{x},{y}"] = {'x': x, 'y': y, 'z': row['z'], 'status': 'HIJAU'}
    
    if len(tree_map) == 0:
        return None
    
    # V8 Algorithm
    z_core = -1.5
    z_neigh = -1.0
    min_n = 3
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    keys = list(tree_map.keys())
    
    # Identify MERAH cores
    cores = set()
    for k in keys:
        if tree_map[k]['z'] < z_core:
            x, y = tree_map[k]['x'], tree_map[k]['y']
            count = sum(1 for o in offsets 
                       if f"{x+o[0]},{y+o[1]}" in tree_map 
                       and tree_map[f"{x+o[0]},{y+o[1]}"]['z'] < z_neigh)
            if count >= min_n:
                tree_map[k]['status'] = 'MERAH'
                cores.add(k)
    
    # BFS for ORANYE
    queue, visited = list(cores), set(cores)
    while queue:
        k = queue.pop(0)
        x, y = tree_map[k]['x'], tree_map[k]['y']
        for o in offsets:
            nk = f"{x+o[0]},{y+o[1]}"
            if nk in tree_map and nk not in visited:
                if tree_map[nk]['z'] < z_neigh and tree_map[nk]['status'] != 'MERAH':
                    tree_map[nk]['status'] = 'ORANYE'
                    visited.add(nk)
                    queue.append(nk)
    
    # KUNING suspects
    for k in keys:
        if tree_map[k]['status'] == 'HIJAU' and tree_map[k]['z'] < z_neigh:
            tree_map[k]['status'] = 'KUNING'
    
    # Count statistics
    counts = {
        'merah': sum(1 for k in keys if tree_map[k]['status'] == 'MERAH'),
        'oranye': sum(1 for k in keys if tree_map[k]['status'] == 'ORANYE'),
        'kuning': sum(1 for k in keys if tree_map[k]['status'] == 'KUNING'),
        'hijau': sum(1 for k in keys if tree_map[k]['status'] == 'HIJAU')
    }
    
    total = len(keys)
    counts['total'] = total
    counts['attack_rate'] = ((counts['merah'] + counts['oranye']) / total * 100) if total > 0 else 0
    
    return counts

# Process all blocks
all_blocks_data = {}
processed = 0
skipped = 0

print("\n" + "="*70)
print("Processing blocks...")
print("="*70)

for block_code in unique_blocks:
    df_block = df[df['Blok'] == block_code].copy()
    
    # Skip if too few trees
    if len(df_block) < 50:
        skipped += 1
        continue
    
    # Calculate V8 stats
    stats = calculate_v8_stats(df_block)
    
    if stats is None:
        skipped += 1
        continue
    
    # Get TT (tahun tanam) if available
    tt = None
    if 'T_TANAM' in df_block.columns:
        tt_vals = df_block['T_TANAM'].dropna().unique()
        if len(tt_vals) > 0:
            try:
                tt = int(tt_vals[0])
            except:
                pass
    
    # Calculate SPH (stand per hectare) - rough estimate
    # SPH = total trees / estimated area
    # For now, use a rough estimate based on grid size
    baris_range = df_block['N_BARIS'].max() - df_block['N_BARIS'].min() + 1
    pokok_range = df_block['N_POKOK'].max() - df_block['N_POKOK'].min() + 1
    estimated_area_ha = (baris_range * pokok_range * 64) / 10000  # Rough estimate (8m x 8m spacing)
    sph = int(stats['total'] / estimated_area_ha) if estimated_area_ha > 0 else None
    
    # Build block data
    block_data = {
        'block_code': block_code,
        'total_pohon': stats['total'],
        'merah': stats['merah'],
        'oranye': stats['oranye'],
        'kuning': stats['kuning'],
        'hijau': stats['hijau'],
        'attack_rate': round(stats['attack_rate'], 1),
        'sph': sph,
        'tt': tt,
        'age': (2026 - tt) if tt else None,
        'sisip': None,  # Will be filled from data_gabungan if available
        'has_map': (Path('data/output') / f"cincin_api_map_{block_code}.png").exists(),  # Check if map exists
        'map_filename': f"cincin_api_map_{block_code}.png"
    }

    # Merge production data if available
    if block_code in production_data_json:
        prod_info = production_data_json[block_code]
        block_data.update({
            'luas_ha': prod_info.get('luas_ha', 0),
            'realisasi_ton_ha': prod_info.get('realisasi_ton_ha', 0),
            'potensi_ton_ha': prod_info.get('potensi_ton_ha', 0),
            'gap_ton_ha': prod_info.get('gap_ton_ha', 0),
            'gap_pct': prod_info.get('gap_pct', 0),
            'realisasi_total_ton': prod_info.get('realisasi_ton_total', 0),
            'potensi_total_ton': prod_info.get('potensi_ton_total', 0)
        })
    else:
        # Default values or estimate based on estimated_area_ha
        block_data.update({
            'luas_ha': round(estimated_area_ha, 1),
            'realisasi_ton_ha': 0,
            'potensi_ton_ha': 0,
            'gap_ton_ha': 0,
            'gap_pct': 0
        })

    # FINANCIAL CALCULATIONS (Centralized Logic)
    # 1. Mitigation Cost
    # Formula: sqrt(Merah + Oranye) * 8 * 4 * Rp 15,000
    infected_count = block_data['merah'] + block_data['oranye']
    mitigation_cost = (math.sqrt(infected_count) * 8 * 4 * 15000) if infected_count > 0 else 0
    block_data['mitigation_cost_idr'] = round(mitigation_cost, 2)
    block_data['mitigation_cost_juta'] = round(mitigation_cost / 1_000_000, 2)

    # 2. Loss Value
    # Formula: Abs(Gap Ton/Ha) * Luas Ha * Rp 1,500,000
    gap = block_data.get('gap_ton_ha', 0)
    luas = block_data.get('luas_ha', 0)
    loss_value = (abs(gap) * luas * 1_500_000) if gap < 0 else 0
    block_data['loss_value_idr'] = round(loss_value, 2)
    block_data['loss_value_juta'] = round(loss_value / 1_000_000, 1)

    # 3. Asset Protection & Ratio
    healthy_trees = block_data['total_pohon'] - infected_count
    asset_value = healthy_trees * 150 * 1500 # 150kg yield * 1500 price
    block_data['asset_value_idr'] = asset_value
    block_data['asset_value_juta'] = round(asset_value / 1_000_000, 0)
    
    if asset_value > 0:
        ratio = (mitigation_cost / asset_value) * 100
        block_data['mitigation_ratio_pct'] = round(ratio, 2)
    else:
        block_data['mitigation_ratio_pct'] = 0

    # 4. Narrative/Interpretation
    gap_pct = block_data.get('gap_pct', 0)
    if gap_pct > 0 and block_data['attack_rate'] > 5:
         block_data['status_narrative'] = "SYMPTOM LAG"
         block_data['status_desc'] = f"Produksi masih surplus ({gap_pct}%) meskipun serangan aktif. Kerugian belum terlihat."
    elif gap_pct < 0:
         block_data['status_narrative'] = "PRODUCTION COLLAPSE"
         block_data['status_desc'] = f"Produksi deficit ({gap_pct}%) akibat kerusakan akar masif."
    else:
         block_data['status_narrative'] = "STABLE"
         block_data['status_desc'] = "Kondisi relatif stabil."
    
    all_blocks_data[block_code] = block_data
    processed += 1
    
    if processed % 10 == 0:
        print(f"  Processed {processed} blocks...")

print(f"\n✅ Processed {processed} blocks")
print(f"⚠️  Skipped {skipped} blocks (insufficient data)")

# Sort blocks by attack rate (descending)
sorted_blocks = sorted(all_blocks_data.items(), key=lambda x: x[1]['attack_rate'], reverse=True)
ranked_data = {}
for rank, (block_code, data) in enumerate(sorted_blocks, 1):
    data['rank'] = rank
    data['severity'] = 'HIGH' if rank <= 20 else ('MEDIUM' if rank <= 50 else 'LOW')
    ranked_data[block_code] = data

# Save to JSON
output_file = 'data/output/all_blocks_data.json'
with open(output_file, 'w') as f:
    json.dump(ranked_data, f, indent=2)

print(f"\n✅ Saved to: {output_file}")

# Save as JS Embed
js_output_file = 'data/output/blocks_data_embed.js'
with open(js_output_file, 'w') as f:
    f.write("const BLOCKS_DATA = ")
    json.dump(ranked_data, f, indent=2)
    f.write(";")
print(f"✅ Saved to: {js_output_file}")

# Print top 10 for verification
print("\n" + "="*70)
print("TOP 10 BLOCKS BY ATTACK RATE:")
print("="*70)
print(f"{'Rank':<6} {'Block':<10} {'Attack Rate':<12} {'Merah':<8} {'Oranye':<8} {'Total':<8}")
print("-"*70)

for rank, (block_code, data) in enumerate(sorted_blocks[:10], 1):
    print(f"{rank:<6} {block_code:<10} {data['attack_rate']:>10.1f}%  {data['merah']:<8} {data['oranye']:<8} {data['total_pohon']:<8}")

print("\n" + "="*70)
print(f"📊 TOTAL BLOCKS IN JSON: {len(ranked_data)}")
print(f"🎯 Ready for interactive dashboard!")
print("="*70)
