# 📊 Integrasi Data Cost Control ke Dashboard Cincin Api
## Dokumen Penjelasan 3 Misi Strategis

**Versi:** 1.0  
**Tanggal:** Desember 2025  
**Penulis:** Tim POAC v3.3

---

## 🎯 Latar Belakang

Algoritma Cincin Api saat ini hanya menggunakan **data NDRE dari drone** untuk mendeteksi potensi infeksi Ganoderma. Hasil validasi menunjukkan bahwa:

- ❌ **Over-detection**: Algoritma mendeteksi ~30% sementara sensus lapangan hanya ~6%
- ❌ **NDRE tidak spesifik**: Indeks vegetasi juga turun karena faktor non-Ganoderma

Untuk meningkatkan **akurasi** dan **value bisnis** dari sistem, diperlukan integrasi dengan **data Cost Control** yang sudah tersedia di perusahaan.

---

## 📁 Data Cost Control Tersedia

| File | Isi | Kegunaan |
|------|-----|----------|
| `data_baru.csv` | Data Real Tanam + Sensus Ganoderma | Ground truth, rasio sisipan, total pohon |
| `tabelNDREnew.csv` | Data NDRE per pohon AME II | Input algoritma |
| `AME_IV.csv` | Data NDRE per pohon AME IV | Input algoritma |

**Kolom Penting di `data_baru.csv`:**
- `TOTAL_PKK` - Jumlah pohon menurut data buku
- `SISIP` + `SISIP_KENTOSAN` - Jumlah pohon sisipan
- `STADIUM 3&4` - Pohon terinfeksi parah (ground truth)
- `% SERANGAN` - Persentase serangan menurut sensus

---

## 🚀 Tiga Misi Strategis

### MISI 1: Ground Truth Check (Early Detection Report)

```
┌─────────────────────────────────────────────────────────────────────┐
│  MENGAPA PERLU?                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Sebelumnya: Tidak ada cara untuk mengetahui apakah deteksi         │
│  algoritma akurat atau tidak.                                       │
│                                                                     │
│  Setelah integrasi: Kita bisa membandingkan hasil algoritma         │
│  dengan data sensus lapangan secara otomatis!                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Nilai Bisnis:**

| Kategori | Artinya | Aksi |
|----------|---------|------|
| **EARLY_DETECT** | Algoritma > Sensus | 🏆 TEMUAN EMAS! Infeksi baru yang lolos sensus manual |
| **MATCH** | Algoritma ≈ Sensus | ✅ Validasi berhasil |
| **UNDER_DETECT** | Algoritma < Sensus | ⚠️ Perlu kalibrasi atau pohon sudah dibongkar |

**Output:**
- `data/output/early_detection/early_detection_report.html`
- Daftar blok yang perlu disurvey ulang

---

### MISI 2: Split-Merge Bias Correction

```
┌─────────────────────────────────────────────────────────────────────┐
│  MENGAPA PERLU?                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MASALAH: Blok dengan banyak sisipan memiliki tanaman dengan        │
│  umur berbeda. Tanaman muda secara alami memiliki NDRE lebih        │
│  rendah karena kanopi belum penuh.                                  │
│                                                                     │
│  AKIBAT: Algoritma salah menganggap tanaman muda sebagai "sakit"    │
│  hanya karena NDRE-nya berbeda dengan tanaman tua di sekitarnya.    │
│                                                                     │
│  SOLUSI: Hitung ranking persentil TERPISAH untuk kelompok umur      │
│  berbeda, lalu gabungkan kembali (Split-Merge).                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Ilustrasi:**

