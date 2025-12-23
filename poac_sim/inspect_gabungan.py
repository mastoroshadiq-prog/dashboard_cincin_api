
import pandas as pd
from pathlib import Path

file_path = Path('data/input/data_gabungan.xlsx')

try:
    # Try Header at row 8 (0-based index)
    df = pd.read_excel(file_path, header=8, nrows=5)
    
    print("HEADER ROW 8 COLUMNS:")
    cols = df.columns.tolist()
    # Print columns with index to locate Total Pokok
    for i, c in enumerate(cols):
        print(f"{i}: {c}")
        
except Exception as e:
    print(f"Error: {e}")
