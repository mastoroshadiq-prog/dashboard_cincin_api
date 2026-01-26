# IMPLEMENTATION PLAN: 3 Major Dashboard Enhancements
**Date:** 14 Januari 2026  
**Status:** Planning Phase

---

## 🎯 **USER REQUIREMENTS:**

### **1. Before/After Treatment Chart (Side-by-Side)**
- Location: Cost of Inaction section
- Type: Bar chart atau line chart
- Data:
  - **BEFORE (No Treatment):** 3-year projection with degradation (Rp 6.2 Miliar)
  - **AFTER (With Treatment):** Reduced loss scenario (Rp 1.86 Miliar)
- Visual: Clear comparison showing savings

### **2. Swap Section Positions**
- **Current Layout:**
  ```
  [PAPARAN RISK ESTATE - Red] | [ESTIMASI KERUGIAN BLOK - Blue]
  ```
- **New Layout:**
  ```
  [ESTIMASI KERUGIAN BLOK - Blue] | [PAPARAN RISK ESTATE - Red]
  ```

### **3. Add Visual Charts to Breakdown Modals**
- Target: All "PAPARAN RISK" detail popups
- Transform tables/text into:
  - Bar charts
  - Pie charts
  - Line charts (for timeline data)
  - Comparison visuals

---

## 📋 **IMPLEMENTATION TASKS:**

### **TASK 1: Before/After Treatment Comparison Chart**

**File:** `dashboard_cincin_api_INTERACTIVE_FULL.html`

**Step 1.1:** Add Chart.js canvas in COI section
```html
<!-- After ROI metrics, before block cards -->
<div class="mt-6 bg-black/30 p-6 rounded-xl border border-white/10">
    <h4 class="text-lg font-bold text-white mb-4">
        📊 Perbandingan: Tanpa vs Dengan Treatment (3 Tahun)
    </h4>
    <canvas id="treatmentComparisonChart" height="300"></canvas>
</div>
```

**Step 1.2:** Create JavaScript for chart
```javascript
// Data preparation
const beforeTreatment = [1353, 1567, 1974, 3133]; // Year 0-3 in Juta
const afterTreatment = [1353, 470, 592, 940]; // With 70% effectiveness

// Chart.js configuration
const ctx = document.getElementById('treatmentComparisonChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Tahun 0', 'Tahun 1', 'Tahun 2', 'Tahun 3'],
        datasets: [
            {
                label: 'TANPA Treatment',
                data: beforeTreatment,
                backgroundColor: 'rgba(239, 68, 68, 0.7)', // Red
                borderColor: 'rgba(239, 68, 68, 1)',
                borderWidth: 2
            },
            {
                label: 'DENGAN Treatment',
                data: afterTreatment,
                backgroundColor: 'rgba(52, 211, 153, 0.7)', // Green
                borderColor: 'rgba(52, 211, 153, 1)',
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: 'white', font: { size: 14, weight: 'bold' } }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': Rp ' + 
                               context.parsed.y.toLocaleString('id-ID') + ' Juta';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { color: 'white' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            },
            x: {
                ticks: { color: 'white' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            }
        }
    }
});
```

**Step 1.3:** Add summary metrics below chart
```html
<div class="grid grid-cols-3 gap-4 mt-4">
    <div class="text-center p-3 bg-red-900/30 rounded-xl">
        <div class="text-xs text-red-300">Total TANPA Treatment</div>
        <div class="text-2xl font-black text-red-400">Rp 6.2 M</div>
    </div>
    <div class="text-center p-3 bg-green-900/30 rounded-xl">
        <div class="text-xs text-green-300">Total DENGAN Treatment</div>
        <div class="text-2xl font-black text-green-400">Rp 1.86 M</div>
    </div>
    <div class="text-center p-3 bg-emerald-900/30 rounded-xl border-2 border-emerald-500">
        <div class="text-xs text-emerald-300">PENGHEMATAN</div>
        <div class="text-2xl font-black text-emerald-400">Rp 4.3 M</div>
    </div>
</div>
```

---

### **TASK 2: Swap Section Positions**

**File:** `dashboard_cincin_api_INTERACTIVE_FULL.html`

