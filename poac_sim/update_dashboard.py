import json
import re

print('='*80)
print('🔄 UPDATING DASHBOARD: D006A/D007A → F008A/D001A')
print('='*80)

# Load dashboard data
with open('data/output/dashboard_data_f008a_d001a.json', 'r') as f:
    data = json.load(f)

# Load current dashboard
with open('data/output/dashboard_cincin_api_final.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('\n📝 Performing replacements...')

# 1. Replace block codes
replacements = [
    # Block names
    ('D006A', 'F008A'),
    ('D007A', 'D001A'),
    ('D 06', 'F 08'),
    ('D 07', 'D 01'),
    ('Blok D006A', 'Blok F008A'),
    ('Blok D007A', 'Blok D001A'),
    
    # Luas
    ('47.7', str(data['combined']['total_luas'])),
    ('23 Ha', f"{data['F008A']['luas']} Ha"),
    ('24.7 Ha', f"{data['D001A']['luas']} Ha"),
    
    # TT and Age
    ('TT 2009', f"TT {data['F008A']['tt']}"),
    ('Usia 16 Tahun', f"Usia {data['F008A']['age']} Tahun"),
    
    # Spread Ratio
    ('2.16x', f"{data['F008A']['spread_ratio']:.0f}x"),
    ('1.87x', f"{data['D001A']['spread_ratio']:.0f}x"),
    
    # Infection counts - F008A
    ('37 Inti', f"{data['F008A']['merah']} Inti"),
    ('80 Ring', f"{data['F008A']['oranye']} Ring"),
    ('80 Cincin Api', f"{data['F008A']['oranye']} Cincin Api"),
    
    # Infection counts - D001A
    ('57 Inti', f"{data['D001A']['merah']} Inti"),
    ('107 Ring', f"{data['D001A']['oranye']} Ring"),
    ('107 Cincin Api', f"{data['D001A']['oranye']} Cincin Api"),
    
    # Production - F008A
    ('17.30', f"{data['F008A']['potensi_ton_ha']:.2f}"),
    ('0.79', f"{data['F008A']['real_ton_ha']:.2f}"),
    
    # Production - D001A  
    ('17.53', f"{data['D001A']['potensi_ton_ha']:.2f}"),
    ('0.30', f"{data['D001A']['real_ton_ha']:.2f}"),
    
    # Gap percentages
    ('-95.4%', f"{data['F008A']['gap_pct']:.1f}%"),
    ('-98.3%', f"{data['D001A']['gap_pct']:.1f}%"),
    
    # Total loss
    ('1.208', f"{data['combined']['total_loss_million']:.3f}"),
    
    # SPH
    ('104', str(data['F008A']['sph'])),
    ('105', str(data['D001A']['sph'])),
    
    # Infection percentage
    ('5.0%', f"{data['F008A']['infection_pct']:.1f}%"),
    ('6.3%', f"{data['D001A']['infection_pct']:.1f}%"),
    
    # Total trees
    ('2,391', f"{data['F008A']['total_trees']:,}"),
    ('2,598', f"{data['D001A']['total_trees']:,}"),
]

# Apply replacements
for old, new in replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f'  ✅ Replaced "{old}" → "{new}" ({count} occurrences)')
    else:
        print(f'  ⚠️  "{old}" not found')

# Save updated dashboard
output_file = 'data/output/dashboard_cincin_api_UPDATED_F008A_D001A.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Dashboard updated successfully!')
print(f'📁 Saved to: {output_file}')

print('\n📊 Summary of changes:')
print(f'  Old blocks: D006A, D007A')
print(f'  New blocks: F008A, D001A')
print(f'  Total luas: {data["combined"]["total_luas"]} Ha')
print(f'  F008A Spread Ratio: {data["F008A"]["spread_ratio"]:.0f}x')
print(f'  D001A Spread Ratio: {data["D001A"]["spread_ratio"]:.0f}x')
print(f'  F008A Gap: {data["F008A"]["gap_pct"]:.1f}%')
print(f'  D001A Gap: {data["D001A"]["gap_pct"]:.1f}%')
