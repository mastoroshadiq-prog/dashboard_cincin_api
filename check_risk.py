import json
with open('complete_risk_data.json', 'r') as f:
    data = json.load(f)
print(f'Total blocks: {len(data)}')
print()
print('Samples:')
for block in ['D001A', 'E007A', 'F004A', 'A001A', 'D005A']:
    if block in data:
        r = data[block]
        print(f"{block}: AR={r['attack_rate']}%, SPH={r['sph']}, Stadium={r['stadium']}, Loss=Rp{r['loss_value_juta']}Jt, Stress={r.get('stress_class','N/A')}")
