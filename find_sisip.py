import pandas as pd
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Find all SISIP occurrences
print('Finding SISIP columns:')
for col in range(df.shape[1]):
    for row in range(10):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'SISIP' in val.upper():
            print(f'  Row {row}, Col {col}: {val}')
            if row > 0:
                above = df.iloc[row-1, col]
                print(f'    Above: {above}')
