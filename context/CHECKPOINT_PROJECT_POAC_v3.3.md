# 📋 CHECKPOINT PROJECT: POAC v3.3 - Algoritma Cincin Api

**Tanggal Checkpoint**: 10 Desember 2025  
**Status Project**: AKTIF - Development & Validation Phase  
**Repository**: https://github.com/mastoroshadiq/dashboard-cincin-api.git  
**Branch**: main

---

## 🎯 EXECUTIVE SUMMARY

Project ini mengembangkan **Sistem Prioritisasi Survey Ganoderma Berbasis NDRE** menggunakan **Algoritma Cincin Api** untuk analisis kesehatan tanaman kelapa sawit. Sistem menganalisis data NDRE (Normalized Difference Red Edge) dari citra satelit/drone untuk mengidentifikasi area dengan stress vegetasi yang perlu divalidasi di lapangan.

> **⚠️ PENTING**: Berdasarkan hasil validasi, algoritma telah di-reposisi dari "Sistem Deteksi Ganoderma" menjadi **"Tool Prioritisasi Survey Lapangan"**. Output algoritma adalah kandidat untuk validasi, bukan diagnosis pasti.

### Key Deliverables:
1. ✅ Multi-divisi analysis dashboard (AME II & AME IV)
2. ✅ 3 preset deteksi (Konservatif, Standar, Agresif)
3. ✅ 3 metode adaptif (Age-Based, Ensemble+Age, Ensemble Pure) **← BARU**
4. ✅ Interactive HTML dashboard dengan lightbox zoom
5. ✅ Validasi algoritma vs data sensus lapangan
6. ✅ Dokumen kesimpulan & repositioning **← BARU**


---

## 📁 STRUKTUR PROJECT

```
d:\PythonProjects\simulasi_poac\
├── context/                          # Dokumentasi & konteks AI
│   ├── SOFTWARE REQUIREMENTS SPECIFICATION (SRS).md
│   ├── Panduan_Teknis_Algoritma_Cincin_Api.md
│   ├── enhancement.md
│   └── CHECKPOINT_PROJECT_POAC_v3.3.md  ← FILE INI
│
├── output/                           # Output HTML dashboard (generated)
│
└── poac_sim/                         # Main application directory
    ├── data/
    │   └── input/
    │       ├── tabelNDREnew.csv      # Data AME II (95,030 pohon)
    │       ├── AME_IV.csv            # Data AME IV (81,962 pohon)
    │       └── ame_2_4_hasil_sensus.csv  # Data sensus lapangan (102 blok)
    │
    ├── docs/
    │   └── METODOLOGI_ALGORITMA_CINCIN_API.md
    │
    ├── output/
    │   ├── validation_report/        # Validasi lama (1 preset)
    │   └── validation_all_presets/   # Validasi semua preset ← TERBARU
    │       ├── validation_all_presets_ame_ii.png
    │       ├── validation_all_presets_ame_iv.png
    │       ├── block_comparison_ame_ii.png
    │       ├── block_comparison_ame_iv.png
    │       ├── LAPORAN_VALIDASI_SEMUA_PRESET.md
    │       ├── metrics_ame_ii.csv
    │       ├── metrics_ame_iv.csv
    │       ├── detail_comparison_ame_ii.csv
    │       └── detail_comparison_ame_iv.csv
    │
    ├── src/                          # Source modules
    │   ├── __init__.py
    │   ├── ingestion.py              # Data loading & preprocessing
    │   ├── engine.py                 # Core analysis engine
    │   ├── clustering.py             # Clustering algorithms
    │   ├── spatial.py                # Spatial analysis
    │   ├── statistics.py             # Statistical functions
    │   ├── visualization.py          # Chart generation
    │   ├── dashboard.py              # Dashboard utilities
    │   └── report_generator.py       # Report generation
    │
    ├── run_all_presets.py            # MAIN ENTRY POINT - Multi-preset analysis
    ├── run_multi_divisi.py           # Multi-divisi runner
    ├── run_cincin_api.py             # Single analysis runner
    ├── validation_analysis.py        # Validasi 1 preset vs sensus
    ├── validation_all_presets.py     # Validasi SEMUA preset vs sensus ← TERBARU
    ├── main.py                       # Legacy entry point
    ├── config.py                     # Configuration
    ├── convert_html_to_pdf.py        # PDF converter utility
    ├── requirements.txt              # Dependencies
    └── README.md                     # Project readme
```

---

