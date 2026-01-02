
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
# Read header from row 6 (0-indexed)
df = pd.read_excel(path, header=6, nrows=0) 
print("Columns found:")
for col in df.columns:
    print(col)
