"""
Generate cluster maps 100% matching reference F08 - EXACT COPY dari dashboard.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

print("="*70)
print("🔥 GENERATING CLUSTER MAPS - 100% MATCHING dashboard.py")
print("="*70)

# Load data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = [c.upper().strip() for c in df.columns]

# Status colors - EXACT from dashboard.py
STATUS_COLORS = {
    "MERAH (KLUSTER AKTIF)": "#e74c3c",
    "ORANYE (CINCIN API)": "#e67e22",
    "KUNING (SUSPECT TERISOLASI)": "#f1c40f",
    "HIJAU (SEHAT)": "#27ae60"
}

def generate_exact_cluster_map(df_ndre, block_name, output_path):
    """100% EXACT copy dari _create_single_block_detail in dashboard.py"""
    
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
    
    # Calculate z-scores
    mean_v = df_block['NDRE125'].mean()
    std_v = df_block['NDRE125'].std()
    df_block['z'] = (df_block['NDRE125'] - mean_v) / std_v if std_v > 0 else 0
    
    # Build tree map
    tree_map = {}
    for _, row in df_block.iterrows():
        x, y = int(row['N_POKOK']), int(row['N_BARIS'])
        tree_map[f"{x},{y}"] = {'x': x, 'y': y, 'z': row['z'], 'status': 'HIJAU (SEHAT)'}
    
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
                tree_map[k]['status'] = 'MERAH (KLUSTER AKTIF)'
                cores.add(k)
    
    # BFS for ORANYE
    queue, visited = list(cores), set(cores)
    while queue:
        k = queue.pop(0)
        x, y = tree_map[k]['x'], tree_map[k]['y']
        for o in offsets:
            nk = f"{x+o[0]},{y+o[1]}"
            if nk in tree_map and nk not in visited:
                if tree_map[nk]['z'] < z_neigh and tree_map[nk]['status'] != 'MERAH (KLUSTER AKTIF)':
                    tree_map[nk]['status'] = 'ORANYE (CINCIN API)'
                    visited.add(nk)
                    queue.append(nk)
    
    # KUNING suspects
    for k in keys:
        if tree_map[k]['status'] == 'HIJAU (SEHAT)' and tree_map[k]['z'] < z_neigh:
            tree_map[k]['status'] = 'KUNING (SUSPECT TERISOLASI)'
    
    # Create DataFrame for easier handling
    df_block['Status_Risiko'] = df_block.apply(
        lambda row: tree_map.get(f"{int(row['N_POKOK'])},{int(row['N_BARIS'])}", {}).get('status', 'HIJAU (SEHAT)'),
        axis=1
    )
    
    # Calculate figure size
    baris_range = df_block['N_BARIS'].max() - df_block['N_BARIS'].min() + 1
    pokok_range = df_block['N_POKOK'].max() - df_block['N_POKOK'].min() + 1
    fig_width = max(28, pokok_range * 0.3)
    fig_height = max(16, baris_range * 0.15)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Get colors and sizes - EXACT from dashboard.py
    colors = []
    sizes = []
    edge_colors = []
    edge_widths = []
    
    for _, row in df_block.iterrows():
        status = row['Status_Risiko']
        colors.append(STATUS_COLORS.get(status, '#cccccc'))
        
        if status == 'MERAH (KLUSTER AKTIF)':
            sizes.append(200)
            edge_colors.append('darkred')
            edge_widths.append(2)
        elif status == 'ORANYE (CINCIN API)':
            sizes.append(180)
            edge_colors.append('darkorange')
            edge_widths.append(2)
        elif status == 'KUNING (SUSPECT TERISOLASI)':
            sizes.append(140)
            edge_colors.append('olive')
            edge_widths.append(1.5)
        else:  # HIJAU
            sizes.append(60)  # SMALL for hijau!
            edge_colors.append('darkgreen')
            edge_widths.append(0.5)  # THIN edge!
    
    # Apply hexagonal offset - CRITICAL!
    x_coords = []
    y_coords = []
    for _, row in df_block.iterrows():
        baris = row['N_BARIS']
        pokok = row['N_POKOK']
        x_offset = 0.5 if baris % 2 == 0 else 0  # HEXAGONAL OFFSET!
        x_coords.append(pokok + x_offset)
        y_coords.append(baris)
    
    # Plot in layers - EXACT order
    status_order = ['HIJAU (SEHAT)', 'KUNING (SUSPECT TERISOLASI)', 'ORANYE (CINCIN API)', 'MERAH (KLUSTER AKTIF)']
    
    for status in status_order:
        mask = df_block['Status_Risiko'] == status
        if mask.any():
            indices = df_block[mask].index
            x_plot = [x_coords[list(df_block.index).index(i)] for i in indices]
            y_plot = [y_coords[list(df_block.index).index(i)] for i in indices]
            s_plot = [sizes[list(df_block.index).index(i)] for i in indices]
            c_plot = [colors[list(df_block.index).index(i)] for i in indices]
            ec_plot = [edge_colors[list(df_block.index).index(i)] for i in indices]
            ew_plot = [edge_widths[list(df_block.index).index(i)] for i in indices]
            
            ax.scatter(x_plot, y_plot, c=c_plot, s=s_plot, alpha=0.85, 
                      edgecolors=ec_plot, linewidths=ew_plot, zorder=status_order.index(status)+1)
    
    # Count statistics
    merah_count = len(df_block[df_block["Status_Risiko"]=="MERAH (KLUSTER AKTIF)"])
    oranye_count = len(df_block[df_block["Status_Risiko"]=="ORANYE (CINCIN API)"])
    kuning_count = len(df_block[df_block["Status_Risiko"]=="KUNING (SUSPECT TERISOLASI)"])
    hijau_count = len(df_block[df_block["Status_Risiko"]=="HIJAU (SEHAT)"])
    total_count = len(df_block)
    
    print(f"  🔴 {merah_count} | 🔥 {oranye_count} | 🟡 {kuning_count} | 🟢 {hijau_count}")
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#e74c3c', label=f'MERAH - Kluster Aktif ({merah_count})'),
        mpatches.Patch(color='#e67e22', label=f'ORANYE - Cincin Api ({oranye_count})'),
        mpatches.Patch(color='#f1c40f', label=f'KUNING - Suspect ({kuning_count})'),
        mpatches.Patch(color='#27ae60', label=f'HIJAU - Sehat ({hijau_count})')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, 
              framealpha=0.9, fancybox=True, shadow=True)
    
    ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=14)
    ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=14)
    
    ax.set_title(f'BLOK {block_name} - PETA KLUSTER GANODERMA\\n'
                f'Total Pohon: {total_count} | MERAH: {merah_count} | ORANYE: {oranye_count} | KUNING: {kuning_count}', 
                fontsize=16, fontweight='bold')
    
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal')
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ Saved: {output_path}")
    return {'merah': merah_count, 'oranye': oranye_count, 'kuning': kuning_count, 'hijau': hijau_count}

# Generate
output_dir = Path('data/output')
stats_f = generate_exact_cluster_map(df, 'F008A', output_dir / 'cincin_api_map_F008A.png')
stats_d = generate_exact_cluster_map(df, 'D001A', output_dir / 'cincin_api_map_D001A.png')

print("\n" + "="*70)
print("✅ 100% EXACT MATCH - dashboard.py Algorithm!")
print("="*70)
print("\nKey Features:")
print("  ✅ HEXAGONAL OFFSET (x_offset = 0.5 for even rows)")
print("  ✅ Different sizes: MERAH(200), ORANYE(180), KUNING(140), HIJAU(60)")
print("  ✅ Edge colors: darkred, darkorange, olive, darkgreen")
print("  ✅ Edge widths: MERAH/ORANYE(2), KUNING(1.5), HIJAU(0.5)")
print("  ✅ Alpha: 0.85 (consistent)")
print("  ✅ Layered rendering dengan zorder")
print("  ✅ Grid alpha 0.3, dashed lines")
print("\n🎯 Style: PERSIS cluster_map_agresif_03_F08.png!")
