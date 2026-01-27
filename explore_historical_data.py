"""
HISTORICAL TREND & FORECASTING ANALYSIS
- Historical: 3 years back (2022, 2023, 2024)
- Current: 2025
- Forecast: 3 years forward (2026, 2027, 2028) - NO TREATMENT scenario

Based on conversation with user, need to find:
1. Production data for 2022-2025
2. Calculate trend
3. Forecast 2026-2028 using linear regression (worst case: no treatment)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_DIR = Path("poac_sim/data/output/trend_analysis")

# Known indices from previous analysis
DIVISI_COL_IDX = 5
BLOK_COL_IDX = 8

# Let's explore what production data exists
# We know index 170 is 2025 Real, 173 is 2025 Pot
# Need to find 2022, 2023, 2024

print("="*80)
print("EXPLORING PRODUCTION DATA STRUCTURE")
print("="*80)

# Load Excel with header inspection
df = pd.read_excel(INPUT_FILE)

print(f"\nTotal Columns: {len(df.columns)}")

# Sample AME02 row to see data pattern
divisi_col = df.columns[DIVISI_COL_IDX]
blok_col = df.columns[BLOK_COL_IDX]

ame02_sample = df[df[divisi_col] == 'AME02'].iloc[0] if len(df[df[divisi_col] == 'AME02']) > 0 else None

if ame02_sample is not None:
    print("\n=== SAMPLE AME02 BLOCK (checking for production columns) ===\n")
    
    # Check columns around known 2025 index (170) and backwards
    # Pattern might be: Year columns repeat for different metrics
    
    production_cols = {}
    
    # Known 2025 columns
    production_cols['2025_real'] = 170
    production_cols['2025_pot'] = 17373
    
    # Let's check some patterns - typically data might be structured in blocks
    # Try checking every ~50 columns before 170
    
    for offset in [0, -30, -60, -90, -120]:
        idx = 170 + offset
        if 0 <= idx < len(df.columns):
            val = ame02_sample.iloc[idx]
            print(f"Index {idx:3d}: {val}")
    
    print("\n=== CHECKING PATTERN AROUND 2025 REAL (170) ===")
    for i in range(max(0, 170-10), min(len(df.columns), 170+15)):
        val = ame02_sample.iloc[i]
        if pd.notna(val) and val != 0:
            print(f"Index {i:3d}: {val:>12} ({type(val).__name__})")

print("\n" + "="*80)
print("RECOMMENDATION:")
print("="*80)
print("""
Based on Excel structure, I need to:
1. Check actual Excel file headers (might be in row 0-2)
2. Identify production columns for each year
3. If historical data not available, will use:
   - FORECASTING ONLY mode (use 2025 as baseline)
   - Apply degradation rate based on Ganoderma/SPH trends
   - Estimate backwards using industry averages
""")
