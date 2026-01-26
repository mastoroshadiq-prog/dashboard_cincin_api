import pandas as pd
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Show header structure around SISIP columns
print("Header structure for SISIP area:")
print("Cols 33-55, Rows 0-6:")
for row in range(7):
    vals = []
    for col in range(33, 56):
        v = df.iloc[row, col]
        vals.append(str(v)[:10] if pd.notna(v) else '')
    print(f"Row {row}: {vals}")

# Find block A005C 
print("\n\nFinding A005C:")
for col in range(10):
    for row in range(10, 700):
        val = str(df.iloc[row, col]).strip() if pd.notna(df.iloc[row, col]) else ''
        if val == 'A005C':
            print(f"Found at row {row}, col {col}")
            # Show data for this row
            print(f"Row {row} data (cols 33-55):")
            for c in range(33, 56):
                header = df.iloc[5, c] if pd.notna(df.iloc[5, c]) else f"C{c}"
                value = df.iloc[row, c]
                if pd.notna(value):
                    print(f"  {header}: {value}")
            break
    else:
        continue
    break
