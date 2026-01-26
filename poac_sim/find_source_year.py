
import pandas as pd
import numpy as np

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=None, skiprows=10) # Data area

targets = ['D006A', 'D007A']
target_vals = {'D006A': 0.79, 'D007A': 0.30}

print("Searching for specific yield values...")

for target in targets:
    row = df[df.iloc[:, 2].astype(str).str.contains(target, na=False)]
    if not row.empty:
        print(f"\n--- {target} Row Values ---")
        vals = row.iloc[0].values
        found = False
        for i, val in enumerate(vals):
            if isinstance(val, (int, float)):
                # Check fuzzy match
                if abs(val - target_vals[target]) < 0.05:
                    print(f"MATCH FOUND! Value {val} at Column Index {i}")
                    found = True
        
        if not found:
            print(f"Value {target_vals[target]} NOT found in row.")
            # Print first few non-nan values to see what we have
            print("Sample values:", [v for v in vals if pd.notna(v) and isinstance(v, (int, float))][:10])
