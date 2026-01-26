# 🔥 POAC v3.3 - Algoritma Cincin Api

**Precision Oil Palm Agriculture Control** - Sistem Deteksi Kluster Ganoderma dengan Auto-Tuning

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📋 Deskripsi

Algoritma Cincin Api adalah sistem deteksi kluster serangan Ganoderma pada perkebunan kelapa sawit berbasis analisis spasial hexagonal. Sistem ini menggunakan:

- **Ranking Relatif (Percentile Rank)** - Normalisasi data NDRE per blok
- **Elbow Method Auto-Tuning** - Penentuan threshold optimal secara otomatis
- **Analisis Tetangga Hexagonal** - Deteksi kluster berdasarkan pola tanam mata lima
- **Klasifikasi 4-Tier** - MERAH, KUNING, ORANYE, HIJAU

## 🎨 Klasifikasi Status

| Status | Emoji | Kriteria | Tindakan |
|--------|-------|----------|----------|
| **MERAH** | 🔴 | Persentil ≤ threshold, ≥3 tetangga sakit | Sanitasi segera |
| **KUNING** | 🟡 | Persentil ≤ threshold, 1-2 tetangga sakit | Monitoring ketat |
| **ORANYE** | 🟠 | Persentil ≤ threshold, 0 tetangga sakit | Investigasi |
| **HIJAU** | 🟢 | Persentil > threshold | Normal |

## 🚀 Quick Start

### Instalasi

```bash
# Clone repository
git clone https://github.com/mastoroshadiq-prog/dashboard-cincin-api.git
cd dashboard-cincin-api

# Install dependencies
pip install -r requirements.txt
```

### Menjalankan Analisis

```bash
# Default (auto-tune dengan preset standar)
python run_cincin_api.py

# Menggunakan preset
python run_cincin_api.py --preset konservatif
python run_cincin_api.py --preset standar
python run_cincin_api.py --preset agresif

# Manual threshold
python run_cincin_api.py -t 0.20

# Override parameter
python run_cincin_api.py --min-neighbors 4 --threshold-max 0.40

# Lihat konfigurasi
python run_cincin_api.py --show-config
```

## 📁 Struktur Proyek

```
poac_sim/
├── config.py               # Konfigurasi & presets
├── run_cincin_api.py       # Entry point utama
├── main.py                 # Entry point Z-Score (legacy)
├── src/
│   ├── ingestion.py        # Data loading & cleaning
│   ├── statistics.py       # Z-Score calculation
│   ├── spatial.py          # Hexagonal geometry
│   ├── clustering.py       # Algoritma Cincin Api
│   ├── dashboard.py        # Visualisasi
│   ├── report_generator.py # README & HTML report
│   └── engine.py           # Simulation engine
├── data/
│   ├── input/              # Data CSV input
│   └── output/             # Hasil analisis
└── requirements.txt
```

## ⚙️ Konfigurasi

### Preset Tersedia

| Preset | Threshold Range | Min Neighbors | Deskripsi |
|--------|-----------------|---------------|-----------|
| **konservatif** | 3% - 15% | 4 | Deteksi ketat, hanya kluster padat |
| **standar** | 5% - 30% | 3 | Setting default, seimbang |
| **agresif** | 10% - 50% | 2 | Deteksi luas, threshold tinggi |

### Kustomisasi

Edit `config.py` untuk menyesuaikan:

```python
CINCIN_API_CONFIG = {
    "threshold_min": 0.05,      # Batas bawah simulasi
    "threshold_max": 0.30,      # Batas atas simulasi
    "threshold_step": 0.05,     # Step increment
    "min_sick_neighbors": 3,    # Min tetangga sakit untuk MERAH
    "top_n_blocks": 10,         # Jumlah top block visualisasi
    ...
}
```

## 📊 Output

Setiap run menghasilkan folder dengan format `YYYYMMDD_HHMM_{preset}_t{threshold}_n{neighbors}`:

```
20251209_1530_standar_t30_n3/
├── dashboard_main.png          # Dashboard utama
├── dashboard_block_heatmap.png # Heatmap per blok
├── dashboard_elbow.png         # Elbow method chart
├── top10_XX_blok_YYY.png      # Detail blok terparah
├── hasil_klasifikasi_lengkap.csv
├── target_prioritas.csv
├── ringkasan_per_blok.csv
├── run_config.json            # Konfigurasi (untuk reproduksi)
├── README.md                  # Panduan interpretasi
├── laporan_mandor.txt         # Laporan untuk mandor
└── report.html                # 🌐 HTML Report interaktif
```

## 📈 Contoh Hasil

### Distribusi Status (Preset Standar)
- 🔴 MERAH: ~11,000 pohon (12%)
- 🟡 KUNING: ~14,000 pohon (15%)
- 🟠 ORANYE: ~3,000 pohon (3%)
- 🟢 HIJAU: ~67,000 pohon (70%)

## 🔧 Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib

## 📖 Dokumentasi

- [Panduan Teknis Algoritma Cincin Api](context/Panduan_Teknis_Algoritma_Cincin_Api.md)
- [Software Requirements Specification](context/SOFTWARE%20REQUIREMENTS%20SPECIFICATION%20(SRS).md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Mastoro Shadiq** - *Initial work*

---

*POAC v3.3 - Precision Oil Palm Agriculture Control*
