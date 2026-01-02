
import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
try:
    df = pd.read_excel(path, header=None, nrows=20)
    print("--- RAW HEADER DUMP ---")
    # Print row by row found to contain text
    for i, row in df.iterrows():
        # filter out nan
        vals = [f"{c}:{v}" for c,v in enumerate(row.tolist()) if pd.notna(v) and str(v).strip() != '']
        if vals:
             print(f"ROW {i}: {vals}")
except Exception as e:
    print(e)
