import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('data/input/tabelNDREnew.csv')
df.columns = df.columns.str.strip()

# Generate maps for F08 and D01
for blok_code, blok_name in [('F08', 'F008A'), ('D01', 'D001A')]:
    print(f'\nGenerating map for {blok_name}...')
    
    # Filter data
    df_blok = df[df['blok'] == blok_code].copy()
    
    # Map stress to scores
    stress_map = {
        'Stres Sangat Berat': 5,
        'Stres Berat': 4,
        'Stres Sedang': 3,
        'Stres Ringan': 2,
        '-': 1
    }
    
    df_blok['stress_score'] = df_blok['klassndre12025'].map(stress_map).fillna(1)
    
    # Classify Cincin Api
    df_blok['cincin_status'] = 'HIJAU'
    df_blok.loc[df_blok['stress_score'] == 5, 'cincin_status'] = 'MERAH'
    
    # Find Ring of Fire
    merah_trees = df_blok[df_blok['cincin_status'] == 'MERAH']
    
    for idx, tree in df_blok.iterrows():
        if tree['cincin_status'] != 'MERAH' and tree['stress_score'] >= 4:
            for _, merah_tree in merah_trees.iterrows():
                row_diff = abs(tree.get('baris', 0) - merah_tree.get('baris', 0))
                col_diff = abs(tree.get('kolom', 0) - merah_tree.get('kolom', 0))
                
                if row_diff <= 2 and col_diff <= 2:
                    df_blok.at[idx, 'cincin_status'] = 'ORANYE'
                    break
    
    # Classify Suspect
    df_blok.loc[(df_blok['stress_score'] >= 3) & (df_blok['cincin_status'] == 'HIJAU'), 'cincin_status'] = 'KUNING'
    
    # Color mapping
    color_map = {
        'MERAH': '#DC2626',
        'ORANYE': '#F97316',
        'KUNING': '#FBBF24',
        'HIJAU': '#10B981'
    }
    
    df_blok['color'] = df_blok['cincin_status'].map(color_map)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 12))
    
    ax.scatter(df_blok['kolom'], df_blok['baris'], 
              c=df_blok['color'], s=100, marker='s', 
              edgecolors='white', linewidths=0.5)
    
    ax.set_title(f'Peta Cincin Api - Blok {blok_name}', 
                fontsize=16, fontweight='bold')
    ax.set_xlabel('Kolom')
    ax.set_ylabel('Baris')
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(f'data/output/cincin_api_map_{blok_name}.png', 
               dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f'  ✅ Generated: cincin_api_map_{blok_name}.png')
    
    # Print stats
    merah_count = (df_blok['cincin_status'] == 'MERAH').sum()
    oranye_count = (df_blok['cincin_status'] == 'ORANYE').sum()
    kuning_count = (df_blok['cincin_status'] == 'KUNING').sum()
    hijau_count = (df_blok['cincin_status'] == 'HIJAU').sum()
    
    print(f'  🔴 Merah: {merah_count}')
    print(f'  🔥 Oranye: {oranye_count}')
    print(f'  🟡 Kuning: {kuning_count}')
    print(f'  🟢 Hijau: {hijau_count}')

print('\n✅ All maps generated!')
