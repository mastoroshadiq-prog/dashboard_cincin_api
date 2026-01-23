"""
Check if data_gabungan.xlsx has SPH trend data for 2023-2025
"""
import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*70)
print("SEARCHING FOR SPH COLUMNS IN DATA_GABUNGAN.XLSX")
print("="*70)

# Search for SPH columns
print("\nSearching for 'SPH' in headers (rows 0-7):")
sph_cols = []
for col in range(df.shape[1]):
    for row in range(8):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'SPH' in val.upper():
            sph_cols.append(col)
            # Get year context
            year_info = []
            for r in range(8):
                v = df.iloc[r, col]
                if pd.notna(v):
                    year_info.append(f"R{r}:{v}")
            print(f"  Col {col}: {year_info}")

# Show header structure around potential SPH columns
print("\n\nHeader structure for cols 30-45 (looking for yearly SPH):")
for col in range(30, min(45, df.shape[1])):
    header_parts = []
    for row in range(8):
        val = df.iloc[row, col]
        if pd.notna(val):
            header_parts.append(f"R{row}:{str(val)[:15]}")
    if header_parts:
        print(f"Col {col}: {header_parts}")

# Check around col 33 where we found SPH before
print("\n\nContext around col 33 (known SPH location):")
for col in range(31, 36):
    header_parts = []
    for row in range(8):
        val = df.iloc[row, col]
        if pd.notna(val):
            header_parts.append(f"R{row}:{str(val)[:15]}")
    print(f"Col {col}: {header_parts}")

# Also check later columns for more years
print("\n\nLooking for yearly SPH in cols 60-80:")
for col in range(60, min(85, df.shape[1])):
    for row in range(8):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'SPH' in val.upper():
            header_parts = []
            for r in range(8):
                v = df.iloc[r, col]
                if pd.notna(v):
                    header_parts.append(f"R{r}:{str(v)[:15]}")
            print(f"  Col {col}: {header_parts}")
