"""
PILOT ANALYSIS V2: AME II (AME02)
Membaca Excel dengan skip rows untuk mendapatkan header yang benar
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")

# Try different header rows
for skip_rows in [0, 1, 2]:
    print("=" * 80)
    print(f"TRYING WITH SKIPROWS={skip_rows}")
    print("=" * 80)
    
    df = pd.read_excel(INPUT_FILE, header=skip_rows if skip_rows > 0 else 0, skiprows=range(1, skip_rows) if skip_rows > 1 else None)
    
    print(f"\n[OK] Loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"\n[INFO] First 30 columns:")
    for i, col in enumerate(df.columns[:30], 1):
        print(f"   {i:3}. {col}")
    
    print(f"\n[INFO] Sample data (first row):")
    print(df.head(1).T)
    
    print("\n" + "=" * 80)
    
    # Check for common column patterns
    div_found = False
    for col in df.columns:
        col_str = str(col).lower()
        if any(keyword in col_str for keyword in ['divisi', 'div', 'afd', 'ame', 'estate', 'blok']):
            print(f"[FOUND] Potential division column: '{col}'")
            print(f"        Unique values ({len(df[col].unique())}): {list(df[col].unique()[:10])}")
            div_found = True
    
    if div_found:
        print(f"\n[SUCCESS] Found division-related columns with skiprows={skip_rows}")
        break
    else:
        print(f"\n[INFO] No division column found with skiprows={skip_rows}, trying next...")
    
    print("\n")
