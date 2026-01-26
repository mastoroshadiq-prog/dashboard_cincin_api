import json

print('='*80)
print('🔄 FINAL DASHBOARD UPDATE WITH CORRECTIONS')
print('='*80)

# Load corrected data
with open('data/output/dashboard_data_f008a_d001a_CORRECTED.json', 'r') as f:
    data = json.load(f)

# Load HTML
with open('data/output/dashboard_cincin_api_F008A_D001A.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('\n📝 Applying final corrections...')

# Additional corrections needed
corrections = {
    # Fix TT for F008A (should already be 2008)
    'TT 2008': f"TT {data['F008A']['tt']}",
    '2008 (18 Tahun)': f"{data['F008A']['tt']} ({data['F008A']['age']} Tahun)",
    
    # Fix TT for D001A (change from 2008 to 2009)
    '2008 (17 Tahun)': f"{data['D001A']['tt']} ({data['D001A']['age']} Tahun)",
    
    # Fix loss for F008A - should show as note, not 0
    'Rp 0.0 Juta': 'Rp 0 Juta*',
    'Rp 0 Juta': 'Rp 0 Juta*',
    
    # Fix loss for D001A
    'Rp 182.5 Juta': f"Rp {data['D001A']['loss_per_year_juta']:.1f} Juta",
    
    # Fix total loss
    'Rp 0.182 Miliar': f"Rp {data['combined']['total_loss_million']:.3f} Miliar",
}

for old, new in corrections.items():
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f'  ✅ "{old}" → "{new}" ({count}x)')

# Add note about F008A surplus after the table
note_html = '''
                <div class="p-4 bg-blue-50 text-xs font-black uppercase tracking-widest text-center border-t border-slate-200">
                    *F008A menunjukkan SURPLUS produksi (+8.7%), bukan kerugian. Ini adalah fenomena "Symptom Lag" - 
                    infeksi ekstrem (29.3%) belum berdampak ke produksi. Kerugian akan muncul dalam 6-12 bulan.
                </div>'''

# Find the table closing tag and insert note before it
table_end = html.find('</table>')
if table_end > 0:
    # Find the div after table
    next_div = html.find('</div>', table_end)
    if next_div > 0:
        html = html[:next_div] + note_html + html[next_div:]
        print('  ✅ Added Symptom Lag note after table')

# Save final version
output_file = 'data/output/dashboard_cincin_api_FINAL_CORRECTED.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Dashboard updated and saved!')
print(f'📁 File: {output_file}')

print('\n📊 Final Summary:')
print(f'  F008A: TT {data["F008A"]["tt"]} ({data["F008A"]["age"]} tahun), Gap {data["F008A"]["gap_pct"]:.1f}%, Loss Rp 0 (SURPLUS)')
print(f'  D001A: TT {data["D001A"]["tt"]} ({data["D001A"]["age"]} tahun), Gap {data["D001A"]["gap_pct"]:.1f}%, Loss Rp {data["D001A"]["loss_per_year_juta"]:.1f} Juta')
print(f'  Total: Rp {data["combined"]["total_loss_million"]:.3f} Miliar/Tahun')
print(f'  Maps: cincin_api_map_F008A.png & cincin_api_map_D001A.png')
