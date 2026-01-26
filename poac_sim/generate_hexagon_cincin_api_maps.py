import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from pathlib import Path
import sys

sys.path.insert(0, '.')

def generate_hexagon_cincin_api_map(df_ndre, block_name, output_path):
    """Generate hexagonal scatter plot exactly matching reference image style"""
    
    # Filter for target block
    if 'BLOK_B' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK_B']
    elif 'BLOK' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK']
    
    df_ndre['Blok'] = df_ndre['Blok'].astype(str).str.strip().str.upper()
    block_data = df_ndre[df_ndre['Blok'] == block_name].copy()
    
    if len(block_data) == 0:
        print(f"No data found for block {block_name}")
        return None
    
    # Ensure columns are numeric
    if 'NDRE125' in block_data.columns:
        block_data['NDRE125'] = pd.to_numeric(
            block_data['NDRE125'].astype(str).str.replace(',', '.'), 
            errors='coerce'
        )
        block_data = block_data.dropna(subset=['NDRE125'])
    else:
        print(f"NDRE125 column not found")
        return None
    
    for col in ['N_POKOK', 'N_BARIS']:
        if col in block_data.columns:
            block_data[col] = pd.to_numeric(block_data[col], errors='coerce')
    
    block_data = block_data.dropna(subset=['N_POKOK', 'N_BARIS'])
    
    if len(block_data) == 0:
        print(f"No valid data after cleaning for {block_name}")
        return None
    
    print(f"Processing {len(block_data)} trees for {block_name}")
    
    # Calculate z-scores
    mean_v = block_data['NDRE125'].mean()
    std_v = block_data['NDRE125'].std()
    
    if std_v == 0:
        block_data['z'] = 0
    else:
        block_data['z'] = (block_data['NDRE125'] - mean_v) / std_v
    
    # Build tree map
    tree_map = {}
    for _, row in block_data.iterrows():
        x = int(row['N_POKOK'])
        y = int(row['N_BARIS'])
        key = f"{x},{y}"
        tree_map[key] = {
            'x': x,
            'y': y,
            'z': row['z'],
            'status': 'HIJAU'
        }
    
    # Cincin Api Algorithm
    z_core = -1.5
    z_neigh = -1.0
    min_n = 3
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    keys = list(tree_map.keys())
    
    # Identify Cores (RED)
    cores = set()
    for k in keys:
        if tree_map[k]['z'] < z_core:
            x, y = tree_map[k]['x'], tree_map[k]['y']
            count = 0
            for o in offsets:
                nk = f"{x+o[0]},{y+o[1]}"
                if nk in tree_map and tree_map[nk]['z'] < z_neigh:
                    count += 1
            if count >= min_n:
                tree_map[k]['status'] = 'MERAH'
                cores.add(k)
    
    # Identify Ring of Fire (ORANGE) - BFS from cores
    queue = list(cores)
    visited = set(cores)
    
    while queue:
        k = queue.pop(0)
        x, y = tree_map[k]['x'], tree_map[k]['y']
        for o in offsets:
            nk = f"{x+o[0]},{y+o[1]}"
            if nk in tree_map and nk not in visited:
                if tree_map[nk]['z'] < z_neigh:
                    if tree_map[nk]['status'] != 'MERAH':
                        tree_map[nk]['status'] = 'ORANYE'
                    visited.add(nk)
                    queue.append(nk)
    
    # Identify Suspects (YELLOW)
    for k in keys:
        if tree_map[k]['status'] == 'HIJAU' and tree_map[k]['z'] < z_neigh:
            tree_map[k]['status'] = 'KUNING'
    
    # Count statistics
    counts = {
        'MERAH': sum(1 for k in keys if tree_map[k]['status'] == 'MERAH'),
        'ORANYE': sum(1 for k in keys if tree_map[k]['status'] == 'ORANYE'),
        'KUNING': sum(1 for k in keys if tree_map[k]['status'] == 'KUNING'),
        'HIJAU': sum(1 for k in keys if tree_map[k]['status'] == 'HIJAU')
    }
    
    total = len(keys)
    
    # Create figure - taller aspect ratio like reference
    fig, ax = plt.subplots(figsize=(8, 14), facecolor='white')
    
    # Color mapping - vibrant colors matching reference
    color_map = {
        'MERAH': '#e74c3c',    # Bright Red
        'ORANYE': '#ff9500',   # Pure Orange
        'KUNING': '#ffd700',   # Gold Yellow
        'HIJAU': '#2ecc71'     # Emerald Green
    }
    
    # Hexagon parameters for tight packing
    hex_radius = 0.48  # Slightly smaller for tighter fit
    
    # Draw hexagons - TWO PASSES for proper layering
    # Pass 1: Draw all non-MERAH hexagons first
    for k in keys:
        tree = tree_map[k]
        if tree['status'] != 'MERAH':
            x = tree['x']
            y = tree['y']
            status = tree['status']
            
            hexagon = RegularPolygon(
                (x, y), 
                numVertices=6, 
                radius=hex_radius,
                orientation=0,
                facecolor=color_map[status],
                edgecolor=color_map[status],
                linewidth=0.3,
                zorder=1
            )
            ax.add_patch(hexagon)
    
    # Pass 2: Draw MERAH hexagons on top with thick black border
    for k in keys:
        tree = tree_map[k]
        if tree['status'] == 'MERAH':
            x = tree['x']
            y = tree['y']
            
            hexagon = RegularPolygon(
                (x, y), 
                numVertices=6, 
                radius=hex_radius,
                orientation=0,
                facecolor=color_map['MERAH'],
                edgecolor='black',
                linewidth=2.5,  # Very thick border
                zorder=2  # Draw on top
            )
            ax.add_patch(hexagon)
    
    # Set axis properties
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    ax.set_xlim(min(x_coords) - 1.5, max(x_coords) + 1.5)
    ax.set_ylim(min(y_coords) - 1.5, max(y_coords) + 1.5)
    
    # Labels
    ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=11, fontweight='bold')
    
    # Title with statistics - matching reference format
    title = f'#05 - BLOK {block_name} - PETA KLUSTER GANODERMA\n'
    title += f'Total Pohon: {total} | MERAH: {counts["MERAH"]} | KUNING: {counts["KUNING"]} | ORANYE: {counts["ORANYE"]}'
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    
    # Legend - matching reference style
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_map['MERAH'], edgecolor='black', linewidth=2,
              label=f'MERAH - Kluster Aktif ({counts["MERAH"]})'),
        Patch(facecolor=color_map['ORANYE'], edgecolor=color_map['ORANYE'],
              label=f'ORANYE - Cincin Api ({counts["ORANYE"]})'),
        Patch(facecolor=color_map['KUNING'], edgecolor=color_map['KUNING'],
              label=f'KUNING - Suspect ({counts["KUNING"]})'),
        Patch(facecolor=color_map['HIJAU'], edgecolor=color_map['HIJAU'],
              label=f'HIJAU - Sehat ({counts["HIJAU"]})')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
              framealpha=0.95, edgecolor='black', fancybox=False)
    
    # Grid - subtle
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5, color='gray')
    ax.set_aspect('equal')
    
    # Invert y-axis to match reference
    ax.invert_yaxis()
    
    # Tight layout
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Generated hexagonal map for {block_name}: {output_path}")
    
    return counts