**Current Structure (Lines ~350-550):**
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- LEFT: PAPARAN RISK ESTATE (Red) -->
    <div class="bg-gradient-to-br from-rose-950/90...">
        ...
    </div>
    
    <!-- RIGHT: ESTIMASI KERUGIAN BLOK (Blue) -->
    <div class="bg-gradient-to-br from-blue-950/90...">
        ...
    </div>
</div>
```

**New Structure:**
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- LEFT: ESTIMASI KERUGIAN BLOK (Blue) - MOVED -->
    <div class="bg-gradient-to-br from-blue-950/90...">
        ...
    </div>
    
    <!-- RIGHT: PAPARAN RISK ESTATE (Red) - MOVED -->
    <div class="bg-gradient-to-br from-rose-950/90...">
        ...
    </div>
</div>
```

**Implementation:**
1. Find the opening tag of PAPARAN section
2. Cut entire section (from opening div to closing div)
3. Find ESTIMASI section
4. Swap positions

---

### **TASK 3: Add Charts to Breakdown Modals**

**Target Modals:**
1. `breakdownCurrentLoss` - Current Loss modal
2. `breakdown3YearLoss` - 3-Year projection modal
3. `breakdownTreatmentCost` - Treatment cost modal
4. `breakdownSavings` - Savings modal
5. `breakdownROI` - ROI modal

**For Each Modal:**

**3.1: Current Loss Modal - Add Bar Chart**
```html
<!-- Before table -->
<div class="bg-black/30 p-5 rounded-xl border border-white/10">
    <h3 class="text-lg font-bold text-white mb-3">📊 Visual Breakdown per Blok:</h3>
    <canvas id="chartCurrentLoss" height="250"></canvas>
</div>

<!-- Keep table for detailed data -->
```

**JavaScript:**
```javascript
function populateCurrentLossChart() {
    const critical = Object.entries(BLOCKS_DATA)
        .filter(([code, data]) => data.severity_hybrid === 'CRITICAL')
        .sort((a, b) => (b[1].loss_value_juta || 0) - (a[1].loss_value_juta || 0));
    
    const labels = critical.map(([code]) => code);
    const values = critical.map(([_, data]) => data.loss_value_juta || 0);
    
    const ctx = document.getElementById('chartCurrentLoss').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Kerugian (Juta)',
                data: values,
                backgroundColor: 'rgba(251, 113, 133, 0.7)',
                borderColor: 'rgba(251, 113, 133, 1)',
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y', // Horizontal bar
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => 'Rp ' + context.parsed.x.toFixed(0) + ' Juta'
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                y: {
                    ticks: { color: 'white', font: { size: 12, weight: 'bold' } },
                    grid: { display: false }
                }
            }
        }
    });
}
```

**3.2: 3-Year Projection Modal - Add Line Chart**
```html
<canvas id="chart3YearTrend" height="300"></canvas>
```

**JavaScript:**
```javascript
function populate3YearChart() {
    const years = ['Tahun 0', 'Tahun 1', 'Tahun 2', 'Tahun 3'];
    const losses = [1353, 1567, 1974, 3133]; // From degradation model
    
    const ctx = document.getElementById('chart3YearTrend').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Kerugian (Juta)',
                data: losses,
                borderColor: 'rgba(251, 146, 60, 1)',
                backgroundColor: 'rgba(251, 146, 60, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: 'white' } }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                x: {
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                }
            }
        }
    });
}
```

**3.3: Treatment Cost Modal - Add Pie Chart**
```html
<canvas id="chartTreatmentBreakdown" height="300"></canvas>
```

**JavaScript:**
```javascript
function populateTreatmentCostChart() {
    const ctx = document.getElementById('chartTreatmentBreakdown').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Parit Isolasi', 'Fungisida', 'Sanitasi', 'Drainage', 'Monitoring'],
            datasets: [{
                data: [25, 10, 8, 5, 2], // Juta per blok
                backgroundColor: [
                    'rgba(52, 211, 153, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(74, 222, 128, 0.8)',
                    'rgba(134, 239, 172, 0.8)',
                    'rgba(187, 247, 208, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: 'white', font: { size: 12 } }
                },
                tooltip: {
                    callbacks: {
                        label: (context) => context.label + ': Rp ' + context.parsed + ' Juta'
                    }
                }
            }
        }
    });
}
```

