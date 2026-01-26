
import pandas as pd

path = 'data/input/Realisasi vs Potensi PT SR.xlsx'
df = pd.read_excel(path, header=6) # Header row is index 6

# Find columns starting with 2024 and 2025
cols_2024 = [c for c in df.columns if str(c).startswith('2024')]
cols_2025 = [c for c in df.columns if str(c).startswith('2025')]

print(f"2024 Column: {cols_2024}")
print(f"2025 Column: {cols_2025}")

# Get row for D006A
row = df[df.iloc[:, 1].astype(str).str.contains('D006A', na=False)]

if not row.empty:
    print("\nData for D006A (2024-2025 area):")
    # Get index of 2024 column
    idx_2024 = df.columns.get_loc(cols_2024[0]) if cols_2024 else -1
    idx_2025 = df.columns.get_loc(cols_2025[0]) if cols_2025 else -1
    
    if idx_2024 != -1:
        print("\n--- 2024 Data ---")
        for i in range(idx_2024, idx_2024 + 9): # Assume 9 cols per year
            if i < len(df.columns):
                col_name = df.columns[i]
                val = row.iloc[0, i]
                print(f"Col {col_name} (idx {i}): {val}")

    if idx_2025 != -1:
        print("\n--- 2025 Data ---")
        for i in range(idx_2025, len(df.columns)):
            col_name = df.columns[i]
            val = row.iloc[0, i]
            print(f"Col {col_name} (idx {i}): {val}")
