# 🔥 POAC Cincin Api Dashboard (V8)

**Precision Oil Palm Agriculture Control** - Sistem Deteksi Dini & Mitigasi Ganoderma Berbasis Analisis Spasial & Finansial.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)
![Version](https://img.shields.io/badge/Version-V8%20(Hybrid)-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Deskripsi

**POAC Cincin Api Dashboard** adalah platform analitik interaktif yang dirancang untuk mendeteksi, memvisualisasikan, dan memitigasi penyebaran penyakit Ganoderma di perkebunan kelapa sawit. Sistem ini menggabungkan analisis citra satelit (NDRE), sensus visual lapangan, dan data produksi (Quick Count Yield) untuk memberikan peringatan dini (**Early Warning System**) yang akurat.

Fitur utama dari dashboard ini adalah **"Vanishing Yield Alert"**, sebuah sistem diagnosa klinis yang mengidentifikasi degradasi produktivitas tak kasat mata akibat kerusakan akar, jauh sebelum gejala visual muncul pada kanopi.

## 🚀 Fitur Utama

### 1. 🚨 Vanishing Yield Alert System
Sistem pendeteksi anomali produksi yang membagi status kesehatan blok ke dalam 4 fase kritis:
*   **Fase 1: Silent Infection (Inkubasi)** - Serangan tinggi tapi produksi masih normal. *Golden Period* intervensi.
*   **Fase 2: Root Degradation (Stres Akar)** - Penurunan yield awal (-5% s/d -15%) & stres penyerapan nutrisi.
*   **Fase 3: Cryptic Collapse (Bahaya Senyap)** - **Yield anjlok drastis** namun gejala visual minim. *The Silent Killer*.
*   **Fase 4: Insolvency (Kebangkrutan)** - SPH < 100 atau sisa umur operasional < 3 tahun.

### 2. 🗺️ Peta Kluster Cincin Api (Interaktif)
Visualisasi spasial berbasis **LeafletJS** yang memetakan setiap pohon ke dalam status risiko:
*   🔴 **MERAH (Inti Infeksi):** Pohon sakit/mati yang menjadi sumber spora.
*   🟠 **ORANYE (Cincin Api):** Zona penyebaran aktif di sekitar inti infeksi (High Risk).
*   🟡 **KUNING (Suspect):** Tanaman dengan anomali vigor yang memerlukan pemeriksaan.
*   🟢 **HIJAU (Sehat):** Tanaman produktif yang perlu dilindungi.

### 3. 📉 Analisis Yield Drop (YoY)
Analisis mendalam tren penurunan produksi tahunan (**Year-on-Year**) untuk memisahkan fluktuasi cuaca biasa dari dampak kerusakan sistem perakaran (Degradasi Biologis).

### 4. 🔮 3-Scenario Reality Check
Simulasi dampak finansial berdasarkan tiga skenario:
*   **Konservatif (Status Quo):** Asumsi penyakit diam (Baseline).
*   **Moderat (Realistis):** Laju infeksi historical (2.5% per tahun).
*   **Agresif (Worst Case):** Eskalasi eksponensial tanpa mitigasi.

## 🛠️ Metodologi V8 (Hybrid)

Algoritma V8 menggabungkan dua pendekatan untuk akurasi maksimal:
1.  **Z-Score Hibrida:** Menggabungkan skor NDRE (Kesehatan Kanopi) dan Sensus (Gejala Batang) untuk mengurangi *False Negative* dan *False Positive*.
2.  **Spatial Clustering:** Analisis tetangga terdekat (Nearest Neighbor) untuk mengidentifikasi pola penyebaran "Cincin Api" yang khas pada Ganoderma.

[Baca Penjelasan Lengkap Metodologi V8](./METHODOLOGY_V8_EXPLAINED.md)

## 📂 Struktur Proyek

```
dashboard-cincin-api/
├── data/
│   ├── output/
│   │   └── dashboard_cincin_api_INTERACTIVE_FULL.html  # 👈 DASHBOARD UTAMA
│   └── ...
├── src/
│   ├── generators/         # Skrip pembuatan data
│   └── ...
├── METHODOLOGY_V8_EXPLAINED.md  # Dokumentasi Teknis
├── README.md                    # File ini
└── ...
```

## 💻 Cara Penggunaan

1.  **Buka Dashboard:**
    Navigasi ke folder `data/output/` dan buka file `dashboard_cincin_api_INTERACTIVE_FULL.html` menggunakan browser modern (Chrome/Edge/Firefox).
2.  **Pilih Blok:**
    Gunakan menu dropdown di sebelah kiri (Blok A) dan kanan (Blok B) untuk membandingkan performa dua blok.
3.  **Analisis:**
    *   Perhatikan indikator **Vanishing Yield Alert**. Klik badge status untuk melihat **Diagnosa Klinis**.
    *   Cek bagian **Peta Kluster** untuk melihat sebaran titik merah/oranye.
    *   Klik tombol **"3Y DROP"** (jika muncul) untuk melihat detail degradasi yield per tahun.

## 🤝 Kontribusi

Silakan ajukan *Pull Request* atau *Issue* untuk saran pengembangan fitur atau perbaikan bug.

## 📄 Lisensi

Project ini dilisensikan di bawah **MIT License**.

---
*Dikembangkan oleh Mastoro Shadiq & Tim POAC*
