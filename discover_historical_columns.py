"""
PHASE 1: DISCOVER HISTORICAL PRODUCTION DATA
Goal: Find 2023, 2024, 2025 production columns in Excel
"""

import pandas as pd
import numpy as np

INPUT_FILE = "poac_sim/data/input/data_gabungan.xlsx"

print("="*80)
print("HISTORICAL DATA DISCOVERY - PRODUCTION COLUMNS")
print("="*80)

# Load with proper header handling
df = pd.read_excel(INPUT_FILE)

print(f"\nTotal Rows: {len(df)}")
print(f"Total Columns: {len(df.columns)}")

# Filter AME02 for inspection
divisi_col = df.columns[5]
ame02_data = df[df[divisi_col] == 'AME02'].copy()

if len(ame02_data) > 0:
    print(f"\nAME02 Blocks: {len(ame02_data)}")
    
    # Get a sample block to check values
    sample_block = ame02_data.iloc[0]
    
    print("\n" + "="*80)
    print("SEARCHING FOR PRODUCTION PATTERNS")
    print("="*80)
    
    # Strategy: Look for numeric columns with production-like values
    # We know 2025 Real is around 14,490 Ton for AME02 total
    # Per block average: ~391 Ton
    
    # Known 2025 indices
    known_2025_real = 170
    known_2025_pot = 173
    
    print(f"\nKnown 2025 Real Index: {known_2025_real}")
    print(f"2025 Real Sample Value: {sample_block.iloc[known_2025_real]}")
    
    # Check pattern: production columns might be spaced regularly
    # Common patterns: every 3 columns (Real, Pot, Gap) or similar
    
    potential_production_cols = []
    
    print("\n" + "="*80)
    print("SCANNING FOR SIMILAR PATTERNS (100-177)")
    print("="*80)
    
    for idx in range(100, len(df.columns)):
        val = sample_block.iloc[idx]
        
        # Look for numeric values in typical production range (50-600 Ton per block)
        if pd.notna(val) and isinstance(val, (int, float)) and 50 < val < 800:
            # Check if column has enough non-null values (should be production data)
            non_null_count = ame02_data.iloc[:, idx].notna().sum()
            if non_null_count > 30:  # Most blocks should have data
                potential_production_cols.append({
                    'index': idx,
                    'sample_value': val,
                    'non_null_count': non_null_count,
                    'column_name': df.columns[idx]
                })
    
    print(f"\nFound {len(potential_production_cols)} potential production columns:")
    print(f"{'Index':<8} {'Sample Val':<12} {'Non-Null':<10} {'Column Name':<20}")
    print("-"*80)
    
    for col in potential_production_cols:
        print(f"{col['index']:<8} {col['sample_value']:<12.2f} {col['non_null_count']:<10} {str(col['column_name'])[:20]}")
    
    # Now check totals to identify years
    print("\n" + "="*80)
    print("CHECKING DIVISION TOTALS TO IDENTIFY YEARS")
    print("="*80)
    
    # We know AME02 2025 total real = 14,490 Ton
    expected_2025_total = 14490
    
    for col_info in potential_production_cols:
        idx = col_info['index']
        total = ame02_data.iloc[:, idx].sum()
        
        # Check if close to known 2025 value or other years
        print(f"Index {idx:3d}: Total = {total:>10,.2f} Ton", end="")
        
        # Identify likely year based on total
        if abs(total - expected_2025_total) < 500:
            print(" ← LIKELY 2025 REAL")
        elif 13000 < total < 14000:
            print(" ← Possible 2024")
        elif 12000 < total < 13000:
            print(" ← Possible 2023")
        elif 15000 < total < 17000:
            print(" ← Possible POTENSI (any year)")
        else:
            print()
    
    # Check spacing pattern
    print("\n" + "="*80)
    print("CHECKING COLUMN SPACING PATTERN")
    print("="*80)
    print("If data is organized by year, columns should be spaced regularly")
    print(f"Known 2025 Real: {known_2025_real}, Pot: {known_2025_pot} (spacing: 3)")
    print("\nLet's check backwards with spacing of 3:")
    
    # Hypothesis: spacing of 3 columns per metric set
    for year_offset in [1, 2]:  # 1 year back, 2 years back
        estimated_idx = known_2025_real - (year_offset * 3)
        if estimated_idx >= 0:
            sample_val = sample_block.iloc[estimated_idx]
            total_val = ame02_data.iloc[:, estimated_idx].sum()
            year = 2025 - year_offset
            print(f"\nYear {year} (estimated idx {estimated_idx}):")
            print(f"  Sample value: {sample_val}")
            print(f"  Division total: {total_val:,.2f} Ton")
    
    print("\n" + "="*80)
    print("ALTERNATIVE: TRY LARGER SPACING")
    print("="*80)
    print("Data might be in blocks (e.g., all metrics per year together)")
    
    # Try spacing of 30-40 columns (typical for full metric sets)
    for spacing in [30, 40, 50]:
        print(f"\nTrying spacing of {spacing} columns:")
        for year_offset in [1, 2]:
            estimated_idx = known_2025_real - (year_offset * spacing)
            if 0 <= estimated_idx < len(df.columns):
                total_val = ame02_data.iloc[:, estimated_idx].sum()
                year = 2025 - year_offset
                print(f"  Year {year} (idx {estimated_idx}): {total_val:,.2f} Ton")

else:
    print("\n[ERROR] No AME02 data found!")

print("\n" + "="*80)
print("DISCOVERY COMPLETE")
print("="*80)
