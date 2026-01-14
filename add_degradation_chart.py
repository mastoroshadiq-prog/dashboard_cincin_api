"""
Add degradation chart rendering to loadBlockData function
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of loadBlockData (before the treatment impact calculation)
old_end = """            const prevented = total3Year * 0.70, netBenefit = prevented - treatmentCost;
            document.getElementById('treatmentPrevented').textContent = 'Rp ' + Math.round(prevented) + ' Juta';
            document.getElementById('treatmentNetBenefit').textContent = 'Rp ' + Math.round(netBenefit) + ' Juta';
        }"""

new_end = """            const prevented = total3Year * 0.70, netBenefit = prevented - treatmentCost;
            document.getElementById('treatmentPrevented').textContent = 'Rp ' + Math.round(prevented) + ' Juta';
            document.getElementById('treatmentNetBenefit').textContent = 'Rp ' + Math.round(netBenefit) + ' Juta';
            
            // DEGRADATION CHART
            document.getElementById('degradationChartContainer').classList.remove('hidden');
            const ctx2 = document.getElementById('degradationChart');
            if (window.degradationChart) window.degradationChart.destroy();
            
            window.degradationChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: ['Tahun 0 (Saat Ini)', 'Tahun 1', 'Tahun 2', 'Tahun 3'],
                    datasets: [
                        {
                            label: 'Tingkat Infeksi (%)',
                            data: [ar0, ar1, ar2, ar3],
                            borderColor: 'rgba(239, 68, 68, 1)',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            yAxisID: 'y1'
                        },
                        {
                            label: 'Gap Hasil (%)',
                            data: [gap0, gap1, gap2, gap3],
                            borderColor: 'rgba(251, 146, 60, 1)',
                            backgroundColor: 'rgba(251, 146, 60, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            yAxisID: 'y1'
                        },
                        {
                            label: 'SPH (trees/ha)',
                            data: [sph0, sph1, sph2, sph3],
                            borderColor: 'rgba(234, 179, 8, 1)',
                            backgroundColor: 'rgba(234, 179, 8, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            yAxisID: 'y2'
                        },
                        {
                            label: 'Kerugian (Juta)',
                            data: [loss0, loss1, loss2, loss3],
                            borderColor: 'rgba(59, 130, 246, 1)',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            yAxisID: 'y3'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: {
                            labels: { color: 'white', font: { size: 11, weight: 'bold' }, padding: 10 }
                        },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    let label = ctx.dataset.label || '';
                                    if (label.includes('Kerugian')) return label + ': Rp ' + Math.round(ctx.parsed.y) + ' Jt';
                                    if (label.includes('SPH')) return label + ': ' + Math.round(ctx.parsed.y) + ' trees/ha';
                                    return label + ': ' + ctx.parsed.y.toFixed(1) + '%';
                                }
                            }
                        }
                    },
                    scales: {
                        x: { ticks: { color: 'white', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.1)' } },
                        y1: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'AR/Gap (%)', color: 'white' }, ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                        y2: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'SPH', color: 'white' }, ticks: { color: 'white' }, grid: { drawOnChartArea: false } },
                        y3: { type: 'linear', display: false, position: 'right' }
                    }
                }
            });
        }"""

content = content.replace(old_end, new_end)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added degradation chart rendering")
print("✅ Multi-line chart with 4 parameters")
print("✅ Shows in container below ESTIMASI panel")
