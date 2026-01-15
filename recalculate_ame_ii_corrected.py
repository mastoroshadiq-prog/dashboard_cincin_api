"""
Recalculate AME II (AME02) with CORRECT data
"""
import json

data = json.load(open('data/output/estate_census_complete_CORRECTED.json'))
ame2 = data['divisions']['AME02']
blocks = ame2['blocks']

total_area = sum(b['luas_ha'] for b in blocks if b['luas_ha'])
block_count = len(blocks)

# Get 2025 yields
yields_2025 = []
for b in blocks:
    if '2025' in b.get('yields', {}):
        y = b['yields']['2025']
        yields_2025.append({
            'block': b['block_code'],
            'area': b['luas_ha'],
            'real_ton_ha': y['real_ton_ha'],
            'poten_ton_ha': y['poten_ton_ha'],
            'gap_ton_ha': y['gap_ton_ha'],
            'gap_pct': y['gap_pct']
        })

# Weighted averages
total_weighted_real = sum(y['real_ton_ha'] * y['area'] for y in yields_2025 if y['area'])
total_weighted_poten = sum(y['poten_ton_ha'] * y['area'] for y in yields_2025 if y['area'])
total_weighted_gap = sum(y['gap_ton_ha'] * y['area'] for y in yields_2025 if y['area'])

avg_real_ton_ha = total_weighted_real / total_area if total_area > 0 else 0
avg_poten_ton_ha = total_weighted_poten / total_area if total_area > 0 else 0
avg_gap_ton_ha = total_weighted_gap / total_area if total_area > 0 else 0
avg_gap_pct = (avg_gap_ton_ha / avg_poten_ton_ha) * 100 if avg_poten_ton_ha > 0 else 0

# Critical blocks
critical = [y for y in yields_2025 if abs(y['gap_pct']) > 25]

# Sort by gap
sorted_blocks = sorted(yields_2025, key=lambda x: abs(x['gap_pct']), reverse=True)
top_8 = sorted_blocks[:8]

print("="*70)
print("AME II (AME02) - CORRECTED SUMMARY")
print("="*70)
print(f"\nTotal Blocks: {block_count}")
print(f"Total Area: {total_area:.1f} Ha")
print(f"\nAVG YIELD 2025:")
print(f"  Realisasi: {avg_real_ton_ha:.2f} Ton/Ha")
print(f"  Potensi: {avg_poten_ton_ha:.2f} Ton/Ha")
print(f"  Gap: {avg_gap_ton_ha:.2f} Ton/Ha ({avg_gap_pct:.1f}%)")
print(f"  Total Gap: {total_weighted_gap:.0f} Tons")
print(f"\nCritical (Gap>25%): {len(critical)}/{len(yields_2025)} ({len(critical)/len(yields_2025)*100:.1f}%)")
print(f"\nTOP 8 CRITICAL:")
for i, b in enumerate(top_8, 1):
    print(f"  {i}. {b['block']}: {b['gap_pct']:.1f}%")

# Save corrected summary
summary = {
    'division_code': 'AME02',
    'total_blocks': block_count,
    'total_area_ha': round(total_area, 1),
    'avg_yield_2025': {
        'real_ton_ha': round(avg_real_ton_ha, 2),
        'poten_ton_ha': round(avg_poten_ton_ha, 2),
        'gap_ton_ha': round(avg_gap_ton_ha, 2),
        'gap_pct': round(avg_gap_pct, 1)
    },
    'total_gap_tons': round(total_weighted_gap, 0),
    'critical_blocks_count': len(critical),
    'critical_blocks_pct': round(len(critical)/len(yields_2025)*100, 1) if len(yields_2025) > 0 else 0,
    'top_8_critical': [b['block'] for b in top_8]
}

with open('data/output/ame_ii_division_summary_CORRECTED.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n✅ SAVED: ame_ii_division_summary_CORRECTED.json")
print("="*70)
