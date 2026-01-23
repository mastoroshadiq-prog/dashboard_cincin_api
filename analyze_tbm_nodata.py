"""
Analyze:
1. What is current TBM display in dashboard vs "No Data"
2. Impact of excluding TBM from yield gap calculations
"""
import json

# Load data
with open('tbm_blocks_analysis.json', 'r') as f:
    tbm_blocks = json.load(f)

with open('complete_historical_yields.json', 'r') as f:
    hist_yields = json.load(f)

print("="*70)
print("1. ANALISIS TBM vs NO DATA")
print("="*70)

# List TBM blocks
tbm_codes = [b['block'] for b in tbm_blocks]
print(f"\nBlok TBM (dari analisis TANAM/SISIP): {len(tbm_codes)}")
print(tbm_codes)

# Find "No Data" blocks (blocks with 0 yields in all years)
no_data_blocks = []
zero_yield_blocks = []
for block_code, data in hist_yields.items():
    y2023 = data.get('yields', {}).get('2023', {}).get('real_ton_ha', 0)
    y2024 = data.get('yields', {}).get('2024', {}).get('real_ton_ha', 0)
    y2025 = data.get('yields', {}).get('2025', {}).get('real_ton_ha', 0)
    
    if y2023 == 0 and y2024 == 0 and y2025 == 0:
        zero_yield_blocks.append(block_code)

print(f"\nBlok dengan Yield = 0 di semua tahun: {len(zero_yield_blocks)}")
print(zero_yield_blocks[:20], "..." if len(zero_yield_blocks) > 20 else "")

# Check overlap
tbm_set = set(tbm_codes)
zero_set = set(zero_yield_blocks)
overlap = tbm_set & zero_set
tbm_only = tbm_set - zero_set
zero_only = zero_set - tbm_set

print(f"\n📊 Perbandingan:")
print(f"  TBM & Zero Yield (overlap): {len(overlap)}")
print(f"  TBM tapi ada yield (aneh): {len(tbm_only)} -> {list(tbm_only)[:5]}")
print(f"  Zero Yield tapi bukan TBM: {len(zero_only)} -> {list(zero_only)[:10]}")

print("\n" + "="*70)
print("2. DAMPAK MENGELUARKAN TBM DARI YIELD GAP")
print("="*70)

# Calculate current average yield gap per division
divisions = {}
for block_code, data in hist_yields.items():
    div = data.get('division', 'Unknown')
    gap = data.get('yields', {}).get('2025', {}).get('gap_pct', 0)
    luas = data.get('luas_ha', 0)
    
    if div not in divisions:
        divisions[div] = {'total_blocks': 0, 'total_gap': 0, 'total_luas': 0,
                          'tm_blocks': 0, 'tm_gap': 0, 'tm_luas': 0,
                          'tbm_blocks': 0, 'tbm_luas': 0}
    
    divisions[div]['total_blocks'] += 1
    divisions[div]['total_gap'] += gap
    divisions[div]['total_luas'] += luas
    
    if block_code in tbm_set:
        divisions[div]['tbm_blocks'] += 1
        divisions[div]['tbm_luas'] += luas
    else:
        divisions[div]['tm_blocks'] += 1
        divisions[div]['tm_gap'] += gap
        divisions[div]['tm_luas'] += luas

print("\n| Divisi | Total Blok | TBM | TM | Avg Gap (All) | Avg Gap (TM only) | Luas TBM | Luas TM |")
print("|--------|------------|-----|----|--------------:|------------------:|----------|---------|")

for div in sorted(divisions.keys()):
    d = divisions[div]
    avg_all = d['total_gap'] / d['total_blocks'] if d['total_blocks'] > 0 else 0
    avg_tm = d['tm_gap'] / d['tm_blocks'] if d['tm_blocks'] > 0 else 0
    print(f"| {div:6s} | {d['total_blocks']:10d} | {d['tbm_blocks']:3d} | {d['tm_blocks']:3d} | {avg_all:13.1f}% | {avg_tm:17.1f}% | {d['tbm_luas']:6.1f}Ha | {d['tm_luas']:6.1f}Ha |")

# Summary
total_all = sum(d['total_blocks'] for d in divisions.values())
total_tbm = sum(d['tbm_blocks'] for d in divisions.values())
total_tm = sum(d['tm_blocks'] for d in divisions.values())
luas_tbm = sum(d['tbm_luas'] for d in divisions.values())
luas_tm = sum(d['tm_luas'] for d in divisions.values())

print(f"\n📊 RINGKASAN TOTAL:")
print(f"  Total Blok: {total_all}")
print(f"  - TBM: {total_tbm} blok ({luas_tbm:.1f} Ha)")
print(f"  - TM : {total_tm} blok ({luas_tm:.1f} Ha)")
print(f"  Persentase TBM: {total_tbm/total_all*100:.1f}% dari blok, {luas_tbm/(luas_tbm+luas_tm)*100:.1f}% dari luas")

print("\n" + "="*70)
print("3. KESIMPULAN")
print("="*70)
print("""
❓ APAKAH "NO DATA" = TBM?
   TIDAK SELALU. "No Data" di dashboard berarti blok tidak punya data yield.
   Ini bisa karena:
   a) TBM (tanaman belum menghasilkan) - seharusnya 0 yield
   b) Data hilang/tidak tercatat
   c) Kombinasi keduanya
   
⚠️ DAMPAK MENGELUARKAN TBM:
   1. Rata-rata Yield Gap akan BERUBAH (biasanya naik karena TBM gap = 0%)
   2. Memisahkan Luas TBM vs TM memberikan gambaran lebih akurat
   3. Produksi potensial hanya dihitung dari TM
   
💡 REKOMENDASI:
   1. Tampilkan badge "TBM" untuk blok yang teridentifikasi TBM
   2. Tampilkan badge "No Data" untuk blok tanpa data yield
   3. Di rekap divisi, pisahkan: Luas TM | Luas TBM | Avg Gap (TM only)
""")
