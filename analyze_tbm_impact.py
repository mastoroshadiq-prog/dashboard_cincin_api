"""
Deep analysis of TBM (Tanaman Belum Menghasilkan) blocks:
1. Load TBM inventory from previous analysis
2. Analyze relevance to Yield Gap
3. Analyze relevance to SPH
"""
import pandas as pd
import json

# Load TBM analysis
with open('tbm_blocks_analysis.json', 'r') as f:
    tbm_data = json.load(f)

# Load historical yields
with open('complete_historical_yields.json', 'r') as f:
    hist_yields = json.load(f)

# Load risk data for SPH
with open('complete_risk_data.json', 'r') as f:
    risk_data = json.load(f)

# Load raw data for more details
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*80)
print("ANALISIS TBM (TANAMAN BELUM MENGHASILKAN)")
print("="*80)

print(f"\nTotal blok TBM ditemukan: {len(tbm_data)}")
print("\n" + "-"*80)
print("INVENTARISASI TBM")
print("-"*80)

print("\n| Blok    | Tahun Tanam | Jumlah Pohon | Umur 2025 | Status |")
print("|---------|-------------|--------------|-----------|--------|")
for block in tbm_data:
    print(f"| {block['block']:7s} | {block['latest_tanam_year'] or 'N/A':11} | {block['total_tanam']:12} | {2025 - (block['latest_tanam_year'] or 2025):4} tahun | {block['status']:6} |")

# Now analyze yield gap relevance
print("\n\n" + "="*80)
print("ANALISIS RELEVANSI TBM DENGAN YIELD GAP")
print("="*80)

print("""
TEORI:
- TBM (Tanaman Belum Menghasilkan) = sawit umur 0-3 tahun
- Sawit mulai produktif pada umur 3-4 tahun  
- Jika blok memiliki TBM dalam proporsi besar, maka:
  * Yield REALISASI akan RENDAH (karena TBM tidak menghasilkan)
  * Yield POTENSI dihitung berdasarkan tanaman produktif  
  * GAP = Potensi - Realisasi akan TINGGI (false positive risk)
""")

print("\n" + "-"*80)
print("YIELD DATA UNTUK BLOK TBM")
print("-"*80)

print("\n| Blok    | Luas (Ha) | Y2023 Real | Y2024 Real | Y2025 Real | Y2025 Pot | Gap (%) | Keterangan |")
print("|---------|-----------|------------|------------|------------|-----------|---------|------------|")

for block in tbm_data:
    block_code = block['block']
    if block_code in hist_yields:
        h = hist_yields[block_code]
        luas = h.get('luas_ha', 0)
        y2023 = h.get('yields', {}).get('2023', {}).get('real_ton_ha', 0)
        y2024 = h.get('yields', {}).get('2024', {}).get('real_ton_ha', 0)
        y2025 = h.get('yields', {}).get('2025', {}).get('real_ton_ha', 0)
        y2025_pot = h.get('yields', {}).get('2025', {}).get('poten_ton_ha', 0)
        gap = h.get('yields', {}).get('2025', {}).get('gap_pct', 0)
        
        # Determine explanation
        if y2023 == 0 and y2024 == 0 and y2025 == 0:
            keterangan = "Belum produktif"
        elif y2025 == 0:
            keterangan = "TBM di 2025"
        else:
            keterangan = "Mulai produktif"
            
        print(f"| {block_code:7s} | {luas:9.1f} | {y2023:10.1f} | {y2024:10.1f} | {y2025:10.1f} | {y2025_pot:9.1f} | {gap:6.0f}% | {keterangan:10s} |")
    else:
        print(f"| {block_code:7s} | Data tidak ditemukan di historical yields |")

# SPH Analysis
print("\n\n" + "="*80)
print("ANALISIS RELEVANSI TBM DENGAN SPH")
print("="*80)

