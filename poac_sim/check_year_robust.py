
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=6)

print("Columns:", df.columns.tolist()[:5])

# Find block column
# It should be the one named 'BLOK'
if 'BLOK' in df.columns:
    print(f"Found 'BLOK' column.")
    # Clean block names
    df['BLOK'] = df['BLOK'].astype(str).str.strip().str.upper()
    
    target = 'D006A'
    row = df[df['BLOK'] == target]
    
    if not row.empty:
        print(f"Found row for {target}!")
        
        # Check years
        cols_2024 = [c for c in df.columns if str(c) == '2024']
        cols_2025 = [c for c in df.columns if str(c) == '2025']
        
        if cols_2024:
            idx_2024 = df.columns.get_loc(cols_2024[0])
            print("\n2024 Data:")
            print(row.iloc[0, idx_2024:idx_2024+9].to_string())
            
        if cols_2025:
            idx_2025 = df.columns.get_loc(cols_2025[0])
            print("\n2025 Data:")
            print(row.iloc[0, idx_2025:idx_2025+9].to_string())
            
    else:
        print(f"Block {target} not found in 'BLOK' column.")
        print("Sample blocks:", df['BLOK'].head().tolist())
else:
    print("'BLOK' column not found.")
