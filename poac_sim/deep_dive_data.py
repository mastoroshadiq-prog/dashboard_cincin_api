
import pandas as pd

# Check CSV for Tree-level info
try:
    print("Checking Tabel NDRE...")
    df_ndre = pd.read_csv('data/input/tabelNDREnew.csv')
    print("Columns:", df_ndre.columns.tolist())
    
    # Filter for D006A
    df_d6 = df_ndre[df_ndre['BLOK_B'].astype(str).str.contains('D006A', na=False)]
    print(f"NDRE Rows for D006A: {len(df_d6)}")
    if not df_d6.empty:
        # Check if there's a planting year column
        possible_year_cols = [c for c in df_d6.columns if 'TAHUN' in c.upper() or 'YEAR' in c.upper() or 'TANAM' in c.upper()]
        if possible_year_cols:
            print(f"Found year columns: {possible_year_cols}")
            for col in possible_year_cols:
                print(f"Values in {col}: {df_d6[col].unique()}")
        else:
            print("No explicit planting year column found in NDRE.")

except Exception as e:
    print(f"Error reading CSV: {e}")

# Check Excel again
try:
    print("\nChecking Excel...")
    path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
    df_xl = pd.read_excel(path, header=None, skiprows=10)
    
    # Col 2 is Block
    # Col 6 is Year
    # Col 5 is Trees
    
    # Filter for contains 'D006A' or 'D007A'
    relevant = df_xl[df_xl[2].astype(str).str.contains('D006A|D007A', na=False, case=False)]
    
    for idx, row in relevant.iterrows():
        print(f"Block: {row[2]}, Year: {row[6]}, Trees: {row[5]}, SPH: {row[7]}")
        
except Exception as e:
    print(f"Error reading Excel: {e}")
