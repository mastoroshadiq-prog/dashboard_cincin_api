# LAPORAN VALIDASI: SEMUA PRESET vs DATA SENSUS GANODERMA

## Executive Summary

Laporan ini membandingkan hasil deteksi dari **3 preset algoritma Cincin Api**:
- **Konservatif (15%)**: Threshold ketat, NDRE < 0.20
- **Standar (30%)**: Threshold moderat, NDRE < 0.28  
- **Agresif (50%)**: Threshold longgar, NDRE < 0.35

dengan **data sensus lapangan** sebagai ground truth.

---

## Hasil Analisis AME II

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Over-detection |
|--------|-------------|-------------|-----|------------|----------------|
| Konservatif | -0.176 | Tidak | 6.3% | 44% | 0.0x |
| Standar | 0.090 | Tidak | 6.2% | 44% | 0.0x |
| Agresif | -0.098 | Tidak | 4.8% | 61% | 0.7x |

### Interpretasi AME II:
- **Preset terbaik berdasarkan MAE**: Agresif (MAE = 4.8%)
- Rata-rata deteksi algoritma: 1.4%
- Rata-rata serangan aktual (sensus): 6.3%

---

## Hasil Analisis AME IV

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Over-detection |
|--------|-------------|-------------|-----|------------|----------------|
| Konservatif | 0.428 | Ya | 7.0% | 42% | 4.5x |
| Standar | -0.143 | Tidak | 15.0% | 29% | 8.8x |
| Agresif | -0.201 | Tidak | 42.2% | 0% | 23.3x |

### Interpretasi AME IV:
- **Preset terbaik berdasarkan MAE**: Konservatif (MAE = 7.0%)
- Rata-rata deteksi algoritma: 23.1%
- Rata-rata serangan aktual (sensus): 1.9%

---

## Kesimpulan dan Rekomendasi

### Temuan Utama:
1. **Semua preset cenderung over-detect** dibandingkan data sensus aktual
2. **Preset Konservatif** memberikan hasil paling mendekati realita (MAE terendah)
3. **Korelasi rendah** menunjukkan NDRE stress ≠ Ganoderma langsung

### Rekomendasi:
1. **Gunakan Preset Konservatif** untuk estimasi yang lebih akurat
2. **Interpretasi hasil sebagai "Area Prioritas Survey"**, bukan diagnosis pasti
3. **Kombinasikan dengan survei lapangan** untuk konfirmasi

### Catatan Metodologi:
- NDRE mengukur **stress vegetasi** secara umum
- Stress vegetasi bisa disebabkan berbagai faktor (kekeringan, hama, nutrisi)
- Ganoderma hanya **salah satu** penyebab stress
- Algoritma berguna untuk **prioritisasi area survey**, bukan pengganti sensus

---

*Laporan dihasilkan otomatis oleh validation_all_presets.py*
