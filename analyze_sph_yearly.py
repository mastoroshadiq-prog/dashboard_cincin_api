"""
Extract yearly production/trees data to calculate SPH trend
Year groupings:
- 2023: starts at col 150
- 2024: starts at col 159
- 2025: starts at col 168
"""
import pandas as pd
import json

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*70)
print("ANALYZING YEARLY DATA STRUCTURE FOR SPH CALCULATION")
print("="*70)

# Show structure for 2023, 2024, 2025 sections
year_starts = {2023: 150, 2024: 159, 2025: 168}

for year, start_col in year_starts.items():
    print(f"\n=== Year {year} (cols {start_col}-{start_col+8}) ===")
    for col in range(start_col, min(start_col + 9, df.shape[1])):
        header_parts = []
        for row in range(6):
            val = df.iloc[row, col]
            if pd.notna(val):
                header_parts.append(f"R{row}:{str(val)[:15]}")
        print(f"  Col {col}: {header_parts}")

# Now check if we have Pokok (trees) data per year
print("\n\n" + "="*70)
print("EXTRACTING POKOK (TREES) DATA PER YEAR")
print("="*70)

# Based on structure, look for production/trees columns in each year section
# First, let's sample some blocks to understand the data

# Get block codes (col 0) and Luas Ha (assumed col 2 or need to find)
luas_col = None
for col in range(10):
    for row in range(8):
        val = str(df.iloc[row, col]).lower() if pd.notna(df.iloc[row, col]) else ''
        if 'ha' in val or 'luas' in val:
            luas_col = col
            print(f"Found Luas Ha at col {col}")
            break

# Sample rows
print("\nSampling data for blocks A001A, D001A:")
for row in range(10, min(50, len(df))):
    block = str(df.iloc[row, 0]).strip() if pd.notna(df.iloc[row, 0]) else ''
    if block in ['A001A', 'D001A']:
        print(f"\n{block} (row {row}):")
        # Show current SPH (col 33 or 68)
        sph_current = df.iloc[row, 33]
        sph_alt = df.iloc[row, 68]
        pokok = df.iloc[row, 66]
        print(f"  Current SPH (col 33): {sph_current}")
        print(f"  SPH alt (col 68): {sph_alt}")
        print(f"  Pokok (col 66): {pokok}")
        
        # Show data for 2023, 2024, 2025
        for year, start in year_starts.items():
            vals = []
            for col in range(start, min(start + 9, df.shape[1])):
                v = df.iloc[row, col]
                if pd.notna(v) and v != 0:
                    vals.append(f"C{col}:{v}")
            if vals:
                print(f"  {year}: {vals}")

# Check if there's declining trees (Pokok) data per year
print("\n\n" + "="*70)
print("CHECKING IF SPH CAN BE CALCULATED FROM YEARLY DATA")
print("="*70)

# SPH = Pokok / Ha
# If we have Pokok per year, we can calculate SPH per year
# Or if we have infected trees per year, SPH would decline

# Check if TANAM/SISIP data helps track tree count changes
print("\nTree population changes via TANAM/SISIP:")
print("We have TANAM/SISIP data for 2020-2025 at cols 34-52")
print("This adds trees, not removes them")

# Check if infection rate changes over years could estimate SPH decline
print("\nInfection data could help estimate SPH decline if available per year")
print("Stadium data at col 55-58 appears to be current snapshot, not yearly")

# Conclusion
print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
Based on analysis:
1. SPH data exists only for CURRENT state (col 33 and 68) - same values
2. No historical SPH data (2023, 2024) in spreadsheet
3. Production data exists per year (col 150+ for 2023, 159+ for 2024, 168+ for 2025)
4. Could potentially ESTIMATE SPH change based on:
   - Initial SPH - cumulative infection losses
   - Or using TANAM/SISIP to adjust tree counts

OPTIONS:
A) Only show current SPH (no trend) - accurate but limited
B) Estimate SPH trend from infection data (less accurate)
C) Add second Y-axis for current SPH as reference line only
""")
