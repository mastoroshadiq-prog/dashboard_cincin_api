# Implementation Plan: Value-Driven Analytics Framework v2

**Date**: 2024-12-17  
**Status**: In Progress  
**Version**: 2.0

---

## 1. Objective

Mengimplementasikan framework analitik berbasis value bisnis yang menyertakan **WHY, WHAT, SO WHAT, NOW WHAT, dan SOLUTIONS** untuk setiap analisis Ganoderma yang dibuat.

---

## 2. Framework: WIWSNS

```
┌─────────────────────────────────────────────────────────────┐
│  1. WHY (Business Context)                                  │
│     Mengapa analisis ini penting untuk bisnis?              │
├─────────────────────────────────────────────────────────────┤
│  2. WHAT (Key Insights)                                     │
│     Apa yang data ini ungkapkan?                            │
├─────────────────────────────────────────────────────────────┤
│  3. SO WHAT (Business Impact)                               │
│     Apa implikasi bisnisnya?                                │
├─────────────────────────────────────────────────────────────┤
│  4. NOW WHAT (Actionable Recommendations)                   │
│     Langkah konkret yang perlu diambil?                     │
├─────────────────────────────────────────────────────────────┤
│  5. SOLUTIONS (Problem Resolution)                          │
│     Solusi spesifik untuk setiap anomali/masalah            │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. DATA GAP ANALYSIS: Drone vs Ground Truth

### 3.1 Summary Comparison Table

| Metrik | Drone | Ground Truth | Gap | Gap % | Severity |
|--------|-------|--------------|-----|-------|----------|
| **Total Pohon AME II** | 94,201 | ~100,000 | -5,799 | -5.8% | 🟡 LOW |
| **Total Pohon AME IV** | 68,372 | ~78,000 | -9,628 | -12.3% | 🟠 MEDIUM |
| **SISIP AME II** | 787 | ~34,000 | -33,213 | -97.7% | 🔴 CRITICAL |
| **SISIP AME IV** | 4,700 | 21,709 | -17,009 | -78.4% | 🔴 HIGH |
| **SPH AME II** | 117 | 117 | 0 | 0% | 🟢 OK |
| **SPH AME IV** | 540 | 122 | +418 | +343% | 🔴 CRITICAL |
| **Ganoderma AME II** | 6,604 (SICK) | ~6,000 | +604 | +10% | 🟡 LOW |
| **Ganoderma AME IV** | 148 (SICK) | 1,400 | -1,252 | -89.4% | 🔴 HIGH |

### 3.2 Gap Severity Legend

| Level | Threshold | Description |
|-------|-----------|-------------|
| 🟢 **OK** | Gap < 5% | Data konsisten |
| 🟡 **LOW** | Gap 5-15% | Acceptable, perlu monitoring |
| 🟠 **MEDIUM** | Gap 15-30% | Perlu investigasi |
| 🔴 **HIGH** | Gap 30-80% | Perlu action segera |
| 🔴 **CRITICAL** | Gap > 80% | Data tidak dapat diandalkan |

---

### 3.3 Detailed Gap Analysis

#### Gap #1: SISIP Mismatch (CRITICAL - Gap 97%)

| Aspect | Description |
|--------|-------------|
| **Problem** | Drone mendeteksi 787 SISIP vs GT 34,000 di AME II |
| **Business Impact** | Analisis YOUNG trees tidak akurat, risiko salah prioritas |
| **Root Cause** | Label "Sisip" tidak konsisten dalam kolom Keterangan drone |
| **Evidence** | Banyak sisip ter-label sebagai "Pokok Utama" atau tanpa label |

**Solutions:**
1. Audit vocabulary labeling di data drone
2. Mapping ulang kategori berdasarkan umur tanaman (cross-ref GT Tahun Tanam)
3. Retrain model deteksi untuk differentiate young vs mature
4. Manual tagging untuk data historis

---

#### Gap #2: SPH Variance AME IV (CRITICAL - Gap 343%)

| Aspect | Description |
|--------|-------------|
| **Problem** | SPH Drone 540 vs GT 122 - 4x lebih tinggi |
| **Business Impact** | Semua metric per-hectare tidak valid untuk AME IV |
| **Root Cause Options** | Data luas (Ha) GT tidak update / Drone over-count |
| **Evidence** | 22 dari 28 blok AME IV memiliki variance > 15% |

**Solutions:**
1. **Prioritas 1**: Audit data luas per blok di Ground Truth
2. Cross-check dengan data GIS/peta tanam
3. Sample verification: ambil 5 blok, hitung manual
4. Update GT dengan data luas terbaru

---

#### Gap #3: Ganoderma Detection AME IV (HIGH - Gap 89%)

| Aspect | Description |
|--------|-------------|
| **Problem** | Drone deteksi 148 SICK vs GT 1,400 Ganoderma |
| **Business Impact** | Under-detection tinggi, risiko pohon sakit tidak teridentifikasi |
| **Root Cause** | Threshold AME IV (-4.0) sangat strict, atau GT over-estimate |
| **Evidence** | MAE 1.79% artinya per-block proportional akurat, tapi absolute berbeda |

**Solutions:**
1. Review threshold untuk AME IV
2. Analisis distribusi Z-Score per blok
3. Kalibrasi ulang dengan lebih banyak sample GT
4. Pertimbangkan per-category threshold

---

#### Gap #4: Ghost Trees / Total Count Mismatch (MEDIUM)

| Aspect | Description |
|--------|-------------|
| **Problem** | AME II: -5,799 trees, AME IV: -9,628 trees (under-count) |
| **Business Impact** | Akurasi baseline calculation terpengaruh |
| **Root Cause** | Cakupan drone tidak lengkap / GT sudah include pohon mati |

**Solutions:**
1. Identifikasi blok dengan ghost tree > 500
2. Verifikasi cakupan area drone (GPS boundary)
3. Regular reconciliation schedule (quarterly)
4. Flag blok dengan variance > 10% untuk review

---

### 3.4 Impact Priority Matrix

```
                    High Business Impact
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    │  SISIP Mismatch      │   SPH AME IV         │
    │  (CRITICAL)          │   (CRITICAL)         │
    │  Priority: 1         │   Priority: 1        │
    │                      │                      │
