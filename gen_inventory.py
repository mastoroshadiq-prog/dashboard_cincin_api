"""
Generate inventory report to file
"""
import json
import pandas as pd

# Load data
with open('complete_historical_yields.json', 'r') as f:
    hist = json.load(f)

ndre_df = pd.read_csv('data/input/tabelNDREnew.csv')
ndre_blocks = set(ndre_df['blok_b'].unique())

# Analyze
report = []
report.append("="*70)
report.append("INVENTORY: DATA COVERAGE ANALYSIS")
report.append("="*70)

# Group by division
divisions = {}
for block, data in hist.items():
    div = data.get('division', 'UNKNOWN')
    if div not in divisions:
        divisions[div] = {'blocks': [], 'no_yield': [], 'no_ndre': []}
    
    divisions[div]['blocks'].append(block)
    
    # Check yield data
    y2025 = data.get('yields', {}).get('2025', {})
    if y2025.get('real_ton_ha', 0) == 0 and y2025.get('poten_ton_ha', 0) == 0:
        divisions[div]['no_yield'].append(block)
    
    # Check NDRE data
    if block not in ndre_blocks:
        divisions[div]['no_ndre'].append(block)

# Summary table
report.append("\nSUMMARY PER DIVISI:")
report.append("-"*70)
report.append(f"{'Division':<12} {'Total':<8} {'Has Yield':<12} {'No Yield':<10} {'Has NDRE':<10} {'No NDRE':<10}")
report.append("-"*70)

for div in sorted(divisions.keys()):
    d = divisions[div]
    total = len(d['blocks'])
    no_yield = len(d['no_yield'])
    has_yield = total - no_yield
    no_ndre = len(d['no_ndre'])
    has_ndre = total - no_ndre
    report.append(f"{div:<12} {total:<8} {has_yield:<12} {no_yield:<10} {has_ndre:<10} {no_ndre:<10}")

# Total
total_blocks = len(hist)
total_no_yield = sum(len(d['no_yield']) for d in divisions.values())
total_no_ndre = sum(len(d['no_ndre']) for d in divisions.values())
report.append("-"*70)
report.append(f"{'TOTAL':<12} {total_blocks:<8} {total_blocks-total_no_yield:<12} {total_no_yield:<10} {len(ndre_blocks):<10} {total_no_ndre:<10}")

# Detail blocks without yield
report.append("\n" + "="*70)
report.append("BLOK TANPA DATA YIELD 2025 (untuk di-crosscheck ke data_gabungan.xlsx):")
report.append("="*70)

for div in sorted(divisions.keys()):
    no_yield = divisions[div]['no_yield']
    if no_yield:
        report.append(f"\n{div} ({len(no_yield)} blok):")
        for block in sorted(no_yield):
            report.append(f"  {block}")

# Write to file
with open('INVENTORY_DATA_COVERAGE.txt', 'w') as f:
    f.write('\n'.join(report))

print('\n'.join(report))
print("\n\nReport saved to: INVENTORY_DATA_COVERAGE.txt")
