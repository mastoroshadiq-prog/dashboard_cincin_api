import pandas as pd
import numpy as np

print('='*80)
print('🔍 ANALISIS FINAL: 2 BLOK TERPARAH - DATA LENGKAP')
print('='*80)

# Step 1: Load Cincin Api ranking
print('\n📂 Step 1: Loading Cincin Api ranking...')
df_ranked = pd.read_csv('data/output/all_blocks_ranked_by_severity.csv')

# Get top 2
top_2_cincin = df_ranked.head(2)
print(f'\nTOP 2 berdasarkan Cincin Api:')
print(top_2_cincin[['blok', 'merah', 'oranye', 'spread_ratio', 'infection_pct', 'severity_score']])

blok1_short = top_2_cincin.iloc[0]['blok']  # e.g., "F08"
blok2_short = top_2_cincin.iloc[1]['blok']  # e.g., "D01"

print(f'\nBlok #1 (short code): {blok1_short}')
print(f'Blok #2 (short code): {blok2_short}')

# Step 2: Load data_gabungan.xlsx
print('\n📂 Step 2: Loading data_gabungan.xlsx...')
df_prod = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

print(f'Total rows: {len(df_prod)}')
print(f'Columns: {len(df_prod.columns)}')

# Step 3: Find matching blocks using BLOK column (short code)
print('\n📊 Step 3: Matching blocks...')

# Convert short codes to BLOK format (e.g., F08 -> F 08)
blok1_formatted = f'{blok1_short[0]} {blok1_short[1:]}'  # F08 -> F 08
blok2_formatted = f'{blok2_short[0]} {blok2_short[1:]}'  # D01 -> D 01

print(f'Searching for: "{blok1_formatted}" and "{blok2_formatted}"')

# Find rows
row_blok1 = df_prod[df_prod['BLOK'] == blok1_formatted]
row_blok2 = df_prod[df_prod['BLOK'] == blok2_formatted]

print(f'\nFound {len(row_blok1)} row(s) for {blok1_formatted}')
print(f'Found {len(row_blok2)} row(s) for {blok2_formatted}')

# Step 4: Extract full data
print('\n' + '='*80)
print('📊 DATA LENGKAP BLOK #1')
print('='*80)

if len(row_blok1) > 0:
    blok1_data = row_blok1.iloc[0]
    
    blok1_code_full = blok1_data['Unnamed: 0']  # Full code like F008A
    blok1_tt = blok1_data['TT']
    blok1_luas = blok1_data['HA STATEMENT']
    
    print(f'\n✅ BLOK #{1}: {blok1_code_full}')
    print(f'   Kode Pendek: {blok1_formatted}')
    print(f'   Tahun Tanam: {blok1_tt}')
    print(f'   Luas (Ha): {blok1_luas}')
    
    # Get Cincin Api data
    blok1_cincin = top_2_cincin.iloc[0]
    print(f'\n   Cincin Api Data:')
    print(f'   - Total Pohon: {int(blok1_cincin["total_trees"])}')
    print(f'   - Merah (Inti): {int(blok1_cincin["merah"])}')
    print(f'   - Oranye (Ring): {int(blok1_cincin["oranye"])}')
    print(f'   - Kuning (Suspect): {int(blok1_cincin["kuning"])}')
    print(f'   - Hijau (Sehat): {int(blok1_cincin["hijau"])}')
    print(f'   - Spread Ratio: {blok1_cincin["spread_ratio"]:.2f}x')
    print(f'   - Infection %: {blok1_cincin["infection_pct"]:.1f}%')
    
    # Look for production data in columns
    print(f'\n   Mencari data produksi...')
    # Check numeric columns in reasonable range
    prod_candidates = []
    for col in df_prod.columns:
        val = blok1_data[col]
        if pd.notna(val) and isinstance(val, (int, float)):
            if 0 < val < 30:  # Reasonable range for Ton/Ha
                prod_candidates.append((col, val))
    
    if prod_candidates:
        print(f'   Kandidat kolom produksi (nilai 0-30):')
        for col, val in prod_candidates[:10]:
            print(f'      {col}: {val}')
else:
    print(f'\n❌ BLOK {blok1_formatted} TIDAK DITEMUKAN')

print('\n' + '='*80)
print('📊 DATA LENGKAP BLOK #2')
print('='*80)