print("""
TEORI:
- SPH (Stands Per Hectare) = Jumlah pohon per hektar
- Untuk blok dengan TBM:
  * SPH bisa TINGGI (pohon banyak karena tanam baru)
  * ATAU SPH bisa RENDAH (jika data hanya menghitung pohon produktif)
  
PERTANYAAN KUNCI:
- Apakah TBM dihitung dalam SPH total blok?
- Bagaimana membedakan SPH TM vs SPH TBM?
""")

print("\n" + "-"*80)
print("SPH DATA UNTUK BLOK TBM")
print("-"*80)

# Get SPH and Pokok data from raw file
POKOK_COL = 66  # Total trees
SPH_COL = 68    # SPH

print("\n| Blok    | Luas (Ha) | Pokok Total | SPH (dari risk) | SPH Calc | TBM Tanam | Status |")
print("|---------|-----------|-------------|-----------------|----------|-----------|--------|")

for block in tbm_data:
    block_code = block['block']
    
    # Get from risk data
    sph_risk = risk_data.get(block_code, {}).get('sph', 0)
    luas = risk_data.get(block_code, {}).get('luas_ha', 0)
    
    # Find in raw data
    pokok = 0
    sph_raw = 0
    for row in range(10, len(df)):
        if str(df.iloc[row, 0]).strip() == block_code:
            pokok = df.iloc[row, POKOK_COL] if pd.notna(df.iloc[row, POKOK_COL]) else 0
            sph_raw = df.iloc[row, SPH_COL] if pd.notna(df.iloc[row, SPH_COL]) else 0
            break
    
    # Calculate SPH
    sph_calc = pokok / luas if luas > 0 else 0
    tbm_count = block['total_tanam']
    status = block['status']
    
    print(f"| {block_code:7s} | {luas:9.1f} | {pokok:11.0f} | {sph_raw:15.1f} | {sph_calc:8.1f} | {tbm_count:9} | {status:6s} |")

# Conclusions
print("\n\n" + "="*80)
print("KESIMPULAN & REKOMENDASI")
print("="*80)

print("""
📊 KESIMPULAN:

1. RELEVANSI TBM DENGAN YIELD GAP:
   ✅ SANGAT RELEVAN - Blok dengan TBM tinggi akan menunjukkan:
   - Yield realisasi = 0 atau sangat rendah (pohon belum produktif)
   - Yield potensi dihitung berdasarkan standar (TIDAK VALID untuk TBM)
   - GAP YIELD TIDAK BERMAKNA untuk blok TBM karena pohon memang belum menghasilkan
   
   ⚠️ IMPLIKASI:
   - Blok TBM SEHARUSNYA DIKELUARKAN dari analisis yield gap
   - Atau ditandai sebagai "TBM - Expected 0 Yield"
   - Gap tinggi pada TBM bukan indikator RISIKO, melainkan kondisi NORMAL

2. RELEVANSI TBM DENGAN SPH:
   ✅ RELEVAN - TBM mempengaruhi interpretasi SPH:
   - SPH pada blok TBM = pohon tanam baru (belum produktif)
   - Tidak bisa dibandingkan dengan SPH blok produktif
   - SPH rendah pada blok campuran TBM+TM bisa karena:
     a) Serangan ganoderma (pohon mati)
     b) Atau TBM belum tumbuh besar
     
   ⚠️ IMPLIKASI:
   - SPH blok TBM perlu diberi FLAG khusus
   - Analisis SPH untuk risiko Ganoderma harus fokus pada blok TM saja

🔧 REKOMENDASI PERBAIKAN DASHBOARD:
   
1. Di Block Detail Panel, jika blok TBM:
   - Tampilkan badge "TBM" (sudah ada)
   - Yield Gap: tampilkan "N/A - TBM" bukan angka %
   - Estimasi Kerugian: tampilkan "N/A - TBM"
   
2. Di Analisis Risiko:
   - Filter blok TBM dari perhitungan rata-rata Yield Gap
   - Buat kategori terpisah "Blok TBM/Pengembangan"

3. Di Rekapitulasi:
   - Pisahkan luas TBM vs TM per divisi
   - Hitung potensi produksi hanya dari TM
""")
