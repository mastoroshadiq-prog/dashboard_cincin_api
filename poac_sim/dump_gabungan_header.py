
import pandas as pd

path = 'data/input/data_gabungan.xlsx'
df = pd.read_excel(path, header=None, nrows=10)

print("Rows 0-9:")
for i, row in df.iterrows():
    # Filter out all-nan rows for cleaner output
    vals = [str(v) for v in row.tolist() if pd.notna(v) and str(v) != 'nan']
    if vals:
        print(f"Row {i}: {vals}")
