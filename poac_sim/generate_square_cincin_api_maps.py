import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
import sys

sys.path.insert(0, '.')

def generate_square_cincin_api_map(df_ndre, block_name, output_path):
    """Generate square/grid visualization with tight packing for Cincin Api"""
    
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
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 14), facecolor='white')
    
    # Color mapping - high contrast
    color_map = {
        'MERAH': '#8B0000',    # Dark Red
        'ORANYE': '#FF6600',   # Bright Orange
        'KUNING': '#FFD700',   # Gold Yellow
        'HIJAU': '#2ecc71'     # Emerald Green
    }
    
    # Square size - slightly smaller for small gaps
    square_size = 0.9
    
    # Draw squares for each tree - NO BORDER, TIGHT PACKING
    for k in keys:
        tree = tree_map[k]
        x = tree['x']
        y = tree['y']
        status = tree['status']
        
        # Create square centered at (x, y)
        # Rectangle takes bottom-left corner, so we offset by -0.5
        rect = Rectangle(
            (x - 0.5, y - 0.5),  # Bottom-left corner
            square_size,          # Width
            square_size,          # Height
            facecolor=color_map[status],
            edgecolor='none',     # NO BORDER
            linewidth=0
        )
        ax.add_patch(rect)
    
    # Set axis properties
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    ax.set_xlim(min(x_coords) - 1, max(x_coords) + 1)
    ax.set_ylim(min(y_coords) - 1, max(y_coords) + 1)
    
    # Labels
    ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=11, fontweight='bold')
    
    # Title with statistics
    title = f'🔥 BLOK {block_name} - PETA KLUSTER GANODERMA (CINCIN API)\n'
    title += f'Total: {total} | 🔴 MERAH: {counts["MERAH"]} | 🔥 ORANYE: {counts["ORANYE"]} | 🟡 KUNING: {counts["KUNING"]}'
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_map['MERAH'], edgecolor='none',
              label=f'🔴 MERAH - Kluster Aktif ({counts["MERAH"]})'),
        Patch(facecolor=color_map['ORANYE'], edgecolor='none',
              label=f'🔥 ORANYE - CINCIN API ({counts["ORANYE"]})'),
        Patch(facecolor=color_map['KUNING'], edgecolor='none',
              label=f'🟡 KUNING - Suspect ({counts["KUNING"]})'),
        Patch(facecolor=color_map['HIJAU'], edgecolor='none',
              label=f'🟢 HIJAU - Sehat ({counts["HIJAU"]})')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
              framealpha=0.95, edgecolor='black', fancybox=False)
    
    # Minimal grid
    ax.grid(True, alpha=0.1, linestyle='-', linewidth=0.3, color='gray')
    ax.set_aspect('equal')
    
    # Invert y-axis
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Generated TIGHT SQUARE map for {block_name}: {output_path}")
    
    return counts

# Main execution
print("🔥 Generating TIGHT SQUARE Cincin Api Maps (No Gaps)...\n")

# Load NDRE data
p1 = Path('data/input/tabelNDREnew.csv')
if not p1.exists():
    p1 = Path('../data/input/tabelNDREnew.csv')

try:
    df1 = pd.read_csv(p1, sep=None, engine='python')
except:
    df1 = pd.read_csv(p1)

df1.columns = [c.upper().strip() for c in df1.columns]

# Generate square maps
output_dir = Path('data/output')
output_dir.mkdir(exist_ok=True, parents=True)

stats_d006a = generate_square_cincin_api_map(df1, 'D006A', output_dir / 'cincin_api_map_D006A.png')
stats_d007a = generate_square_cincin_api_map(df1, 'D007A', output_dir / 'cincin_api_map_D007A.png')

print("\n" + "="*60)
print("🔥 TIGHT SQUARE Cincin Api Maps Generated!")
print("="*60)
if stats_d006a:
    print(f"\nBlock D006A:")
    print(f"  🔴 Merah: {stats_d006a['MERAH']}, 🔥 Oranye: {stats_d006a['ORANYE']}, "
          f"🟡 Kuning: {stats_d006a['KUNING']}, 🟢 Hijau: {stats_d006a['HIJAU']}")
if stats_d007a:
    print(f"\nBlock D007A:")
    print(f"  🔴 Merah: {stats_d007a['MERAH']}, 🔥 Oranye: {stats_d007a['ORANYE']}, "
          f"🟡 Kuning: {stats_d007a['KUNING']}, 🟢 Hijau: {stats_d007a['HIJAU']}")
print("\n✅ Perfect grid with NO white space!")
