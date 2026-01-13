import json

# Load data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    data = json.load(f)

d003a = data['D003A']

print('='*80)
print('BLOK D003A - DATA VERIFICATION')
print('='*80)
print(f"Gap Ton/Ha: {d003a['gap_ton_ha']}")
print(f"Gap %: {d003a['gap_pct']}")
print(f"Luas Ha: {d003a['luas_ha']}")
print(f"Loss (Juta): {d003a['loss_value_juta']}")
print()
print('Calculation:')
print(f"  abs({d003a['gap_ton_ha']}) × {d003a['luas_ha']} × 1.5M TBS price")
print(f"  = {abs(d003a['gap_ton_ha'])} × {d003a['luas_ha']} × 1.5")
print(f"  = {abs(d003a['gap_ton_ha']) * d003a['luas_ha'] * 1.5} Juta")
print(f"  = {abs(d003a['gap_ton_ha']) * d003a['luas_ha'] * 1.5 / 1000:.3f} Miliar")
print()
print(f"JSON value: Rp {d003a['loss_value_juta']:.1f} Juta = Rp {d003a['loss_value_juta']/1000:.2f} Miliar")
print()
print("✅ Dashboard should show: Rp 177 Juta (from JSON)")
print("✅ Modal table will populate from same JSON data")
print('='*80)
