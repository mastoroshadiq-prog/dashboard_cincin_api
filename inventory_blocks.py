"""
Inventory blocks without gap yield data
Cross-check for validation
"""
import json
import pandas as pd

# Load historical yields
with open('complete_historical_yields.json', 'r') as f:
    hist = json.load(f)

# Load risk data
with open('complete_risk_data.json', 'r') as f:
    risk = json.load(f)

print("="*70)
print("INVENTORY: BLOK TANPA DATA GAP YIELD")
print("="*70)

# Analyze blocks by division
blocks_no_gap = {}
blocks_with_gap = {}

for block_code, data in hist.items():
    yields = data.get('yields', {})
    y2025 = yields.get('2025', {})
    gap = y2025.get('gap_pct', 0)
    division = data.get('division', 'UNKNOWN')
    
    # Check if gap is meaningful (non-zero and has actual data)
    real = y2025.get('real_ton_ha', 0)
    poten = y2025.get('poten_ton_ha', 0)
    
    if real == 0 and poten == 0:
        # No yield data at all
        if division not in blocks_no_gap:
            blocks_no_gap[division] = []
        blocks_no_gap[division].append({
            'block': block_code,
            'gap_pct': gap,
            'real_2025': real,
            'poten_2025': poten
        })
    else:
        if division not in blocks_with_gap:
            blocks_with_gap[division] = []
        blocks_with_gap[division].append(block_code)

print("\n" + "="*70)
print("SUMMARY PER DIVISI")
print("="*70)
print(f"{'Division':<15} {'With Gap Data':<15} {'No Gap Data':<15} {'Total':<10}")
print("-"*55)

all_divisions = set(list(blocks_no_gap.keys()) + list(blocks_with_gap.keys()))
for div in sorted(all_divisions):
    with_gap = len(blocks_with_gap.get(div, []))
    no_gap = len(blocks_no_gap.get(div, []))
    print(f"{div:<15} {with_gap:<15} {no_gap:<15} {with_gap + no_gap:<10}")

print("\n" + "="*70)
print("DETAIL: BLOK TANPA GAP YIELD DATA")
print("="*70)

total_no_gap = 0
for div in sorted(blocks_no_gap.keys()):
    blocks = blocks_no_gap[div]
    total_no_gap += len(blocks)
    print(f"\n{div} ({len(blocks)} blok tanpa data):")
    for b in blocks[:10]:  # Show max 10
        print(f"  - {b['block']}: gap={b['gap_pct']}%, real2025={b['real_2025']}, poten2025={b['poten_2025']}")
    if len(blocks) > 10:
        print(f"  ... dan {len(blocks) - 10} blok lainnya")

print(f"\n\nTOTAL BLOK TANPA GAP DATA: {total_no_gap}")
print(f"TOTAL BLOK DENGAN GAP DATA: {len(hist) - total_no_gap}")

# Also check NDRE coverage
print("\n" + "="*70)
print("NDRE DATA COVERAGE")
print("="*70)

ndre_df = pd.read_csv('data/input/tabelNDREnew.csv')
ndre_blocks = set(ndre_df['blok_b'].unique())
all_blocks = set(hist.keys())

blocks_with_ndre = all_blocks.intersection(ndre_blocks)
blocks_without_ndre = all_blocks - ndre_blocks

print(f"Blok dengan data NDRE: {len(blocks_with_ndre)}")
print(f"Blok TANPA data NDRE: {len(blocks_without_ndre)}")

# Group blocks without NDRE by division
no_ndre_by_div = {}
for block in blocks_without_ndre:
    div = hist[block].get('division', 'UNKNOWN')
    if div not in no_ndre_by_div:
        no_ndre_by_div[div] = []
    no_ndre_by_div[div].append(block)

print("\nBlok tanpa NDRE per divisi:")
for div in sorted(no_ndre_by_div.keys()):
    blocks = no_ndre_by_div[div]
    print(f"  {div}: {len(blocks)} blok")
    if len(blocks) <= 5:
        print(f"    {blocks}")
