import pandas as pd
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Find years in header rows
print("Looking for year info in header rows 1-4:")
for col in range(33, 60):
    for row in range(5):
        val = df.iloc[row, col]
        if pd.notna(val):
            val_str = str(val)
            if any(str(y) in val_str for y in range(2018, 2026)):
                print(f"Row {row}, Col {col}: {val}")

# Show header structure more clearly
print("\n\nDetailed header for cols 40-55:")
for col in range(40, 56):
    header_parts = []
    for row in range(6):
        val = df.iloc[row, col]
        if pd.notna(val):
            header_parts.append(f"R{row}:{str(val)[:20]}")
    print(f"Col {col}: {header_parts}")

# Check TT SISIP column (col 65)
print("\n\nTT SISIP column (col 65) - should have year of sisipan:")
print(f"Header: {df.iloc[3, 65]}")
print("Sample values:")
for row in [26, 27, 28, 29, 30]:  # Around A005C row
    val = df.iloc[row, 65]
    block = df.iloc[row, 0] if pd.notna(df.iloc[row, 0]) else ''
    print(f"  Row {row} ({block}): TT SISIP = {val}")
