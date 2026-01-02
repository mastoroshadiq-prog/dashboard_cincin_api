import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

print('='*80)
print('🗺️  GENERATING CINCIN API MAPS - F008A & D001A')
print('='*80)

# Load NDRE data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = df.columns.str.strip()

# Generate maps for both blocks
for blok_code, blok_name in [('F08', 'F008A'), ('D01', 'D001A')]:
    print(f'\n📍 Generating map for {blok_name}...')
    
    # Filter data for this block
    df_blok = df[df['blok'] == blok_code].copy()
    
    print(f'   Total trees: {len(df_blok)}')
    
    # Map stress levels to scores
    stress_map = {
        'Stres Sangat Berat': 5,
        'Stres Berat': 4,
        'Stres Sedang': 3,
        'Stres Ringan': 2,
        '-': 1
    }
    
    df_blok['stress_score'] = df_blok['klassndre12025'].map(stress_map).fillna(1)
    
    # Classify Cincin Api
    df_blok['cincin_status'] = 'HIJAU'  # Default: healthy
    
    # MERAH: Stress Sangat Berat
    df_blok.loc[df_blok['stress_score'] == 5, 'cincin_status'] = 'MERAH'
    
    # Find Ring of Fire (ORANYE): Trees near MERAH with high stress
    merah_trees = df_blok[df_blok['cincin_status'] == 'MERAH']
    
    if len(merah_trees) > 0:
        for idx, tree in df_blok.iterrows():
            if tree['cincin_status'] != 'MERAH' and tree['stress_score'] >= 4:
                # Check distance to nearest MERAH tree
                for _, merah_tree in merah_trees.iterrows():
                    row_diff = abs(tree['n_baris'] - merah_tree['n_baris'])
                    col_diff = abs(tree['n_pokok'] - merah_tree['n_pokok'])
                    
                    # If within 2 cells (adjacent or nearby)
                    if row_diff <= 2 and col_diff <= 2:
                        df_blok.at[idx, 'cincin_status'] = 'ORANYE'
                        break
    
    # KUNING: Moderate stress but not near MERAH
    df_blok.loc[(df_blok['stress_score'] >= 3) & (df_blok['cincin_status'] == 'HIJAU'), 'cincin_status'] = 'KUNING'
    
    # Count statistics
    merah_count = (df_blok['cincin_status'] == 'MERAH').sum()
    oranye_count = (df_blok['cincin_status'] == 'ORANYE').sum()
    kuning_count = (df_blok['cincin_status'] == 'KUNING').sum()
    hijau_count = (df_blok['cincin_status'] == 'HIJAU').sum()
    
    print(f'   🔴 Merah: {merah_count}')
    print(f'   🔥 Oranye: {oranye_count}')
    print(f'   🟡 Kuning: {kuning_count}')
    print(f'   🟢 Hijau: {hijau_count}')
    
    # Color mapping
    color_map = {
        'MERAH': '#DC2626',
        'ORANYE': '#F97316',
        'KUNING': '#FBBF24',
        'HIJAU': '#10B981'
    }
    
    df_blok['color'] = df_blok['cincin_status'].map(color_map)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Plot trees as squares
    ax.scatter(df_blok['n_pokok'], df_blok['n_baris'], 
              c=df_blok['color'], s=80, marker='s', 
              edgecolors='white', linewidths=0.3, alpha=0.9)
    
    # Title and labels
    ax.set_title(f'Peta Kluster Cincin Api - Blok {blok_name}', 
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Nomor Pokok (Kolom)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nomor Baris', fontsize=12, fontweight='bold')
    
    # Invert Y axis so row 1 is at top
    ax.invert_yaxis()
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#DC2626', edgecolor='white', label=f'Merah (Inti): {merah_count} pohon'),
        mpatches.Patch(facecolor='#F97316', edgecolor='white', label=f'Oranye (Cincin Api): {oranye_count} pohon'),
        mpatches.Patch(facecolor='#FBBF24', edgecolor='white', label=f'Kuning (Suspect): {kuning_count} pohon'),
        mpatches.Patch(facecolor='#10B981', edgecolor='white', label=f'Hijau (Sehat): {hijau_count} pohon')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    output_file = f'data/output/cincin_api_map_{blok_name}.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f'   ✅ Saved: {output_file}')

print('\n' + '='*80)
print('✅ ALL MAPS GENERATED SUCCESSFULLY!')
print('='*80)
