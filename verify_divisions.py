"""
URGENT: Check actual division assignments in Excel
"""

import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Column 0 = Block code
# Column 5 = Division (based on header row 3)

# Get all rows with block codes
blocks_with_div = []
for idx in df.index:
    block_code = df.iloc[idx, 0]
    division = df.iloc[idx, 5]
    if pd.notna(block_code) and isinstance(block_code, str) and len(block_code) > 0:
        # Filter out header rows
        if block_code not in ['BLOK', 'Blok', 'NaN']:
            blocks_with_div.append({
                'block': block_code,
                'division': division
            })

print("="*70)
print("DIVISION VERIFICATION")
print("="*70)

# Count by division
from collections import Counter
div_counts = Counter(b['division'] for b in blocks_with_div)

print(f"\nTotal blocks found: {len(blocks_with_div)}")
print(f"\nBlocks per division:")
for div, count in sorted(div_counts.items()):
    print(f"  {div}: {count} blocks")

# Show AME II specifically
ame_ii_blocks = [b for b in blocks_with_div if b['division'] == 'AME II']
print(f"\n🔍 AME II BLOCKS: {len(ame_ii_blocks)}")
print("First 20 AME II blocks:")
for b in ame_ii_blocks[:20]:
    print(f"  {b['block']}")

print("\n" + "="*70)
