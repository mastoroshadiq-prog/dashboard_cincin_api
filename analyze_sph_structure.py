"""
Deep dive into SPH data structure
Check if there's historical SPH data (2023, 2024, 2025) or just current snapshot
"""
import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*70)
print("ANALYZING SPH DATA STRUCTURE")
print("="*70)

# Show sample data for cols 30-75 where years are structured
print("\nLooking at header rows 3-5 for years + SPH pattern:")
for row in range(3, 6):
    vals = []
    for col in range(30, 75):
        v = df.iloc[row, col]
        if pd.notna(v):
            vals.append(f"C{col}:{str(v)[:10]}")
    print(f"Row {row}: {vals}")

# Check if there's any yearly SPH data
print("\n\nChecking for yearly data in POKOK/Real sections:")
# Years typically start around col 69+
for col in range(65, min(150, df.shape[1])):
    header_parts = []
    for row in range(5):
        val = df.iloc[row, col]
        if pd.notna(val):
            header_parts.append(f"R{row}:{str(val)[:12]}")
    if any('SPH' in str(p).upper() for p in header_parts) or any('POKOK' in str(p).upper() for p in header_parts):
        print(f"Col {col}: {header_parts}")

# Let's also check the structure by looking at year groupings
print("\n\nLooking for year groupings (2014-2025) in header:")
years_found = {}
for col in range(50, min(200, df.shape[1])):
    for row in range(5):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        for year in range(2014, 2026):
            if str(year) in val and col not in [c for cols in years_found.values() for c in cols]:
                if year not in years_found:
                    years_found[year] = []
                years_found[year].append(col)
                
for year in sorted(years_found.keys()):
    print(f"  Year {year}: cols {years_found[year]}")

# Check the Pokok column (total trees) for each year to calculate potential SPH
print("\n\nLooking for 'POKOK' (total trees) data:")
for col in range(60, min(200, df.shape[1])):
    for row in range(8):
        val = str(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else ''
        if 'POKOK' in val.upper():
            header = [str(df.iloc[r, col])[:15] for r in range(5) if pd.notna(df.iloc[r, col])]
            print(f"  Col {col}: {header}")
