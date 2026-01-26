import pandas as pd
import numpy as np

print('='*80)
print('🔍 ANALISIS: MENCARI 2 BLOK DENGAN KONDISI TERPARAH')
print('='*80)

# Read data_gabungan.xlsx
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

print('\n📋 Total columns:', len(df.columns))
print('Sample columns:', df.columns.tolist()[:20])

# Filter for Divisi AME002 (Divisi D)
divisi_d = df[df['DIVISI'].astype(str).str.contains('AME002', case=False, na=False)].copy()

print(f'\n✅ Found {len(divisi_d)} blocks in Divisi AME002')

# Look for production/yield columns
# Based on file structure, find columns with production data
print('\n🔍 Mencari kolom produksi (Potensi, Realisasi, Gap)...')

# Show all column names to identify production columns
prod_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['potensi', 'realisasi', 'gap', 'prod', 'yield', 'ton'])]
print(f'\nKolom produksi yang ditemukan: {prod_cols[:10]}')

# Let's check what data we have for blocks
print('\n📊 Sample data untuk beberapa blok:')
sample_blocks = divisi_d[['BLOK', 'TT', 'HA STATEMENT']].head(15)
print(sample_blocks)

# Now let's find columns with numeric data that could be yield/production
print('\n🔍 Mencari kolom numerik yang mungkin berisi data produksi...')

# Check columns around index 100-120 (based on previous attempts)
numeric_cols = []
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        # Check if values are in reasonable range for yield (0-30 ton/ha)
        sample_vals = divisi_d[col].dropna()
        if len(sample_vals) > 0:
            if sample_vals.min() >= -100 and sample_vals.max() <= 1000:
                numeric_cols.append(col)

print(f'\nFound {len(numeric_cols)} numeric columns with reasonable ranges')

# Let's specifically look for blocks with TT 2009 (same as our target)
blocks_2009 = divisi_d[divisi_d['TT'] == 2009].copy()
print(f'\n✅ Found {len(blocks_2009)} blocks with TT 2009 in AME002')

print('\nBlocks TT 2009:')
print(blocks_2009[['BLOK', 'TT', 'HA STATEMENT']])

# Save this for further analysis
blocks_2009.to_csv('data/output/blocks_2009_ame002.csv', index=False)
print('\n✅ Data saved to: data/output/blocks_2009_ame002.csv')

print('\n' + '='*80)
print('📝 LANGKAH SELANJUTNYA:')
print('='*80)
print('1. Identifikasi kolom yang berisi Potensi dan Realisasi 2025')
print('2. Hitung Gap Yield untuk setiap blok')
print('3. Ranking blok berdasarkan Gap Yield tertinggi')
print('4. Cross-check dengan data Cincin Api (infeksi Ganoderma)')
