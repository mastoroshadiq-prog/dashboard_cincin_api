import pandas as pd
import numpy as np

print('='*80)
print('📊 EKSTRAKSI DATA PRODUKSI UNTUK TOP 2 BLOK TERPARAH')
print('='*80)

# Load TOP 2 blocks
df_top2 = pd.read_csv('data/output/top_2_worst_blocks_final.csv')
print('\nTOP 2 Blok:')
print(df_top2[['blok', 'merah', 'oranye', 'spread_ratio', 'infection_pct']])

blok1 = df_top2.iloc[0]['blok']
blok2 = df_top2.iloc[1]['blok']

print(f'\nBlok #1: {blok1}')
print(f'Blok #2: {blok2}')

# Load data_gabungan.xlsx
print('\n📂 Loading data_gabungan.xlsx...')
df_prod = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

# Find these blocks in production data
# Blocks are stored as "D 01", "D 02" in BLOK column
blok1_formatted = f'D {blok1[1:]}'  # D01 -> D 01
blok2_formatted = f'D {blok2[1:]}'  # D02 -> D 02

print(f'\nSearching for: {blok1_formatted} and {blok2_formatted}')

# Find rows
row_blok1 = df_prod[df_prod['BLOK'] == blok1_formatted]
row_blok2 = df_prod[df_prod['BLOK'] == blok2_formatted]

if len(row_blok1) > 0:
    print(f'\n✅ Found {blok1_formatted}:')
    blok1_data = row_blok1.iloc[0]
    print(f'   Unnamed: 0: {blok1_data["Unnamed: 0"]}')
    print(f'   TT: {blok1_data["TT"]}')
    print(f'   Luas (Ha): {blok1_data["HA STATEMENT"]}')
else:
    print(f'\n❌ {blok1_formatted} NOT FOUND in production data')

if len(row_blok2) > 0:
    print(f'\n✅ Found {blok2_formatted}:')
    blok2_data = row_blok2.iloc[0]
    print(f'   Unnamed: 0: {blok2_data["Unnamed: 0"]}')
    print(f'   TT: {blok2_data["TT"]}')
    print(f'   Luas (Ha): {blok2_data["HA STATEMENT"]}')
else:
    print(f'\n❌ {blok2_formatted} NOT FOUND in production data')

# Now we need to find production columns
# Let's check what columns might contain 2025 production data
print('\n🔍 Searching for production data columns...')

# Sample some numeric columns
print('\nSample numeric data for Blok 1:')
for col in df_prod.columns[:30]:
    if len(row_blok1) > 0:
        val = blok1_data[col]
        if pd.notna(val) and isinstance(val, (int, float)) and 0 < val < 100:
            print(f'   {col}: {val}')

# Create summary
print('\n' + '='*80)
print('📝 SUMMARY FOR REPORT GENERATION')
print('='*80)

summary_data = {
    'Blok #1': {
        'code': blok1,
        'blok_name': blok1_formatted if len(row_blok1) > 0 else 'NOT FOUND',
        'tt': blok1_data['TT'] if len(row_blok1) > 0 else 'N/A',
        'luas': blok1_data['HA STATEMENT'] if len(row_blok1) > 0 else 'N/A',
        'merah': int(df_top2.iloc[0]['merah']),
        'oranye': int(df_top2.iloc[0]['oranye']),
        'kuning': int(df_top2.iloc[0]['kuning']),
        'spread_ratio': df_top2.iloc[0]['spread_ratio'],
        'infection_pct': df_top2.iloc[0]['infection_pct']
    },
    'Blok #2': {
        'code': blok2,
        'blok_name': blok2_formatted if len(row_blok2) > 0 else 'NOT FOUND',
        'tt': blok2_data['TT'] if len(row_blok2) > 0 else 'N/A',
        'luas': blok2_data['HA STATEMENT'] if len(row_blok2) > 0 else 'N/A',
        'merah': int(df_top2.iloc[1]['merah']),
        'oranye': int(df_top2.iloc[1]['oranye']),
        'kuning': int(df_top2.iloc[1]['kuning']),
        'spread_ratio': df_top2.iloc[1]['spread_ratio'],
        'infection_pct': df_top2.iloc[1]['infection_pct']
    }
}

# Save summary
import json
with open('data/output/top_2_blocks_summary.json', 'w') as f:
    json.dump(summary_data, f, indent=2, default=str)

print('\n✅ Summary saved to: data/output/top_2_blocks_summary.json')

print('\n' + '='*80)
print('🎯 NEXT STEP: Generate report in format of 2 blok.md')
print('='*80)

for key, data in summary_data.items():
    print(f'\n{key}: {data["code"]} ({data["blok_name"]})')
    print(f'   TT: {data["tt"]} | Luas: {data["luas"]} Ha')
    print(f'   Merah: {data["merah"]} | Oranye: {data["oranye"]} | Kuning: {data["kuning"]}')
    print(f'   Spread Ratio: {data["spread_ratio"]:.2f}x | Infection: {data["infection_pct"]:.1f}%')
