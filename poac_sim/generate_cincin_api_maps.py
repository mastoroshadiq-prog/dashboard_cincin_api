import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
from pathlib import Path
import sys

sys.path.insert(0, '.')

def generate_cincin_api_heatmap(df_ndre, block_name, output_path):
    """Generate grid-based heatmap of Cincin Api detection (like dashboard v8 style)"""
    
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
            tree_map[k][' status'] = 'KUNING'
    
    # Build grid matrix
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    # Create matrix (wider for better visibility)
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
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white')
    
    # Color map (matching dashboard v8)
    colors = ['#27ae60', '#ffd700', '#ff9800', '#e74c3c']  # Green, Yellow, Orange, Red
    cmap = ListedColormap(colors)
    
    # Plot grid as heatmap
    im = ax.imshow(grid, cmap=cmap, interpolation='nearest', aspect='auto', 
                   vmin=0, vmax=3, origin='lower')
    
    # Add grid lines for clarity
    ax.set_xticks(np.arange(-0.5, grid_width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid_height, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.3, alpha=0.3)
    
    # Labels
    ax.set_xlabel(f'Kolom Pohon (N_POKOK) [{x_min} - {x_max}]', 
                  fontsize=14, fontweight='bold')
    ax.set_ylabel(f'Baris Pohon (N_BARIS) [{y_min} - {y_max}]', 
                  fontsize=14, fontweight='bold')
    ax.set_title(f'CINCIN API CLUSTER MAP - BLOCK {block_name}\n'
                 f'Grid-Based Spatial Health Status Analysis', 
                 fontsize=18, fontweight='bold', pad=20)
    
    # Count statistics
    counts = {
        'MERAH': sum(1 for k in keys if tree_map[k]['status'] == 'MERAH'),
        'ORANYE': sum(1 for k in keys if tree_map[k]['status'] == 'ORANYE'),
        'KUNING': sum(1 for k in keys if tree_map[k]['status'] == 'KUNING'),
        'HIJAU': sum(1 for k in keys if tree_map[k]['status'] == 'HIJAU')
    }
    
    total = len(keys)
    
    # Stats box (top-left)
    stats_text = f"BLOCK {block_name}\n"
    stats_text += f"─────────────────────\n"
    stats_text += f"Total: {total:,} trees\n"
    stats_text += f"🔴 Merah: {counts['MERAH']:,} ({counts['MERAH']/total*100:.1f}%)\n"
    stats_text += f"🟠 Oranye: {counts['ORANYE']:,} ({counts['ORANYE']/total*100:.1f}%)\n"
    stats_text += f"🟡 Kuning: {counts['KUNING']:,} ({counts['KUNING']/total*100:.1f}%)\n"
    stats_text += f"🟢 Hijau: {counts['HIJAU']:,} ({counts['HIJAU']/total*100:.1f}%)\n"
    stats_text += f"\nGrid: {grid_width} x {grid_height}"
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                     edgecolor='black', linewidth=2, alpha=0.95))
    
    # Legend (bottom-right)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#e74c3c', edgecolor='black', linewidth=1.5, 
              label='🔴 MERAH (Core Infection)'),
        Patch(facecolor='#ff9800', edgecolor='black', linewidth=1.5, 
              label='🟠 ORANYE (Ring of Fire)'),
        Patch(facecolor='#ffd700', edgecolor='black', linewidth=1.5, 
              label='🟡 KUNING (Suspect/At-Risk)'),
        Patch(facecolor='#27ae60', edgecolor='black', linewidth=1.5, 
              label='🟢 HIJAU (Healthy)')
    ]
    
    ax.legend(handles=legend_elements, loc='lower right', fontsize=12, 
              framealpha=0.95, edgecolor='black', fancybox=True, shadow=True)
    
    # Highlight infected clusters with boundary box
    if counts['MERAH'] > 0 or counts['ORANYE'] > 0:
        # Find bounding box of infected area
        infected_coords = []
        for k in keys:
            if tree_map[k]['status'] in ['MERAH', 'ORANYE']:
                infected_coords.append((tree_map[k]['x'] - x_min, tree_map[k]['y'] - y_min))
        
        if infected_coords:
            inf_xs = [c[0] for c in infected_coords]
            inf_ys = [c[1] for c in infected_coords]
            
            # Add padding
            pad = 2
            box_x = max(0, min(inf_xs) - pad)
            box_y = max(0, min(inf_ys) - pad)
            box_w = min(grid_width - box_x - 1, max(inf_xs) - min(inf_xs) + 2*pad + 1)
            box_h = min(grid_height - box_y - 1, max(inf_ys) - min(inf_ys) + 2*pad + 1)
            
            rect = Rectangle((box_x - 0.5, box_y - 0.5), box_w, box_h,
                           linewidth=3, edgecolor='yellow', facecolor='none',
                           linestyle='--', label='Isolation Zone')
            ax.add_patch(rect)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Generated heatmap for {block_name}: {output_path}")
    
    return counts

# Main execution
print("🎨 Generating Cincin Api Grid-Based Heatmaps (Dashboard v8 Style)...\n")

# Load NDRE data
p1 = Path('data/input/tabelNDREnew.csv')
if not p1.exists():
    p1 = Path('../data/input/tabelNDREnew.csv')

try:
    df1 = pd.read_csv(p1, sep=None, engine='python')
except:
    df1 = pd.read_csv(p1)

df1.columns = [c.upper().strip() for c in df1.columns]

# Generate heatmaps for both blocks
output_dir = Path('data/output')
output_dir.mkdir(exist_ok=True, parents=True)

stats_d006a = generate_cincin_api_heatmap(df1, 'D006A', output_dir / 'cincin_api_map_D006A.png')
stats_d007a = generate_cincin_api_heatmap(df1, 'D007A', output_dir / 'cincin_api_map_D007A.png')

print("\n" + "="*60)
print("📊 Heatmap Generation Complete!")
print("="*60)
if stats_d006a:
    print(f"\nBlock D006A:")
    print(f"  🔴 Red: {stats_d006a['MERAH']}, 🟠 Orange: {stats_d006a['ORANYE']}, "
          f"🟡 Yellow: {stats_d006a['KUNING']}, 🟢 Green: {stats_d006a['HIJAU']}")
if stats_d007a:
    print(f"\nBlock D007A:")
    print(f"  🔴 Red: {stats_d007a['MERAH']}, 🟠 Orange: {stats_d007a['ORANYE']}, "
          f"🟡 Yellow: {stats_d007a['KUNING']}, 🟢 Green: {stats_d007a['HIJAU']}")
print("\n✅ Grid-based heatmaps saved to data/output/ directory")
print("   Style: Similar to Dashboard v8 with clear grid blocks")
