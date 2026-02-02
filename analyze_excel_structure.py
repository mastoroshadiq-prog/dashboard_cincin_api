"""
Read ACTUAL historical data from data_gabungan.xlsx
Extract real 2023-2025 gap data and ganoderma stadium for attack rate
"""

import pandas as pd
import json

# Read Excel file
excel_file = r"f:\PythonProjects\poac_cincin_api\poac_sim\data\input\data_gabungan.xlsx"

print(f"📖 Reading Excel file: {excel_file}")
df = pd.read_excel(excel_file)

print(f"✅ Loaded {len(df)} rows")
print(f"📊 Total columns: {len(df.columns)}")

# Show first few column names to understand structure
print(f"\n📋 First 30 columns:")
for i, col in enumerate(df.columns[:30]):
    print(f"  {i}: {col}")

# Find the columns we need
# User said:
# FC = 2023 gap
# FL = 2024 gap  
# FU = 2025 gap

print(f"\n🔍 Looking for gap columns (FC, FL, FU)...")
fc_idx = None
fl_idx = None
fu_idx = None

for i, col in enumerate(df.columns):
    col_upper = str(col).upper()
    if i == 81:  # FC is typically column 82 (0-indexed = 81)
        fc_idx = i
        print(f"  Column {i} (FC ~82nd): {col}")
    if i == 90:  # FL is typically column 91
        fl_idx = i
        print(f"  Column {i} (FL ~91st): {col}")
    if i == 99:  # FU is typically column 100
        fu_idx = i
        print(f"  Column {i} (FU ~100th): {col}")

# Also look for block code column
block_col = None
for col in df.columns[:20]:
    if 'BLOK' in str(col).upper() or 'CODE' in str(col).upper():
        block_col = col
        print(f"\n📌 Block code column: '{col}'")
        break

# Show sample data for D008A
if block_col:
    sample = df[df[block_col] == 'D008A']
    if len(sample) > 0:
        print(f"\n🎯 Sample data for D008A:")
        row = sample.iloc[0]
        print(f"  Block: {row[block_col]}")
        if fc_idx: print(f"  Gap 2023 (col {fc_idx}): {row.iloc[fc_idx]}")
        if fl_idx: print(f"  Gap 2024 (col {fl_idx}): {row.iloc[fl_idx]}")
        if fu_idx: print(f"  Gap 2025 (col {fu_idx}): {row.iloc[fu_idx]}")

# Look for ganoderma stadium columns
print(f"\n🍄 Looking for ganoderma stadium columns...")
stadium_cols = []
for col in df.columns:
    col_str = str(col).upper()
    if 'STADIUM' in col_str or 'GANODERMA' in col_str:
        stadium_cols.append(col)
        print(f"  Found: {col}")

if len(stadium_cols) > 0 and block_col:
    sample = df[df[block_col] == 'D008A']
    if len(sample) > 0:
        print(f"\n🎯 D008A Ganoderma data:")
        row = sample.iloc[0]
        for scol in stadium_cols[:10]:
            print(f"  {scol}: {row[scol]}")

print(f"\n✅ Analysis complete. Will use this data to update COMPLETE_BLOCKS_DATA")
