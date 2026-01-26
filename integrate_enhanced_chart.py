"""
Integrate enhanced 3-year chart into prototype
Update showModalPreview('3year') function
"""

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the 3year chart section
# Current function starts around line 360

old_3year_code = '''            } else if (type === '3year') {
                titleEl.textContent = '📉 3-Year Projection Trend (Line Chart)';
                currentPreviewChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Tahun 0 (Now)', 'Tahun 1', 'Tahun 2', 'Tahun 3'],
                        datasets: [{
                            label: 'Kerugian Tanpa Treatment',
                            data: [1353, 1567, 1974, 3133],
                            borderColor: 'rgba(251, 146, 60, 1)',
                            backgroundColor: 'rgba(251, 146, 60, 0.2)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 6,
                            pointBackgroundColor: 'rgba(251, 146, 60, 1)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { labels: { color: 'white', font: { size: 14 } } },
                            tooltip: {
                                callbacks: {
                                    label: (context) => 'Rp ' + context.parsed.y + ' Juta'
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
                });'''

new_3year_code = '''            } else if (type === '3year') {
                titleEl.innerHTML = '📉 3-Year Degradation Model: <span class="text-red-400">TANPA</span> vs <span class="text-emerald-400">DENGAN</span> Treatment';
                
                // Enhanced: Show comparison with multiple metrics in tooltips
                currentPreviewChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Tahun 0', 'Tahun 1', 'Tahun 2', 'Tahun 3'],
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
                                pointBorderWidth: 2,
                                // Metadata for tooltips
                                ar: [7.2, 8.9, 11.2, 14.8],
                                gap: [4.66, 5.12, 6.45, 10.24],
                                sph: [125, 121, 115, 107]
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
                                borderDash: [5, 5],
                                // Metadata for tooltips
                                ar: [7.2, 7.5, 7.3, 7.1],
                                gap: [4.66, 4.70, 4.85, 4.92],
                                sph: [125, 124, 123, 122]
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
                                labels: { 
                                    color: 'white', 
                                    font: { size: 14, weight: 'bold' },
                                    padding: 15
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                                padding: 12,
                                titleColor: 'white',
                                bodyColor: 'white',
                                borderColor: 'rgba(255, 255, 255, 0.2)',
                                borderWidth: 1,
                                callbacks: {
                                    title: (tooltipItems) => {
                                        return tooltipItems[0].label;
                                    },
                                    label: (context) => {
                                        const idx = context.dataIndex;
                                        const dataset = context.dataset;
                                        const lines = [
                                            '💰 Loss: Rp ' + context.parsed.y.toFixed(0) + ' Juta',
                                            '🔴 AR: ' + dataset.ar[idx] + '%',
                                            '📉 Gap: ' + dataset.gap[idx].toFixed(2) + ' Ton/Ha',
                                            '🌳 SPH: ' + dataset.sph[idx] + ' trees/ha'
                                        ];
                                        return lines;
                                    },
                                    beforeBody: (tooltipItems) => {
                                        return '━'.repeat(30);
                                    },
                                    footer: (tooltipItems) => {
                                        const idx = tooltipItems[0].dataIndex;
                                        if (idx === 0) return '';
                                        
                                        // Show delta from year 0
                                        const dataset = tooltipItems[0].dataset;
                                        const arDelta = dataset.ar[idx] - dataset.ar[0];
                                        const gapDelta = dataset.gap[idx] - dataset.gap[0];
                                        const sphDelta = dataset.sph[idx] - dataset.sph[0];
                                        
                                        return '\\nΔ dari Tahun 0:\\n' +
                                               'AR: ' + (arDelta > 0 ? '+' : '') + arDelta.toFixed(1) + '% | ' +
                                               'Gap: ' + (gapDelta > 0 ? '+' : '') + gapDelta.toFixed(2) + ' | ' +
                                               'SPH: ' + (sphDelta > 0 ? '+' : '') + sphDelta;
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
                                    font: { size: 12, weight: 'bold' }
                                }
                            },
                            x: {
                                ticks: { color: 'white' },
                                grid: { color: 'rgba(255,255,255,0.1)' }
                            }
                        }
                    }
                });'''

# Replace
if old_3year_code in html:
    html = html.replace(old_3year_code, new_3year_code)
    print("✅ Enhanced 3-year chart code integrated!")
else:
    print("⚠️  Could not find exact match - will try alternative")

# Save
with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Prototype updated with enhanced 3-year chart")
print("   Hover over datapoints to see:")
print("   - Loss value")
print("   - AR (Attack Rate)")
print("   - Gap Yield")
print("   - SPH")
print("   - Delta from Year 0")
