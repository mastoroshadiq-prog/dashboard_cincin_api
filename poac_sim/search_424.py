import pandas as pd

df = pd.read_excel('data/input/data_gabungan.xlsx', header=None)
headers = df.iloc[6]

df_data = df.iloc[8:].copy()
df_data.columns = [f'col_{i}' for i in range(df_data.shape[1])]

e011a = df_data[df_data['col_0'] == 'E011A'].iloc[0]

print('=== Searching for 424.4196 in E011A row ===')
found_cols = []
for i, val in enumerate(e011a):
    if pd.notna(val):
        try:
            if abs(float(val) - 424.4196) < 0.01:
                header = headers[i] if i < len(headers) and pd.notna(headers[i]) else 'N/A'
                print(f'✅ FOUND at col_{i} (header: {header}): {val}')
                found_cols.append(i)
        except (ValueError, TypeError):
            pass

if not found_cols:
    print('❌ Value 424.4196 NOT FOUND in E011A row')
    print('\n=== Looking for closest values ===')
    closest = []
    for i, val in enumerate(e011a):
        if pd.notna(val):
            try:
                fval = float(val)
                if 420 < fval < 430:  # Close range
                    header = headers[i] if i < len(headers) and pd.notna(headers[i]) else 'N/A'
                    closest.append((i, fval, header))
            except (ValueError, TypeError):
                pass
    
    print(f'Found {len(closest)} values in range 420-430:')
    for col_idx, val, header in closest:
        print(f'  col_{col_idx} (header: {header}): {val}')

# Let me also check what FR column should be
# F = 6th letter, R = 18th letter
# But maybe user means different columns

print('\n=== Maybe FR means different column? ===')
print('If FR is two-letter Excel column:')
print('  F=6, R=18')
print('  Excel column number = (6-1)*26 + 18 = 148')
print('  Python 0-indexed = col_147')

# Let me search for standard "Potensi" columns
print('\n=== Columns with "Pot" or values around 424 ===')
for i in range(len(headers)):
    h = headers[i]
    if pd.notna(h) and ('pot' in str(h).lower() or 'target' in str(h).lower()):
        val = e011a[f'col_{i}'] if f'col_{i}' in e011a.index else None
        print(f'col_{i} ({h}): {val}')
