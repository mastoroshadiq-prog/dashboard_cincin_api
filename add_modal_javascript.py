"""
Add JavaScript for modal open/close and chart rendering
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add modal JavaScript before closing script tag
js_code = '''
        // ====== MODAL FUNCTIONS ======
        let currentBlockCode = null;
        let modalNoTxChart = null;
        let modalWithTxChart = null;

        function openAnalysisModal() {
            if (!currentBlockCode || !BLOCKS_DATA[currentBlockCode]) return;
            
            const data = BLOCKS_DATA[currentBlockCode];
            document.getElementById('analysisModal').classList.remove('hidden');
            document.getElementById('modalBlockCode').textContent = currentBlockCode;
            
            // Update metrics
            const total3Year = data.projected_loss_3yr || 0;
            const treatmentCost = data.mitigation_cost_juta || 50;
            const savings = total3Year * 0.70;
            const netBenefit = savings - treatmentCost;
            
            document.getElementById('modalNoTreatmentLoss').textContent = 'Rp ' + Math.round(total3Year) + ' Jt';
            document.getElementById('modalTreatmentCost').textContent = 'Rp ' + Math.round(treatmentCost) + ' Jt';
            document.getElementById('modalSavings').textContent = 'Rp ' + Math.round(savings) + ' Jt';
            document.getElementById('modalNetBenefit').textContent = 'Rp ' + Math.round(netBenefit) + ' Jt';
            
            // Render charts
            renderModalCharts(data);
        }

        function closeAnalysisModal() {
            document.getElementById('analysisModal').classList.add('hidden');
            if (modalNoTxChart) modalNoTxChart.destroy();
            if (modalWithTxChart) modalWithTxChart.destroy();
        }

        function renderModalCharts(data) {
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
        }

        // ESC key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeAnalysisModal();
        });

        // ====== AUTO-RUN ======'''

# Replace the AUTO-RUN comment
content = content.replace('        // ====== AUTO-RUN ======', js_code)

# Update loadBlockData to save current block
old_load_start = '        function loadBlockData(code) {'
new_load_start = '''        function loadBlockData(code) {
            currentBlockCode = code;'''

content = content.replace(old_load_start, new_load_start)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added modal open/close functions")
print("✅ Added side-by-side chart rendering")
print("✅ No Treatment: Degradation curves")
print("✅ With Treatment: Stabilization curves (70% effective)")
print("✅ ESC key support")
print("✅ Saves currentBlockCode for modal access")
