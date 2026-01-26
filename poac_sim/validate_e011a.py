import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)
df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

# Find E011A
e011a = df_data[df_data['col_0'] == 'E011A']

if not e011a.empty:
    print('=== Data untuk Blok E011A ===')
    row = e011a.iloc[0]
    print(f'Blok: {row["col_0"]}')
    print(f'col_11 (Luas Ha): {row["col_11"]}')
    print(f'col_170 (Produksi Realisasi Ton): {row["col_170"]}')
    print(f'col_171 (Yield Realisasi Ton/Ha): {row["col_171"]}')
    print(f'col_172 (Potensi Produksi Kg): {row["col_172"]}')
    
    print('\n=== Perhitungan Manual ===')
    luas_col11 = float(row["col_11"])
    produksi = float(row["col_170"])
    yield_real = float(row["col_171"])
    potensi_kg = float(row["col_172"])
    
    print(f'Luas dari col_11: {luas_col11} Ha')
    print(f'Produksi Realisasi: {produksi} Ton')
    print(f'Yield Realisasi (col_171): {yield_real} Ton/Ha')
    
    # Luas actual = Produksi / Yield
    luas_actual = produksi / yield_real
    print(f'\nLuas Actual (Produksi/Yield): {produksi}/{yield_real} = {luas_actual:.2f} Ha')
    
    # Potensi yield = Potensi Prod (Ton) / Luas Actual  
    potensi_ton = potensi_kg / 1000
    potensi_yield = potensi_ton / luas_actual
    print(f'\nPotensi Produksi: {potensi_kg} Kg = {potensi_ton} Ton')
    print(f'Potensi Yield: {potensi_ton}/{luas_actual:.2f} = {potensi_yield:.4f} Ton/Ha')
    
    gap = potensi_yield - yield_real
    print(f'\nGap: {potensi_yield:.4f} - {yield_real} = {gap:.4f} Ton/Ha')
    
    print('\n=== Yang User Lihat ===')
    print(f'Luas Ha: 24.3 (dari col_11)')
    print(f'Realisasi: 396.81')
    print(f'Potensi: 424.4196')
    
    print('\n=== Kesimpulan ===')
    print(f'User benar bahwa Luas di Excel = {luas_col11} Ha')
    print(f'User benar bahwa Produksi Realisasi = {produksi} Ton')
    print(f'Potensi Prod (Kg) = {potensi_kg} Kg')
else:
    print('Blok E011A tidak ditemukan!')
    
print('\n=== Checking all E blocks ===')
e_blocks = df_data[df_data['col_0'].astype(str).str.startswith('E', na=False)]
print(f'Found {len(e_blocks)} E blocks')
print(e_blocks[['col_0', 'col_11', 'col_170']].head(20))
