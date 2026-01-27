"""
Cari kolom dengan keyword 2025, Real, Potensi
"""

import pandas as pd

INPUT_FILE = "poac_sim/data/input/data_gabungan.xlsx"

df = pd.read_excel(INPUT_FILE)

# Check rows 0, 1, 2 for headers containing "2025"
print("Searching for columns with '2025' in headers...")
print("=" * 80)

for i, col in enumerate(df.columns):
    # Check first 3 rows for potential headers
    vals = []
    for row_idx in range(3):
        val = df.iloc[row_idx, i]
        if pd.notna(val):
            vals.append(str(val))
    
    combined = " ".join(vals)
    
    # Look for 2025
    if "2025" in combined:
        print(f"\nColumn {i}: {col}")
        print(f"  Row 0: {df.iloc[0, i] if pd.notna(df.iloc[0, i]) else 'NaN'}")
        print(f"  Row 1: {df.iloc[1, i] if pd.notna(df.iloc[1, i]) else 'NaN'}")
        print(f"  Row 2: {df.iloc[2, i] if pd.notna(df.iloc[2, i]) else 'NaN'}")
        
        # Sample data from AME02
        divisi_col = df.columns[5]
        ame02_data = df[df[divisi_col] == 'AME02']
        if len(ame02_data) > 0:
            sample_val = ame02_data.iloc[0, i]
            print(f"  AME02 Sample: {sample_val}")
