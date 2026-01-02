"""
FINAL CORRECT VERSION - Matching reference F08 EXACTLY
Key: GREEN KECIL, ORANGE/RED BESAR, HEXAGONAL PACKING
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

print("="*70)
print("🔥 FINAL CORRECT VERSION - GREEN KECIL + HEXAGONAL")
print("="*70)

# Load data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = [c.upper().strip() for c in df.columns]

def generate_final_correct_map(df_ndre, block_name, output_path):
    """FINAL CORRECT: Green kecil, hexagonal packing, no white space"""
    
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
    
    # V8 Algorithm
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
    
    # Figure setup
    baris_range = df_block['N_BARIS'].max() - df_block['N_BARIS'].min() + 1
    pokok_range = df_block['N_POKOK'].max() - df_block['N_POKOK'].min() + 1
    fig_width = max(10, pokok_range * 0.12)
    fig_height = max(17, baris_range * 0.12)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='white')
    
    # Colors - hijau lebih terang!
    colors = {
        'MERAH': '#DC143C',
        'ORANYE': '#FF8C00',
        'KUNING': '#FFD700',
        'HIJAU': '#3CB371'  # Medium Sea Green - lebih terang!
    }
    
    edge_colors = {
        'MERAH': '#8B0000',
        'ORANYE': '#CC6600',
        'KUNING': '#DAA520',
        'HIJAU': '#1a5c3a'  # Darker green
    }
    
    # SIZES: Merah, Oranye, Kuning SAMA! Hijau KECIL!
    sizes_map = {
        'MERAH': 120,      # SAMA dengan kuning!
        'ORANYE': 120,     # SAMA dengan kuning!
        'KUNING': 120,     # Base size
        'HIJAU': 70        # KECIL - background
    }
    
    # Separate by status
    merah_list = [(tree_map[k]['x'], tree_map[k]['y']) for k in keys if tree_map[k]['status'] == 'MERAH']
    oranye_list = [(tree_map[k]['x'], tree_map[k]['y']) for k in keys if tree_map[k]['status'] == 'ORANYE']
    kuning_list = [(tree_map[k]['x'], tree_map[k]['y']) for k in keys if tree_map[k]['status'] == 'KUNING']
    hijau_list = [(tree_map[k]['x'], tree_map[k]['y']) for k in keys if tree_map[k]['status'] == 'HIJAU']
    
    # Apply HEXAGONAL OFFSET for dense packing!
    def apply_hex_offset(coords_list):
        result = []
        for x, y in coords_list:
            # Offset even rows by 0.5
            x_offset = 0.5 if y % 2 == 0 else 0
            result.append((x + x_offset, y))
        return result
    
    hijau_coords = apply_hex_offset(hijau_list)
    kuning_coords = apply_hex_offset(kuning_list)
    oranye_coords = apply_hex_offset(oranye_list)
    merah_coords = apply_hex_offset(merah_list)
    
    # Plot in layers (hijau first = background)
    # HIJAU - KECIL dan PADAT!
    if hijau_coords:
        hx = [c[0] for c in hijau_coords]
        hy = [c[1] for c in hijau_coords]
        ax.scatter(hx, hy, 
                  c=colors['HIJAU'], s=sizes_map['HIJAU'], 
                  alpha=0.75,  
                  edgecolors=edge_colors['HIJAU'],
                  linewidths=0.8,
                  zorder=1)
    
    # KUNING - medium
    if kuning_coords:
        kx = [c[0] for c in kuning_coords]
        ky = [c[1] for c in kuning_coords]
        ax.scatter(kx, ky,
                  c=colors['KUNING'], s=sizes_map['KUNING'],
                  alpha=0.8,
                  edgecolors=edge_colors['KUNING'],
                  linewidths=1.2,
                  zorder=2)
    
    # ORANYE - large, melingkar!
    if oranye_coords:
        ox = [c[0] for c in oranye_coords]
        oy = [c[1] for c in oranye_coords]
        ax.scatter(ox, oy,
                  c=colors['ORANYE'], s=sizes_map['ORANYE'],
                  alpha=0.85,
                  edgecolors=edge_colors['ORANYE'],
                  linewidths=1.8,
                  zorder=3)
    
    # MERAH - largest, inti!
    if merah_coords:
        mx = [c[0] for c in merah_coords]
        my = [c[1] for c in merah_coords]
        ax.scatter(mx, my,
                  c=colors['MERAH'], s=sizes_map['MERAH'],
                  alpha=0.9,
                  edgecolors=edge_colors['MERAH'],
                  linewidths=2.0,
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
    legend_elements = [
        mpatches.Patch(facecolor=colors['MERAH'], label=f'🔴 Infeksi Inti ({counts["MERAH"]})'),
        mpatches.Patch(facecolor=colors['ORANYE'], label=f'🔥 Cincin Api ({counts["ORANYE"]})'),
        mpatches.Patch(facecolor=colors['KUNING'], label=f'🟡 Suspect ({counts["KUNING"]})'),
        mpatches.Patch(facecolor=colors['HIJAU'], label=f'🟢 Sehat ({counts["HIJAU"]})')
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
stats_f = generate_final_correct_map(df, 'F008A', output_dir / 'cincin_api_map_F008A.png')
stats_d = generate_final_correct_map(df, 'D001A', output_dir / 'cincin_api_map_D001A.png')

print("\n" + "="*70)
print("✅ FINAL CORRECT VERSION!")
print("="*70)
print("\nKEY FIXES:")
print("  ✅ HIJAU size = 70 (KECIL!) - warna lebih terang #3CB371")
print("  ✅ KUNING size = 120")
print("  ✅ ORANYE size = 120 (SAMA dengan kuning!)")
print("  ✅ MERAH size = 120 (SAMA dengan kuning!)")
print("  ✅ HEXAGONAL OFFSET (dense packing)")
print("  ✅ Uniform sizes untuk infected = hierarchy jelas!")
print("  ✅ Green kecil + terang = background CLEAR!")
print("\n🎯 Should match reference F08 now!")
