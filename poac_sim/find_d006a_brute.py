
import pandas as pd

path = 'data/input/data_gabungan.xlsx'
df = pd.read_excel(path, header=3) 

# Print cleaned column names
clean_cols = [str(c).strip().upper() for c in df.columns]
print("Cleaned Cols:", clean_cols[:20])

# Search for D006A anywhere
print("\nSearching for 'D006A' in entire dataframe...")
# Iterate rows manually or use apply
found = False
for idx, row in df.iterrows():
    # Convert row to string and search
    row_str = row.astype(str).str.cat(sep=' ')
    if 'D006A' in row_str.upper():
        print(f"Found D006A at Index {idx}")
        # Print the row content with column names
        for col in df.columns:
            val = row[col]
            if pd.notna(val):
                print(f"  {col}: {val}")
        found = True
        break

if not found:
    print("D006A strictly not found.")
