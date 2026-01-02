
import pandas as pd

path = 'data/input/data_gabungan.xlsx'
# Header at row 3 (0-indexed)
df = pd.read_excel(path, header=3)

print("Columns (First 20):", df.columns.tolist()[:20])
print("Columns with '2024' or '2025':", [c for c in df.columns if '2024' in str(c) or '2025' in str(c)])
print("Columns with 'POTENSI' or 'REALISASI' or 'GAP':", [c for c in df.columns if any(x in str(c).upper() for x in ['POTENSI', 'REAL', 'GAP'])])

# Clean block column
# Assume 'BLOK' is the name
if 'BLOK' in df.columns:
    df['BLOK'] = df['BLOK'].astype(str).str.strip().str.upper()
    targets = ['D006A', 'D007A']
    
    for t in targets:
        row = df[df['BLOK'] == t]
        if not row.empty:
            print(f"\n=== Found {t} ===")
            # Print non-null values
            r = row.iloc[0]
            for col, val in r.items():
                if pd.notna(val) and val != 0 and 'Unnamed' not in str(col):
                     print(f"{col}: {val}")
        else:
            print(f"Block {t} not found.")
else:
    print("'BLOK' column not found.")
