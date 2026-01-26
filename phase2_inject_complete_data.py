"""
PHASE 2: Make Division Selector Functional
Load all estate data and enable dynamic filtering
"""

import json

# Read dashboard HTML
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Load estate data
with open('data/output/estate_census_complete_CORRECTED.json', 'r') as f:
    estate_data = json.load(f)

# Find where to insert the complete BLOCKS_DATA
# Look for existing BLOCKS_DATA or HISTORICAL_YIELDS section
marker = '// ====== DATA ======'

if marker not in content:
    print("❌ Data section marker not found!")
    exit(1)

# Build complete BLOCKS_DATA from all divisions
all_blocks_data = {}

for div_code, div_info in estate_data['divisions'].items():
    for block in div_info['blocks']:
        block_code = block['block_code']
        
        # Get 2025 yield data
        yield_2025 = block.get('yields', {}).get('2025', {})
        
        all_blocks_data[block_code] = {
            'block_code': block_code,
            'division': div_code,
            'tier': block['tier'],
            'ndre_available': block['ndre_available'],
            'luas_ha': block.get('luas_ha', 0),
            'realisasi_ton_ha': yield_2025.get('real_ton_ha', 0),
            'potensi_ton_ha': yield_2025.get('poten_ton_ha', 0),
            'gap_ton_ha': yield_2025.get('gap_ton_ha', 0),
            'gap_pct': yield_2025.get('gap_pct', 0),
        }

# Create JavaScript code for complete BLOCKS_DATA
blocks_data_js = f"""
    // ====== COMPLETE ESTATE DATA ======
    // Generated from estate_census_complete_CORRECTED.json
    // Total: {len(all_blocks_data)} blocks across 14 divisions
    
    const COMPLETE_BLOCKS_DATA = {json.dumps(all_blocks_data, indent=8)};
    
    // Division metadata
    const DIVISIONS_META = {json.dumps({
        div: {
            'code': div,
            'blocks': len(info['blocks']),
            'area': round(sum(b.get('luas_ha', 0) or 0 for b in info['blocks']), 1),
            'ndre': info['ndre_available'],
            'tier': info['tier']
        }
        for div, info in estate_data['divisions'].items()
    }, indent=8)};
"""

# Find location to insert (after existing data declarations)
insert_point = content.find('const HISTORICAL_YIELDS = {')
if insert_point == -1:
    insert_point = content.find('// ====== DATA ======')
    
if insert_point > 0:
    # Insert before HISTORICAL_YIELDS or at data section
    content = content[:insert_point] + blocks_data_js + '\n    ' + content[insert_point:]
    
    # Save
    with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("="*70)
    print("✅ COMPLETE BLOCKS DATA INJECTED!")
    print("="*70)
    print(f"Total blocks: {len(all_blocks_data)}")
    print(f"Divisions: {len(estate_data['divisions'])}")
    print("\nNext: Implement filter function to use this data")
else:
    print("❌ Could not find insertion point!")
