import pandas as pd
import json

# Read Excel file
file_path = r'f:\PythonProjects\poac_cincin_api\poac_sim\data\input\data_gabungan.xlsx'

print("="*80)
print("EXTRACTING TBM BLOCKS (2023-2025)")
print("="*80)

# Read Excel, skip first 6 rows (headers)
df = pd.read_excel(file_path, header=None)

print(f"\nTotal rows: {len(df)}")

# Based on analysis:
# Col 0: Block Code (e.g., A005C)
# Col 1: Year (TT - Tahun Tanam)
# Col 3-6: Estate/Division codes
# Col 8: Block Code (repeating)

# Extract data starting from row 7 (actual data starts)
data_rows = []

for idx in range(7, len(df)):  # Start from row 7 (data rows)
    row = df.iloc[idx]
    
    block_code = row[8] if pd.notna(row[8]) else row[0]  # Col 8 or Col 0
    tahun_tanam = row[1] if pd.notna(row[1]) else row[9]  # Col 1 or Col 9
    estate = row[3] if pd.notna(row[3]) else None
    division = row[5] if pd.notna(row[5]) else None
    
    # Skip if no block code or year
    if pd.isna(block_code) or pd.isna(tahun_tanam):
        continue
    
    # Convert year to int
    try:
        year = int(tahun_tanam)
    except:
        continue
    
    data_rows.append({
        'block_code': str(block_code).strip(),
        'tahun_tanam': year,
        'estate': estate,
        'division': division,
        'row_index': idx
    })

print(f"\nTotal blocks extracted: {len(data_rows)}")

# Filter TBM blocks (2023-2025)
tbm_blocks = [b for b in data_rows if b['tahun_tanam'] >= 2023]

print(f"\n{'='*80}")
print(f"TBM BLOCKS FOUND (tahun_tanam >= 2023): {len(tbm_blocks)}")
print(f"{'='*80}\n")

# Group by division
by_division = {}
for block in tbm_blocks:
    div = block['division'] or 'Unknown'
    if div not in by_division:
        by_division[div] = []
    by_division[div].append(block)

# Print summary by division
print("SUMMARY BY DIVISION:")
print("-" * 80)
for div in sorted(by_division.keys()):
    blocks = by_division[div]
    print(f"\n{div}: {len(blocks)} TBM blocks")
    for b in blocks:
        print(f"  - {b['block_code']:<10} (Tahun: {b['tahun_tanam']}, Row: {b['row_index']})")

# Detailed list
print(f"\n{'='*80}")
print("DETAILED TBM BLOCKS LIST:")
print(f"{'='*80}\n")

# Sort by division and block code
tbm_sorted = sorted(tbm_blocks, key=lambda x: (x['division'] or '', x['block_code']))

print(f"{'No':<5} {'Block Code':<12} {'Year':<6} {'Estate':<8} {'Division':<12} {'Row':<6}")
print("-" * 80)

for idx, block in enumerate(tbm_sorted, 1):
    print(f"{idx:<5} {block['block_code']:<12} {block['tahun_tanam']:<6} "
          f"{block['estate'] or 'N/A':<8} {block['division'] or 'N/A':<12} {block['row_index']:<6}")

# Export to JSON
tbm_data = {
    'total_tbm_blocks': len(tbm_blocks),
    'by_division': {
        div: [
            {
                'block_code': b['block_code'],
                'tahun_tanam': b['tahun_tanam'],
                'estate': b['estate'],
                'row_index': b['row_index']
            }
            for b in blocks
        ]
        for div, blocks in by_division.items()
    },
    'all_blocks': [
        {
            'block_code': b['block_code'],
            'tahun_tanam': b['tahun_tanam'],
            'estate': b['estate'],
            'division': b['division'],
            'row_index': b['row_index']
        }
        for b in tbm_sorted
    ]
}

# Save to JSON
with open('tbm_blocks_data.json', 'w') as f:
    json.dump(tbm_data, f, indent=2)

print(f"\n{'='*80}")
print(f"Data exported to: tbm_blocks_data.json")
print(f"{'='*80}")

# Also check 2021-2022 (might still be immature)
recent_blocks = [b for b in data_rows if 2021 <= b['tahun_tanam'] <= 2022]
print(f"\n\nBONUS - BLOCKS PLANTED 2021-2022 (might still be immature): {len(recent_blocks)}")
if recent_blocks:
    print("\nThese blocks might still be in TBM phase (typically 3-4 years):")
    for b in recent_blocks[:10]:  # Show first 10
        print(f"  - {b['block_code']:<10} (Tahun: {b['tahun_tanam']})")
    if len(recent_blocks) > 10:
        print(f"  ... and {len(recent_blocks) - 10} more")

print("\n" + "="*80)
print("Analysis complete!")
print("="*80)
