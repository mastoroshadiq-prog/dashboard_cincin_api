
import pandas as pd
from pathlib import Path

try:
    print("Reading data_baru.csv...")
    df = pd.read_csv('data/input/data_baru.csv', header=4)
    
    # Find all columns containing 'BARU'
    baru_cols = [c for c in df.columns if 'BARU' in c]
    print(f"BARU Columns: {baru_cols}")
    
    print("\nContent Sample:")
    print(df[baru_cols].head(10).to_string())
    
    print("\nChecking TOTAL PKK:")
    print(df['TOTAL PKK'].head(10).to_string())
    
except Exception as e:
    print(f"Error: {e}")