High│──────────────────────┼──────────────────────│
Gap │                      │                      │
    │  Ganoderma AME IV    │   Ghost Trees        │
    │  (HIGH)              │   (MEDIUM)           │
    │  Priority: 2         │   Priority: 3        │
    │                      │                      │
    └──────────────────────┼──────────────────────┘
                           │
                    Low Business Impact
```

---

## 4. Solutions Matrix

| # | Anomali | Root Cause | Solusi | Priority | Owner | Timeline |
|---|---------|------------|--------|----------|-------|----------|
| 1 | SISIP mismatch 97% | Label tidak konsisten | Standardisasi labeling | 🔴 P1 | Tim Data | 1 minggu |
| 2 | SPH AME IV 343% | Data luas GT salah | Audit luas per blok | 🔴 P1 | Tim Survei | 1 minggu |
| 3 | Ganoderma AME IV -89% | Threshold terlalu strict | Review threshold | 🟠 P2 | Tim Analyst | 2 minggu |
| 4 | Ghost trees variance | Cakupan tidak lengkap | Reconciliation | 🟡 P3 | Tim Drone | 3 minggu |

---

## 5. Deliverables

| # | Deliverable | File | Status |
|---|-------------|------|--------|
| 1 | Analysis Template | `docs/ANALYSIS_TEMPLATE.md` | ⏳ Pending |
| 2 | Executive Summary | `docs/EXECUTIVE_SUMMARY.md` | ⏳ Pending |
| 3 | Data Gap Analysis | `docs/DATA_GAP_ANALYSIS.md` | ⏳ Pending |
| 4 | Updated Dashboard | `poac_sim/comprehensive_dashboard.py` | ✅ Done |
| 5 | SPH Detail Analysis | `poac_sim/sph_detail_analysis.py` | ✅ Done |

---

## 6. Implementation Phases

### Phase 1: Data Quality Fix (PRIORITY)
- [ ] Audit SISIP labeling di drone data
- [ ] Audit luas per blok di GT AME IV
- [ ] Document gap findings

### Phase 2: Create Templates
- [ ] Create `docs/ANALYSIS_TEMPLATE.md`
- [ ] Create `docs/DATA_GAP_ANALYSIS.md`
- [ ] Define standard sections

### Phase 3: Executive Summary
- [ ] Create `docs/EXECUTIVE_SUMMARY.md`
- [ ] Compile all insights with WHY-WHAT-SO WHAT-SOLUTIONS
- [ ] Build prioritized action plan

### Phase 4: Update Dashboard
- [ ] Add Business Context section header
- [ ] Add Data Gap summary panel
- [ ] Add Solutions recommendations
- [ ] Regenerate HTML

---

## 7. Current Status Summary

| Component | Status |
|-----------|--------|
| Threshold Calibration | ✅ Complete (AME II: -1.5, AME IV: -4.0) |
| Comprehensive Dashboard | ✅ Complete (11 sections) |
| SPH Analysis | ✅ Complete |
| Option A vs B | ✅ Complete (Option A selected) |
| Data Gap Analysis | ✅ Documented |
| Value-Driven Framework | ⏳ Template pending |
| Solutions Implementation | ⏳ Pending |

---

## 8. Appendix: Technical Details

### Calibrated Thresholds
```python
# config.py
CALIBRATED_THRESHOLDS = {
    'AME002': {'Z_Threshold_G3': -1.5, 'Z_Threshold_G2': -0.5},
    'AME004': {'Z_Threshold_G3': -4.0, 'Z_Threshold_G2': -2.0},
}
```

### Detection Algorithm
- Method: Option A (MATURE only)
- Z-Score: Block-level normalization
- Cincin Api: ≥2 sick neighbors triggers cluster flag

### Data Sources
- Drone AME II: `tabelNDREnew.csv` (94,201 records)
- Drone AME IV: `AME_IV.csv` (68,372 records)
- Ground Truth: `areal_inti_serangan_gano_AMEII_AMEIV.xlsx`
