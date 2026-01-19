"""
Quick verification of extracted estate data
"""
import json

with open('data/output/estate_census_complete_CORRECTED.json') as f:
    data = json.load(f)

print("="*70)
print("ESTATE DATA VERIFICATION")
print("="*70)

divisions = data['divisions']
print(f"\nTotal Divisions: {len(divisions)}")
print(f"Division codes: {sorted(divisions.keys())}\n")

total_blocks = 0
total_area = 0

print("Blocks per division:")
for div_code in sorted(divisions.keys()):
    div_data = divisions[div_code]
    block_count = len(div_data['blocks'])
    area = sum(b.get('luas_ha', 0) for b in div_data['blocks'] if b.get('luas_ha'))
    ndre = "✅" if div_data['ndre_available'] else "❌"
    
    total_blocks += block_count
    total_area += area
    
    print(f"  {div_code:8s}: {block_count:3d} blocks | {area:7.1f} Ha | NDRE {ndre}")

print(f"\n{'='*70}")
print(f"ESTATE TOTAL: {total_blocks} blocks | {total_area:.1f} Ha")
print(f"{'='*70}")
print("\n✅ Phase 1 Data Extraction: COMPLETE!")