**3.4: ROI Modal - Add Comparison Bar Chart**
```html
<canvas id="chartROIComparison" height="250"></canvas>
```

**JavaScript:**
```javascript
function populateROIChart() {
    const ctx = document.getElementById('chartROIComparison').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Deposito', 'Obligasi', 'Saham', 'Property', 'Treatment'],
            datasets: [{
                label: 'ROI 3 Tahun (%)',
                data: [15, 24, 45, 30, 986],
                backgroundColor: [
                    'rgba(148, 163, 184, 0.7)',
                    'rgba(148, 163, 184, 0.7)',
                    'rgba(148, 163, 184, 0.7)',
                    'rgba(148, 163, 184, 0.7)',
                    'rgba(250, 204, 21, 0.9)' // Yellow for treatment (highlight)
                ],
                borderColor: [
                    'rgba(148, 163, 184, 1)',
                    'rgba(148, 163, 184, 1)',
                    'rgba(148, 163, 184, 1)',
                    'rgba(148, 163, 184, 1)',
                    'rgba(250, 204, 21, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => 'ROI: ' + context.parsed.y + '%'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                x: {
                    ticks: { color: 'white' },
                    grid: { display: false }
                }
            }
        }
    });
}
```

**3.5: Update showBreakdown() Function**
```javascript
function showBreakdown(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
    
    // Populate charts based on modal
    setTimeout(() => {
        if (modalId === 'breakdownCurrentLoss') {
            populateCurrentLossTable();
            populateCurrentLossChart(); // NEW
        } else if (modalId === 'breakdown3YearLoss') {
            populate3YearChart(); // NEW
        } else if (modalId === 'breakdownTreatmentCost') {
            populateTreatmentCostChart(); // NEW
        } else if (modalId === 'breakdownROI') {
            populateROIChart(); // NEW
        }
    }, 100); // Small delay to ensure canvas is rendered
}
```

---

## 🛠️ **IMPLEMENTATION ORDER:**

### **Phase 1: Swap Sections (EASY - 30 mins)**
1. Locate PAPARAN and ESTIMASI sections
2. Cut & paste to swap positions
3. Test layout responsiveness

### **Phase 2: Add Treatment Comparison Chart (MEDIUM - 1-2 hours)**
1. Add canvas HTML in COI section
2. Create chart initialization function
3. Add summary metrics boxes
4. Test with real data

### **Phase 3: Add Charts to Modals (COMPLEX - 3-4 hours)**
1. Add canvas elements to each modal
2. Create chart population functions
3. Update showBreakdown() to trigger charts
4. Test all 5 modals
5. Adjust styling and colors

---

## 📊 **EXPECTED RESULTS:**

### **Before:**
- ❌ No visual comparison of treatment scenarios
- ❌ Sections in suboptimal order
- ❌ Modals are text/table heavy

### **After:**
- ✅ Clear before/after treatment chart
- ✅ Better section flow (Blue → Red)
- ✅ Rich visual charts in all modals
- ✅ Enhanced data storytelling
- ✅ Easier decision making

---

## ⚠️ **DEPENDENCIES:**

1. **Chart.js Library:** Already included in dashboard ✅
2. **Existing Data:** BLOCKS_DATA available ✅
3. **Modal Structure:** Already implemented ✅

---

## 🎯 **SUCCESS CRITERIA:**

1. ✅ Treatment comparison chart shows side-by-side bars
2. ✅ Section positions swapped correctly
3. ✅ All 5 modals have meaningful charts
4. ✅ Charts are responsive and clear
5. ✅ Data matches existing calculations
6. ✅ No performance issues

---

**Total Estimated Time:** 5-7 hours  
**Complexity:** Medium-High  
**Priority:** High (User Request)

---

**NEXT STEP:** Start with Phase 1 (swap sections) for quick win, then Phase 2 and 3.

**Ready to begin implementation?** 🚀
