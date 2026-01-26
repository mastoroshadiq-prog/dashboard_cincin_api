
import pandas as pd
import sys

try:
    path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
    # Load with header at row 6 (0-indexed -> 5)
    df = pd.read_excel(path, header=5)
    
    # Filter for D006A and D007A
    # Column 2 (index 2) is usually block. Let's check columns.
    # Based on previous analysis: Col 2 is BLOCK.
    
    # We'll just look for rows containing D006A or D007A in any string column or specifically col 2
    # The dataframe columns will be named from row 6.
    
    # Let's clean column names
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Identify block column. Previous analysis said index 2.
    block_col = df.columns[2]
    print(f"Block Column likely: {block_col}")
    
    targets = ['D006A', 'D007A']
    
    for target in targets:
        print(f"\n--- Data for {target} ---")
        # Try to find exactly
        row = df[df.iloc[:, 2].astype(str).str.strip().str.upper() == target]
        
        if not row.empty:
            # Print non-null values to see what we have
            for col in df.columns:
                val = row.iloc[0][col]
                if pd.notna(val) and val != 0:
                    print(f"{col}: {val}")
        else:
            print("Not found.")

except Exception as e:
    print(f"Error: {e}")
