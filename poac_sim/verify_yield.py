import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)
df_data = df.iloc[8:11].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

print('=== Verifying Yield calculation ===')
print('Row 8 (C006A):')
print(f'  col_11 (Luas?): {df_data.iloc[0]["col_11"]}')
print(f'  col_170 (Produksi): {df_data.iloc[0]["col_170"]}')
print(f'  col_171 (Yield?): {df_data.iloc[0]["col_171"]}')
print(f'  col_172: {df_data.iloc[0]["col_172"]}')
print(f'  Manual calc: {df_data.iloc[0]["col_170"]} / {df_data.iloc[0]["col_11"]} = {df_data.iloc[0]["col_170"] / df_data.iloc[0]["col_11"]:.4f}')
print(f'  Expected: {df_data.iloc[0]["col_171"]}')

# Maybe col_171 is already calculated yield (Realisasi Yield)
# and col_172 is Potensi Yield?
# Let's check if col_172 looks like potential yield

print('\n=== Checking if col_172 could be Potensi Yield ===')
for i in range(3):
    row = df_data.iloc[i]
    print(f'{row["col_0"]}: Prod={row["col_170"]}, Yield={row["col_171"]}, col_172={row["col_172"]}')
    # If col_172 is potensi prod in kg, then potensi yield = col_172 / (col_11 * 1000)?
    if row["col_11"] > 0:
        potensi_yield_calc = row["col_172"] / (row["col_11"] * 1000)
        print(f'  If col_172 is Potensi Prod (kg): {row["col_172"]} / ({row["col_11"]} * 1000) = {potensi_yield_calc:.4f} ton/ha')

print('\n=== Trying to find actual Luas Ha ===')
# Check if Produksi / Yield = Luas
for i in range(3):
    row = df_data.iloc[i]
    if row["col_171"] > 0:
        luas_calc = row["col_170"] / row["col_171"]
        print(f'{row["col_0"]}: Luas = Produksi/Yield = {row["col_170"]}/{row["col_171"]} = {luas_calc:.2f} Ha')
        print(f'  col_11 shows: {row["col_11"]} Ha')
