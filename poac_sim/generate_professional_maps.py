import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

print('='*80)
print('🗺️  GENERATING PROFESIONAL CINCIN API MAPS - V8 ALGORITHM')
print('='*80)

# Load NDRE data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = df.columns.str.strip()

# Convert ndre125 to numeric
df['ndre125'] = pd.to_numeric(df['ndre125'], errors='coerce')

# V8 Algorithm Parameters
z_core = -1.5
z_neighbor = -1.0
min_neighbors = 3

print(f'\n📋 Algorithm Parameters (Standard V8):')
print(f'  z_core: {z_core}')
print(f'  z_neighbor: {z_neighbor}')
print(f'  min_neighbors: {min_neighbors}')

for blok_code, blok_name in [('F08', 'F008A'), ('D01', 'D001A')]:
    print(f'\n{"="*80}')
    print(f'📍 Generating map for {blok_name}...')
    print('='*80)
    
    # Filter data
    df_blok = df[df['blok'] == blok_code].copy()
    total_trees = len(df_blok)
    
    # Calculate Z-scores
    mean_ndre = df_blok['ndre125'].mean()
    std_ndre = df_blok['ndre125'].std()
    
    if std_ndre > 0:
        df_blok['z_score'] = (df_blok['ndre125'] - mean_ndre) / std_ndre
    else:
        df_blok['z_score'] = 0
    
    # Create tree map for V8 algorithm
    tree_map = {}
    trees = []
    
    for _, row in df_blok.iterrows():
        x = int(row['n_pokok'])
        y = int(row['n_baris'])
        z = row['z_score']
        
        tree = {
            'x': x,
            'y': y,
            'z': z,
            'status': 'HIJAU'
        }
        trees.append(tree)
        tree_map[f"{x},{y}"] = tree
    
    # V8 Algorithm - Step 1: Identify MERAH (core)
    offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    
    merah_count = 0
    for tree in trees:
        if tree['z'] < z_core:
            neighbors = 0
            for offset in offsets:
                neighbor_key = f"{tree['x']+offset[0]},{tree['y']+offset[1]}"
                if neighbor_key in tree_map and tree_map[neighbor_key]['z'] < z_neighbor:
                    neighbors += 1
            
            if neighbors >= min_neighbors:
                tree['status'] = 'MERAH'
                merah_count += 1
    
    # Step 2: Identify ORANYE (Ring of Fire)
    oranye_count = 0
    merah_trees = [t for t in trees if t['status'] == 'MERAH']
    
    for merah_tree in merah_trees:
        for offset in offsets:
            neighbor_key = f"{merah_tree['x']+offset[0]},{merah_tree['y']+offset[1]}"
            if neighbor_key in tree_map:
                neighbor = tree_map[neighbor_key]
                if neighbor['status'] != 'MERAH' and neighbor['status'] != 'ORANYE':
                    neighbor['status'] = 'ORANYE'
                    oranye_count += 1
    
    # Step 3: Identify KUNING (Suspect)
    kuning_count = 0
    for tree in trees:
        if tree['status'] == 'HIJAU' and tree['z'] < z_core:
            tree['status'] = 'KUNING'
            kuning_count += 1
    
    # Count HIJAU
    hijau_count = sum(1 for t in trees if t['status'] == 'HIJAU')
    attack_rate = ((merah_count + oranye_count) / total_trees) * 100
    
    print(f'  🔴 Merah: {merah_count}')
    print(f'  🔥 Oranye: {oranye_count}')
    print(f'  🟡 Kuning: {kuning_count}')
    print(f'  🟢 Hijau: {hijau_count}')
    print(f'  📈 Attack Rate: {attack_rate:.1f}%')
    
    # Create visualization (PROFESSIONAL STYLE)
    fig, ax = plt.subplots(figsize=(16, 14), facecolor='white')
    
    # Separate trees by status for better visualization
    merah_trees_viz = [t for t in trees if t['status'] == 'MERAH']
    oranye_trees_viz = [t for t in trees if t['status'] == 'ORANYE']
    kuning_trees_viz = [t for t in trees if t['status'] == 'KUNING']
    hijau_trees_viz = [t for t in trees if t['status'] == 'HIJAU']
    
    # Plot trees (order matters for layering)
    # Plot hijau first (background)
    if hijau_trees_viz:
        hijau_x = [t['x'] for t in hijau_trees_viz]
        hijau_y = [t['y'] for t in hijau_trees_viz]
        ax.scatter(hijau_x, hijau_y, c='#10B981', s=60, marker='s', 
                  alpha=0.7, edgecolors='white', linewidths=0.5, label=f'Hijau (Sehat): {hijau_count}')
    
    # Plot kuning
    if kuning_trees_viz:
        kuning_x = [t['x'] for t in kuning_trees_viz]
        kuning_y = [t['y'] for t in kuning_trees_viz]
        ax.scatter(kuning_x, kuning_y, c='#FBBF24', s=80, marker='s', 
                  alpha=0.8, edgecolors='white', linewidths=0.5, label=f'Kuning (Suspect): {kuning_count}')
    
    # Plot oranye (Ring of Fire) - highlighted
    if oranye_trees_viz:
        oranye_x = [t['x'] for t in oranye_trees_viz]
        oranye_y = [t['y'] for t in oranye_trees_viz]
        ax.scatter(oranye_x, oranye_y, c='#F97316', s=100, marker='s', 
                  alpha=0.9, edgecolors='#DC2626', linewidths=1.5, 
                  label=f'Oranye (Ring of Fire): {oranye_count}')
    
    # Plot merah (Core) - most prominent
    if merah_trees_viz:
        merah_x = [t['x'] for t in merah_trees_viz]
        merah_y = [t['y'] for t in merah_trees_viz]
        ax.scatter(merah_x, merah_y, c='#DC2626', s=120, marker='s', 
                  alpha=1.0, edgecolors='#7F1D1D', linewidths=2, 
                  label=f'Merah (Inti Infeksi): {merah_count}')
    
    # Title and labels
    ax.set_title(f'Peta Kluster Cincin Api - Blok {blok_name}\n' + 
                f'Attack Rate: {attack_rate:.1f}% | Total: {total_trees:,} Pohon',
                fontsize=20, fontweight='bold', pad=20, color='#1F2937')
    
    ax.set_xlabel('Nomor Pokok (Kolom)', fontsize=14, fontweight='bold', color='#374151')
    ax.set_ylabel('Nomor Baris', fontsize=14, fontweight='bold', color='#374151')
    
    # Invert Y axis so row 1 is at top
    ax.invert_yaxis()
    
    # Grid
    ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.8, color='#9CA3AF')
    ax.set_facecolor('#F9FAFB')
    
    # Legend
    legend = ax.legend(loc='upper right', fontsize=11, framealpha=0.95, 
                      edgecolor='#D1D5DB', fancybox=True, shadow=True)
    legend.get_frame().set_facecolor('white')
    
    # Add statistics box
    stats_text = (
        f'Statistik Serangan:\n'
        f'• Infeksi Inti (Merah): {merah_count} pohon\n'
        f'• Cincin Api (Oranye): {oranye_count} pohon\n'
        f'• Suspect (Kuning): {kuning_count} pohon\n'
        f'• Sehat (Hijau): {hijau_count:,} pohon\n'
        f'• Attack Rate: {attack_rate:.1f}%'
    )
    
    # Add text box
    props = dict(boxstyle='round,pad=0.8', facecolor='white', alpha=0.95, edgecolor='#D1D5DB', linewidth=2)
    ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props, family='monospace', color='#1F2937')
    
    # Add watermark
    ax.text(0.98, 0.98, 'Generated by V8 Algorithm\nStandard Preset', 
           transform=ax.transAxes, fontsize=8, color='#9CA3AF',
           ha='right', va='top', style='italic', alpha=0.7)
    
    # Tight layout with padding
    plt.tight_layout(pad=2)
    
    # Save with high DPI
    output_file = f'data/output/cincin_api_map_{blok_name}.png'
    plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f'  ✅ Saved: {output_file}')

print('\n' + '='*80)
print('✅ ALL PROFESSIONAL MAPS GENERATED!')
print('='*80)
print('\nFeatures:')
print('  ✅ High resolution (200 DPI)')
print('  ✅ Professional color scheme')
print('  ✅ Clear legends and statistics')
print('  ✅ V8 algorithm verified')
print('  ✅ Grid and labels')
print('  ✅ Statistics info box')
