import pandas as pd

# Load data_gabungan.xlsx
df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)

# Check specific rows for year mapping
print('=== Mapping Historical Yield Columns ===')
print('Looking for pattern in P columns that represent yearly yield...\n')

# Headers
headers_row6 = df.iloc[6]
headers_row5 = df.iloc[5]
headers_row4 = df.iloc[4]

# Sample E011A
df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]
e011a = df_data[df_data['col_0'] == 'E011A'].iloc[0]

print('Looking for yearly yield pattern in P columns:')
print('Expected: ~12 years * some columns per year\n')

# P columns typically start around col_62
# Let's check the pattern
print('Sample E011A values with headers:')
for i in range(62, min(177, len(headers_row6))):
    val = e011a[f'col_{i}']
    if pd.notna(val) and val != 0:
        h4 = headers_row4[i] if i < len(headers_row4) else ''
        h5 = headers_row5[i] if i < len(headers_row5) else ''
        h6 = headers_row6[i] if i < len(headers_row6) else ''
        
        # Look for yield-like values (reasonable Ton/Ha range)
        if isinstance(val, (int, float)) and 0 < val < 100:
            print(f'col_{i}: Row4={h4} | Row5={h5} | Row6={h6} | Value={val:.2f}')

print('\n=== Checking known yield columns ===')
print(f'col_171 (current year yield from previous analysis): {e011a["col_171"]:.2f}')

# Based on E011A sample, let me try to find the pattern
# Typically production data has: Year, Yield BJR, Produksi, etc
# We want the yield (Ton/Ha) values

# Let's look for columns that might be "Yield" per year
print('\n=== Looking for "Ton/Ha" or "Yield" pattern ===')
yield_cols = []
for i in range(60, 177):
    if i >= len(headers_row5):
        continue
    h5 = str(headers_row5[i]).upper() if pd.notna(headers_row5[i]) else ''
    h6 = str(headers_row6[i]).upper() if pd.notna(headers_row6[i]) else ''
    
    # Check if it's a yield column (Ton/Ha or BJR related)
    if 'TON' in h5 or 'BJR' in h5 or 'YIELD' in h5:
        val = e011a[f'col_{i}']
        if pd.notna(val):
            print(f'col_{i}: {headers_row5[i]} | Value={val}')
            if isinstance(val, (int, float)) and 0 < val < 100:
                yield_cols.append(i)

print(f'\nPotential yield columns: {yield_cols}')
