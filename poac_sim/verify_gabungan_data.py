import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

# Get D006A and D007A data
d006a = df[df['Unnamed: 0'] == 'D006A'].iloc[0]
d007a = df[df['Unnamed: 0'] == 'D007A'].iloc[0]

print('='*80)
print('📊 VERIFIKASI DATA PRODUKSI 2025 - data_gabungan.xlsx')
print('='*80)

print('\n=== BLOK D006A ===')
print(f'Blok Code: {d006a["Unnamed: 0"]}')
print(f'Blok: {d006a["BLOK"]}')
print(f'TT: {d006a["TT"]}')
print(f'Luas (Ha): {d006a["HA STATEMENT"]}')

print('\n=== BLOK D007A ===')
print(f'Blok Code: {d007a["Unnamed: 0"]}')
print(f'Blok: {d007a["BLOK"]}')
print(f'TT: {d007a["TT"]}')
print(f'Luas (Ha): {d007a["HA STATEMENT"]}')

# Read header rows to find column names
print('\n' + '='*80)
print('🔍 MENCARI KOLOM POTENSI DAN REALISASI 2025')
print('='*80)

# Read with multi-level header to see structure
df_multi = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=[0,1,2,3])
print('\nMulti-level columns (sample):')
for i, col in enumerate(df_multi.columns[:20]):
    print(f'{i}: {col}')

# Look for columns containing production data
# Based on typical structure, production data is usually in later columns
print('\n📊 Checking numeric columns for D006A and D007A...')

# Get all numeric data for both blocks
d006a_data = {}
d007a_data = {}

for i, col in enumerate(df.columns):
    val_d006a = d006a[col]
    val_d007a = d007a[col]
    
    if pd.notna(val_d006a) and isinstance(val_d006a, (int, float)):
        # Check if value is in reasonable range for yield (0-30 ton/ha)
        if 0 <= val_d006a <= 30:
            d006a_data[f'Col_{i}_{col}'] = val_d006a
    
    if pd.notna(val_d007a) and isinstance(val_d007a, (int, float)):
        if 0 <= val_d007a <= 30:
            d007a_data[f'Col_{i}_{col}'] = val_d007a

print('\n🎯 D006A - Nilai dalam range 0-30 (kemungkinan Ton/Ha):')
for col, val in list(d006a_data.items())[:20]:
    print(f'  {col}: {val}')

print('\n🎯 D007A - Nilai dalam range 0-30 (kemungkinan Ton/Ha):')
for col, val in list(d007a_data.items())[:20]:
    print(f'  {col}: {val}')

print('\n' + '='*80)
print('✅ Selesai - Silakan review data di atas untuk identifikasi kolom yang tepat')
print('='*80)
