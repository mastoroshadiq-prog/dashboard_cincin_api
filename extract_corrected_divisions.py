"""
FIX: Re-extract with CORRECT division assignments
Use column 5 (DIVISI) from Excel
"""

import pandas as pd
import json

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Column mappings (from previous investigation)
COL_BLOCK = 0
COL_DIV = 5
COL_AREA = 11

YEAR_COLS = {
    '2023': {'real_ton': 152, 'poten_ton': 155},
    '2024': {'real_ton': 161, 'poten_ton': 164},
    '2025': {'real_ton': 170, 'poten_ton': 173},
}

# Extract all blocks with correct divisions
estate_data = {
    'metadata': {
        'extraction_date': '2026-01-15',
        'source': 'data_gabungan.xlsx - CORRECTED',
    },
    'divisions': {}
}

print("="*70)
print("CORRECTED EXTRACTION - Using actual Excel division column")
print("="*70)

for idx in df.index:
    block_code = df.iloc[idx, COL_BLOCK]
    division = df.iloc[idx, COL_DIV]
    
    if pd.notna(block_code) and isinstance(block_code, str):
        if block_code in ['BLOK', 'Blok']:  # Skip headers
            continue
            
        luas_ha = df.iloc[idx, COL_AREA]
        
        # Convert area to float safely
        try:
            luas_ha_val = float(luas_ha) if pd.notna(luas_ha) else 0
        except (ValueError, TypeError):
            luas_ha_val = 0
        
        # Extract yields
        yields = {}
        for year, cols in YEAR_COLS.items():
            real_ton = df.iloc[idx, cols['real_ton']]
            poten_ton = df.iloc[idx, cols['poten_ton']]
            
            if pd.notna(real_ton) and luas_ha_val > 0:
                real_ton_ha = round(float(real_ton) / luas_ha_val, 2)
                poten_ton_ha = round(float(poten_ton) / luas_ha_val, 2) if pd.notna(poten_ton) else 0
                gap_ton_ha = round(poten_ton_ha - real_ton_ha, 2)
                gap_pct = round((gap_ton_ha / poten_ton_ha) * 100, 1) if poten_ton_ha > 0 else 0
                
                yields[year] = {
                    'real_ton_ha': real_ton_ha,
                    'poten_ton_ha': poten_ton_ha,
                    'gap_ton_ha': gap_ton_ha,
                    'gap_pct': gap_pct
                }
        
        # Determine tier (AME01-04 have NDRE)
        tier = 'TIER_1' if division in ['AME02', 'AME04'] else 'TIER_2'
        ndre = division in ['AME02', 'AME04']
        
        # Create block entry
        block_data = {
            'block_code': block_code,
            'division': division,
            'tier': tier,
            'ndre_available': ndre,
            'luas_ha': luas_ha_val if luas_ha_val > 0 else None,
            'yields': yields
        }
        
        # Add to correct division
        if division not in estate_data['divisions']:
            estate_data['divisions'][division] = {
                'division_code': division,
                'tier': tier,
                'ndre_available': ndre,
                'blocks': []
            }
        
        estate_data['divisions'][division]['blocks'].append(block_data)

# Print summary
print("\n📊 EXTRACTION SUMMARY:")
for div_code, div_data in sorted(estate_data['divisions'].items()):
    block_count = len(div_data['blocks'])
    area = sum(b['luas_ha'] for b in div_data['blocks'] if b['luas_ha'])
    print(f"  {div_code}: {block_count} blocks, {area:.1f} Ha, NDRE={div_data['ndre_available']}")

# Save
output_file = 'data/output/estate_census_complete_CORRECTED.json'
with open(output_file, 'w') as f:
    json.dump(estate_data, f, indent=2)

print(f"\n✅ SAVED: {output_file}")
print("="*70)
