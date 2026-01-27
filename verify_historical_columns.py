"""
PHASE 1B: VERIFY HISTORICAL COLUMNS
Based on discovery, verify and extract 2023-2025 data
"""

import pandas as pd
import json
from pathlib import Path

INPUT_FILE = "poac_sim/data/input/data_gabungan.xlsx"
OUTPUT_FILE = Path("poac_sim/data/output/historical_production_analysis.json")

print("="*80)
print("HISTORICAL PRODUCTION VERIFICATION (2023-2025)")
print("="*80)

df = pd.read_excel(INPUT_FILE)
divisi_col = df.columns[5]
ame02_data = df[df[divisi_col] == 'AME02'].copy()

print(f"\nAME02 Blocks: {len(ame02_data)}")

# Test indices based on pattern discovery
# Known: 2025 Real = 170, Pot = 173
# Hypothesis: Regular spacing

test_indices = {
    'index_101': 101,  # Discovered: 13,244 Ton - possible 2024
    'index_140': 140,  # Test: might be 2023  
    'index_170': 170,  # Known: 2025 Real
    'index_173': 173,  # Known: 2025 Pot
}

print("\n" + "="*80)
print("TESTING CANDIDATE INDICES")
print("="*80)

results = {}

for name, idx in test_indices.items():
    if idx < len(df.columns):
        total = ame02_data.iloc[:, idx].sum()
        non_null = ame02_data.iloc[:, idx].notna().sum()
        sample = ame02_data.iloc[0, idx]
        
        results[name] = {
            'index': idx,
            'total_ame02': float(total),
            'non_null_blocks': int(non_null),
            'sample_value': float(sample) if pd.notna(sample) else None
        }
        
        print(f"\n{name} (Index {idx}):")
        print(f"  Total AME02: {total:>10,.2f} Ton")
        print(f"  Non-null blocks: {non_null}/37")
        print(f"  Sample value: {sample}")

# Based on totals, try to identify years
print("\n" + "="*80)
print("YEAR IDENTIFICATION")
print("="*80)

# We know 2025 Real total = 14,490 Ton
# Look for decreasing pattern (production decline)

# Scan range 100-175 for Real columns
potential_years = []

for idx in range(100, 176, 10):  # Check every 10th column
    if idx < len(df.columns):
        total = ame02_data.iloc[:, idx].sum()
        non_null = ame02_data.iloc[:, idx].notna().sum()
        
        if non_null > 30 and 10000 < total < 20000:  # Production range
            potential_years.append({
                'index': int(idx),
                'total': float(total),
                'non_null': int(non_null)
            })

print(f"\nFound {len(potential_years)} potential production columns:")
print(f"{'Index':<8} {'Total (Ton)':<15} {'Non-Null':<10}")
print("-"*50)

for item in sorted(potential_years, key=lambda x: x['index']):
    print(f"{item['index']:<8} {item['total']:<15,.2f} {item['non_null']:<10}")

# Now test specific spacing hypothesis
print("\n" + "="*80)
print("TESTING SPACING PATTERNS FROM 2025")
print("="*80)

base_2025 = 170

# Try different spacings
for spacing in [3, 30, 35, 40]:
    print(f"\nSpacing: {spacing} columns")
    for year_back in [1, 2]:
        idx = base_2025 - (year_back * spacing)
        if 0 <= idx < len(df.columns):
            total = ame02_data.iloc[:, idx].sum()
            year = 2025 - year_back
            print(f"  {year} (idx {idx}): {total:,.2f} Ton")

# Save findings
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w') as f:
    json.dump({
        'test_results': results,
        'potential_columns': potential_years,
        'notes': 'Awaiting pattern confirmation'
    }, f, indent=2)

print(f"\n\nResults saved to: {OUTPUT_FILE}")
print("="*80)
