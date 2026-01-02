
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=None, skiprows=7, nrows=1) # Row 7 is index 7

print("Sub-headers (Row 7):")
print(df.values[0])
