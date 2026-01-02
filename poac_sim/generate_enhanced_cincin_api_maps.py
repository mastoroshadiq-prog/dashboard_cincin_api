import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle, Circle
from pathlib import Path
import sys

sys.path.insert(0, '.')

def generate_enhanced_cincin_api_map(df_ndre, block_name, output_path):
    """Generate enhanced grid-based heatmap with clear Ring of Fire visualization"""
    
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
    ring_of_fire = set()
    
    while queue:
        k = queue.pop(0)
        x, y = tree_map[k]['x'], tree_map[k]['y']
        for o in offsets:
            nk = f"{x+o[0]},{y+o[1]}"
            if nk in tree_map and nk not in visited:
                if tree_map[nk]['z'] < z_neigh:
                    if tree_map[nk]['status'] != 'MERAH':
                        tree_map[nk]['status'] = 'ORANYE'
                        ring_of_fire.add(nk)
                    visited.add(nk)
                    queue.append(nk)
    
    # Identify Suspects (YELLOW)
    for k in keys:
        if tree_map[k]['status'] == 'HIJAU' and tree_map[k]['z'] < z_neigh:
            tree_map[k]['status'] = 'KUNING'
    
    # Build grid matrix
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    grid_width = x_max - x_min + 1
    grid_height = y_max - y_min + 1
    
    # Status to numeric mapping
    status_map = {
        'MERAH': 3,     # Red - Core infection
        'ORANYE': 2,    # Orange - Ring of Fire
        'KUNING': 1,    # Yellow - Suspect
        'HIJAU': 0      # Green - Healthy
    }
    
    # Initialize grid with NaN
    grid = np.full((grid_height, grid_width), np.nan)
    
    # Fill grid
    for k in keys:
        tree = tree_map[k]
        grid_x = tree['x'] - x_min
        grid_y = tree['y'] - y_min
        grid[grid_y, grid_x] = status_map[tree['status']]
    
    # Create visualization with enhanced Ring of Fire
    fig, ax = plt.subplots(figsize=(20, 12), facecolor='white')
    
    # Enhanced color map with more vibrant Ring of Fire
    colors = ['#2ecc71', '#f1c40f', '#ff6b35', '#c0392b']  # Green, Yellow, Vibrant Orange, Dark Red
    cmap = ListedColormap(colors)
    
    # Plot grid as heatmap
    im = ax.imshow(grid, cmap=cmap, interpolation='nearest', aspect='auto', 
                   vmin=0, vmax=3, origin='lower')
    
    # Add prominent grid lines
    ax.set_xticks(np.arange(-0.5, grid_width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid_height, 1), minor=True)
    ax.grid(which='minor', color='#34495e', linestyle='-', linewidth=0.5, alpha=0.4)
    
    # Highlight Ring of Fire cells with border
    for k in ring_of_fire:
        tree = tree_map[k]
        grid_x = tree['x'] - x_min
        grid_y = tree['y'] - y_min
        rect = Rectangle((grid_x - 0.5, grid_y - 0.5), 1, 1,
                        linewidth=2, edgecolor='#e67e22', facecolor='none')
        ax.add_patch(rect)
    
    # Labels
    ax.set_xlabel(f'Kolom Pohon (N_POKOK) [{x_min} - {x_max}]', 
                  fontsize=16, fontweight='bold', color='#2c3e50')
    ax.set_ylabel(f'Baris Pohon (N_BARIS) [{y_min} - {y_max}]', 
                  fontsize=16, fontweight='bold', color='#2c3e50')
    ax.set_title(f'🔥 CINCIN API CLUSTER MAP - BLOCK {block_name}\n'
                 f'Ring of Fire Detection & Spatial Analysis', 
                 fontsize=22, fontweight='bold', pad=25, color='#c0392b')
    
    # Count statistics
    counts = {
        'MERAH': sum(1 for k in keys if tree_map[k]['status'] == 'MERAH'),
        'ORANYE': sum(1 for k in keys if tree_map[k]['status'] == 'ORANYE'),
        'KUNING': sum(1 for k in keys if tree_map[k]['status'] == 'KUNING'),
        'HIJAU': sum(1 for k in keys if tree_map[k]['status'] == 'HIJAU')
    }
    
    total = len(keys)
    
    # Enhanced stats box
    stats_text = f"BLOCK {block_name}\n"
    stats_text += f"{'='*30}\n"
    stats_text += f"Total Pohon: {total:,}\n"
    stats_text += f"Grid: {grid_width} x {grid_height}\n\n"
    stats_text += f"STATUS KESEHATAN:\n"
    stats_text += f"{'─'*30}\n"
    stats_text += f"🔴 MERAH (Core):\n"
    stats_text += f"   {counts['MERAH']:,} pohon ({counts['MERAH']/total*100:.1f}%)\n\n"
    stats_text += f"🟠 ORANYE (Ring of Fire):\n"
    stats_text += f"   {counts['ORANYE']:,} pohon ({counts['ORANYE']/total*100:.1f}%)\n"
    stats_text += f"   ⚠️ ZONA PENYEBARAN AKTIF\n\n"
    stats_text += f"🟡 KUNING (Suspect):\n"
    stats_text += f"   {counts['KUNING']:,} pohon ({counts['KUNING']/total*100:.1f}%)\n\n"
    stats_text += f"🟢 HIJAU (Sehat):\n"
    stats_text += f"   {counts['HIJAU']:,} pohon ({counts['HIJAU']/total*100:.1f}%)\n\n"
    stats_text += f"Spread Ratio:\n"
    if counts['MERAH'] > 0:
        ratio = counts['ORANYE'] / counts['MERAH']
        stats_text += f"   {ratio:.2f}x (Ring/Core)"
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=12, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1.0', facecolor='#ecf0f1', 
                     edgecolor='#34495e', linewidth=3, alpha=0.95))
    
    # Enhanced legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#c0392b', edgecolor='black', linewidth=2, 
              label='🔴 MERAH - Core Infection (Pusat Infeksi)'),
        Patch(facecolor='#ff6b35', edgecolor='#e67e22', linewidth=3, 
              label='🔥 ORANYE - RING OF FIRE (Zona Penyebaran Aktif)'),
        Patch(facecolor='#f1c40f', edgecolor='black', linewidth=2, 
              label='🟡 KUNING - Suspect/At-Risk'),
        Patch(facecolor='#2ecc71', edgecolor='black', linewidth=2, 
              label='🟢 HIJAU - Healthy')
    ]
    
    ax.legend(handles=legend_elements, loc='lower right', fontsize=13, 
              framealpha=0.95, edgecolor='#34495e', fancybox=True, 
              shadow=True, title='LEGEND', title_fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Generated enhanced map for {block_name}: {output_path}")
    
    return counts

# Main execution
print("🔥 Generating Enhanced Cincin Api Maps with Clear Ring of Fire...\n")

# Load NDRE data
p1 = Path('data/input/tabelNDREnew.csv')
if not p1.exists():
    p1 = Path('../data/input/tabelNDREnew.csv')

try:
    df1 = pd.read_csv(p1, sep=None, engine='python')
except:
    df1 = pd.read_csv(p1)

df1.columns = [c.upper().strip() for c in df1.columns]

# Generate enhanced maps
output_dir = Path('data/output')
output_dir.mkdir(exist_ok=True, parents=True)

stats_d006a = generate_enhanced_cincin_api_map(df1, 'D006A', output_dir / 'cincin_api_map_D006A.png')
stats_d007a = generate_enhanced_cincin_api_map(df1, 'D007A', output_dir / 'cincin_api_map_D007A.png')

print("\n" + "="*60)
print("🔥 Enhanced Ring of Fire Maps Generated!")
print("="*60)
if stats_d006a:
    print(f"\nBlock D006A:")
    print(f"  🔴 Red: {stats_d006a['MERAH']}, 🔥 Orange: {stats_d006a['ORANYE']}, "
          f"🟡 Yellow: {stats_d006a['KUNING']}, 🟢 Green: {stats_d006a['HIJAU']}")
if stats_d007a:
    print(f"\nBlock D007A:")
    print(f"  🔴 Red: {stats_d007a['MERAH']}, 🔥 Orange: {stats_d007a['ORANYE']}, "
          f"🟡 Yellow: {stats_d007a['KUNING']}, 🟢 Green: {stats_d007a['HIJAU']}")
print("\n✅ Maps saved with enhanced Ring of Fire visualization")
