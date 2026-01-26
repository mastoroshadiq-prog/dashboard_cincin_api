"""
Extract ALL AME Divisions Census Data
Target: 100-200 blocks across 5 divisions
Focus: Ganoderma Stadium, Production, Yield, Sisipan, Pokok Utama
"""

import pandas as pd
import json
from collections import defaultdict

# Read Excel
print("Loading data_gabungan.xlsx...")
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Division configuration
DIVISIONS = {
    'AME_I': {'ndre': False, 'tier': 'TIER_2'},
    'AME_II': {'ndre': True, 'tier': 'TIER_1'},
    'AME_III': {'ndre': False, 'tier': 'TIER_2'},
    'AME_IV': {'ndre': True, 'tier': 'TIER_1'},
    'AME_V': {'ndre': False, 'tier': 'TIER_2'},
}

# Production columns (from previous investigation)
YEAR_COLS = {
    2023: {'real_ton': 152, 'poten_ton': 155},
    2024: {'real_ton': 161, 'poten_ton': 164},
    2025: {'real_ton': 170, 'poten_ton': 173},
}

# Stadium columns (need to identify - placeholder)
# Sisipan, Pokok columns (need to identify - placeholder)

estate_data = {
    'metadata': {
        'extraction_date': '2026-01-15',
        'source': 'data_gabungan.xlsx',
        'divisions': DIVISIONS
    },
    'divisions': {}
}

print("\n" + "="*80)
print("EXTRACTING ALL DIVISION DATA")
print("="*80)

# Get all unique block codes
all_blocks = df[df[0].notna()][0].unique()
print(f"Total unique entries found: {len(all_blocks)}")

# Filter for block codes (pattern: starts with letter, contains numbers)
import re
block_pattern = re.compile(r'^[A-Z]\d{3}[A-Z]?$')
blocks = [b for b in all_blocks if isinstance(b, str) and block_pattern.match(b)]

print(f"Total block codes identified: {len(blocks)}")

# Process each block
for block_code in blocks:
    block_rows = df[df[0] == block_code]
    
    if len(block_rows) == 0:
        continue
    
    row_idx = block_rows.index[0]
    
    # Extract basic info
    year_planted = df.iloc[row_idx, 1]
    luas_ha = df.iloc[row_idx, 11]
    
    # Try to determine division from block code or other columns
    # For now, using pattern matching
    division = None
    if block_code.startswith('D'):
        # AME II division pattern (based on existing data)
        division = 'AME_II'
    elif block_code.startswith('E'):
        # AME II division pattern (based on existing data)
        division = 'AME_II'
    elif block_code.startswith('F'):
        # AME II division pattern (based on existing data)
        division = 'AME_II'
    # TODO: Add logic for other divisions (need column mapping)
    
    if not division:
        continue  # Skip blocks we can't assign to a division yet
    
    # Extract yield data for each year
    yields = {}
    for year, cols in YEAR_COLS.items():
        real_ton_total = df.iloc[row_idx, cols['real_ton']]
        poten_ton_total = df.iloc[row_idx, cols['poten_ton']]
        
        if pd.notna(real_ton_total) and pd.notna(luas_ha) and luas_ha > 0:
            real_ton_ha = round(float(real_ton_total) / float(luas_ha), 2)
            poten_ton_ha = round(float(poten_ton_total) / float(luas_ha), 2) if pd.notna(poten_ton_total) else 0
            gap_ton_ha = round(poten_ton_ha - real_ton_ha, 2)
            gap_pct = round((gap_ton_ha / poten_ton_ha) * 100, 1) if poten_ton_ha > 0 else 0
            
            yields[year] = {
                'real_ton_total': float(real_ton_total),
                'poten_ton_total': float(poten_ton_total) if pd.notna(poten_ton_total) else None,
                'real_ton_ha': real_ton_ha,
                'poten_ton_ha': poten_ton_ha,
                'gap_ton_ha': gap_ton_ha,
                'gap_pct': gap_pct
            }
    
    # Create block entry
    block_data = {
        'block_code': block_code,
        'division': division,
        'tier': DIVISIONS[division]['tier'],
        'ndre_available': DIVISIONS[division]['ndre'],
        'year_planted': int(year_planted) if pd.notna(year_planted) else None,
        'luas_ha': float(luas_ha) if pd.notna(luas_ha) else None,
        'yields': yields,
        # TODO: Add when column mappings identified
        'ganoderma_stadium': None,  # 1-4 scale
        'sisipan_count': None,
        'pokok_utama_count': None,
    }
    
    # Add to division
    if division not in estate_data['divisions']:
        estate_data['divisions'][division] = {
            'division_code': division,
            'tier': DIVISIONS[division]['tier'],
            'ndre_available': DIVISIONS[division]['ndre'],
            'blocks': []
        }
    
    estate_data['divisions'][division]['blocks'].append(block_data)

# Calculate division aggregates
print("\n" + "="*80)
print("DIVISION SUMMARY")
print("="*80)

for div_code, div_data in estate_data['divisions'].items():
    blocks = div_data['blocks']
    
    if not blocks:
        continue
    
    total_area = sum(b['luas_ha'] for b in blocks if b['luas_ha'])
    block_count = len(blocks)
    
    # Calculate avg yield 2025
    yields_2025 = [b['yields'].get(2025, {}).get('real_ton_ha') for b in blocks if b.get('yields', {}).get(2025)]
    avg_yield_2025 = sum(yields_2025) / len(yields_2025) if yields_2025 else 0
    
    print(f"\n{div_code} ({div_data['tier']}):")
    print(f"  Blocks: {block_count}")
    print(f"  Total Area: {total_area:.1f} Ha")
    print(f"  Avg Yield 2025: {avg_yield_2025:.2f} Ton/Ha")
    print(f"  NDRE: {'✅ Available' if div_data['ndre_available'] else '❌ Not Available'}")
    
    # Add summary to division
    div_data['summary'] = {
        'total_area_ha': total_area,
        'block_count': block_count,
        'avg_yield_2025': round(avg_yield_2025, 2),
    }

# Save to JSON
output_file = 'data/output/estate_census_complete.json'
with open(output_file, 'w') as f:
    json.dump(estate_data, f, indent=2)

print("\n" + "="*80)
print(f"✅ SAVED TO: {output_file}")
print("="*80)

# Summary stats
total_blocks = sum(len(d['blocks']) for d in estate_data['divisions'].values())
total_area = sum(d['summary']['total_area_ha'] for d in estate_data['divisions'].values())

print(f"\nESTATE TOTALS:")
print(f"  Total Divisions: {len(estate_data['divisions'])}")
print(f"  Total Blocks: {total_blocks}")
print(f"  Total Area: {total_area:.1f} Ha")
print("\nNOTE: Ganoderma Stadium, Sisipan, Pokok Utama columns need to be identified!")
print("      Currently set to NULL - will update once column mappings confirmed.")
