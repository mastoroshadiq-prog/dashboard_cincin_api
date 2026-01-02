
import pandas as pd
from pathlib import Path

path = Path('data/input/Realisasi vs Potensi PT SR.xlsx')
if not path.exists(): path = Path('../data/input/Realisasi vs Potensi PT SR.xlsx')

df = pd.read_excel(path, header=None)

# We know header is row 6
header_row = 6
data_start = 10  # Approximate

# Check header rows 3-9 for columns 105-116
print("--- HEADER INSPECTION (Cols 105-116) ---")
for r in range(3, 10):
    print(f"Row {r}: ", end="")
    for c in range(105, 116):
        val = df.iloc[r, c]
        if pd.notna(val):
            print(f"[{c}:{val}]", end=" ")
    print()

# Check data values for D004A (should be in data rows)
print("\n--- SAMPLE DATA VALUES (Cols 105-116) ---")
# Find D004A row
for r in range(10, min(50, len(df))):
    blok_val = str(df.iloc[r, 2]).strip().upper()
    if blok_val == 'D004A':
        print(f"Block D004A (Row {r}):")
        for c in range(105, 116):
            val = df.iloc[r, c]
            print(f"  Col {c}: {val}")
        break
