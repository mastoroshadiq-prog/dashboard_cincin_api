"""
STEP 1: Calculate AME II Division Aggregates
Extract all blocks and calculate division-level metrics
"""

import json
from statistics import mean

# Load data
with open('data/output/estate_census_complete.json', 'r') as f:
    data = json.load(f)

ame_ii = data['divisions']['AME_II']
blocks = ame_ii['blocks']

print("="*70)
print("STEP 1: AME II DIVISION EXTRACTION")
print("="*70)

print(f"\n📊 Total Blocks Found: {len(blocks)}")
print(f"Division: {ame_ii['division_code']}")
print(f"Tier: {ame_ii['tier']}")
print(f"NDRE Available: {ame_ii['ndre_available']}")

# Calculate aggregates
total_area = sum(b['luas_ha'] for b in blocks if b['luas_ha'])
block_count = len(blocks)

# Get 2025 yields (NOTE: years are stored as strings in JSON)
yields_2025 = []
for b in blocks:
    if b.get('yields', {}).get('2025'):  # Use string key!
        y = b['yields']['2025']
        yields_2025.append({
            'block': b['block_code'],
            'area': b['luas_ha'],
            'real_ton_ha': y['real_ton_ha'],
            'poten_ton_ha': y['poten_ton_ha'],
            'gap_ton_ha': y['gap_ton_ha'],
            'gap_pct': y['gap_pct']
        })

# Weighted averages (by area)
total_weighted_real = sum(y['real_ton_ha'] * y['area'] for y in yields_2025)
total_weighted_poten = sum(y['poten_ton_ha'] * y['area'] for y in yields_2025)
total_weighted_gap = sum(y['gap_ton_ha'] * y['area'] for y in yields_2025)

avg_real_ton_ha = total_weighted_real / total_area
avg_poten_ton_ha = total_weighted_poten / total_area
avg_gap_ton_ha = total_weighted_gap / total_area
avg_gap_pct = (avg_gap_ton_ha / avg_poten_ton_ha) * 100 if avg_poten_ton_ha > 0 else 0

# Total production gaps
total_gap_tons = total_weighted_gap

print(f"\n📍 DIVISION METRICS (2025):")
print(f"  Total Area: {total_area:.1f} Ha")
print(f"  Avg Realisasi: {avg_real_ton_ha:.2f} Ton/Ha")
print(f"  Avg Potensi: {avg_poten_ton_ha:.2f} Ton/Ha")
print(f"  Avg Gap: {avg_gap_ton_ha:.2f} Ton/Ha ({avg_gap_pct:.1f}%)")
print(f"  Total Gap: {total_gap_tons:.0f} Tons")

# Estimate critical blocks (assuming gap > 25% = critical)
critical_blocks = [y for y in yields_2025 if abs(y['gap_pct']) > 25]
print(f"\n⚠️ CRITICAL BLOCKS (Gap > 25%): {len(critical_blocks)}/{len(yields_2025)}")

# Sort by gap to find top 8 critical
sorted_by_gap = sorted(yields_2025, key=lambda x: abs(x['gap_pct']), reverse=True)
top_8_critical = sorted_by_gap[:8]

print(f"\n🔴 TOP 8 CRITICAL BLOCKS:")
for i, b in enumerate(top_8_critical, 1):
    print(f"  {i}. {b['block']}: Gap {b['gap_pct']:.1f}% ({b['gap_ton_ha']:.2f} Ton/Ha)")

# Safety check
if len(yields_2025) == 0:
    print("\n❌ ERROR: No blocks have 2025 yield data!")
    print("   Checking what data is available...")
    for b in blocks[:5]:
        print(f"   Block {b['block_code']}: yields keys = {list(b.get('yields', {}).keys())}")
    exit(1)

division_summary = {
    'division_code': 'AME_II',
    'total_blocks': block_count,
    'total_area_ha': round(total_area, 1),
    'avg_yield_2025': {
        'real_ton_ha': round(avg_real_ton_ha, 2),
        'poten_ton_ha': round(avg_poten_ton_ha, 2),
        'gap_ton_ha': round(avg_gap_ton_ha, 2),
        'gap_pct': round(avg_gap_pct, 1)
    },
    'total_gap_tons': round(total_gap_tons, 0),
    'critical_blocks_count': len(critical_blocks),
    'critical_blocks_pct': round(len(critical_blocks)/len(yields_2025)*100, 1) if len(yields_2025) > 0 else 0,
    'top_8_critical': [b['block'] for b in top_8_critical]
}

# Save summary
output_file = 'data/output/ame_ii_division_summary.json'
with open(output_file, 'w') as f:
    json.dump(division_summary, f, indent=2)

print(f"\n✅ SAVED: {output_file}")
print("="*70)
print("STEP 1 COMPLETE!")
print("="*70)
