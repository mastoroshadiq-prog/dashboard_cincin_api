
import pandas as pd
from pathlib import Path

# Load full file
path = Path('data/input/Realisasi vs Potensi PT SR.xlsx')
if not path.exists(): path = Path('../data/input/Realisasi vs Potensi PT SR.xlsx')

# Read without header
df = pd.read_excel(path, header=None)

print(f"Total Rows: {len(df)}, Total Cols: {len(df.columns)}")

# Find header row (row with 'BLOK')
header_row = -1
for r in range(min(20, len(df))):
    row_vals = df.iloc[r].astype(str).str.upper().tolist()
    if 'BLOK' in row_vals:
        header_row = r
        print(f"\nHeader Row: {r}")
        print(f"Header: {row_vals[:20]}")
        break

# Find data start row (first row after header with actual block name like A001A or D001A)
data_start = -1
for r in range(header_row+1, min(header_row+20, len(df))):
    val = str(df.iloc[r, 2]).strip().upper()  # Column 2 should be BLOK
    if len(val) >= 4 and val[0].isalpha() and val[-1].isalpha():
        data_start = r
        print(f"\nData Start Row: {r}")
        print(f"Sample Data Row: {df.iloc[r, :15].tolist()}")
        break

# Now look at actual data columns
if data_start != -1:
    # Inspect columns 150-180 for production values
    print(f"\n--- Inspecting Columns 150-180 (Sample from row {data_start}) ---")
    sample_row = df.iloc[data_start, 150:180]
    for i, val in enumerate(sample_row):
        if pd.notna(val) and str(val).strip() != '':
            print(f"Col {150+i}: {val}")
            
    # Check what header says for these columns
    print(f"\n--- Header for Cols 150-180 ---")
    if header_row != -1:
        for r in range(max(0, header_row-3), min(header_row+5, len(df))):
            header_vals = df.iloc[r, 150:180]
            non_empty = [(i, v) for i, v in enumerate(header_vals) if pd.notna(v) and str(v).strip() != '']
            if non_empty:
                print(f"Row {r}: {[(f'Col{150+i}', v) for i, v in non_empty]}")
    
    # Try a different approach: look for numeric columns with reasonable production values (0-50 range)
    print(f"\n--- Searching for Production Columns (Numeric 0-100 range) ---")
    for c in range(50, min(200, len(df.columns))):
        sample_vals = df.iloc[data_start:data_start+10, c]
        numeric_vals = pd.to_numeric(sample_vals, errors='coerce').dropna()
        if len(numeric_vals) > 0:
            mean_val = numeric_vals.mean()
            if 0 < mean_val < 100 and len(numeric_vals) >= 5:  # Likely production data
                print(f"Col {c}: Mean={mean_val:.2f}, Sample: {numeric_vals.head(3).tolist()}")
