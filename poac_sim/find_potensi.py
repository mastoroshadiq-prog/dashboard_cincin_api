import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)
headers = df.iloc[6]

print(f'Total columns: {len(headers)}')
print(f'\n=== Headers around Produksi (col_165-175) ===')
for i in range(165, min(176, len(headers))):
    if pd.notna(headers[i]):
        print(f'col_{i}: {headers[i]}')

print('\n=== Searching ALL columns for "potensi" keyword ===')
found = []
for i, h in enumerate(headers):
    if pd.notna(h):
        h_lower = str(h).lower()
        if any(word in h_lower for word in ['pot', 'real', 'gap', 'selisih', 'target']):
            found.append((i, h))

if found:
    for i, h in found:
        print(f'col_{i}: {h}')
else:
    print('❌ Tidak ditemukan')

print('\n=== Sample data ===')
df_data = df.iloc[8:11].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]
cols_to_show = ['col_0', 'col_11', 'col_170']
if len(df_data.columns) > 171:
    cols_to_show.append('col_171')
if len(df_data.columns) > 172:
    cols_to_show.append('col_172')
print(df_data[cols_to_show].to_string())
