# 📋 CHECKPOINT: Historical Trends Chart Enhancement & Data Validation Analysis

**Date:** 2026-01-21  
**Version:** V12.3.0  
**Git Commit:** 0535716

---

## 🎯 Objectives Completed

### 1. Historical Trends Chart Enhancement
- ✅ Added 6-year historical trends chart (2023-2028) with dual Y-axis
- ✅ Implemented click-on-point popup showing detailed data in table format
- ✅ Fixed data aggregation to support ALL divisions (not just AME02)
- ✅ Added proxy attack rate calculation for non-NDRE divisions
- ✅ Created `showHistoricalDataModal()` function with comparison table

### 2. Data Validation Analysis
- ✅ Analyzed `tabelNDREnew.csv` - confirmed NDRE data is for year 2025 (column `klassndre12025`)
- ✅ Analyzed `data_gabungan.xlsx` - found Stadium 1&2, Stadium 3&4, SPH, and production data 2023-2025
- ✅ Calculated historical Gap trend: 2023(32.3%) → 2024(35.9%) → 2025(32.6%)
- ✅ Identified data limitations for Attack Rate historical estimation

---

## 📊 Data Source Validation Summary

### Available Data Sources

| Data Source | Content | Years | Divisions |
|-------------|---------|-------|-----------|
| `tabelNDREnew.csv` | NDRE Index & Classification | 2025 only | AME II, AME IV |
| `data_gabungan.xlsx` | Stadium, SPH, Production | 2023-2025 (production) | All 14 divisions |
| `HISTORICAL_YIELDS` (in HTML) | Production Real/Potential | 2023-2025 | Selected blocks |
| `COMPLETE_BLOCKS_DATA` (in HTML) | Block info, gap_pct | 2025 | All 642 blocks |

### Data That IS Validated ✅

1. **Attack Rate 2025 (NDRE)** - From `tabelNDREnew.csv`
   - Method: Drone spectral scanning
   - Coverage: AME II (36 blocks), AME IV (76 blocks)
   - Reliability: HIGH (objective measurement)

2. **Attack Rate 2025 (Stadium)** - From `data_gabungan.xlsx`
   - Method: Ground census
   - Coverage: All 641 blocks
   - Reliability: MEDIUM (visual/subjective assessment)

3. **Production Gap 2023-2025** - From `data_gabungan.xlsx`
   - Avg Gap 2023: 32.3%
   - Avg Gap 2024: 35.9%
   - Avg Gap 2025: 32.6%
   - Reliability: HIGH (actual production data)

### Data That CANNOT Be Validated ❌

1. **Attack Rate 2023** - NO DATA AVAILABLE
2. **Attack Rate 2024** - NO DATA AVAILABLE
3. **Historical NDRE scans** - Only 2025 exists
4. **Historical Census per year** - Only 2025 snapshot exists

---

## ⚠️ Critical Findings

### Issue 1: Attack Rate Historical Estimation Not Valid
**Current Implementation:**
```javascript
// Attack rate (only 2025 actual, estimate backwards)
historicalData[2025].attackRate += currentAR;
historicalData[2024].attackRate += currentAR * 0.90; // ❌ ESTIMASI
historicalData[2023].attackRate += currentAR * 0.80; // ❌ ESTIMASI
```

**Problem:** 
- Multiplying by 0.90/0.80 has NO scientific basis
- No correlation coefficient between Gap % and Attack Rate validated
- Cannot use Gap trend as direct proxy for Attack Rate

**Impact:**
- Attack Rate values for 2023-2024 in the chart are UNRELIABLE
- Decision-making based on these values is NOT recommended

### Issue 2: Projection Model Assumptions
**Current Assumptions (NOT validated):**

| Parameter | Value | Basis |
|-----------|-------|-------|
| Degradation Rate | 15%/year | ❌ Assumed |
| Treatment Effectiveness | 70% | ❌ Assumed |
| SPH Decline Rate | 3%/year | ❌ Assumed |
| Gap Yield Increase | 10%/year | ❌ Assumed |

**Required:** Peer-reviewed literature or estate historical data to validate

---

## 🔧 Technical Changes Made

### Files Modified

1. **DASHBOARD_DEMO_FEATURES.html**
   - Lines 9417-9420: Added global variables `historicalTooltipData`, `currentHistoricalDivision`
   - Lines 9420-9540: Rewrote `renderHistoricalTrendsChart()` for multi-division support
   - Lines 9851-10020: Added `showHistoricalDataModal()` and `closeHistoricalDataModal()` functions
   - Lines 9720-9726: Added onClick handler to chart for popup trigger

### New Features

1. **Click-to-Popup Modal**
   - Shows detailed data in table format when clicking chart points
   - Different display for historical vs projection years
   - Shows comparison table for projection years (No Treatment vs With Treatment)

2. **Multi-Division Support**
   - Uses `COMPLETE_BLOCKS_DATA` for division filtering
   - Falls back to proxy attack rate when `BLOCKS_DATA` not available
   - Estimates SPH from gap percentage when not available

---

## 📝 Recommendations for Next Session

### Priority 1: Data Transparency
- [ ] Add visible disclaimer on chart that Attack Rate 2023-2024 are estimates
- [ ] Consider removing Attack Rate for 2023-2024 from display
- [ ] Keep only Gap/Loss on historical chart, show Attack Rate only for 2025

### Priority 2: Projection Model Validation
- [ ] Research Ganoderma progression literature for validated parameters
- [ ] Find estate historical census data if available
- [ ] Consider using Monte Carlo simulation for uncertainty range

### Priority 3: Code Improvements
- [ ] Test all 14 divisions to ensure chart displays correctly
- [ ] Add loading indicator during data aggregation
- [ ] Optimize performance for large block counts

---

## 🔗 Related Files

- Analysis scripts: `f:\PythonProjects\poac_cincin_api\analyze_excel.py`
- Main dashboard: `f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html`
- Data sources:
  - `dashboard-cincin-api\poac_sim\data\input\data_gabungan.xlsx`
  - `dashboard-cincin-api\data\input\tabelNDREnew.csv`

---

## 📌 Decision Points for User

1. **Attack Rate Display:**
   - Option A: Show only 2025 Attack Rate (honest but incomplete)
   - Option B: Show all years with clear "ESTIMATED" label
   - Option C: Remove Attack Rate line, keep only Gap/Loss

2. **Projection Model:**
   - Option A: Keep current assumptions with disclaimer
   - Option B: Use literature-based parameters
   - Option C: Allow user to input custom parameters

**Awaiting user decision on these points.**
