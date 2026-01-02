
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
# Read all data starting from row 10 (header assumption based on previous step)
df = pd.read_excel(path, header=None, skiprows=10)

targets = ['D006A', 'D007A']

print("Checking for multiple entries (Pokok vs Sisip) for D006A and D007A...")

for target in targets:
    # Column 2 seems to be Block Code based on previous inspection
    rows = df[df.iloc[:, 2].astype(str).str.strip().str.upper() == target]
    
    if not rows.empty:
        print(f"\n=== Found {len(rows)} entries for {target} ===")
        for idx, row in rows.iterrows():
            # Based on previous find_year.py:
            # Col 2: Block
            # Col 5: Total Trees?
            # Col 6: Year (Tahun Tanam)
            # Col 0: SPH maybe? Or Col 7? Previous output showed Col 7 ~ 103-105 which looks like SPH.
            # Let's print relevant cols
            
            block = row.iloc[2]
            year = row.iloc[6]
            trees = row.iloc[5]
            sph = row.iloc[7] 
            
            print(f"Row {idx}: Year={year}, Trees={trees}, SPH={sph}")
    else:
        print(f"No entries found for {target}")
