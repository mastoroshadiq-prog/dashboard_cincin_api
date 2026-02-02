"""
Read ACTUAL historical data from data_gabungan.xlsx - simplified output
"""

import pandas as pd
import json

# Read Excel file
excel_file = r"f:\PythonProjects\poac_cincin_api\poac_sim\data\input\data_gabungan.xlsx"

print("Reading Excel file...")
df = pd.read_excel(excel_file)

print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Show column names with indices
print("\nColumn indices 78-105 (around FC, FL, FU):")
for i in range(78, min(105, len(df.columns))):
    print(f"  Col {i}: {df.columns[i]}")

# Find block code column
block_col = None
for col in ['BLOK', 'CODE_BLOCK', 'code_block', 'block_code', 'Block Code']:
    if col in df.columns:
        block_col = col
        break

if not block_col:
    # Try first few columns
    for col in df.columns[:10]:
        if 'blok' in str(col).lower() or 'code' in str(col).lower():
            block_col = col
            break

print(f"\nBlock column: {block_col}")

# Get D008A sample
if block_col:
    sample = df[df[block_col] == 'D008A']
    if len(sample) > 0:
        print(f"\nD008A data (columns 80-100):")
        row = sample.iloc[0]
        for i in range(80, min(100, len(df.columns))):
            val = row.iloc[i]
            if pd.notna(val) and val != 0:
                print(f"  Col {i} ({df.columns[i]}): {val}")

# Look for stadium columns
print("\nGanoderma stadium columns:")
for i, col in enumerate(df.columns):
    if 'stadium' in str(col).lower() or ('gano' in str(col).lower() and 'pct' in str(col).lower()):
        print(f"  Col {i}: {col}")
        if i > 120:  # Limit search
            break
