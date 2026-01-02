
import pandas as pd
from pathlib import Path

files_to_check = [
    'data/input/data_baru.csv',
    'data/input/Realisasi vs Potensi PT SR.xlsx'
]

for f in files_to_check:
    path = Path(f)
    if not path.exists(): path = Path('../' + f)
    
    if path.exists():
        print(f"\n--- Inspecting {path.name} ---")
        try:
            if 'csv' in path.suffix:
                df = pd.read_csv(path, nrows=5)
            else:
                df = pd.read_excel(path, nrows=5)
            print(f"Columns: {df.columns.tolist()}")
            print(df.head(2).to_string())
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"\n❌ File not found: {f}")