## 🔧 TEKNOLOGI & DEPENDENCIES

### Runtime
- **Python**: 3.13+
- **OS**: Windows (PowerShell)

### Libraries (requirements.txt)
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
scipy>=1.10.0
pathlib
```

### Struktur Data

#### 1. Data AME II (`tabelNDREnew.csv`)
```csv
blok,blok_b,t_tanam,n_baris,n_pokok,objectid,ndre125,KlassNDRE12025,Ket
D001A,A,2014,1,1,1,0.284,Stres Berat,
```
- **Total**: 95,030 pohon
- **Blok**: 36 blok (D001A - D036B)
- **Format blok**: D001A → normalize ke D01

#### 2. Data AME IV (`AME_IV.csv`)
```csv
DIVISI;Blok;Blok_B;T_Tanam;N_Baris;N_Pokok;objectid;NDRE125;KlassNDRE12025;Ket
AME;IV;K18A;A;2016;10;1;41364;0,294;Stres Berat;
```
- **Total**: 81,962 pohon
- **Blok**: 28 blok (K01 - L28)
- **Format**: Semicolon separated, decimal comma
- **⚠️ PENTING**: Kolom ter-shift! Perlu mapping khusus di `ingestion.py`

#### 3. Data Sensus (`ame_2_4_hasil_sensus.csv`)
```csv
ESTATE,DIVISI,BLOK,TT,LUAS_TANAM,TOTAL_PKK,SPH,STADIUM_1_2,STADIUM_3_4,TOTAL_GANODERMA,SERANGAN_PCT,REALISASI_HA,REALISASI_PKK
ADOLINA,AME002,D001A,2014,27.42,3648,133,-,-,-,0%,-,-
ADOLINA,AME004,K001,2016,...
```
- **Total**: 102 blok (36 AME002 + 66 AME004)
- **Ground truth** untuk validasi algoritma

---

## 🔥 ALGORITMA CINCIN API

### Konsep Dasar
Algoritma mendeteksi pola **spreading** infeksi Ganoderma dengan menganalisis nilai NDRE:
- **NDRE rendah** = Stress vegetasi tinggi = Potensi infeksi
- **Pola cincin** = Infeksi menyebar dari titik pusat ke area sekitar

### Klasifikasi Stress (dari data)
| Kategori | NDRE Range | Warna | Level Risiko |
|----------|------------|-------|--------------|
| Stres Sangat Berat | < 0.20 | MERAH | Tinggi |
| Stres Berat | 0.20 - 0.28 | ORANYE | Sedang-Tinggi |
| Stres Sedang | 0.28 - 0.35 | KUNING | Sedang |
| Stres Ringan / Sehat | > 0.35 | HIJAU | Rendah |

### 3 Preset Deteksi

| Preset | Ring1 | Ring2 | Ring3 | NDRE Threshold | Use Case |
|--------|-------|-------|-------|----------------|----------|
| **Konservatif** | 15% | 25% | 35% | < 0.20 | Deteksi ketat, akurasi tinggi |
| **Standar** | 30% | 50% | 70% | < 0.28 | Keseimbangan |
| **Agresif** | 50% | 70% | 85% | < 0.35 | Sensitif, tangkap semua |

---

## 📊 HASIL VALIDASI TERBARU

### AME II (36 Blok) - Sensus: 6.32% rata-rata serangan

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Deteksi Algo |
|--------|-------------|-------------|-----|------------|--------------|
| Konservatif | -0.176 | ❌ | 6.3% | 44% | 0.00% |
| Standar | 0.090 | ❌ | 6.2% | 44% | 0.07% |
| **Agresif** | -0.098 | ❌ | **4.8%** | **61%** | 4.09% |

**📌 Temuan AME II**: Algoritma **UNDER-DETECT**. Preset Agresif paling mendekati.

### AME IV (66 Blok) - Sensus: 1.89% rata-rata serangan

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Deteksi Algo |
|--------|-------------|-------------|-----|------------|--------------|
| **Konservatif** | **0.428** | ✅ Ya | **7.0%** | **42%** | 8.53% |
| Standar | -0.143 | ❌ | 15.0% | 29% | 16.57% |
| Agresif | -0.201 | ❌ | 42.2% | 0% | 44.06% |

**📌 Temuan AME IV**: Algoritma **OVER-DETECT**. Preset Konservatif paling akurat (satu-satunya signifikan!).

### Kesimpulan Validasi

1. **NDRE stress ≠ Ganoderma langsung** - korelasi rendah/tidak signifikan
2. **Dua divisi berperilaku berbeda** - perlu kalibrasi per lokasi
3. **Keterbatasan data** - NDRE saja tidak cukup spesifik untuk Ganoderma
4. **Rekomendasi**: Gunakan hasil sebagai **"Daftar Prioritas Survey"**, bukan diagnosis pasti
5. **Preset optimal**: Konservatif untuk AME IV, Agresif untuk AME II

> 📋 **Lihat dokumen lengkap**: `context/KESIMPULAN_ANALISIS_POAC_v3.3.md`

---

## 🎯 METODE DETEKSI ADAPTIF (BARU)

### 3 Metode yang Diimplementasikan

| # | Metode | Deskripsi | Output |
|---|--------|-----------|--------|
| 1 | **📅 Age-Based Selection** | Otomatis pilih preset berdasarkan umur blok | Klasifikasi per preset |
| 2 | **⚖️ Ensemble + Age Weight** | Kombinasi 3 preset dengan bobot umur | Confidence Level |
| 3 | **🗳️ Ensemble Pure** | Voting murni dari 3 preset | Votes 0-3 |

### Konfigurasi Age-Based

| Umur Blok | Preset Terpilih | Alasan |
|-----------|-----------------|--------|
| >12 tahun | Agresif | Risiko tinggi, perlu deteksi luas |
| 8-12 tahun | Standar | Risiko sedang, keseimbangan |
| <8 tahun | Konservatif | Risiko rendah, hindari false positive |

### Penggunaan Confidence Level untuk Prioritisasi Survey

| Confidence | Prioritas | Aksi |
|------------|-----------|------|
| **HIGH** (3/3 votes) | 🔴 P1 | Survey segera |
| **MEDIUM** (2/3 votes) | 🟠 P2 | Survey dalam 1 minggu |
| **LOW** (1/3 votes) | 🟡 P3 | Sampling / next cycle |
| **NONE** (0/3 votes) | 🟢 Skip | Fokus area lain |

### File Terkait

| File | Deskripsi |
|------|-----------|
| `src/adaptive_detection.py` | Modul implementasi 3 metode adaptif |
| `validation_adaptive_methods.py` | Script validasi metode adaptif |
| `data/output/validation_adaptive/` | Hasil validasi (HTML, CSV, PNG) |


---

## 🖥️ CARA MENJALANKAN

### 1. Multi-Divisi Analysis (Dashboard HTML)
```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim
python run_all_presets.py --divisi MULTI
```
Output: `output/multi_divisi_dashboard_*.html`

### 2. Single Divisi Analysis
```powershell
python run_all_presets.py --divisi AME_II
python run_all_presets.py --divisi AME_IV
```

### 3. Validasi vs Sensus (Semua Preset)
```powershell
python validation_all_presets.py
```
Output: `output/validation_all_presets/`

### 4. Validasi Single Preset
```powershell
python validation_analysis.py
```
Output: `output/validation_report/`

---

## 🐛 KNOWN ISSUES & FIXES

### Issue 1: AME IV Column Shift
**Problem**: CSV AME IV memiliki kolom yang ter-shift (DIVISI=AME, Blok=IV)

**Fix** di `src/ingestion.py`:
```python
def load_ame_iv_data(filepath: Path) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep=';', decimal=',')
    # Fix column alignment
    df_fixed = pd.DataFrame({
        'blok': df['blok_b'],
        'ndre125': df['klassndre12025'],
        'klassndre12025': df['ket'],
        # ... mapping lainnya
    })
