
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=None, nrows=6)

print("Check Rows 0-5 for Title/Year:")
for i, row in df.iterrows():
    print(f"Row {i}: {row.dropna().tolist()}")
