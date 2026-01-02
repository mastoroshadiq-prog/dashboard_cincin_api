
import pandas as pd
path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=None, skiprows=10) # Data starts row 10
# Filter D006A/D007A
targets = ['D006A', 'D007A']
for target in targets:
    row = df[df.iloc[:, 2].astype(str).str.strip().str.upper() == target]
    if not row.empty:
        print(f"\nBLOCK {target}:")
        # Print first 20 columns
        for i in range(20):
            val = row.iloc[0, i]
            print(f"Col {i}: {val}")
