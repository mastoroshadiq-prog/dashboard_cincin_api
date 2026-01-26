import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)

# Check headers
headers = df.iloc[6]
print('=== Headers around col_172 ===')
for i in range(168, 177):
    print(f'col_{i}: {headers[i] if pd.notna(headers[i]) else "NaN"}')

# Get E011A data
df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]
e011a = df_data[df_data['col_0'] == 'E011A'].iloc[0]

print('\n=== Data E011A (col_168-176) ===')
for i in range(168, 177):
    print(f'col_{i}: {e011a[f"col_{i}"]}')

# Check if 424.4196 appears somewhere
print('\n=== Searching for 424.4196 in E011A row ===')
for i, val in enumerate(e011a):
    if pd.notna(val):
        try:
            if abs(float(val) - 424.4196) < 0.01:
                print(f'FOUND at col_{i}: {val}')
        except:
            pass

# Maybe it's Luas * Potensi Yield?
print('\n=== Hypothesis: Potensi Total = Luas * Potensi Yield ===')
luas = 24.3
# If Potensi Total = 424.4196, then Potensi Yield = 424.4196 / 24.3
if luas > 0:
    implied_yield = 424.4196 / luas
    print(f'Implied Potensi Yield: 424.4196 / {luas} = {implied_yield:.4f} Ton/Ha')