```
SEBELUM SPLIT-MERGE:                 SESUDAH SPLIT-MERGE:
─────────────────────                ─────────────────────
                                     
Semua pohon di-ranking bersama:      Ranking terpisah per kelompok:
                                     
  Pohon Tua (tinggi)    ┐            Grup TUA:
  Pohon Tua (tinggi)    │ NDRE       ├─ Ranking internal
  Pohon Tua (sedang)    │ tinggi     └─ Persentil 0-1
  ─────────────────     │            
  Pohon Muda (rendah)   │ NDRE       Grup MUDA:
  Pohon Muda (rendah)   ┘ rendah     ├─ Ranking internal
                                     └─ Persentil 0-1
❌ Muda dianggap SAKIT!              
                                     ✅ Muda dibandingkan dengan
                                        sesama muda saja!
```

**Data Dibutuhkan:**
- ⚠️ Saat ini: Hanya ada tahun tanam per BLOK
- ✅ Idealnya: Koordinat pohon sisipan vs pohon induk

**Output:**
- `data/output/split_merge_analysis/split_merge_report.html`
- Fungsi `calculate_percentile_rank_split_merge()` di `src/clustering.py`

---

### MISI 3: Ghost Tree Detection (Asset Audit)

```
┌─────────────────────────────────────────────────────────────────────┐
│  MENGAPA PERLU?                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MASALAH: Data buku mencatat 100.000 pohon, tapi drone hanya        │
│  mendeteksi 95.000 pohon. Kemana 5.000 pohon sisanya?               │
│                                                                     │
│  KEMUNGKINAN:                                                       │
│  1. Pohon mati/tumbang tidak dilaporkan (Ghost Trees)               │
│  2. Pohon di area tidak tercover drone                              │
│  3. Kesalahan data administratif                                    │
│                                                                     │
│  NILAI BISNIS: Finance dan Management sangat membutuhkan            │
│  informasi ini untuk audit aset dan perencanaan replanting!         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Nilai Bisnis:**

| Stakeholder | Kebutuhan | Bagaimana Misi Ini Membantu |
|-------------|-----------|----------------------------|
| **Finance** | Audit aset pohon | Mengetahui selisih data buku vs aktual |
| **Management** | Perencanaan replanting | Identifikasi blok dengan kehilangan tinggi |
| **Wk. Direktur** | Akuntabilitas lapangan | Laporan per blok dengan anomaly |

**Output:**
- `data/output/ghost_tree_audit/ghost_tree_audit.html`
- Daftar blok dengan selisih >5% atau >10%

---

## 📈 Dampak Implementasi

### Sebelum Integrasi
```
Data NDRE → Algoritma → Deteksi (30%)
                           ↓
                    "Apakah akurat?"
                    "Tidak tahu..." ❓
```

### Setelah Integrasi
```
Data NDRE ─────→ Algoritma ─────→ Deteksi
                      ↓
Data Cost Control ─→ Validasi ─→ Confidence Level
                      │
                      ├─→ MISI 1: Ground Truth Check
                      ├─→ MISI 2: Bias Correction
                      └─→ MISI 3: Asset Audit
```

---

## 📊 Ringkasan Hasil

| Misi | Script | Output | Status |
|------|--------|--------|--------|
| **Ground Truth** | `early_detection_report.py` | HTML + CSV | ✅ Berhasil |
| **Split-Merge** | `split_merge_analysis.py` | HTML + CSV | ⚠️ Butuh data T_Tanam per pohon |
| **Ghost Tree** | `ghost_tree_audit.py` | HTML + CSV | ✅ Berhasil |

---

## 🔮 Langkah Selanjutnya

1. **Validasi Lapangan**: Gunakan output EARLY_DETECT sebagai prioritas survey
2. **Pengumpulan Data**: Kumpulkan koordinat pohon sisipan untuk split-merge yang lebih akurat
3. **Investigasi Ghost Tree**: Follow-up blok dengan selisih >10%
4. **Continuous Improvement**: Gunakan hasil survey untuk kalibrasi algoritma

---

*Dokumen ini adalah bagian dari POAC v3.3 - Precision Oil Palm Agriculture Control*

**Script Terkait:**
- `poac_sim/early_detection_report.py`
- `poac_sim/split_merge_analysis.py`
- `poac_sim/ghost_tree_audit.py`
- `poac_sim/src/cost_control_loader.py`
