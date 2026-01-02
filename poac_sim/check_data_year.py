
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'

# Read the first few rows (header area) to look for year information
df_header = pd.read_excel(path, header=None, nrows=15)

print("=== Header Inspection ===")
for i, row in df_header.iterrows():
    # Print row index and content, filtering out NaNs
    content = [str(x) for x in row.values if pd.notna(x)]
    if content:
        print(f"Row {i}: {content}")
