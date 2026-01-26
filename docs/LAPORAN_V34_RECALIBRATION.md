# POAC v3.4 Recalibration Report

**Tanggal:** 18 Desember 2024  
**Status:** Testing Complete - Needs Further Tuning

---

## Executive Summary

Implementasi v3.4 dengan **Widened Ranges** telah dilakukan. Hasil testing menunjukkan:

| Scenario | Result | vs GT (5,969) | Status |
|----------|--------|---------------|--------|
| v3.3 (Capped + min_votes=2) | 1,022 | -83% | ❌ UNDER |
| **v3.4 A (Wide + min_votes=2)** | **1,022** | **-83%** | ❌ UNDER |
| **v3.4 B (Wide + min_votes=1)** | **9,697** | **+62%** | ⚠️ OVER |

**Target Range:** 4,500 - 8,000

---

## Perubahan yang Dilakukan

### Config v3.4 (Widened Ranges):

| Preset | v3.3 | v3.4 |
|--------|------|------|
| Konservatif | 1-10% | 5-20% |
| Standar | 10-20% | 10-40% |
| Agresif | 15-30% | 20-60% |

---

## Hasil Detail

### Threshold Selection (Kneedle):

| Preset | Range | Kneedle Selects |
|--------|-------|-----------------|
| Konservatif | 5-20% | ~5% |
| Standar | 10-40% | ~10% |
| Agresif | 20-60% | **20%** |

### Single Preset Results:

- **Agresif (20%):** 9,697 MERAH (+62% over GT)

---

## Analisis

1. **Widening ranges tidak mengubah hasil Scenario A**
   - Kneedle masih memilih threshold rendah
   - Consensus Voting (min_votes=2) masih sangat ketat

2. **Scenario B (Union) terlalu longgar**
   - 9,697 melebihi batas atas 8,000
   - +62% dari GT

3. **Gap besar antara A dan B**
   - A: 1,022
   - B: 9,697
   - Tidak ada "sweet spot" diantaranya

---

## Opsi Selanjutnya

### Opsi 1: Hibrid Voting (1.5 votes concept)
- Gunakan weighted voting berdasarkan konfiden preset

### Opsi 2: Single Preset Tuning
- Gunakan hanya **Standar** dengan threshold manual ~25%

### Opsi 3: Adjust Kneedle + Constraint
- Tambah minimum threshold floor agar tidak terlalu rendah

---

## Pertanyaan untuk Konsultan

1. Apakah 9,697 (Scenario B) dapat diterima dengan toleransi +62%?
2. Atau haruskah dicoba pendekatan single preset?
3. Apakah ada formula hibrid untuk voting yang direkomendasikan?

---

*Menunggu arahan konsultan untuk langkah selanjutnya.*
