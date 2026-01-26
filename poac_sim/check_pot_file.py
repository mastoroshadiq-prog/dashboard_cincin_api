import pandas as pd

# Check the separate Realisasi vs Potensi file
print('=== Checking Realisasi vs Potensi PT SR.xlsx ===')
df_pot = pd.read_excel('data/input/Realisasi vs Potensi PT SR.xlsx', header=None)

print(f'Shape: {df_pot.shape}')
print('\nFirst 10 rows, first 10 columns:')
print(df_pot.iloc[0:10, 0:10])

# Try to find E011A
print('\n=== Searching for E011A ===')
for idx, row in df_pot.iterrows():
    for col_idx, val in enumerate(row):
        if pd.notna(val) and str(val).strip() == 'E011A':
            print(f'Found E011A at row {idx}, col {col_idx}')
            print(f'Row data: {df_pot.iloc[idx, :15].tolist()}')
            break
    if idx > 50:  # Don't search too far
        break

# Maybe data starts from a specific row?
print('\n=== Checking rows 5-15 ===')
for i in range(5, 15):
    print(f'Row {i}: {df_pot.iloc[i, :8].tolist()}')
