import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from geojson import Feature, FeatureCollection, Point

print("="*80)
print("🚀 GENERATING GEOJSON VECTOR MAPS (INTERACTIVE ZOOM)")
print("="*80)

# Load data
input_file = 'data/input/tabelNDREnew.csv'
if not os.path.exists(input_file):
    input_file = 'poac_sim/data/input/tabelNDREnew.csv'

df = pd.read_csv(input_file)
df.columns = [c.upper().strip() for c in df.columns]

output_dir = Path('data/output/geojson')
output_dir.mkdir(parents=True, exist_ok=True)

def get_hex_neighbors(r: int, p: int) -> list:
    if r % 2 != 0:
        return [(r - 1, p - 1), (r - 1, p), (r, p - 1), (r, p + 1), (r + 1, p - 1), (r + 1, p)]
    else:
        return [(r - 1, p), (r - 1, p + 1), (r, p - 1), (r, p + 1), (r + 1, p), (r + 1, p + 1)]

def generate_block_geojson(df_ndre, block_name, output_path):
    # Filter Block
    if 'BLOK_B' in df_ndre.columns:
        df_ndre['Blok_Filter'] = df_ndre['BLOK_B']
    else:
        df_ndre['Blok_Filter'] = df_ndre['BLOK']
    
    df_block = df_ndre[df_ndre['Blok_Filter'].astype(str).str.strip().str.upper() == block_name].copy()
    if len(df_block) < 10: return None

    # Cleaning
    df_block['NDRE125'] = pd.to_numeric(df_block['NDRE125'].astype(str).str.replace(',', '.'), errors='coerce')
    df_block = df_block.dropna(subset=['NDRE125'])
    
    # Z-Score Calculation
    mean_v, std_v = df_block['NDRE125'].mean(), df_block['NDRE125'].std()
    df_block['z'] = (df_block['NDRE125'] - mean_v) / std_v if std_v > 0 else 0

    # Build Tree Map
    tree_map = {}
    for _, row in df_block.iterrows():
        x, y = int(row['N_POKOK']), int(row['N_BARIS'])
        tree_map[f"{x},{y}"] = {'x': x, 'y': y, 'z': row['z'], 'ndre': row['NDRE125'], 'status': 'HIJAU'}

    # Cincin Api Logic (V8)
    z_threshold = -1.2 
    min_neighbors = 3
    merah_coords = set()

    # 1. Detect Core (Red)
    for key, tree in tree_map.items():
        if tree['z'] < z_threshold:
            sick_count = 0
            for ny_neigh, nx_neigh in get_hex_neighbors(tree['y'], tree['x']):
                nk = f"{nx_neigh},{ny_neigh}"
                if nk in tree_map and tree_map[nk]['z'] < z_threshold:
                    sick_count += 1
            if sick_count >= min_neighbors:
                tree['status'] = 'MERAH'
                merah_coords.add((tree['y'], tree['x']))

    # 2. Detect Ring (Orange)
    for ry, rx in merah_coords:
        for ny, nx in get_hex_neighbors(ry, rx):
            nk = f"{nx},{ny}"
            if nk in tree_map and tree_map[nk]['status'] == 'HIJAU':
                tree_map[nk]['status'] = 'ORANYE'

    # 3. Detect Suspect (Yellow)
    for key, tree in tree_map.items():
        if tree['status'] == 'HIJAU' and tree['z'] < z_threshold:
            tree['status'] = 'KUNING'

    # Convert to GeoJSON Features
    features = []
    
    # We map Logic (Row, Pokok) to Cartesian (X, Y) for visualization
    # Hexagonal Offset Logic for visual
    for key, tree in tree_map.items():
        # X coordinate with offset for hexagonal layout
        # If Row (Y) is even, offset X by 0.5
        x_coord = tree['x'] + (0.5 if tree['y'] % 2 == 0 else 0)
        # Y coordinate stays as Row index (inverted in map usually, but clean here)
        y_coord = tree['y']

        # Determine color for frontend consumption
        color_map = {
            'MERAH': '#ef4444',   # red-500
            'ORANYE': '#f97316',  # orange-500
            'KUNING': '#eab308',  # yellow-500
            'HIJAU': '#22c55e'    # green-500
        }

        feature = Feature(
            geometry=Point((x_coord, y_coord)),
            properties={
                "id": key,
                "row": tree['y'],
                "tree": tree['x'],
                "ndre": round(tree['ndre'], 3),
                "z_score": round(tree['z'], 2),
                "status": tree['status'],
                "color": color_map[tree['status']]
            }
        )
        features.append(feature)

    feature_collection = FeatureCollection(features)

    with open(output_path, 'w') as f:
        json.dump(feature_collection, f)
    
    return len(features)

# Excecute for all AME II Blocks
ame2_blocks = df[df['DIVISI'] == 'AME II']['BLOK_B'].unique()
processed_count = 0

print(f"🎯 Processing {len(ame2_blocks)} blocks for GeoJSON export...")

for i, block in enumerate(sorted(ame2_blocks)):
    out_file = output_dir / f"{block}.json"
    count = generate_block_geojson(df, block, out_file)
    if count:
        processed_count += 1
        if i % 5 == 0:
            print(f"  [{i+1}/{len(ame2_blocks)}] Filtered {block}: {count} trees")

print(f"\n✅ SUCCESS: Generated {processed_count} GeoJSON vector maps in data/output/geojson/")
