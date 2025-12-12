# 📋 Panduan Menjalankan Analisis POAC v3.3
## Algoritma Cincin Api - Quick Reference Guide

**Versi:** 3.3  
**Update:** Desember 2025

---

## 📁 Struktur File

```
poac_sim/
├── config.py                    # Konfigurasi utama & preset
├── run_all_presets.py          # Dashboard multi-preset
├── run_multi_divisi.py         # Analisis multi-divisi
├── validation_adaptive_methods.py  # Validasi metode adaptif
├── early_detection_report.py   # Misi 1: Ground Truth Check
├── ghost_tree_audit.py         # Misi 3: Audit Aset
├── split_merge_analysis.py     # Misi 2: Koreksi Bias Umur
├── src/
│   ├── ingestion.py            # Load & clean data
│   ├── clustering.py           # Algoritma utama
│   ├── adaptive_detection.py   # Metode adaptif
│   └── cost_control_loader.py  # Parser data_baru.csv
└── data/
    ├── input/                  # Data input
    └── output/                 # Hasil analisis
```

---

## 🚀 METODE 1: Analisis Multi-Preset (Dashboard Utama)

**Tujuan:** Menjalankan 3 preset (Konservatif, Standar, Agresif) + metode adaptif

**Script:** `run_all_presets.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Default: AME II saja
python run_all_presets.py

# Analisis AME IV saja
python run_all_presets.py --divisi AME_IV

# Analisis semua divisi (gabung jadi satu)
python run_all_presets.py --divisi ALL

# Analisis multi-divisi (terpisah per divisi dengan tab)
python run_all_presets.py --divisi MULTI
```

### Options:

| Option | Values | Default | Deskripsi |
|--------|--------|---------|-----------|
| `--divisi` | `AME_II`, `AME_IV`, `ALL`, `MULTI` | `AME_II` | Divisi yang dianalisis |

### Output:
- `data/output/multi_preset_report_<divisi>.html` - Dashboard visual
- Visualisasi superimpose semua preset

---

## 🚀 METODE 2: Analisis Multi-Divisi

**Tujuan:** Menjalankan analisis untuk AME II dan AME IV dengan preset tertentu

**Script:** `run_multi_divisi.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Default: preset standar
python run_multi_divisi.py

# Dengan preset konservatif (untuk blok tua)
python run_multi_divisi.py --preset konservatif

# Dengan preset agresif (untuk blok muda)
python run_multi_divisi.py --preset agresif
```

### Options:

| Option | Values | Default | Deskripsi |
|--------|--------|---------|-----------|
| `--preset` | `konservatif`, `standar`, `agresif` | `standar` | Konfigurasi preset |

### Karakteristik Preset:

| Preset | Threshold Max | Min Neighbors | Cocok Untuk |
|--------|---------------|---------------|-------------|
| `konservatif` | 15% | 4 | Blok tua (>10 tahun) |
| `standar` | 30% | 3 | Mayoritas blok |
| `agresif` | 40% | 2 | Blok muda (<5 tahun) |

### Output:
- `data/output/multi_divisi_report.html` - Dashboard gabungan

---

## 🚀 METODE 3: Validasi Metode Adaptif

**Tujuan:** Membandingkan 3 metode adaptif dengan data sensus

**Script:** `validation_adaptive_methods.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Jalankan validasi (tidak ada options)
python validation_adaptive_methods.py
```

### Output:
- `data/output/adaptive_validation/validation_summary.html`
- `data/output/adaptive_validation/validation_summary.md`
- `data/output/adaptive_validation/metrics_per_method.csv`

### 3 Metode Adaptif yang Divalidasi:
1. **Age-Based Preset Selection** - Pilih preset otomatis berdasarkan umur blok
2. **Ensemble + Age Weight** - Voting dari 3 preset + bobot umur
3. **Ensemble Pure** - Voting murni tanpa bobot umur

---

## 🚀 METODE 4: Ground Truth Check (Misi 1)

**Tujuan:** Membandingkan hasil algoritma vs data sensus lapangan

**Script:** `early_detection_report.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Jalankan report (tidak ada options, otomatis AME II + AME IV)
python early_detection_report.py
```

### Output:
- `data/output/early_detection/early_detection_report.html`
- `data/output/early_detection/early_detection_report.csv`

### Kategori Output:

| Kategori | Kondisi | Artinya |
|----------|---------|---------|
| `EARLY_DETECT` | Algoritma > Sensus + 2% | 🏆 Potensi temuan baru! |
| `MATCH` | Selisih ≤ 2% | ✅ Validasi berhasil |
| `UNDER_DETECT` | Algoritma < Sensus - 2% | ⚠️ Perlu investigasi |

---

## 🚀 METODE 5: Ghost Tree Audit (Misi 3)

**Tujuan:** Membandingkan jumlah pohon buku vs deteksi drone

**Script:** `ghost_tree_audit.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Jalankan audit (tidak ada options)
python ghost_tree_audit.py
```

