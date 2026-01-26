import json

# Load the extracted data
with open('complete_historical_yields.json', 'r') as f:
    data = json.load(f)

# Filter AME02
ame02 = {k: v for k, v in data.items() if v['division'] == 'AME02'}

print(f"=== AME02 ANALYSIS ===")
print(f"Total blocks: {len(ame02)}")

# Classify by trend
declining = [(k, v) for k, v in ame02.items() if v['trend'] == 'DECLINING']
increasing = [(k, v) for k, v in ame02.items() if v['trend'] == 'INCREASING']
stable = [(k, v) for k, v in ame02.items() if v['trend'] == 'STABLE']

print(f"\nDECLINING: {len(declining)} blocks")
print(f"STABLE: {len(stable)} blocks")
print(f"INCREASING: {len(increasing)} blocks")

print("\n--- TOP 10 DECLINING BLOCKS ---")
for code, data in sorted(declining, key=lambda x: x[1]['change_2023_2025_pct'])[:10]:
    y23 = data['yields']['2023']['real_ton_ha']
    y25 = data['yields']['2025']['real_ton_ha']
    chg = data['change_2023_2025_pct']
    print(f"  {code}: {chg:+.1f}% | 2023: {y23:.1f} -> 2025: {y25:.1f} T/Ha")

print("\n--- TOP 10 INCREASING BLOCKS ---")
for code, data in sorted(increasing, key=lambda x: -x[1]['change_2023_2025_pct'])[:10]:
    y23 = data['yields']['2023']['real_ton_ha']
    y25 = data['yields']['2025']['real_ton_ha']
    chg = data['change_2023_2025_pct']
    print(f"  {code}: {chg:+.1f}% | 2023: {y23:.1f} -> 2025: {y25:.1f} T/Ha")

# Also show overall statistics
print("\n=== ALL DIVISIONS SUMMARY ===")
divisions = {}
for code, block in data.items():
    div = block['division']
    if div not in divisions:
        divisions[div] = {'total': 0, 'declining': 0, 'stable': 0, 'increasing': 0}
    divisions[div]['total'] += 1
    divisions[div][block['trend'].lower()] += 1

for div, counts in sorted(divisions.items()):
    print(f"{div}: {counts['total']} | Dec: {counts['declining']} | Stb: {counts['stable']} | Inc: {counts['increasing']}")