```

### Issue 2: Block Normalization
**Problem**: Format blok berbeda (D001A vs K18A)

**Fix** di `validation_all_presets.py`:
```python
def normalize_block(blok: str) -> str:
    if len(blok) >= 2:
        letter = blok[0]
        digits = ''.join(c for c in blok[1:] if c.isdigit())
        if digits:
            return f"{letter}{int(digits):02d}"
    return blok
```

### Issue 3: Unicode Encoding (Windows)
**Problem**: Error saat print karakter khusus

**Fix**:
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

## 🎨 FITUR DASHBOARD HTML

### Multi-Tab Navigation
- Tab AME II / AME IV terpisah
- Tab per preset (Konservatif, Standar, Agresif)

### Lightbox Zoom
- Klik gambar untuk fullscreen
- Keyboard: Arrow keys untuk navigasi, +/- untuk zoom, ESC untuk close
- Mouse wheel untuk zoom
- Drag untuk pan

### Panduan Interpretasi Warna
- Legend warna MERAH/ORANYE/KUNING/HIJAU
- Penjelasan setiap kategori stress

---

## 📝 GIT STATUS

### Last Commit
```
fcb1000 (HEAD -> main, origin/main) 
Initial commit: POAC v3.3 - Algoritma Cincin Api Ganoderma Detection
```

### Pending Changes (belum di-commit)
- `validation_all_presets.py` - Script validasi semua preset
- `output/validation_all_presets/` - Hasil validasi terbaru
- `context/CHECKPOINT_PROJECT_POAC_v3.3.md` - File ini

### Untuk Commit
```powershell
cd d:\PythonProjects\simulasi_poac
git add .
git commit -m "Add validation all presets & checkpoint documentation"
git push origin main
```

---

## 🔮 RENCANA PENGEMBANGAN SELANJUTNYA

### Short-term (Implementasi Segera)
1. [x] **3 Metode deteksi adaptif** - Age-Based, Ensemble+Age, Ensemble Pure ✅
2. [x] **Dokumen kesimpulan & repositioning** ✅
3. [ ] Training tim survey tentang interpretasi output
4. [ ] Setup feedback loop untuk validasi lapangan

### Medium-term (3-6 bulan)
1. [ ] **Integrasi data gambut** - Kedalaman gambut dari survey tanah/GIS
2. [ ] **Integrasi data drainase** - Kondisi genangan dari observasi
3. [ ] **Riwayat serangan blok** - Data sensus historis per blok
4. [ ] Kalibrasi threshold per divisi berdasarkan feedback lapangan
5. [ ] Export ke format GIS (GeoJSON, Shapefile)

### Long-term (6-12 bulan)
1. [ ] **Multi-source fusion model** - ML dengan data lengkap
2. [ ] Continuous learning dari validasi lapangan
3. [ ] Mobile app untuk field verification
4. [ ] Real-time monitoring system
5. [ ] Multi-estate dashboard

### Data Tambahan yang Diprioritaskan

| Prioritas | Data | Sumber | Status |
|-----------|------|--------|--------|
| ⭐⭐⭐ | Kedalaman gambut | Survey tanah / GIS | Belum tersedia |
| ⭐⭐⭐ | Kondisi drainase | Observasi lapangan | Belum tersedia |
| ⭐⭐⭐ | Riwayat serangan | Sensus historis | Perlu dikompilasi |
| ⭐⭐ | Curah hujan | Stasiun cuaca | Dapat diperoleh |
| ⭐⭐ | Data hara tanah | Soil test | Perlu survey |
| ⭐ | Topografi/DEM | GIS | Dapat diperoleh |


---

## 📞 CONTACT & NOTES

### Untuk AI Agent Baru
1. **Baca file ini dulu** sebelum melakukan perubahan
2. **Cek struktur folder** - ada 2 level (simulasi_poac dan poac_sim)
3. **Data AME IV** perlu special handling (kolom shift)
4. **Validasi penting** - selalu bandingkan dengan sensus
5. **Git remote** sudah terkoneksi ke GitHub

### File Penting untuk Dibaca
1. `context/SOFTWARE REQUIREMENTS SPECIFICATION (SRS).md` - Requirements lengkap
2. `context/KESIMPULAN_ANALISIS_POAC_v3.3.md` - **Kesimpulan & repositioning** ← BARU
3. `poac_sim/docs/METODOLOGI_ALGORITMA_CINCIN_API.md` - Metodologi teknis
4. `poac_sim/src/adaptive_detection.py` - Modul metode adaptif ← BARU
5. `poac_sim/run_all_presets.py` - Main entry point (~3300 baris)
6. `poac_sim/validation_adaptive_methods.py` - Validasi metode adaptif ← BARU

### Quick Commands
```powershell
# Jalankan dashboard (termasuk metode adaptif)
cd d:\PythonProjects\simulasi_poac\poac_sim
python run_all_presets.py --divisi MULTI

# Jalankan validasi metode adaptif
python validation_adaptive_methods.py

# Git status
cd d:\PythonProjects\simulasi_poac
git status
git log --oneline -5
```

---

**📅 Last Updated**: 11 Desember 2025  
**✍️ Updated By**: Gemini 2.5 Pro (Antigravity)  
**🔄 Session**: Implementasi Metode Adaptif + Kesimpulan + Repositioning Algoritma

