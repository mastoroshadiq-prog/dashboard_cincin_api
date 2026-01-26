import pandas as pd
import json

# Read the Excel file
file_path = r'poac_sim\data\input\data_gabungan.xlsx'

try:
    # Read with multi-row header
    df = pd.read_excel(file_path, header=[0, 1, 2, 3, 4, 5])
    
    print("=== COLUMN STRUCTURE (multi-level) ===")
    for i, col in enumerate(df.columns[:50]):  # First 50 columns
        print(f"Column {i}: {col}")
    
    print("\n=== FIRST 10 ROWS ===")
    print(df.head(10))
    
    # Try simpler header
    df_simple = pd.read_excel(file_path, header=6)
    
    print("\n\n=== SIMPLE HEADER (row 6) ===")
    print("Column names:")
    for i, col in enumerate(df_simple.columns[:50]):
        print(f"{i}: {col}")
    
    print("\n=== FIRST 10 ROWS (simple header) ===")
    print(df_simple.head(10))
    
    # Search for year/tanam columns
    year_cols = [i for i, col in enumerate(df_simple.columns) if 'tahun' in str(col).lower() or 'tanam' in str(col).lower() or 'year' in str(col).lower() or 'thn' in str(col).lower()]
    
    print(f"\n=== YEAR/TANAM COLUMNS (indices: {year_cols}) ===")
    if year_cols:
        for idx in year_cols:
            print(f"Column {idx}: {df_simple.columns[idx]}")
            print(df_simple.iloc[:10, idx])
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
