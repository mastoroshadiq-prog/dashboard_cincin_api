
import pandas as pd
import os

# Relative to CWD: d:\PythonProjects\simulasi_poac\poac_sim
path = 'data/input/data_gabungan.xlsx'

if not os.path.exists(path):
    print(f"File not found at: {os.path.abspath(path)}")
    # Try alternate location just in case
    path2 = 'd:/PythonProjects/simulasi_poac/poac_sim/data/input/data_gabungan.xlsx'
    if os.path.exists(path2):
        path = path2
    else:
        print("Still not found.")
        exit()

try:
    df = pd.read_excel(path, nrows=5)
    print(f"Read success from {path}")
    print("Columns:", df.columns.tolist())
    print("\nFirst row sample:")
    print(df.iloc[0].to_dict())
    
except Exception as e:
    print(f"Error reading file: {e}")
