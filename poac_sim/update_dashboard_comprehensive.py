import json
import re

print('='*80)
print('🔄 COMPREHENSIVE DASHBOARD UPDATE: F008A & D001A')
print('='*80)

# Load data
with open('data/output/dashboard_data_f008a_d001a.json', 'r') as f:
    data = json.load(f)

# Load HTML
with open('data/output/dashboard_cincin_api_final.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('\n📝 Updating all data points...')

# Define all replacements systematically
replacements = {
    # Title and headers
    'D006A & D007A': 'F008A & D001A',
    'D006A \u0026 D007A': 'F008A \u0026 D001A',
    'Blok D006A \u0026 D007A': 'Blok F008A \u0026 D001A',
    
    # Individual block names in table
    'D006A': 'F008A',
    'D007A': 'D001A',
    
    # Block display names
    'Blok D006A': 'Blok F008A',
    'Blok D007A': 'Blok D001A',
    
    # Luas
    '47.7': f"{data['combined']['total_luas']:.1f}",
    '23 Ha': f"{data['F008A']['luas']} Ha",
    '23.0 Ha': f"{data['F008A']['luas']} Ha",
    '24.7 Ha': f"{data['D001A']['luas']} Ha",
    
    # TT and Age - F008A
    'TT 2009': f"TT {data['F008A']['tt']}",
    '2009 (16 Tahun)': f"{data['F008A']['tt']} ({data['F008A']['age']} Tahun)",
    'Usia 16 Tahun': f"Usia {data['F008A']['age']} Tahun",
    
    # Production - F008A (Potensi)
    '17.30': f"{data['F008A']['potensi_ton_ha']:.2f}",
    
    # Production - F008A (Real)
    '0.79': f"{data['F008A']['real_ton_ha']:.2f}",
    
    # Production - D001A (Potensi)
    '17.53': f"{data['D001A']['potensi_ton_ha']:.2f}",
    
    # Production - D001A (Real)
    '0.30': f"{data['D001A']['real_ton_ha']:.2f}",
    
    # Gap - F008A
    '16.51': f"{abs(data['F008A']['gap_ton_ha']):.2f}",
    '-95.4%': f"{data['F008A']['gap_pct']:.1f}%",
    '95-98%': f"{abs(data['F008A']['gap_pct']):.0f}-{abs(data['D001A']['gap_pct']):.0f}%",
    
    # Gap - D001A
    '17.23': f"{abs(data['D001A']['gap_ton_ha']):.2f}",
    '-98.3%': f"{data['D001A']['gap_pct']:.1f}%",
    
    # Spread Ratio - F008A
    '2.16x': f"{data['F008A']['spread_ratio']:.0f}x",
    
    # Spread Ratio - D001A
    '1.87x': f"{data['D001A']['spread_ratio']:.0f}x",
    
    # Infection counts - F008A
    '37 Inti': f"{data['F008A']['merah']} Inti",
    '80 Ring': f"{data['F008A']['oranye']} Ring",
    '80 Cincin Api': f"{data['F008A']['oranye']} Cincin Api",
    '244 Suspect': f"{data['F008A']['kuning']} Suspect",
    
    # Infection counts - D001A
    '57 Inti': f"{data['D001A']['merah']} Inti",
    '107 Ring': f"{data['D001A']['oranye']} Ring",
    '107 Cincin Api': f"{data['D001A']['oranye']} Cincin Api",
    '200 Suspect': f"{data['D001A']['kuning']} Suspect",
    
    # SPH
    '104': str(data['F008A']['sph']),
    '105': str(data['D001A']['sph']),
    '104 Pokok/Ha': f"{data['F008A']['sph']} Pokok/Ha",
    '105 Pokok/Ha': f"{data['D001A']['sph']} Pokok/Ha",
    
    # Total trees
    '2,391': f"{data['F008A']['total_trees']:,}",
    '2,382': f"{data['F008A']['total_trees']:,}",
    '2,598': f"{data['D001A']['total_trees']:,}",
    '2,586': f"{data['D001A']['total_trees']:,}",
    
    # Loss
    'Rp 569.6': f"Rp {data['F008A']['loss_per_year_million']*1000:.1f}" if data['F008A']['loss_per_year_million'] > 0 else "Rp 0",
    'Rp 638.4': f"Rp {data['D001A']['loss_per_year_million']*1000:.1f}",
    'Rp 1.208': f"Rp {data['combined']['total_loss_million']:.3f}",
    'Rp 1.2 M': f"Rp {data['combined']['total_loss_million']:.1f} M",
    
    # Infection percentage
    '5.0%': f"{data['F008A']['infection_pct']:.1f}%",
    '6.3%': f"{data['D001A']['infection_pct']:.1f}%",
    
    # Healthy trees (calculated)
    '2,021': str(data['F008A']['hijau']),
    '2,222': str(data['D001A']['hijau']),
}

# Apply replacements
count_total = 0
for old, new in replacements.items():
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f'  ✅ "{old}" → "{new}" ({count}x)')
        count_total += count
    else:
        print(f'  ⚠️  "{old}" not found')

print(f'\n📊 Total replacements: {count_total}')

# Save
output_file = 'data/output/dashboard_cincin_api_F008A_D001A.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Dashboard updated successfully!')
print(f'📁 Saved to: {output_file}')

print('\n📊 Summary:')
print(f'  Blocks: F008A ({data["F008A"]["luas"]} Ha) & D001A ({data["D001A"]["luas"]} Ha)')
print(f'  F008A: Spread {data["F008A"]["spread_ratio"]:.0f}x, Gap {data["F008A"]["gap_pct"]:.1f}%')
print(f'  D001A: Spread {data["D001A"]["spread_ratio"]:.0f}x, Gap {data["D001A"]["gap_pct"]:.1f}%')
print(f'  Total Loss: Rp {data["combined"]["total_loss_million"]:.3f} Miliar/Tahun')