# Main execution
print("🔥 Generating Hexagonal Cincin Api Maps (Exact Reference Match)...\n")

# Load NDRE data
p1 = Path('data/input/tabelNDREnew.csv')
if not p1.exists():
    p1 = Path('../data/input/tabelNDREnew.csv')

try:
    df1 = pd.read_csv(p1, sep=None, engine='python')
except:
    df1 = pd.read_csv(p1)

df1.columns = [c.upper().strip() for c in df1.columns]

# Generate hexagonal maps
output_dir = Path('data/output')
output_dir.mkdir(exist_ok=True, parents=True)

stats_d006a = generate_hexagon_cincin_api_map(df1, 'D006A', output_dir / 'cincin_api_map_D006A.png')
stats_d007a = generate_hexagon_cincin_api_map(df1, 'D007A', output_dir / 'cincin_api_map_D007A.png')

print("\n" + "="*60)
print("🔥 Hexagonal Cincin Api Maps Generated!")
print("="*60)
if stats_d006a:
    print(f"\nBlock D006A:")
    print(f"  🔴 Merah: {stats_d006a['MERAH']}, 🔥 Oranye: {stats_d006a['ORANYE']}, "
          f"🟡 Kuning: {stats_d006a['KUNING']}, 🟢 Hijau: {stats_d006a['HIJAU']}")
if stats_d007a:
    print(f"\nBlock D007A:")
    print(f"  🔴 Merah: {stats_d007a['MERAH']}, 🔥 Oranye: {stats_d007a['ORANYE']}, "
          f"🟡 Kuning: {stats_d007a['KUNING']}, 🟢 Hijau: {stats_d007a['HIJAU']}")
print("\n✅ Maps generated matching reference image style")