### Output:
- `data/output/ghost_tree_audit/ghost_tree_audit.html`
- `data/output/ghost_tree_audit/ghost_tree_audit.csv`

### Kategori Output:

| Kategori | Kondisi | Artinya |
|----------|---------|---------|
| `OK` | Selisih ≤ 5% | ✅ Data konsisten |
| `GHOST_TREES` | Buku > Drone + 5% | 👻 Pohon hilang di lapangan |
| `EXTRA_TREES` | Drone > Buku + 5% | ➕ Sisipan tidak tercatat |

---

## 🚀 METODE 6: Split-Merge Analysis (Misi 2)

**Tujuan:** Analisis perbandingan dengan/tanpa koreksi bias umur

**Script:** `split_merge_analysis.py`

### Contoh Penggunaan:

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Jalankan analisis (tidak ada options)
python split_merge_analysis.py
```

### Output:
- `data/output/split_merge_analysis/split_merge_report.html`
- `data/output/split_merge_analysis/comparison_AME002_AME_II.csv`
- `data/output/split_merge_analysis/comparison_AME004_AME_IV.csv`

### Logika Split-Merge:
```
TANPA SPLIT-MERGE:
┌─────────────────────┐
│ Semua pohon di-rank │
│ bersama dalam blok  │
│ ❌ Sisipan false+   │
└─────────────────────┘

DENGAN SPLIT-MERGE:
┌─────────────────────┐
│ Pokok Utama: rank   │
│ terpisah            │
├─────────────────────┤
│ Sisipan: rank       │
│ terpisah            │
│ ✅ Fair comparison  │
└─────────────────────┘
```

---

## ⚙️ KONFIGURASI UTAMA (config.py)

```python
# Konfigurasi default
CINCIN_API_CONFIG = {
    'threshold_min': 0.05,      # Min threshold simulasi (5%)
    'threshold_max': 0.30,      # Max threshold simulasi (30%)
    'threshold_step': 0.05,     # Step increment (5%)
    'min_sick_neighbors': 3,    # Min tetangga sakit untuk MERAH
    'min_clusters_for_valid': 10,  # Min kluster valid
    'elbow_method': 'efficiency',  # atau 'gradient'
}

# Preset konfigurasi
CINCIN_API_PRESETS = {
    'konservatif': {
        'threshold_max': 0.15,
        'min_sick_neighbors': 4,
    },
    'standar': {
        'threshold_max': 0.30,
        'min_sick_neighbors': 3,
    },
    'agresif': {
        'threshold_max': 0.40,
        'min_sick_neighbors': 2,
    }
}
```

---

## 📊 DATA INPUT

| File | Divisi | Deskripsi |
|------|--------|-----------|
| `tabelNDREnew.csv` | AME II | Data NDRE per pohon |
| `AME_IV.csv` | AME IV | Data NDRE per pohon |
| `data_baru.csv` | Semua | Data cost control (sensus, sisipan, total pohon) |
| `ame_2_4_hasil_sensus.csv` | Semua | Data sensus historis |

---

## 🎯 QUICK START - Skenario Umum

### Skenario 1: Analisis Lengkap Pertama Kali
```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# 1. Dashboard utama dengan semua preset
python run_all_presets.py --divisi MULTI

# 2. Validasi hasil dengan sensus
python early_detection_report.py

# 3. Audit aset pohon
python ghost_tree_audit.py

# 4. Analisis split-merge
python split_merge_analysis.py
```

### Skenario 2: Fokus Satu Divisi (AME II)
```powershell
python run_all_presets.py --divisi AME_II
```

### Skenario 3: Analisis dengan Preset Konservatif (Blok Tua)
```powershell
python run_multi_divisi.py --preset konservatif
```

### Skenario 4: Validasi Metode Adaptif
```powershell
python validation_adaptive_methods.py
```

---

## 📂 Membuka Hasil Report

```powershell
cd d:\PythonProjects\simulasi_poac\poac_sim

# Dashboard multi-preset
start data\output\multi_preset_report_AME_II.html

# Early Detection Report  
start data\output\early_detection\early_detection_report.html

# Ghost Tree Audit
start data\output\ghost_tree_audit\ghost_tree_audit.html

# Split-Merge Analysis
start data\output\split_merge_analysis\split_merge_report.html

# Validasi Adaptif
start data\output\adaptive_validation\validation_summary.html
```

---

## 📝 CATATAN PENTING

1. **Pastikan data input tersedia** di folder `data/input/`
2. **Python 3.10+** dengan pandas, numpy, matplotlib terinstall
3. Semua output tersimpan di `data/output/`
4. Split-merge saat ini masih terpisah dari algoritma utama (belum terintegrasi)
5. Untuk troubleshooting, cek log di console

---

*Dokumen ini adalah bagian dari POAC v3.3 - Precision Oil Palm Agriculture Control*
