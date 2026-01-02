import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path
import sys

sys.path.insert(0, '.')

def generate_circle_cincin_api_map(df_ndre, block_name, output_path):
    """Generate circular scatter plot with VERY CLEAR Ring of Fire visualization"""
    
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
    
    # Color mapping - VERY HIGH CONTRAST
    color_map = {
        'MERAH': '#8B0000',    # Dark Red (very dark for maximum contrast)
        'ORANYE': '#FF6600',   # Bright Orange (very bright)
        'KUNING': '#FFD700',   # Gold Yellow
        'HIJAU': '#2ecc71'     # Emerald Green
    }
    
    # Different sizes for different status - CINCIN API MUCH LARGER
    size_map = {
        'HIJAU': 0.42,    # Normal size for healthy
        'KUNING': 0.45,   # Slightly larger for suspect
        'ORANYE': 0.52,   # MUCH LARGER for Ring of Fire
        'MERAH': 0.55     # LARGEST for Core
    }
    
    # THREE-PASS RENDERING for maximum visibility
    # Pass 1: Draw healthy trees (smallest, background)
    for k in keys:
        tree = tree_map[k]
        if tree['status'] == 'HIJAU':
            x, y = tree['x'], tree['y']
            circle = Circle(
                (x, y), 
                radius=size_map['HIJAU'],
                facecolor=color_map['HIJAU'],
                edgecolor=color_map['HIJAU'],
                linewidth=0.3,
                alpha=0.8,
                zorder=1
            )
            ax.add_patch(circle)
    
    # Pass 2: Draw suspect trees
    for k in keys:
        tree = tree_map[k]
        if tree['status'] == 'KUNING':
            x, y = tree['x'], tree['y']
            circle = Circle(
                (x, y), 
                radius=size_map['KUNING'],
                facecolor=color_map['KUNING'],
                edgecolor=color_map['KUNING'],
                linewidth=0.3,
                zorder=2
            )
            ax.add_patch(circle)
    
    # Pass 3: Draw CINCIN API (Orange) with GLOW EFFECT
    for k in keys:
        tree = tree_map[k]
        if tree['status'] == 'ORANYE':
            x, y = tree['x'], tree['y']
            
            # Outer glow (halo effect)
            glow = Circle(
                (x, y), 
                radius=size_map['ORANYE'] + 0.08,
                facecolor=color_map['ORANYE'],
                edgecolor='none',
                linewidth=0,
                alpha=0.3,
                zorder=3
            )
            ax.add_patch(glow)
            
            # Main circle
            circle = Circle(
                (x, y), 
                radius=size_map['ORANYE'],
                facecolor=color_map['ORANYE'],
                edgecolor='#FF4500',  # Darker orange edge
                linewidth=1.5,
                zorder=4
            )
            ax.add_patch(circle)
    
    # Pass 4: Draw CORE (Red) - MOST PROMINENT
    for k in keys:
        tree = tree_map[k]
        if tree['status'] == 'MERAH':
            x, y = tree['x'], tree['y']
            
            # Outer glow
            glow = Circle(
                (x, y), 
                radius=size_map['MERAH'] + 0.1,
                facecolor=color_map['MERAH'],
                edgecolor='none',
                linewidth=0,
                alpha=0.4,
                zorder=5
            )
            ax.add_patch(glow)
            
            # Main circle
            circle = Circle(
                (x, y), 
                radius=size_map['MERAH'],
                facecolor=color_map['MERAH'],
                edgecolor='#4B0000',  # Even darker red edge
                linewidth=2.0,
                zorder=6
            )
            ax.add_patch(circle)
    
    # Set axis properties
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    ax.set_xlim(min(x_coords) - 1.5, max(x_coords) + 1.5)
    ax.set_ylim(min(y_coords) - 1.5, max(y_coords) + 1.5)
    
    # Labels
    ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=11, fontweight='bold')
    
    # Title with statistics - HIGHLIGHT CINCIN API
    title = f'🔥 BLOK {block_name} - PETA KLUSTER GANODERMA (CINCIN API)\n'
    title += f'Total: {total} | 🔴 MERAH: {counts["MERAH"]} | 🔥 ORANYE: {counts["ORANYE"]} | 🟡 KUNING: {counts["KUNING"]}'
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    
    # Legend with emphasis
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_map['MERAH'], edgecolor='#4B0000', linewidth=2,
              label=f'🔴 MERAH - Kluster Aktif ({counts["MERAH"]})'),
        Patch(facecolor=color_map['ORANYE'], edgecolor='#FF4500', linewidth=1.5,
              label=f'🔥 ORANYE - CINCIN API ({counts["ORANYE"]})'),
        Patch(facecolor=color_map['KUNING'], edgecolor=color_map['KUNING'],
              label=f'🟡 KUNING - Suspect ({counts["KUNING"]})'),
        Patch(facecolor=color_map['HIJAU'], edgecolor=color_map['HIJAU'],
              label=f'🟢 HIJAU - Sehat ({counts["HIJAU"]})')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
              framealpha=0.95, edgecolor='black', fancybox=False)
    
    # Grid
    ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5, color='gray')
    ax.set_aspect('equal')
    
    # Invert y-axis
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Generated ENHANCED circular map for {block_name}: {output_path}")
    
    return counts

# Main execution
print("🔥 Generating ENHANCED Circular Cincin Api Maps (Maximum Visibility)...\n")

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

stats_d006a = generate_circle_cincin_api_map(df1, 'D006A', output_dir / 'cincin_api_map_D006A.png')
stats_d007a = generate_circle_cincin_api_map(df1, 'D007A', output_dir / 'cincin_api_map_D007A.png')

print("\n" + "="*60)
print("🔥 ENHANCED Cincin Api Maps Generated!")
print("="*60)
if stats_d006a:
    print(f"\nBlock D006A:")
    print(f"  🔴 Merah: {stats_d006a['MERAH']}, 🔥 Oranye: {stats_d006a['ORANYE']}, "
          f"🟡 Kuning: {stats_d006a['KUNING']}, 🟢 Hijau: {stats_d006a['HIJAU']}")
if stats_d007a:
    print(f"\nBlock D007A:")
    print(f"  🔴 Merah: {stats_d007a['MERAH']}, 🔥 Oranye: {stats_d007a['ORANYE']}, "
          f"🟡 Kuning: {stats_d007a['KUNING']}, 🟢 Hijau: {stats_d007a['HIJAU']}")
print("\n✅ Cincin Api now HIGHLY VISIBLE without zoom!")
