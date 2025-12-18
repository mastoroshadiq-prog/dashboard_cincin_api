# Laporan Implementasi: Gradient Elbow + Consensus Voting

**Tanggal:** 18 Desember 2024  
**Kepada:** Konsultan POAC v3.3  
**Status:** DRAFT - Menunggu Feedback

---

## Executive Summary

Implementasi **Gradient Elbow (Kneedle)** dan **Consensus Voting** telah selesai sesuai Technical Guideline. Namun, hasil menunjukkan **under-detection** yang signifikan dibanding Ground Truth.

| Metric | Nilai |
|--------|-------|
| Ground Truth (Sensus) | **5,969** pohon terinfeksi |
| Consensus Voting Result | **1,022** pohon |
| Gap | **-82.9%** (under-detect) |

---

## 1. Implementasi yang Dilakukan

### 1.1 Kneedle Algorithm

Mengganti metode `efficiency` dengan algoritma Kneedle untuk find_optimal_threshold():

```
- Normalize X (threshold) dan Y (clusters) ke skala 0-1
- Hitung jarak perpendicular ke garis diagonal
- Pilih titik dengan jarak maksimum (knee point)
```

### 1.2 Consensus Voting

Menjalankan 3 preset dan filter berdasarkan voting:

```
Pohon APPROVED jika di-flag MERAH oleh ≥2 preset
```

### 1.3 Preset Ranges (Capped)

| Preset | Min | Max |
|--------|-----|-----|
| Konservatif | 1% | 10% |
| Standar | 10% | 20% |
| Agresif | 15% | **30%** (was 50%) |

---

## 2. Hasil Testing

### 2.1 Threshold Selection

| Preset | Efficiency (Old) | Gradient (New) |
|--------|-----------------|----------------|
| Konservatif | 10% | **1%** |
| Standar | 20% | **10%** |
| Agresif | 30% | **15%** |

**Finding:** Gradient memilih threshold di **batas bawah** range.

### 2.2 Vote Distribution

| Votes | Count | % |
|-------|-------|---|
| 3 (All preset) | 25 | 0.0% |
| 2 (Majority) | 997 | 1.0% |
| 1 | 4,751 | 5.0% |
| 0 | 89,257 | 93.9% |

**APPROVED (≥2 votes): 1,022**

---

## 3. Perbandingan dengan Ground Truth

### AME II Ground Truth

| Kategori | Jumlah |
|----------|--------|
| Total Pohon | 95,055 |
| Stadium 1-2 | 4,733 |
| Stadium 3-4 | 1,236 |
| **TOTAL GANO** | **5,969** |

### Comparison

| Pendekatan | Deteksi | vs GT |
|------------|---------|-------|
| Efficiency (Old) | 40,455 | **+578%** over |
| **Gradient + Consensus** | **1,022** | **-83%** under |
| Target Ideal | ~5,969 | 0% |

---

## 4. Root Cause Analysis

### Mengapa Under-Detect?

1. **Kneedle memilih threshold rendah** karena kurva clusters vs threshold relatif linear (tidak ada knee point yang jelas)

2. **Range preset terlalu sempit** dengan CAP yang ketat

3. **Consensus voting (min_votes=2)** terlalu strict

---

## 5. Pertanyaan untuk Konsultan

1. Apakah target deteksi sebaiknya **mendekati GT (~6,000)** atau ada tolerance yang diterima?

2. Jika perlu adjustment, mana yang direkomendasikan:
   - Naikkan threshold range preset
   - Turunkan min_votes dari 2 ke 1
   - Gunakan single preset tanpa consensus

3. Apakah perlu **hybrid approach**: Gradient untuk memilih threshold, tapi dengan **floor minimum** agar tidak terlalu rendah?

---

## Lampiran

### File yang Dimodifikasi

- `src/clustering.py` - Kneedle + Consensus Voting
- `config.py` - New settings + capped ranges

### Test Scripts

- `test_gradient_consensus.py`
- `compare_with_gt.py`

---

*Dokumen ini menunggu feedback dari konsultan sebelum adjustment lebih lanjut.*
