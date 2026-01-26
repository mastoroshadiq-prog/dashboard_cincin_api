"""
Generate cluster maps dengan VISUAL STYLE reference F08
- Overlapping circles (no white space)
- Tapi tetap pakai V8 statistics yang benar
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

print("="*70)
print("🔥 GENERATING OVERLAPPING CIRCLE MAPS - VISUAL STYLE ONLY")
print("="*70)

# Load data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = [c.upper().strip() for c in df.columns]

def generate_overlapping_visual(df_ndre, block_name, output_path):
    """Generate dengan OVERLAP style, V8 stats"""
    
    # Filter
    if 'BLOK_B' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK_B']
    elif 'BLOK' in df_ndre.columns:
        df_ndre['Blok'] = df_ndre['BLOK']
    
    df_ndre['Blok'] = df_ndre['Blok'].astype(str).str.strip().str.upper()
    df_block = df_ndre[df_ndre['Blok'] == block_name].copy()
    
    if len(df_block) == 0:
        print(f"❌ No data for {block_name}")
        return None
    
    # Process NDRE
    if 'NDRE125' in df_block.columns:
        df_block['NDRE125'] = pd.to_numeric(
            df_block['NDRE125'].astype(str).str.replace(',', '.'), errors='coerce'
        )
        df_block = df_block.dropna(subset=['NDRE125'])
    
    # Process coordinates
    for col in ['N_POKOK', 'N_BARIS']:
        if col in df_block.columns:
            df_block[col] = pd.to_numeric(df_block[col], errors='coerce')
    
    df_block = df_block.dropna(subset=['N_POKOK', 'N_BARIS'])
    
    print(f"\n📊 {block_name}: {len(df_block)} trees")
    
    # V8 Algorithm - Standard Preset
    mean_v = df_block['NDRE125'].mean()
    std_v = df_block['NDRE125'].std()
    df_block['z'] = (df_block['NDRE125'] - mean_v) / std_v if std_v > 0 else 0
    
    tree_map = {}
    for _, row in df_block.iterrows():
        x, y = int(row['N_POKOK']), int(row['N_BARIS'])
        tree_map[f"{x},{y}"] = {'x': x, 'y': y, 'z': row['z'], 'status': 'HIJAU'}
    
    z_core = -1.5
    z_neigh = -1.0
    min_n = 3
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    keys = list(tree_map.keys())
    
    # MERAH cores
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
    
    # ORANYE BFS
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
    
    # KUNING
    for k in keys:
        if tree_map[k]['status'] == 'HIJAU' and tree_map[k]['z'] < z_neigh:
            tree_map[k]['status'] = 'KUNING'
    
    # Stats
    counts = {s: sum(1 for k in keys if tree_map[k]['status'] == s) 
              for s in ['MERAH', 'ORANYE', 'KUNING', 'HIJAU']}
    
    print(f"  🔴 {counts['MERAH']} | 🔥 {counts['ORANYE']} | 🟡 {counts['KUNING']} | 🟢 {counts['HIJAU']}")
    
    # VISUAL SETUP - Focus on OVERLAP
    baris_range = df_block['N_BARIS'].max() - df_block['N_BARIS'].min() + 1
    pokok_range = df_block['N_POKOK'].max() - df_block['N_POKOK'].min() + 1
    fig_width = max(10, pokok_range * 0.15)
    fig_height = max(17, baris_range * 0.15)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='white')
    
    # Colors - matching reference
    colors = {
        'MERAH': '#DC143C',
        'ORANYE': '#FF8C00',
        'KUNING': '#FFD700',
        'HIJAU': '#2E8B57'
    }
    
    # Edge colors (darker)
    edge_colors = {
        'MERAH': '#8B0000',
        'ORANYE': '#CC6600',
        'KUNING': '#DAA520',
        'HIJAU': '#228B22'
    }
    
    # Separate by status
    merah_trees = [tree_map[k] for k in keys if tree_map[k]['status'] == 'MERAH']
    oranye_trees = [tree_map[k] for k in keys if tree_map[k]['status'] == 'ORANYE']
    kuning_trees = [tree_map[k] for k in keys if tree_map[k]['status'] == 'KUNING']
    hijau_trees = [tree_map[k] for k in keys if tree_map[k]['status'] == 'HIJAU']
    
    # CRITICAL: LARGE circles for OVERLAP (bigger than 300 untuk no white space!)
    # Ini yang bikin circles saling overlap banyak
    circle_size = 400  # BIGGER = more overlap, less white space!
    
    # Plot hijau first (background) - SALING OVERLAP!
    if hijau_trees:
        hijau_x = [t['x'] for t in hijau_trees]
        hijau_y = [t['y'] for t in hijau_trees]
        ax.scatter(hijau_x, hijau_y, 
                  c=colors['HIJAU'], s=circle_size, 
                  alpha=0.7,  # Semi-transparent untuk lihat overlap
                  edgecolors=edge_colors['HIJAU'],
                  linewidths=1.5,
                  zorder=1)
    
    # Kuning
    if kuning_trees:
        kuning_x = [t['x'] for t in kuning_trees]
        kuning_y = [t['y'] for t in kuning_trees]
        ax.scatter(kuning_x, kuning_y,
                  c=colors['KUNING'], s=circle_size,
                  alpha=0.75,
                  edgecolors=edge_colors['KUNING'],
                  linewidths=1.5,
                  zorder=2)
    
    # Oranye (cincin api) - clearly visible
    if oranye_trees:
        oranye_x = [t['x'] for t in oranye_trees]
        oranye_y = [t['y'] for t in oranye_trees]
        ax.scatter(oranye_x, oranye_y,
                  c=colors['ORANYE'], s=circle_size,
                  alpha=0.8,
                  edgecolors=edge_colors['ORANYE'],
                  linewidths=2,
                  zorder=3)
    
    # Merah (inti) - on top
    if merah_trees:
        merah_x = [t['x'] for t in merah_trees]
        merah_y = [t['y'] for t in merah_trees]
        ax.scatter(merah_x, merah_y,
                  c=colors['MERAH'], s=circle_size,
                  alpha=0.85,
                  edgecolors=edge_colors['MERAH'],
                  linewidths=2,
                  zorder=4)
    
    # Axis setup
    x_coords = [tree_map[k]['x'] for k in keys]
    y_coords = [tree_map[k]['y'] for k in keys]
    ax.set_xlim(min(x_coords) - 0.5, max(x_coords) + 0.5)
    ax.set_ylim(min(y_coords) - 0.5, max(y_coords) + 0.5)
    
    # Labels
    ax.set_xlabel('Nomor Pokok', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nomor Baris', fontsize=12, fontweight='bold')
    
    # Title
    title = f'Peta Kluster Ganoderma - Blok {block_name}\\n'
    title += f'🔴 Merah: {counts["MERAH"]} | 🔥 Oranye: {counts["ORANYE"]} | '
    title += f'🟡 Kuning: {counts["KUNING"]} | 🟢 Hijau: {counts["HIJAU"]}'
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    
    # Legend
    status_labels = {
        'MERAH': '🔴 Infeksi Inti',
        'ORANYE': '🔥 Cincin Api',
        'KUNING': '🟡 Suspect',
        'HIJAU': '🟢 Sehat'
    }
    legend_elements = [
        mpatches.Patch(facecolor=colors[s], label=f'{status_labels[s]} ({counts[s]})')
        for s in ['MERAH', 'ORANYE', 'KUNING', 'HIJAU']
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, 
             framealpha=0.95, edgecolor='black')
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='gray')
    ax.set_aspect('equal')
    ax.invert_yaxis()
    
    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ Saved: {output_path}")
    return counts

# Generate
output_dir = Path('data/output')
stats_f = generate_overlapping_visual(df, 'F008A', output_dir / 'cincin_api_map_F008A.png')
stats_d = generate_overlapping_visual(df, 'D001A', output_dir / 'cincin_api_map_D001A.png')

print("\n" + "="*70)
print("✅ OVERLAPPING CIRCLES - NO WHITE SPACE!")
print("="*70)
print("\nVisual Features:")
print("  ✅ LARGE circles (size=400) untuk OVERLAP banyak")
print("  ✅ NO white space - circles saling tumpang tindih")
print("  ✅ Semi-transparent (alpha 0.7-0.85)")
print("  ✅ Bordered circles (dark edges)")
print("  ✅ Layered rendering")
print("\nData:")
print("  ✅ V8 Algorithm (statistik yang BENAR)")
print("  ✅ z_core=-1.5, z_neigh=-1.0, min=3")
print("\n🎯 VISUAL style reference, DATA accuracy V8!")
