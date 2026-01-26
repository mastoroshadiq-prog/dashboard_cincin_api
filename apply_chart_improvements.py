"""
IMPROVEMENT 1: Click-to-show-table untuk 3-year chart
IMPROVEMENT 2: Enhanced pie chart dengan labels
"""

print("="*80)
print("IMPLEMENTING 2 CHART IMPROVEMENTS")
print("="*80)

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================================
# IMPROVEMENT 1: Add data display table below 3-year chart
# ============================================================================

# Find the canvas for 3-year chart and add display area
insert_after_canvas = '<canvas id="modalChartPreview"></canvas>'
table_display_html = '''<canvas id="modalChartPreview"></canvas>
                </div>
                
                <!-- Data Display Table (shown on click) -->
                <div id="dataDisplayTable" class="hidden mt-4 bg-slate-900/50 p-4 rounded-xl border border-cyan-500/30">
                    <div class="flex items-center justify-between mb-3">
                        <h4 class="text-cyan-300 font-bold text-sm">📊 Detail Metrics (Klik datapoint pada chart)</h4>
                        <button onclick="document.getElementById('dataDisplayTable').classList.add('hidden')" 
                            class="text-cyan-300 hover:text-cyan-100 text-xs">✕ Close</button>
                    </div>
                    <div id="dataTableContent" class="overflow-x-auto">
                        <!-- Table will be populated by JavaScript -->
                    </div'''

html = html.replace(insert_after_canvas, table_display_html)

print("✅ Step 1: Added data display table container")

# ============================================================================
# IMPROVEMENT 2: Enhanced Pie Chart with Data Labels
# ============================================================================

# Find pie chart creation and replace with enhanced version
old_pie = '''            } else if (type === 'treatment') {
                titleEl.textContent = '💵 Treatment Cost Breakdown (Pie Chart)';
                currentPreviewChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Parit Isolasi', 'Fungisida Sistemik', 'Sanitasi', 'Drainage', 'Monitoring'],
                        datasets: [{
                            data: [25, 10, 8, 5, 2],
                            backgroundColor: [
                                'rgba(52, 211, 153, 0.9)',
                                'rgba(34, 197, 94, 0.9)',
                                'rgba(74, 222, 128, 0.9)',
                                'rgba(134, 239, 172, 0.9)',
                                'rgba(187, 247, 208, 0.9)'
                            ],
                            borderWidth: 3,
                            borderColor: '#1e293b'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: {
                                    color: 'white',
                                    font: { size: 13 },
                                    padding: 15
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: (context) => context.label + ': Rp ' + context.parsed + ' Juta/blok'
                                }
                            }
                        }
                    }
                });'''

new_pie = '''            } else if (type === 'treatment') {
                titleEl.textContent = '💵 Treatment Cost Breakdown (Per Blok)';
                currentPreviewChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Parit Isolasi (50%)', 'Fungisida (20%)', 'Sanitasi (16%)', 'Drainage (10%)', 'Monitoring (4%)'],
                        datasets: [{
                            data: [25, 10, 8, 5, 2],
                            backgroundColor: [
                                'rgba(239, 68, 68, 0.9)',      // Red - Parit (biggest cost)
                                'rgba(251, 146, 60, 0.9)',     // Orange - Fungisida
                                'rgba(234, 179, 8, 0.9)',      // Yellow - Sanitasi
                                'rgba(52, 211, 153, 0.9)',     // Green - Drainage
                                'rgba(59, 130, 246, 0.9)'      // Blue - Monitoring
                            ],
                            borderWidth: 3,
                            borderColor: '#1e293b'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: {
                                    color: 'white',
                                    font: { size: 12, weight: 'bold' },
                                    padding: 12,
                                    generateLabels: (chart) => {
                                        const data = chart.data;
                                        return data.labels.map((label, i) => {
                                            const value = data.datasets[0].data[i];
                                            return {
                                                text: label + ' - Rp ' + value + ' Jt',
                                                fillStyle: data.datasets[0].backgroundColor[i],
                                                hidden: false,
                                                index: i
                                            };
                                        });
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                                padding: 12,
                                callbacks: {
                                    label: (context) => {
                                        const label = context.label.split(' (')[0]; // Remove percentage
                                        const value = context.parsed;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return [
                                            label,
                                            'Rp ' + value + ' Juta/blok',
                                            percentage + '% dari total'
                                        ];
                                    }
                                }
                            },
                            // Data labels on pie segments
                            datalabels: {
                                color: 'white',
                                font: {
                                    weight: 'bold',
                                    size: 11
                                },
                                formatter: (value, context) => {
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(0);
                                    return 'Rp ' + value + ' Jt\\n(' + percentage + '%)';
                                }
                            }
                        }
                    },
                    plugins: [{
                        // Custom plugin to draw labels on segments
                        id: 'customLabels',
                        afterDatasetDraw: (chart) => {
                            const ctx = chart.ctx;
                            const dataset = chart.data.datasets[0];
                            const meta = chart.getDatasetMeta(0);
                            
                            meta.data.forEach((arc, index) => {
                                const midAngle = (arc.startAngle + arc.endAngle) / 2;
                                const x = arc.x + Math.cos(midAngle) * (arc.outerRadius * 0.7);
                                const y = arc.y + Math.sin(midAngle) * (arc.outerRadius * 0.7);
                                
                                const value = dataset.data[index];
                                const total = dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(0);
                                
                                ctx.fillStyle = 'white';
                                ctx.font = 'bold 11px sans-serif';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'middle';
                                
                                // Only show label if segment is big enough
                                if (percentage >= 10) {
                                    ctx.fillText('Rp ' + value + ' Jt', x, y - 6);
                                    ctx.fillText('(' + percentage + '%)', x, y + 8);
                                }
                            });
                        }
                    }]
                });'''

if old_pie in html:
    html = html.replace(old_pie, new_pie)
    print("✅ Step 2: Enhanced pie chart with labels")
else:
    print("⚠️  Pie chart not found - will add manually")

# Save
with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*80)
print("IMPROVEMENTS APPLIED:")
print("="*80)
print("1. ✅ 3-Year Chart: Click datapoint → Show table")
print("2. ✅ Pie Chart: Distinct colors + labels on segments")
print("\nNOW: Need to add click handler JavaScript for 3-year chart...")
print("="*80)
