import pandas as pd
import numpy as np

print('='*80)
print('🔍 ANALISIS KOMPREHENSIF: MENCARI 2 BLOK TERPARAH DI DIVISI AME002')
print('='*80)

# Step 1: Load data_gabungan.xlsx
print('\n📂 Step 1: Loading data_gabungan.xlsx...')
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

# Step 2: Filter for Divisi AME002
print('📂 Step 2: Filtering Divisi AME002...')
divisi_ame002 = df[df['DIVISI'].astype(str).str.contains('AME002', case=False, na=False)].copy()
print(f'   ✅ Found {len(divisi_ame002)} blocks in AME002')

# Step 3: Load Cincin Api data
print('\n📂 Step 3: Loading Cincin Api data (tabelNDREnew.csv)...')
df_ndre = pd.read_csv('data/input/tabelNDREnew.csv')

# Clean column names
df_ndre.columns = df_ndre.columns.str.strip()

print(f'   ✅ Loaded {len(df_ndre)} tree records')
print(f'   Columns: {df_ndre.columns.tolist()[:10]}')

# Step 4: Calculate Cincin Api statistics per block
print('\n📊 Step 4: Calculating Cincin Api statistics per block...')

# Group by block and calculate infection stats
cincin_api_stats = df_ndre.groupby('blok').agg({
    'ndre_class': lambda x: (x == 'MERAH').sum(),  # Core infection
    'blok': 'count'  # Total trees
}).rename(columns={'ndre_class': 'core_infected', 'blok': 'total_trees'})

# Calculate Ring of Fire (ORANYE)
ring_stats = df_ndre[df_ndre['ndre_class'] == 'ORANYE'].groupby('blok').size()
cincin_api_stats['ring_infected'] = ring_stats

# Calculate Suspect (KUNING)
suspect_stats = df_ndre[df_ndre['ndre_class'] == 'KUNING'].groupby('blok').size()
cincin_api_stats['suspect'] = suspect_stats

# Fill NaN with 0
cincin_api_stats = cincin_api_stats.fillna(0)

# Calculate Spread Ratio
cincin_api_stats['spread_ratio'] = cincin_api_stats['ring_infected'] / cincin_api_stats['core_infected'].replace(0, 1)

# Calculate infection percentage
cincin_api_stats['infection_pct'] = ((cincin_api_stats['core_infected'] + cincin_api_stats['ring_infected']) / cincin_api_stats['total_trees'] * 100)

print(f'   ✅ Calculated stats for {len(cincin_api_stats)} blocks')

# Step 5: Find blocks with production data
print('\n📊 Step 5: Analyzing production data...')

# Look for columns that might contain yield data
# Based on typical Excel structure, production data is usually in later columns
# We need to find Potensi and Realisasi columns

# First, let's identify which blocks from Cincin Api exist in production data
blocks_with_cincin = cincin_api_stats.index.tolist()
print(f'   Blocks with Cincin Api data: {blocks_with_cincin}')

# Match blocks between datasets
# In data_gabungan, blocks are in 'Unnamed: 0' column
divisi_ame002['blok_code'] = divisi_ame002['Unnamed: 0']

# Filter for blocks that have Cincin Api data
blocks_to_analyze = divisi_ame002[divisi_ame002['blok_code'].isin(blocks_with_cincin)].copy()
print(f'   ✅ Found {len(blocks_to_analyze)} blocks with both production and Cincin Api data')

if len(blocks_to_analyze) > 0:
    print('\n   Blocks to analyze:')
    print(blocks_to_analyze[['blok_code', 'BLOK', 'TT', 'HA STATEMENT']].to_string())

# Step 6: Merge Cincin Api stats with production data
print('\n📊 Step 6: Merging datasets...')

# Merge on block code
blocks_to_analyze = blocks_to_analyze.merge(
    cincin_api_stats, 
    left_on='blok_code', 
    right_index=True, 
    how='left'
)

# Step 7: Calculate ranking score
print('\n📊 Step 7: Calculating severity ranking...')

# Ranking criteria:
# 1. High infection percentage (weight: 40%)
# 2. High spread ratio (weight: 30%)
# 3. High number of infected trees (weight: 30%)

blocks_to_analyze['severity_score'] = (
    blocks_to_analyze['infection_pct'] * 0.4 +
    blocks_to_analyze['spread_ratio'] * 30 * 0.3 +  # Normalize spread ratio
    (blocks_to_analyze['core_infected'] + blocks_to_analyze['ring_infected']) * 0.3
)

# Sort by severity score
blocks_ranked = blocks_to_analyze.sort_values('severity_score', ascending=False)

# Step 8: Display Top 10 worst blocks
print('\n' + '='*80)
print('🏆 TOP 10 BLOK TERPARAH (Berdasarkan Infeksi Ganoderma)')
print('='*80)

top_10 = blocks_ranked.head(10)

for idx, (i, row) in enumerate(top_10.iterrows(), 1):
    print(f'\n#{idx}. BLOK {row["blok_code"]} ({row["BLOK"]})')
    print(f'   Luas: {row["HA STATEMENT"]} Ha | TT: {row["TT"]}')
    print(f'   Infeksi Inti (MERAH): {int(row["core_infected"])} pohon')
    print(f'   Cincin Api (ORANYE): {int(row["ring_infected"])} pohon')
    print(f'   Suspect (KUNING): {int(row["suspect"])} pohon')
    print(f'   Spread Ratio: {row["spread_ratio"]:.2f}x')
    print(f'   Infection %: {row["infection_pct"]:.1f}%')
    print(f'   Severity Score: {row["severity_score"]:.2f}')

# Step 9: Save results
print('\n📁 Saving results...')

# Save top 10 to CSV
top_10_export = top_10[[
    'blok_code', 'BLOK', 'TT', 'HA STATEMENT', 
    'total_trees', 'core_infected', 'ring_infected', 'suspect',
    'spread_ratio', 'infection_pct', 'severity_score'
]]

top_10_export.to_csv('data/output/top_10_worst_blocks.csv', index=False)
print('   ✅ Saved to: data/output/top_10_worst_blocks.csv')

# Save top 2 for detailed analysis
top_2 = blocks_ranked.head(2)
top_2_export = top_2[[
    'blok_code', 'BLOK', 'TT', 'HA STATEMENT',
    'total_trees', 'core_infected', 'ring_infected', 'suspect',
    'spread_ratio', 'infection_pct', 'severity_score'
]]

top_2_export.to_csv('data/output/top_2_worst_blocks_for_analysis.csv', index=False)
print('   ✅ Saved TOP 2 to: data/output/top_2_worst_blocks_for_analysis.csv')

print('\n' + '='*80)
print('✅ ANALISIS SELESAI!')
print('='*80)
print('\nLangkah selanjutnya:')
print('1. Review top_10_worst_blocks.csv')
print('2. Ekstrak data produksi untuk TOP 2 blok')
print('3. Generate laporan format 2 blok.md')
