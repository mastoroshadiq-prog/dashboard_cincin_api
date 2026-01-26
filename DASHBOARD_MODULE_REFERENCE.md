# 📋 DASHBOARD CINCIN API - Module & Function Reference

**Generated:** 2026-01-21  
**File:** DASHBOARD_DEMO_FEATURES.html  
**Total Functions:** 38

---

## 🏗️ MODULE STRUCTURE

### 1. DIVISION SELECTOR MODULE
**Purpose:** Toggle between 14 divisions for viewing blocks

| Function | Description |
|----------|-------------|
| `filterByDivision(division)` | Filter blocks by selected division code |
| `getBlocksByDivision(divisionCode)` | Get array of blocks for a division |

**Related HTML IDs:**
- `divBtn_AME01` to `divBtn_C003` - Division selector buttons
- `divisionStats` - Division statistics display

---

### 2. DIVISION METRICS MODULE
**Purpose:** Calculate and display division-level metrics

| Function | Description |
|----------|-------------|
| `calculateDivisionMetrics(divisionCode)` | Calculate comprehensive metrics for a division |
| `getAllDivisionMetrics()` | Get metrics for all divisions |
| `getDivisionMetrics(divisionCode)` | Get cached or calculate division metrics |
| `updateDivisionSummary(divisionCode)` | Update UI with division summary |

**Data Sources:**
- `COMPLETE_BLOCKS_DATA` - 642 blocks with gap_pct, luas_ha, division
- `DIVISIONS_META` - Division metadata (code, name, tier)

---

### 3. HISTORICAL TRENDS CHART MODULE
**Purpose:** Display 6-year historical trends (2023-2028) with projections

| Function | Description |
|----------|-------------|
| `renderHistoricalTrendsChart(divisionCode, metrics)` | Render dual Y-axis chart with Loss + Attack Rate |
| `showHistoricalDataModal(year)` | Show popup with detailed data table |
| `closeHistoricalDataModal()` | Close the historical data modal |

**Chart Features:**
- Loss - TANPA Treatment (Red line)
- Loss - DENGAN Treatment (Green dashed)
- Attack Rate / Stadium % (Orange)

**Related HTML IDs:**
- `historicalTrendsChart` - Canvas element
- `historicalChartDivision` - Division label
- `historicalDataModal` - Popup modal

---

### 4. PAPARAN RISIKO (RISK EXPOSURE) MODULE
**Purpose:** Display risk summary and critical blocks

| Function | Description |
|----------|-------------|
| `updatePaparanRisiko(metrics)` | Update risk exposure section |
| `renderPaparanRisk(divisionCode)` | Render risk visualization |
| `openPaparanRisikoModal(divisionCode)` | Open detailed risk modal |
| `closePaparanRisikoModal()` | Close risk modal |
| `renderModalChart(blocks, sortBy)` | Render chart in modal |
| `sortModalChart(sortBy)` | Sort modal chart by metric |

**Related HTML IDs:**
- `paparanRisikoModal` - Modal container
- `modalDivisionSubtitle` - Modal subtitle
- `modalTotalLoss`, `modalCriticalCount`, `modalRiskArea` - Summary stats

---

### 5. BLOCK BREAKDOWN MODULE
**Purpose:** Per-block detailed analysis

| Function | Description |
|----------|-------------|
| `openBlockBreakdownModal(divisionCode)` | Open block categorization modal |
| `closeBlockBreakdownModal()` | Close block breakdown modal |
| `loadBlockData(blockCode)` | Load data for specific block |
| `populateBlockSelector(divisionCode)` | Populate block dropdown |
| `switchBlock(blockCode)` | Switch to different block |

**Related HTML IDs:**
- `blockBreakdownSection` - Breakdown section
- `finTitleLeft`, `finLossLeft`, etc. - Block detail displays

---

### 6. BLOCK CATEGORIZATION MODULE
**Purpose:** Classify blocks into CRITICAL, HIGH, MEDIUM, LOW

| Function | Description |
|----------|-------------|
| `getGanodermaStadium(attackRate, gapPct)` | Determine stadium (1-4) and severity |
| `getStadium(attackRate, gapPct)` | Get stadium classification |
| `getSeverityClass(stadium)` | Get CSS class for severity |
| `getPriorityBadge(priority)` | Get priority badge HTML |

**Classification Criteria:**
- Stadium 4 (CRITICAL): AR ≥30% OR Gap ≥40%
- Stadium 3 (HIGH): AR ≥15% OR Gap ≥20%
- Stadium 2 (MEDIUM): AR ≥5% OR Gap ≥10%
- Stadium 1 (LOW): AR <5% AND Gap <10%

