import pandas as pd

# Load data_gabungan.xlsx
df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)

# Check header rows
print('=== Header Row 5 (index 4) ===')
print(df.iloc[4].to_string())

print('\n=== Header Row 6 (index 5) ===')
print(df.iloc[5].to_string())

print('\n=== Header Row 7 (index 6) - MAIN HEADER ===')
headers = df.iloc[6]
print(headers.to_string())

print('\n=== Searching for Stadium columns ===')
for i, h in enumerate(headers):
    if pd.notna(h):
        h_str = str(h).upper()
        # Search more broadly
        if any(word in h_str for word in ['STAD', 'GANO', 'STAK', 'INFEK', 'SERN', '%']):
            print(f'col_{i}: {h}')

# Check sample data for blocks
df_data = df.iloc[8:11].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

print('\n=== Sample data (first 3 blocks, cols 0-20) ===')
print(df_data[['col_0'] + [f'col_{i}' for i in range(1, 21)]].to_string())
