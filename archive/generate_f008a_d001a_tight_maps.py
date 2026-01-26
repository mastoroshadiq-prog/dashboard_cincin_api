import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from pathlib import Path

print("="*70)
print("🔥 GENERATING TIGHT SQUARE MAPS FOR F008A & D001A")
print("="*70)

# Load NDRE data
df1 = pd.read_csv('data/input/tabelNDREnew.csv')
df1.columns = [c.upper().strip() for c in df1.columns]

def generate_tight_square_map(df_ndre, block_name, output_path):
    """Generate TIGHT SQUARE visualization matching D007A style"""
    
    # Filter for target block - handle different column names
    if 'BLOK_B' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK_B']
    elif 'BLOK' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK']
    
    df_ndre['Blok'] = df_ndre['Blok'].astype(str).str.strip().str.upper()
    block_data = df_ndre[df_ndre['Blok'] == block_name].copy()
    
    if len(block_data) == 0:
        print(f"❌ No data found for block {block_name}")
        return None
    
    # Ensure NDRE125 is numeric
    if 'NDRE125' in block_data.columns:
        block_data['NDRE125'] = pd.to_numeric(
            block_data['NDRE125'].astype(str).str.replace(',', '.'), 
            errors='coerce'
        )
        block_data = block_data.dropna(subset=['NDRE125'])
    else:
        print(f"❌ NDRE125 column not found")
        return None
    
    # Ensure coordinates are numeric
    for col in ['N_POKOK', 'N_BARIS']:
        if col in block_data.columns:
            block_data[col] = pd.to_numeric(block_data[col], errors='coerce')
    
    block_data = block_data.dropna(subset=['N_POKOK', 'N_BARIS'])
    
    if len(block_data) == 0:
        print(f"❌ No valid data after cleaning for {block_name}")
        return None
    
    print(f"\n📊 Processing {len(block_data)} trees for {block_name}")
    
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
    
    # V8 Cincin Api Algorithm
    z_core = -1.5
    z_neigh = -1.0
    min_n = 3
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    keys = list(tree_map.keys())
    
    # Step 1: Identify Cores (MERAH/RED)
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
    
    # Step 2: Identify Ring of Fire (ORANYE) - BFS from cores
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
    
    # Step 3: Identify Suspects (KUNING/YELLOW)
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
    
    print(f"  🔴 Merah: {counts['MERAH']}")
    print(f"  🔥 Oranye: {counts['ORANYE']}")
    print(f"  🟡 Kuning: {counts['KUNING']}")
    print(f"  🟢 Hijau: {counts['HIJAU']}")
    
    # Create figure - EXACT SAME SIZE AS D007A (8x14)
    fig, ax = plt.subplots(figsize=(8, 14), facecolor='white')
    
    # Color mapping - EXACT SAME AS D007A
    color_map = {
        'MERAH': '#8B0000',    # Dark Red
        'ORANYE': '#FF6600',   # Bright Orange
        'KUNING': '#FFD700',   # Gold Yellow
        'HIJAU': '#2ecc71'     # Emerald Green
    }
    
    # Square size - EXACT SAME AS D007A
    square_size = 0.9
    
    # Draw squares - TIGHT PACKING, NO BORDERS
    for k in keys:
        tree = tree_map[k]
        x = tree['x']
        y = tree['y']
        status = tree['status']
        
        # Rectangle at (x, y) with NO border
        rect = Rectangle(
            (x - 0.5, y - 0.5),     # Bottom-left corner
            square_size,             # Width
            square_size,             # Height
            facecolor=color_map[status],
            edgecolor='none',        # NO BORDER - KEY!
            linewidth=0
        )
        ax.add_patch(rect)
    
    # Set axis limits
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    
    ax.set_xlim(min(x_coords) - 1, max(x_coords) + 1)
    ax.set_ylim(min(y_coords) - 1, max(y_coords) + 1)
    
    # Labels - EXACT SAME AS D007A
    ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=11, fontweight='bold')
    
    # Title - EXACT FORMAT AS D007A
    title = f'🔥 BLOK {block_name} - PETA KLUSTER GANODERMA (CINCIN API)\\n'
    title += f'Total: {total} | 🔴 MERAH: {counts["MERAH"]} | 🔥 ORANYE: {counts["ORANYE"]} | 🟡 KUNING: {counts["KUNING"]}'
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    
    # Legend - EXACT SAME AS D007A
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
    
    # Grid - EXACT SAME AS D007A
    ax.grid(True, alpha=0.1, linestyle='-', linewidth=0.3, color='gray')
    ax.set_aspect('equal')
    
    # Invert y-axis - MATCH D007A
    ax.invert_yaxis()
    
    # Save - HIGH DPI LIKE D007A
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ Saved: {output_path}")
    
    return counts

# Generate maps for F008A and D001A
output_dir = Path('data/output')

stats_f008a = generate_tight_square_map(df1, 'F008A', output_dir / 'cincin_api_map_F008A.png')
stats_d001a = generate_tight_square_map(df1, 'D001A', output_dir / 'cincin_api_map_D001A.png')

print("\n" + "="*70)
print("✅ TIGHT SQUARE MAPS GENERATED - MATCHING D007A STYLE!")
print("="*70)
print("\nFeatures:")
print("  ✅ Tight square grid (0.9 size, no gaps)")
print("  ✅ NO borders on squares")
print("  ✅ Same colors as D007A")
print("  ✅ Same layout (8x14 figsize)")
print("  ✅ Same legend & title format")
print("  ✅ High DPI (300)")
print("\nStyle: PERSIS SAMA dengan D007A! 🎯")
