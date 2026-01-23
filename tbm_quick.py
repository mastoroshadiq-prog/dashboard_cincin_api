"""Quick TBM analysis output"""
import json

with open('tbm_blocks_analysis.json', 'r') as f:
    tbm_data = json.load(f)

with open('complete_historical_yields.json', 'r') as f:
    hist_yields = json.load(f)

with open('complete_risk_data.json', 'r') as f:
    risk_data = json.load(f)

print("="*70)
print("INVENTARISASI TBM (TANAMAN BELUM MENGHASILKAN)")
print("="*70)
print(f"Total blok TBM: {len(tbm_data)}")
print()

for block in tbm_data:
    b = block['block']
    tanam = block['latest_tanam_year'] or 'N/A'
    jml = block['total_tanam']
    status = block['status']
    print(f"  {b:7s} | Tanam: {tanam} | Jumlah: {jml:4} | Status: {status}")

print()
print("="*70)
print("YIELD GAP UNTUK BLOK TBM")
print("="*70)

for block in tbm_data:
    b = block['block']
    if b in hist_yields:
        h = hist_yields[b]
        y2023 = h.get('yields', {}).get('2023', {}).get('real_ton_ha', 0)
        y2024 = h.get('yields', {}).get('2024', {}).get('real_ton_ha', 0)
        y2025 = h.get('yields', {}).get('2025', {}).get('real_ton_ha', 0)
        gap = h.get('yields', {}).get('2025', {}).get('gap_pct', 0)
        print(f"  {b}: Y2023={y2023:.1f} | Y2024={y2024:.1f} | Y2025={y2025:.1f} | Gap={gap:.0f}%")

print()
print("="*70)
print("SPH UNTUK BLOK TBM")
print("="*70)

for block in tbm_data:
    b = block['block']
    if b in risk_data:
        sph = risk_data[b].get('sph', 0)
        luas = risk_data[b].get('luas_ha', 0)
        infected = risk_data[b].get('total_infected', 0)
        print(f"  {b}: SPH={sph:.0f} | Luas={luas:.1f}Ha | Infected={infected}")

print()
print("="*70)
print("KESIMPULAN")
print("="*70)
print("""
1. TBM vs YIELD GAP:
   - Blok TBM menunjukkan Yield = 0 atau sangat rendah
   - Ini BUKAN indikator risiko, melainkan kondisi NORMAL
   - Yield Gap pada TBM tidak bermakna
   
2. TBM vs SPH:
   - SPH blok TBM = pohon baru tanam (belum produktif)
   - Tidak valid untuk analisis risiko Ganoderma
   
3. REKOMENDASI:
   - Tampilkan badge TBM di dashboard (sudah ada)
   - Yield Gap tampilkan "N/A" untuk TBM
   - Keluarkan TBM dari perhitungan rata-rata divisi
""")
