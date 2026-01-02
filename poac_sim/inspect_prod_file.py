
import pandas as pd
from pathlib import Path
import sys

# Path to file
file_path = Path('../data/input/Realisasi vs Potensi PT SR.xlsx')
if not file_path.exists():
    file_path = Path('data/input/Realisasi vs Potensi PT SR.xlsx')

with open('inspect_results.txt', 'w', encoding='utf-8') as f:
    f.write(f"Inspecting: {file_path}\n")
    try:
        # Read first 20 rows without header
        df = pd.read_excel(file_path, header=None, nrows=20)
        f.write("\n--- FIRST 20 ROWS ---\n")
        f.write(df.to_string())
    except Exception as e:
        f.write(f"Error: {e}")
