
import pandas as pd
from pathlib import Path

file_path = Path('data/input/Arael Inti & Serangan Ganoderma.xlsx')

try:
    # Try header at row 3 (index 2)
    df = pd.read_excel(file_path, header=2)
    print("HEADER ROW 2 COLUMNS:")
    print(df.columns.tolist())
    
    # Try header at row 4 (index 3)
    df2 = pd.read_excel(file_path, header=3)
    print("\nHEADER ROW 3 COLUMNS:")
    print(df2.columns.tolist())
    
except Exception as e:
    print(f"Error: {e}")