if len(row_blok2) > 0:
    blok2_data = row_blok2.iloc[0]
    
    blok2_code_full = blok2_data['Unnamed: 0']
    blok2_tt = blok2_data['TT']
    blok2_luas = blok2_data['HA STATEMENT']
    
    print(f'\n✅ BLOK #{2}: {blok2_code_full}')
    print(f'   Kode Pendek: {blok2_formatted}')
    print(f'   Tahun Tanam: {blok2_tt}')
    print(f'   Luas (Ha): {blok2_luas}')
    
    # Get Cincin Api data
    blok2_cincin = top_2_cincin.iloc[1]
    print(f'\n   Cincin Api Data:')
    print(f'   - Total Pohon: {int(blok2_cincin["total_trees"])}')
    print(f'   - Merah (Inti): {int(blok2_cincin["merah"])}')
    print(f'   - Oranye (Ring): {int(blok2_cincin["oranye"])}')
    print(f'   - Kuning (Suspect): {int(blok2_cincin["kuning"])}')
    print(f'   - Hijau (Sehat): {int(blok2_cincin["hijau"])}')
    print(f'   - Spread Ratio: {blok2_cincin["spread_ratio"]:.2f}x')
    print(f'   - Infection %: {blok2_cincin["infection_pct"]:.1f}%')
    
    print(f'\n   Mencari data produksi...')
    prod_candidates = []
    for col in df_prod.columns:
        val = blok2_data[col]
        if pd.notna(val) and isinstance(val, (int, float)):
            if 0 < val < 30:
                prod_candidates.append((col, val))
    
    if prod_candidates:
        print(f'   Kandidat kolom produksi (nilai 0-30):')
        for col, val in prod_candidates[:10]:
            print(f'      {col}: {val}')
else:
    print(f'\n❌ BLOK {blok2_formatted} TIDAK DITEMUKAN')

# Step 5: Save final summary
print('\n' + '='*80)
print('💾 MENYIMPAN SUMMARY FINAL')
print('='*80)

if len(row_blok1) > 0 and len(row_blok2) > 0:
    final_summary = {
        'Blok #1': {
            'code_full': blok1_code_full,
            'code_short': blok1_formatted,
            'tt': str(blok1_tt),
            'luas': float(blok1_luas) if pd.notna(blok1_luas) else None,
            'total_trees': int(blok1_cincin['total_trees']),
            'merah': int(blok1_cincin['merah']),
            'oranye': int(blok1_cincin['oranye']),
            'kuning': int(blok1_cincin['kuning']),
            'hijau': int(blok1_cincin['hijau']),
            'spread_ratio': float(blok1_cincin['spread_ratio']),
            'infection_pct': float(blok1_cincin['infection_pct']),
            'severity_score': float(blok1_cincin['severity_score'])
        },
        'Blok #2': {
            'code_full': blok2_code_full,
            'code_short': blok2_formatted,
            'tt': str(blok2_tt),
            'luas': float(blok2_luas) if pd.notna(blok2_luas) else None,
            'total_trees': int(blok2_cincin['total_trees']),
            'merah': int(blok2_cincin['merah']),
            'oranye': int(blok2_cincin['oranye']),
            'kuning': int(blok2_cincin['kuning']),
            'hijau': int(blok2_cincin['hijau']),
            'spread_ratio': float(blok2_cincin['spread_ratio']),
            'infection_pct': float(blok2_cincin['infection_pct']),
            'severity_score': float(blok2_cincin['severity_score'])
        }
    }
    
    import json
    with open('data/output/FINAL_TOP_2_BLOCKS.json', 'w') as f:
        json.dump(final_summary, f, indent=2)
    
    print('\n✅ Saved to: data/output/FINAL_TOP_2_BLOCKS.json')
    
    print('\n' + '='*80)
    print('🎯 SUMMARY')
    print('='*80)
    print(f'\nBLOK #1: {blok1_code_full} ({blok1_formatted})')
    print(f'  TT: {blok1_tt} | Luas: {blok1_luas} Ha')
    print(f'  Spread Ratio: {blok1_cincin["spread_ratio"]:.2f}x | Infection: {blok1_cincin["infection_pct"]:.1f}%')
    
    print(f'\nBLOK #2: {blok2_code_full} ({blok2_formatted})')
    print(f'  TT: {blok2_tt} | Luas: {blok2_luas} Ha')
    print(f'  Spread Ratio: {blok2_cincin["spread_ratio"]:.2f}x | Infection: {blok2_cincin["infection_pct"]:.1f}%')

print('\n✅ ANALISIS SELESAI!')
