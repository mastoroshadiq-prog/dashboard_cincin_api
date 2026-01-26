"""
Update JavaScript to render single comparison chart with toggle
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace renderModalCharts function
old_func = '''        function renderModalCharts(data) {
            const ar0 = data.attack_rate || 7.5, gap0 = Math.abs(data.gap_pct || 21), sph0 = data.sph || 108;
            const loss0 = data.loss_value_juta || 0;
            
            // NO TREATMENT DATA (degradation)
            const noTx_ar = [ar0, ar0 * 1.33, ar0 * 1.59, ar0 * 2.27];
            const noTx_gap = [gap0, gap0 * 1.23, gap0 * 1.56, gap0 * 2.50];
            const noTx_sph = [sph0, sph0 - 10, sph0 - 25, sph0 - 45];
            const noTx_loss = [loss0, loss0 * 1.12, loss0 * 1.42, loss0 * 2.27];
            
            // WITH TREATMENT DATA (stabilization 70% effective)
            const withTx_ar = [ar0, ar0 * 1.05, ar0 * 1.08, ar0 * 1.10];
            const withTx_gap = [gap0, gap0 * 1.05, gap0 * 1.08, gap0 * 1.10];
            const withTx_sph = [sph0, sph0 - 2, sph0 - 4, sph0 - 5];
            const withTx_loss = [loss0, loss0 * 1.03, loss0 * 1.05, loss0 * 1.08];
            
            const labels = ['Year 0', 'Year 1', 'Year 2', 'Year 3'];
            
            // Chart 1: No Treatment
            const ctx1 = document.getElementById('modalNoTreatmentChart');
            if (modalNoTxChart) modalNoTxChart.destroy();
            
            modalNoTxChart = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'AR (%)', data: noTx_ar, borderColor: 'rgba(239, 68, 68, 1)', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y1' },
                        { label: 'Gap (%)', data: noTx_gap, borderColor: 'rgba(251, 146, 60, 1)', backgroundColor: 'rgba(251, 146, 60, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y1' },
                        { label: 'SPH', data: noTx_sph, borderColor: 'rgba(234, 179, 8, 1)', backgroundColor: 'rgba(234, 179, 8, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y2' },
                        { label: 'Loss (Jt)', data: noTx_loss, borderColor: 'rgba(147, 51, 234, 1)', backgroundColor: 'rgba(147, 51, 234, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y3' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, plugins: { legend: { labels: { color: 'white', font: { size: 11 } } } }, scales: { x: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }, y1: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'AR/Gap (%)', color: 'white' }, ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }, y2: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'SPH', color: 'white' }, ticks: { color: 'white' }, grid: { drawOnChartArea: false } }, y3: { type: 'linear', display: false } } }
            });
            
            // Chart 2: With Treatment
            const ctx2 = document.getElementById('modalWithTreatmentChart');
            if (modalWithTxChart) modalWithTxChart.destroy();
            
            modalWithTxChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'AR (%)', data: withTx_ar, borderColor: 'rgba(34, 197, 94, 1)', backgroundColor: 'rgba(34, 197, 94, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y1' },
                        { label: 'Gap (%)', data: withTx_gap, borderColor: 'rgba(59, 130, 246, 1)', backgroundColor: 'rgba(59, 130, 246, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y1' },
                        { label: 'SPH', data: withTx_sph, borderColor: 'rgba(168, 85, 247, 1)', backgroundColor: 'rgba(168, 85, 247, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y2' },
                        { label: 'Loss (Jt)', data: withTx_loss, borderColor: 'rgba(6, 182, 212, 1)', backgroundColor: 'rgba(6, 182, 212, 0.1)', borderWidth: 3, tension: 0.3, yAxisID: 'y3' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, plugins: { legend: { labels: { color: 'white', font: { size: 11 } } } }, scales: { x: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }, y1: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'AR/Gap (%)', color: 'white' }, ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }, y2: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'SPH', color: 'white' }, ticks: { color: 'white' }, grid: { drawOnChartArea: false } }, y3: { type: 'linear', display: false } } }
            });
        }'''

new_func = '''        let modalComparisonChart = null;
        let modalData = null;
        
        function renderModalCharts(data) {
            modalData = data;
            renderComparisonChart('ar'); // Default to AR
        }
        
        function renderComparisonChart(metric) {
            if (!modalData) return;
            
            // Update button states
            ['AR', 'Gap', 'SPH', 'Loss'].forEach(m => {
                const btn = document.getElementById('toggle' + m);
                btn.className = metric === m.toLowerCase() 
                    ? 'px-4 py-2 rounded-lg text-sm font-bold bg-indigo-600 text-white border-2 border-indigo-400'
                    : 'px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600';
            });
            
            const ar0 = modalData.attack_rate || 7.5, gap0 = Math.abs(modalData.gap_pct || 21);
            const sph0 = modalData.sph || 108, loss0 = modalData.loss_value_juta || 0;
            
            // NO TREATMENT DATA (degradation)
            const noTx = {
                ar: [ar0, ar0 * 1.33, ar0 * 1.59, ar0 * 2.27],
                gap: [gap0, gap0 * 1.23, gap0 * 1.56, gap0 * 2.50],
                sph: [sph0, sph0 - 10, sph0 - 25, sph0 - 45],
                loss: [loss0, loss0 * 1.12, loss0 * 1.42, loss0 * 2.27]
            };
            
            // WITH TREATMENT DATA (70% effective stabilization)
            const withTx = {
                ar: [ar0, ar0 * 1.05, ar0 * 1.08, ar0 * 1.10],
                gap: [gap0, gap0 * 1.05, gap0 * 1.08, gap0 * 1.10],
                sph: [sph0, sph0 - 2, sph0 - 4, sph0 - 5],
                loss: [loss0, loss0 * 1.03, loss0 * 1.05, loss0 * 1.08]
            };
            
            const labels = ['Year 0 (Now)', 'Year 1', 'Year 2', 'Year 3'];
            const config = {
                ar: { label: 'Attack Rate', unit: '%', color1: 'rgba(239, 68, 68, 1)', color2: 'rgba(34, 197, 94, 1)' },
                gap: { label: 'Gap Hasil', unit: '%', color1: 'rgba(251, 146, 60, 1)', color2: 'rgba(59, 130, 246, 1)' },
                sph: { label: 'SPH', unit: ' trees/ha', color1: 'rgba(234, 179, 8, 1)', color2: 'rgba(168, 85, 247, 1)' },
                loss: { label: 'Loss', unit: ' Juta', color1: 'rgba(147, 51, 234, 1)', color2: 'rgba(6, 182, 212, 1)' }
            };
            
            const c = config[metric];
            const ctx = document.getElementById('modalComparisonChart');
            if (modalComparisonChart) modalComparisonChart.destroy();
            
            modalComparisonChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: '❌ No Treatment',
                            data: noTx[metric],
                            borderColor: c.color1,
                            backgroundColor: c.color1.replace('1)', '0.1)'),
                            borderWidth: 4,
                            pointRadius: 6,
                            pointHoverRadius: 8,
                            tension: 0.3
                        },
                        {
                            label: '✅ With Treatment',
                            data: withTx[metric],
                            borderColor: c.color2,
                            backgroundColor: c.color2.replace('1)', '0.1)'),
                            borderWidth: 4,
                            pointRadius: 6,
                            pointHoverRadius: 8,
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: {
                            labels: { color: 'white', font: { size: 14, weight: 'bold' }, padding: 20 }
                        },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    const val = metric === 'loss' ? 'Rp ' + Math.round(ctx.parsed.y) : ctx.parsed.y.toFixed(1);
                                    return ctx.dataset.label + ': ' + val + c.unit;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: 'white', font: { size: 12, weight: 'bold' } },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        },
                        y: {
                            title: {
                                display: true,
                                text: c.label + ' (' + c.unit.trim() + ')',
                                color: 'white',
                                font: { size: 14, weight: 'bold' }
                            },
                            ticks: { 
                                color: 'white',
                                font: { size: 12, weight: 'bold' },
                                callback: (val) => metric === 'loss' ? 'Rp ' + val : val
                            },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        }
                    }
                }
            });
        }'''

content = content.replace(old_func, new_func)

# Update variable declarations
content = content.replace('let modalNoTxChart = null;\n        let modalWithTxChart = null;', 
                         'let modalComparisonChart = null;\n        let modalData = null;')

# Update closeAnalysisModal
old_close = '''function closeAnalysisModal() {
            document.getElementById('analysisModal').classList.add('hidden');
            if (modalNoTxChart) modalNoTxChart.destroy();
            if (modalWithTxChart) modalWithTxChart.destroy();
        }'''

new_close = '''function closeAnalysisModal() {
            document.getElementById('analysisModal').classList.add('hidden');
            if (modalComparisonChart) modalComparisonChart.destroy();
            modalData = null;
        }'''

content = content.replace(old_close, new_close)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Replaced renderModalCharts with single comparison chart")
print("✅ Added renderComparisonChart(metric) function")
print("✅ Toggle updates button states and re-renders chart")
print("✅ Shows 2 lines: red (no treatment) vs green (with treatment)")
print("✅ Dynamic Y-axis label based on metric")
print("✅ Default: AR% on modal open")
