import json

with open('tbm_blocks_analysis.json', 'r') as f:
    tbm_blocks = json.load(f)

with open('complete_historical_yields.json', 'r') as f:
    hist_yields = json.load(f)

tbm_codes = set([b['block'] for b in tbm_blocks])

# Calculate per division
divisions = {}
for block_code, data in hist_yields.items():
    div = data.get('division', 'Unknown')
    gap = data.get('yields', {}).get('2025', {}).get('gap_pct', 0)
    luas = data.get('luas_ha', 0)
    
    if div not in divisions:
        divisions[div] = {'total': 0, 'tm': 0, 'tbm': 0, 'gap_all': 0, 'gap_tm': 0, 'luas_tm': 0, 'luas_tbm': 0}
    
    divisions[div]['total'] += 1
    divisions[div]['gap_all'] += gap
    
    is_tbm = block_code in tbm_codes
    if is_tbm:
        divisions[div]['tbm'] += 1
        divisions[div]['luas_tbm'] += luas
    else:
        divisions[div]['tm'] += 1
        divisions[div]['gap_tm'] += gap
        divisions[div]['luas_tm'] += luas

print("DAMPAK MENGELUARKAN TBM DARI YIELD GAP")
print("="*80)
print()

for div in sorted(divisions.keys()):
    d = divisions[div]
    avg_all = d['gap_all'] / d['total'] if d['total'] > 0 else 0
    avg_tm = d['gap_tm'] / d['tm'] if d['tm'] > 0 else 0
    delta = avg_tm - avg_all
    print(f"{div}: Blok={d['total']} (TBM:{d['tbm']}, TM:{d['tm']})")
    print(f"        Gap All: {avg_all:.1f}% -> Gap TM: {avg_tm:.1f}% (delta: {delta:+.1f}%)")
    print(f"        Luas TBM: {d['luas_tbm']:.1f}Ha, Luas TM: {d['luas_tm']:.1f}Ha")
    print()

# Total
total_blocks = sum(d['total'] for d in divisions.values())
total_tbm = sum(d['tbm'] for d in divisions.values())
total_tm = sum(d['tm'] for d in divisions.values())
total_luas_tbm = sum(d['luas_tbm'] for d in divisions.values())
total_luas_tm = sum(d['luas_tm'] for d in divisions.values())

print("="*80)
print("RINGKASAN:")
print(f"  Total Blok: {total_blocks}")
print(f"  - TBM: {total_tbm} blok ({total_luas_tbm:.1f} Ha)")
print(f"  - TM : {total_tm} blok ({total_luas_tm:.1f} Ha)")
print(f"  Persentase TBM: {total_tbm/total_blocks*100:.1f}% blok, {total_luas_tbm/(total_luas_tbm+total_luas_tm)*100:.2f}% luas")
