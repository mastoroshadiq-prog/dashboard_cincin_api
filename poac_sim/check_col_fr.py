import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)

# Excel column FR = column 148 (F=6, R=18 -> (6-1)*26+18 = 148)
# In 0-indexed Python: col_147

headers = df.iloc[6]
print('=== Checking Column FR (Excel col 148 = Python col_147) ===')
print(f'Header row 6, col_147: {headers[147] if len(headers) > 147 else "NOT EXIST"}')

# Get E011A data
df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

e011a = df_data[df_data['col_0'] == 'E011A']
if not e011a.empty:
    row = e011a.iloc[0]
    print(f'\nE011A col_147 value: {row["col_147"]}')
    print(f'\nExpected: 424.4196')
    
    print('\n=== Checking nearby columns (145-150) ===')
    for i in range(145, 151):
        col_name = f'col_{i}'
        if col_name in row:
            print(f'col_{i}: {row[col_name]} (header: {headers[i] if len(headers) > i else "N/A"})')
    
    # Verify: Is 424.4196 = Potensi Produksi?
    if abs(float(row['col_147']) - 424.4196) < 0.01:
        print(f'\n✅ CONFIRMED! col_147 = {row["col_147"]} matches user value!')
        
        # Now calculate correct Potensi Yield
        luas = float(row['col_11'])
        potensi_prod_ton = float(row['col_147'])
        potensi_yield = potensi_prod_ton / luas
        
        print(f'\n=== Correct Calculation ===')
        print(f'Luas Ha: {luas}')
        print(f'Potensi Produksi: {potensi_prod_ton} Ton (from col_147 / FR)')
        print(f'Potensi Yield: {potensi_prod_ton} / {luas} = {potensi_yield:.4f} Ton/Ha')
        
        # Compare with current values
        realisasi_prod = float(row['col_170'])
        realisasi_yield = float(row['col_171'])
        print(f'\nRealisasi Produksi: {realisasi_prod} Ton')
        print(f'Realisasi Yield: {realisasi_yield:.4f} Ton/Ha')
        
        gap_prod = potensi_prod_ton - realisasi_prod
        gap_yield = potensi_yield - realisasi_yield
        print(f'\nGap Produksi: {gap_prod:.4f} Ton')
        print(f'Gap Yield: {gap_yield:.4f} Ton/Ha')
else:
    print('E011A not found!')
