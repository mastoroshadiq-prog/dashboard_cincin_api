"""
Extract 8 critical blocks from all_blocks_data_hybrid.json
and create FULL content dashboard demo
"""

import json

# Load all blocks data
with open('data/output/all_blocks_data_hybrid.json', 'r', encoding='utf-8') as f:
    all_blocks = json.load(f)

# Find CRITICAL blocks (or top 8 by risk score)
critical_blocks = []

for code, data in all_blocks.items():
    if data.get('severity_hybrid') == 'CRITICAL' or data.get('severity') == 'CRITICAL':
        critical_blocks.append((code, data))

# If no CRITICAL severity, get top 8 by risk_score
if len(critical_blocks) < 8:
    sorted_blocks = sorted(all_blocks.items(), key=lambda x: x[1].get('risk_score', 0), reverse=True)
    critical_blocks = sorted_blocks[:8]

print(f"Found {len(critical_blocks)} blocks")
print("\n✅ 8 CRITICAL BLOCKS:")
print("="*80)

for i, (code, data) in enumerate(critical_blocks[:8], 1):
    loss = data.get('loss_value_juta', 0)
    ar = data.get('attack_rate', 0)
    gap = data.get('gap_ton_ha', 0)
    sph = data.get('sph', 0)
    risk = data.get('risk_score', 0)
    
    print(f"{i}. {code:8s} - Loss: {loss:6.1f} Jt | AR: {ar:5.1f}% | Gap: {gap:6.2f} | SPH: {sph:3d} | Risk: {risk:.1f}")

# Save blocks data for HTML generation
blocks_data = {}
for code, data in critical_blocks[:8]:
    blocks_data[code] = {
        'code': code,
        'loss_juta': round(data.get('loss_value_juta', 0), 2),
        'ar': data.get('attack_rate', 0),
        'gap': data.get('gap_ton_ha', 0),
        'sph': data.get('sph', 0),
        'risk_score': data.get('risk_score', 0),
        'luas_ha': data.get('luas_ha', 0),
        'severity': data.get('severity_hybrid', data.get('severity', 'HIGH'))
    }

with open('critical_blocks_data.json', 'w', encoding='utf-8') as f:
    json.dump(blocks_data, f, indent=2)

print("\n✅ Data saved to: critical_blocks_data.json")
print("="*80)

# Calculate totals
total_loss = sum(b['loss_juta'] for b in blocks_data.values())
print(f"\n💰 TOTAL LOSS: Rp {total_loss:.2f} Juta = Rp {total_loss/1000:.2f} Miliar")
