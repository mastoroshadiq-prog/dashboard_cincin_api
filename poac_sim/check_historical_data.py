import pandas as pd

# Load data_gabungan.xlsx
df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)

# Check headers for P (production) columns with years
print('=== Checking for Historical Production Data ===')
headers_row6 = df.iloc[6]
headers_row5 = df.iloc[5]
headers_row4 = df.iloc[4]

# Look for year patterns
print('\nSearching for year columns (2014-2025)...')
year_cols = {}
for i in range(len(headers_row6)):
    # Check all header rows
    for row_idx, row in enumerate([headers_row4, headers_row5, headers_row6]):
        if pd.notna(row[i]):
            val = str(row[i])
            # Check if it's a year
            if any(year in val for year in ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']):
                year_cols[i] = {'row': row_idx, 'header': val}
                print(f'col_{i}: {val}')

# Check P columns (production columns)
print('\n=== Production Columns (P001-P115) ===')
for i in range(62, 177):  # P columns range
    if i < len(headers_row6) and pd.notna(headers_row6[i]):
        print(f'col_{i}: Row4={headers_row4[i] if i < len(headers_row4) else "N/A"} | Row5={headers_row5[i] if i < len(headers_row5) else "N/A"} | Row6={headers_row6[i]}')

# Sample data to see structure
print('\n=== Sample E011A production data (P columns) ===')
df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]
e011a = df_data[df_data['col_0'] == 'E011A']
if not e011a.empty:
    for i in range(62, min(177, len(e011a.columns))):
        val = e011a[f'col_{i}'].iloc[0]
        if pd.notna(val) and val != 0:
            print(f'col_{i} = {val}')
