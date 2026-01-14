"""
Enhanced 3-Year Trend Chart dengan multiple metrics
Option 1: Separate charts (small multiples)
Option 2: Combined chart dengan dual Y-axis
"""

html_enhancement = '''
<!-- ENHANCED: 3-Year Trend with Multiple Metrics -->
<div class="space-y-6">
    
    <!-- Main: Financial Loss Comparison -->
    <div class="bg-black/30 p-6 rounded-xl border border-white/10">
        <h4 class="text-white font-bold mb-3">💰 Proyeksi Kerugian Finansial (3 Tahun)</h4>
        <canvas id="chart3YearLoss" height="250"></canvas>
    </div>
    
    <!-- Degradation Metrics Grid -->
    <div class="grid grid-cols-3 gap-4">
        
        <!-- Attack Rate Trend -->
        <div class="bg-red-900/20 p-4 rounded-xl border border-red-500/30">
            <h5 class="text-red-300 font-bold text-sm mb-2">⬆️ Attack Rate (AR)</h5>
            <canvas id="chart3YearAR" height="150"></canvas>
            <p class="text-xs text-red-200 mt-2 italic">Escalating infection without treatment</p>
        </div>
        
        <!-- Gap Yield Trend -->
        <div class="bg-orange-900/20 p-4 rounded-xl border border-orange-500/30">
            <h5 class="text-orange-300 font-bold text-sm mb-2">⬇️ Gap Yield (Ton/Ha)</h5>
            <canvas id="chart3YearGap" height="150"></canvas>
            <p class="text-xs text-orange-200 mt-2 italic">Production loss widening</p>
        </div>
        
        <!-- SPH Degradation -->
        <div class="bg-yellow-900/20 p-4 rounded-xl border border-yellow-500/30">
            <h5 class="text-yellow-300 font-bold text-sm mb-2">⬇️ SPH (Trees/Ha)</h5>
            <canvas id="chart3YearSPH" height="150"></canvas>
            <p class="text-xs text-yellow-200 mt-2 italic">Stand population declining</p>
        </div>
        
    </div>
    
    <!-- Explanation Box -->
    <div class="bg-indigo-900/20 p-4 rounded-xl border border-indigo-500/30">
        <p class="text-indigo-200 text-sm">
            <strong>📚 Degradation Model:</strong> Tanpa treatment, infeksi menyebar eksponensial:
            <span class="text-indigo-300 font-bold">AR naik → Gap yield memburuk → SPH turun → Loss meningkat drastis</span>.
            Dengan treatment (70% effective), metrics tetap stabil.
        </p>
    </div>
    
</div>

<script>
// ========================================
// Data Preparation
// ========================================

// Degradation model (without treatment)
const degradationModel = {
    year0: { ar: 7.2, gap: 4.66, sph: 125, loss: 1353 },
    year1: { ar: 8.9, gap: 5.12, sph: 121, loss: 1567 },
    year2: { ar: 11.2, gap: 6.45, sph: 115, loss: 1974 },
    year3: { ar: 14.8, gap: 10.24, sph: 107, loss: 3133 }
};

// With treatment (70% effective - metrics stabilized)
const withTreatment = {
    year0: { ar: 7.2, gap: 4.66, sph: 125, loss: 1353 },
    year1: { ar: 7.5, gap: 4.70, sph: 124, loss: 470 },  // Intervention starts
    year2: { ar: 7.3, gap: 4.85, sph: 123, loss: 592 },  // Stabilizing
    year3: { ar: 7.1, gap: 4.92, sph: 122, loss: 940 }   // Under control
};

const years = ['Tahun 0', 'Tahun 1', 'Tahun 2', 'Tahun 3'];

// ========================================
// Chart 1: Financial Loss (Main Chart)
// ========================================
const ctx1 = document.getElementById('chart3YearLoss').getContext('2d');
new Chart(ctx1, {
    type: 'line',
    data: {
        labels: years,
        datasets: [
            {
                label: 'TANPA Treatment',
                data: [1353, 1567, 1974, 3133],
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: 'rgba(239, 68, 68, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            },
            {
                label: 'DENGAN Treatment (70% effective)',
                data: [1353, 470, 592, 940],
                borderColor: 'rgba(52, 211, 153, 1)',
                backgroundColor: 'rgba(52, 211, 153, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: 'rgba(52, 211, 153, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                borderDash: [5, 5]  // Dashed line for treatment
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                labels: { color: 'white', font: { size: 13, weight: 'bold' } }
            },
            tooltip: {
                callbacks: {
                    label: (context) => {
                        const val = context.parsed.y;
                        return context.dataset.label + ': Rp ' + val.toFixed(0) + ' Juta';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { 
                    color: 'white',
                    callback: (val) => 'Rp ' + val + ' Jt'
                },
                grid: { color: 'rgba(255,255,255,0.1)' },
                title: {
                    display: true,
                    text: 'Kerugian Finansial (Juta)',
                    color: 'white',
                    font: { weight: 'bold' }
                }
            },
            x: {
                ticks: { color: 'white' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            }
        }
    }
});

// ========================================
// Chart 2: Attack Rate Trend
// ========================================
const ctx2 = document.getElementById('chart3YearAR').getContext('2d');
new Chart(ctx2, {
    type: 'line',
    data: {
        labels: years,
        datasets: [
            {
                label: 'TANPA Treatment',
                data: [7.2, 8.9, 11.2, 14.8],
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4
            },
            {
                label: 'DENGAN Treatment',
                data: [7.2, 7.5, 7.3, 7.1],
                borderColor: 'rgba(52, 211, 153, 1)',
                backgroundColor: 'rgba(52, 211, 153, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                borderDash: [3, 3]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.y + '%'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { color: 'white', font: { size: 10 } },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            x: {
                ticks: { color: 'white', font: { size: 10 } },
                grid: { display: false }
            }
        }
    }
});

// ========================================
// Chart 3: Gap Yield Trend
// ========================================
const ctx3 = document.getElementById('chart3YearGap').getContext('2d');
new Chart(ctx3, {
    type: 'line',
    data: {
        labels: years,
        datasets: [
            {
                label: 'TANPA Treatment',
                data: [4.66, 5.12, 6.45, 10.24],
                borderColor: 'rgba(251, 146, 60, 1)',
                backgroundColor: 'rgba(251, 146, 60, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4
            },
            {
                label: 'DENGAN Treatment',
                data: [4.66, 4.70, 4.85, 4.92],
                borderColor: 'rgba(52, 211, 153, 1)',
                backgroundColor: 'rgba(52, 211, 153, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                borderDash: [3, 3]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(2) + ' Ton/Ha'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { color: 'white', font: { size: 10 } },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            x: {
                ticks: { color: 'white', font: { size: 10 } },
                grid: { display: false }
            }
        }
    }
});

// ========================================
// Chart 4: SPH Degradation
// ========================================
const ctx4 = document.getElementById('chart3YearSPH').getContext('2d');
new Chart(ctx4, {
    type: 'line',
    data: {
        labels: years,
        datasets: [
            {
                label: 'TANPA Treatment',
                data: [125, 121, 115, 107],
                borderColor: 'rgba(234, 179, 8, 1)',
                backgroundColor: 'rgba(234, 179, 8, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4
            },
            {
                label: 'DENGAN Treatment',
                data: [125, 124, 123, 122],
                borderColor: 'rgba(52, 211, 153, 1)',
                backgroundColor: 'rgba(52, 211, 153, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                borderDash: [3, 3]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.y + ' trees/ha'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                min: 100,
                max: 130,
                ticks: { color: 'white', font: { size: 10 } },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            x: {
                ticks: { color: 'white', font: { size: 10 } },
                grid: { display: false }
            }
        }
    }
});

</script>
'''

print("="*80)
print("ENHANCED 3-YEAR TREND CHART CODE READY")
print("="*80)
print("\nFEATURES:")
print("✅ 2 lines per chart: TANPA vs DENGAN treatment")
print("✅ 4 metrics visualized:")
print("   1. Financial Loss (main chart)")
print("   2. Attack Rate (AR ↑)")
print("   3. Gap Yield (Ton/Ha ↓)")
print("   4. SPH (trees/ha ↓)")
print("\n✅ Visual indicators:")
print("   - Red line (no treatment) = solid")
print("   - Green line (with treatment) = dashed")
print("   - Color-coded per metric")
print("\n✅ Interactive tooltips on all charts")
print("="*80)

# Save to file for easy integration
with open('enhanced_3year_chart_code.html', 'w', encoding='utf-8') as f:
    f.write(html_enhancement)

print("\n✅ Code saved to: enhanced_3year_chart_code.html")
print("   Ready to integrate into prototype!")
print("="*80)
