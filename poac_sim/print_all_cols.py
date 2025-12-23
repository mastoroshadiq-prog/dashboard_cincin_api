import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)
headers = df.iloc[6]

# Search ALL columns, print any that might be related
print('=== ALL COLUMNS (showing all non-empty headers) ===')
for i in range(len(headers)):
    if pd.notna(headers[i]):
        print(f'col_{i}: {headers[i]}')

# Also check row 4 and 5 which might have category labels
print('\n=== ROW 4 (Categories) ===')
for i in range(len(df.iloc[4])):
    if pd.notna(df.iloc[4][i]):
        print(f'col_{i}: {df.iloc[4][i]}')

print('\n=== ROW 5 (Sub-categories) ===')
for i in range(len(df.iloc[5])):
    if pd.notna(df.iloc[5][i]):
        print(f'col_{i}: {df.iloc[5][i]}')

# Sample one block to see data pattern
df_data = df.iloc[8:9].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

print(f'\n=== Sample E011A data (all {len(df_data.columns)} columns) ===')
e011a = df_data[df_data['col_0'] == 'E011A']
if not e011a.empty:
    for i in range(len(e011a.columns)):
        val = e011a[f'col_{i}'].iloc[0]
        if pd.notna(val) and val != 0:
            print(f'col_{i} = {val}')
