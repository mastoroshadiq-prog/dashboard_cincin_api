
import pandas as pd

path = 'data/input/data_gabungan.xlsx'
df = pd.read_excel(path, header=3)

# Strip column names
df.columns = [str(c).strip() for c in df.columns]

if 'BLOK' not in df.columns:
    print("BLOK column missing. Available columns matching 'BLO':")
    print([c for c in df.columns if 'BLO' in c])
    exit()

df['BLOK'] = df['BLOK'].astype(str).str.strip().str.upper()
targets = ['D006A', 'D007A']

for t in targets:
    row = df[df['BLOK'] == t]
    if not row.empty:
        r = row.iloc[0]
        print(f"\n--- {t} ---")
        
        # Agronomy
        print(f"TT: {r.get('TT', 'N/A')}")
        # Ha is likely column index 3 (0-based) if BLOK is 2.
        # Let's try to find keys starting with 'LUAS' or 'Ha'
        ha_col = next((c for c in df.columns if 'HA' in c.upper() or 'LUAS' in c.upper()), None)
        if ha_col:
            print(f"Ha ({ha_col}): {r[ha_col]}")
        else:
             # Fallback to index 3 (based on brute force observation)
             print(f"Ha (idx 3): {r.iloc[3]}")

        print(f"Pokok (idx 5): {r.iloc[5]}")
        print(f"SPH (idx 6): {r.iloc[6]}")

        # Production 2024
        col_2024 = next((c for c in df.columns if str(c) == '2024'), None)
        if col_2024:
            idx = df.columns.get_loc(col_2024)
            real = r.iloc[idx]
            pot = r.iloc[idx+2]
            gap = r.iloc[idx+5]
            print(f"Prod 2024: {real}")
            print(f"Pot 2024: {pot}")
            print(f"Gap 2024: {gap}")
        else:
            print("Column 2024 not found")
    else:
        print(f"{t} not found")
