import pandas as pd
import numpy as np
from pathlib import Path

print('='*80)
print('🔍 RANKING BLOK TERPARAH - DIVISI AME002')
print('='*80)

# Load NDRE data
print('\n📂 Loading tabelNDREnew.csv...')
df_ndre = pd.read_csv('data/input/tabelNDREnew.csv')
df_ndre.columns = df_ndre.columns.str.strip()

print(f'✅ Loaded {len(df_ndre)} tree records')

# Implement Cincin Api algorithm (same as generate_square_cincin_api_maps.py)
def classify_cincin_api(df_block):
    """Classify trees into MERAH (core), ORANYE (ring), KUNING (suspect), HIJAU (healthy)"""
    
    # Map stress levels to numeric scores
    stress_map = {
        'Stres Sangat Berat': 5,
        'Stres Berat': 4,
        'Stres Sedang': 3,
        'Stres Ringan': 2,
        '-': 1
    }
    
    df_block['stress_score'] = df_block['klassndre12025'].map(stress_map).fillna(1)
    
    # MERAH: Stres Sangat Berat (score 5)
    merah_mask = df_block['stress_score'] == 5
    df_block['cincin_status'] = 'HIJAU'  # Default
    df_block.loc[merah_mask, 'cincin_status'] = 'MERAH'
    
    # Find neighbors of MERAH trees (ORANYE - Ring of Fire)
    merah_trees = df_block[merah_mask]
    
    if len(merah_trees) > 0:
        # For each tree, check if it's near a MERAH tree
        for idx, tree in df_block.iterrows():
            if tree['cincin_status'] != 'MERAH':
                # Check distance to nearest MERAH tree
                # Using grid position (baris, kolom)
                for _, merah_tree in merah_trees.iterrows():
                    # Simple neighbor check (adjacent cells)
                    row_diff = abs(tree.get('baris', 0) - merah_tree.get('baris', 0))
                    col_diff = abs(tree.get('kolom', 0) - merah_tree.get('kolom', 0))
                    
                    # If adjacent (1-2 cells away) and has stress
                    if (row_diff <= 2 and col_diff <= 2) and tree['stress_score'] >= 4:
                        df_block.at[idx, 'cincin_status'] = 'ORANYE'
                        break
    
    # KUNING: Stres Sedang/Berat but not MERAH or ORANYE
    kuning_mask = (df_block['stress_score'] >= 3) & (df_block['cincin_status'] == 'HIJAU')
    df_block.loc[kuning_mask, 'cincin_status'] = 'KUNING'
    
    return df_block

# Process each block
print('\n📊 Processing blocks...')

blocks = df_ndre['blok'].unique()
print(f'Found {len(blocks)} unique blocks')

block_stats = []

for blok in blocks:
    df_block = df_ndre[df_ndre['blok'] == blok].copy()
    
    # Classify Cincin Api
    df_block = classify_cincin_api(df_block)
    
    # Calculate statistics
    total_trees = len(df_block)
    merah = (df_block['cincin_status'] == 'MERAH').sum()
    oranye = (df_block['cincin_status'] == 'ORANYE').sum()
    kuning = (df_block['cincin_status'] == 'KUNING').sum()
    hijau = (df_block['cincin_status'] == 'HIJAU').sum()
    
    # Calculate spread ratio
    spread_ratio = oranye / merah if merah > 0 else 0
    
    # Calculate infection percentage
    infection_pct = ((merah + oranye) / total_trees * 100) if total_trees > 0 else 0
    
    # Severity score
    severity_score = (
        infection_pct * 0.4 +
        spread_ratio * 30 * 0.3 +
        (merah + oranye) * 0.3
    )
    
    block_stats.append({
        'blok': blok,
        'total_trees': total_trees,
        'merah': merah,
        'oranye': oranye,
        'kuning': kuning,
        'hijau': hijau,
        'spread_ratio': spread_ratio,
        'infection_pct': infection_pct,
        'severity_score': severity_score
    })

# Create DataFrame
df_stats = pd.DataFrame(block_stats)

# Sort by severity score
df_ranked = df_stats.sort_values('severity_score', ascending=False)

# Display Top 10
print('\n' + '='*80)
print('🏆 TOP 10 BLOK TERPARAH (Berdasarkan Cincin Api Analysis)')
print('='*80)

top_10 = df_ranked.head(10)

for idx, (i, row) in enumerate(top_10.iterrows(), 1):
    print(f'\n#{idx}. BLOK {row["blok"]}')
    print(f'   Total Pohon: {int(row["total_trees"])}')
    print(f'   🔴 Infeksi Inti (MERAH): {int(row["merah"])} pohon')
    print(f'   🔥 Cincin Api (ORANYE): {int(row["oranye"])} pohon')
    print(f'   🟡 Suspect (KUNING): {int(row["kuning"])} pohon')
    print(f'   🟢 Sehat (HIJAU): {int(row["hijau"])} pohon')
    print(f'   📊 Spread Ratio: {row["spread_ratio"]:.2f}x')
    print(f'   📈 Infection %: {row["infection_pct"]:.1f}%')
    print(f'   ⚠️  Severity Score: {row["severity_score"]:.2f}')

# Save results
print('\n📁 Saving results...')
df_ranked.to_csv('data/output/all_blocks_ranked_by_severity.csv', index=False)
print('   ✅ Saved to: data/output/all_blocks_ranked_by_severity.csv')

top_10.to_csv('data/output/top_10_worst_blocks_cincin_api.csv', index=False)
print('   ✅ Saved TOP 10 to: data/output/top_10_worst_blocks_cincin_api.csv')

# Get TOP 2
top_2 = df_ranked.head(2)
top_2.to_csv('data/output/top_2_worst_blocks_final.csv', index=False)
print('   ✅ Saved TOP 2 to: data/output/top_2_worst_blocks_final.csv')

print('\n' + '='*80)
print('🎯 TOP 2 BLOK TERPARAH UNTUK ANALISIS DETAIL:')
print('='*80)

for idx, (i, row) in enumerate(top_2.iterrows(), 1):
    print(f'\n#{idx}. BLOK {row["blok"]}')
    print(f'   🔴 Merah: {int(row["merah"])} | 🔥 Oranye: {int(row["oranye"])} | 🟡 Kuning: {int(row["kuning"])}')
    print(f'   Spread Ratio: {row["spread_ratio"]:.2f}x | Infection: {row["infection_pct"]:.1f}%')

print('\n✅ RANKING SELESAI!')
print('\nLangkah selanjutnya: Ekstrak data produksi untuk TOP 2 blok ini')