---

### 7. YIELD TREND MODAL MODULE
**Purpose:** Show production trend analysis

| Function | Description |
|----------|-------------|
| `openYieldTrendModal(blockCode)` | Open yield trend modal |
| `closeYieldTrendModal()` | Close yield trend modal |
| `renderYieldTrendModal(blockCode)` | Render yield trend chart |

---

### 8. ANALYSIS MODAL MODULE  
**Purpose:** Treatment impact and ROI analysis

| Function | Description |
|----------|-------------|
| `openAnalysisModal(blockCode)` | Open treatment analysis modal |
| `closeAnalysisModal()` | Close analysis modal |
| `renderTotalAnalysis()` | Render aggregate analysis |
| `renderModalCharts(data)` | Render modal charts |
| `renderComparisonChart(metric)` | Render comparison chart (AR/Gap/SPH/Loss) |

**Related HTML IDs:**
- `toggleAR`, `toggleGap`, `toggleSPH`, `toggleLoss` - Metric toggles
- `modalNoTreatmentLoss`, `modalTreatmentCost`, `modalSavings`, `modalNetBenefit`

---

### 9. DEGRADATION MODEL CHART MODULE
**Purpose:** Show projected degradation over time

| Function | Description |
|----------|-------------|
| `renderDegradationModelChart(blockCode)` | Render 3-year degradation chart |

---

### 10. DIVISION COMPARISON MODULE
**Purpose:** Compare metrics across divisions

| Function | Description |
|----------|-------------|
| `renderDivisionComparison()` | Render division comparison chart |
| `renderCategoryDistributionChart(divisionCode)` | Render category distribution pie chart |

---

### 11. CHART DEMO MODULE
**Purpose:** Demo/showcase chart functionality

| Function | Description |
|----------|-------------|
| `showChartDemo(chartType)` | Show demo chart by type |

---

### 12. UTILITY FUNCTIONS

| Function | Description |
|----------|-------------|
| `formatLossMiliar(value)` | Format loss value in Miliar Rp |
| `switchViewMode(mode)` | Switch between view modes |

---

## 📊 DATA CONSTANTS

| Constant | Description | Source |
|----------|-------------|--------|
| `COMPLETE_BLOCKS_DATA` | 642 blocks with gap, area, division | Embedded JSON |
| `BLOCKS_DATA` | Block details with attack_rate, sph | Embedded JSON |
| `HISTORICAL_YIELDS` | 2023-2025 production data per block | Embedded JSON |
| `DIVISIONS_META` | 14 divisions metadata | Embedded JSON |

---

## 🎨 MODAL INVENTORY

| Modal ID | Trigger Function | Close Function |
|----------|-----------------|----------------|
| `paparanRisikoModal` | `openPaparanRisikoModal()` | `closePaparanRisikoModal()` |
| `blockBreakdownModal` | `openBlockBreakdownModal()` | `closeBlockBreakdownModal()` |
| `yieldTrendModal` | `openYieldTrendModal()` | `closeYieldTrendModal()` |
| `analysisModal` | `openAnalysisModal()` | `closeAnalysisModal()` |
| `historicalDataModal` | `showHistoricalDataModal()` | `closeHistoricalDataModal()` |

---

## 📈 CHART INVENTORY

| Chart ID | Render Function | Type |
|----------|----------------|------|
| `historicalTrendsChart` | `renderHistoricalTrendsChart()` | Line (Dual Y-axis) |
| `riskBarChart` | Part of `updateDivisionSummary()` | Bar |
| `degradationChart` | `renderDegradationModelChart()` | Line |
| `comparisonChart` | `renderComparisonChart()` | Line |
| `categoryDistChart` | `renderCategoryDistributionChart()` | Doughnut |

---

## 🔗 MODULE RELATIONSHIPS

```
DIVISION SELECTOR
       │
       ▼
DIVISION METRICS ──────────────────┐
       │                           │
       ├──► HISTORICAL TRENDS      │
       │    CHART                  │
       │                           │
       ├──► PAPARAN RISIKO ────────┤
       │                           │
       └──► BLOCK BREAKDOWN        │
            │                      │
            ├──► YIELD TREND       │
            │                      │
            └──► ANALYSIS MODAL ◄──┘
```

---

## 📝 NOTES

- All data is embedded directly in HTML (no external API calls)
- Charts use Chart.js library
- Styling uses TailwindCSS
- Each division filter triggers recalculation of all metrics
