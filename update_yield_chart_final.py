"""
1. Update production trend chart to 2023-2025 only
2. Add zoom button
3. Create popup modal for larger chart view
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add zoom button next to title
old_header = '''                        <div class="flex justify-between items-center mb-3">
                            <h4 class="text-white text-xs font-bold flex items-center gap-2">
                                📊 Trend Realisasi Produksi (3 Tahun Terakhir)
                            </h4>
                            <button onclick="openAnalysisModal()"'''

new_header = '''                        <div class="flex justify-between items-center mb-3">
                            <h4 class="text-white text-xs font-bold flex items-center gap-2">
                                📊 Trend Realisasi Produksi (2023-2025)
                            </h4>
                            <div class="flex gap-2">
                                <button onclick="openYieldTrendModal()" 
                                    class="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-lg border border-cyan-400 transition-all flex items-center gap-1">
                                    🔍 Perbesar
                                </button>
                                <button onclick="openAnalysisModal()"'''

content = content.replace(old_header, new_header)

# 2. Close the button div
old_button_close = '''                                🔍 Analisa Lengkap
                            </button>
                        </div>'''

new_button_close = '''                                🔍 Analisa Lengkap
                                </button>
                            </div>
                        </div>'''

content = content.replace(old_button_close, new_button_close)

# 3. Update chart data to 2023-2025 only (remove 2026)
old_chart_labels = "labels: ['2023', '2024', '2025', '2026 (Saat Ini)'],"
new_chart_labels = "labels: ['2023', '2024', '2025'],"

content = content.replace(old_chart_labels, new_chart_labels)

# 4. Update dataset data arrays (3 points instead of 4)
old_realisasi_data = "data: [year3ago, year2ago, year1ago, currentYield],"
new_realisasi_data = "data: [year3ago, year2ago, year1ago],"

content = content.replace(old_realisasi_data, new_realisasi_data)

old_potensi_data = "data: [potentialYield, potentialYield, potentialYield, potentialYield],"
new_potensi_data = "data: [potentialYield, potentialYield, potentialYield],"

content = content.replace(old_potensi_data, new_potensi_data)

old_gap_data = '''data: [
                                potentialYield - year3ago,
                                potentialYield - year2ago,
                                potentialYield - year1ago,
                                potentialYield - currentYield
                            ],'''

new_gap_data = '''data: [
                                potentialYield - year3ago,
                                potentialYield - year2ago,
                                potentialYield - year1ago
                            ],'''

content = content.replace(old_gap_data, new_gap_data)

# 5. Add modal HTML for zoom view (insert before closing </body>)
modal_html = '''
    <!-- YIELD TREND ZOOM MODAL -->
    <div id="yieldTrendModal" class="hidden fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-8">
        <div class="w-full h-full max-w-6xl bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border-2 border-cyan-500/50 shadow-2xl overflow-hidden flex flex-col">
            
            <!-- Modal Header -->
            <div class="flex justify-between items-center p-6 border-b border-white/10 bg-slate-900/50">
                <div>
                    <h2 class="text-2xl font-black text-white">📊 Trend Realisasi Produksi (Ton/Ha)</h2>
                    <p class="text-sm text-slate-400 mt-1">Block: <span id="yieldModalBlockCode" class="text-cyan-400 font-bold">--</span> | Periode: 2023-2025</p>
                    <p class="text-xs text-yellow-400 mt-1">⚠️ Data trend dihitung dari realisasi 2025 (data historis belum tersedia)</p>
                </div>
                <button onclick="closeYieldTrendModal()" 
                    class="w-10 h-10 rounded-lg bg-red-600/20 hover:bg-red-600 border border-red-500/50 text-white font-bold text-xl transition-all">
                    ×
                </button>
            </div>

            <!-- Modal Content -->
            <div class="flex-1 overflow-y-auto p-8">
                <div class="bg-slate-900/50 p-6 rounded-xl border border-cyan-500/30">
                    <div style="height: 500px;">
                        <canvas id="yieldTrendModalChart"></canvas>
                    </div>
                </div>

                <!-- Data Table -->
                <div class="mt-6 bg-slate-800/50 p-4 rounded-xl">
                    <h3 class="text-white font-bold mb-3">📋 Data Tahun-ke-Tahun</h3>
                    <table class="w-full text-white text-sm">
                        <thead class="bg-slate-700/50">
                            <tr>
                                <th class="p-3 text-left">Tahun</th>
                                <th class="p-3 text-right">Realisasi (Ton/Ha)</th>
                                <th class="p-3 text-right">Potensi (Ton/Ha)</th>
                                <th class="p-3 text-right">Gap (Ton/Ha)</th>
                                <th class="p-3 text-right">Gap (%)</th>
                            </tr>
                        </thead>
                        <tbody id="yieldModalTableBody" class="text-slate-300">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>

</body>'''

content = content.replace('</body>', modal_html)

# 6. Add JavaScript functions for modal
modal_js = '''
    // ====== YIELD TREND MODAL FUNCTIONS ======
    let yieldTrendModalChart = null;

    function openYieldTrendModal() {
        if (!currentBlockCode || !BLOCKS_DATA[currentBlockCode]) return;
        
        const data = BLOCKS_DATA[currentBlockCode];
        document.getElementById('yieldTrendModal').classList.remove('hidden');
        document.getElementById('yieldModalBlockCode').textContent = currentBlockCode;
        
        renderYieldTrendModal(data);
    }

    function closeYieldTrendModal() {
        document.getElementById('yieldTrendModal').classList.add('hidden');
        if (yieldTrendModalChart) yieldTrendModalChart.destroy();
    }

    function renderYieldTrendModal(data) {
        const currentYield = data.realisasi_ton_ha || 18.5;
        const potentialYield = data.potensi_ton_ha || 26.0;
        const gapTonHa = Math.abs(data.gap_ton_ha || 7.5);
        
        // Calculate historical trend
        const year3ago = currentYield + (gapTonHa * 0.7);  // 2023
        const year2ago = currentYield + (gapTonHa * 0.5);  // 2024
        const year1ago = currentYield;  // 2025 (actual census data)
        
        // Populate table
        const tableData = [
            { year: '2023', real: year3ago, pot: potentialYield, gap: potentialYield - year3ago },
            { year: '2024', real: year2ago, pot: potentialYield, gap: potentialYield - year2ago },
            { year: '2025', real: year1ago, pot: potentialYield, gap: potentialYield - year1ago }
        ];
        
        let tableHTML = '';
        tableData.forEach(row => {
            const gapPct = (row.gap / row.pot * 100).toFixed(1);
            tableHTML += `
                <tr class="border-t border-slate-700">
                    <td class="p-3 font-bold">${row.year}</td>
                    <td class="p-3 text-right text-blue-400">${row.real.toFixed(2)}</td>
                    <td class="p-3 text-right text-green-400">${row.pot.toFixed(2)}</td>
                    <td class="p-3 text-right text-red-400">${row.gap.toFixed(2)}</td>
                    <td class="p-3 text-right text-orange-400">${gapPct}%</td>
                </tr>`;
        });
        document.getElementById('yieldModalTableBody').innerHTML = tableHTML;
        
        // Render chart
        const ctx = document.getElementById('yieldTrendModalChart');
        if (yieldTrendModalChart) yieldTrendModalChart.destroy();
        
        yieldTrendModalChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['2023', '2024', '2025'],
                datasets: [
                    {
                        label: 'Realisasi Produksi',
                        data: [year3ago, year2ago, year1ago],
                        borderColor: 'rgba(59, 130, 246, 1)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 5,
                        pointRadius: 8,
                        pointHoverRadius: 12,
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Potensi Produksi',
                        data: [potentialYield, potentialYield, potentialYield],
                        borderColor: 'rgba(34, 197, 94, 1)',
                        backgroundColor: 'rgba(34, 197, 94, 0.05)',
                        borderWidth: 3,
                        borderDash: [10, 5],
                        pointRadius: 5,
                        tension: 0,
                        fill: false
                    },
                    {
                        label: 'Gap Kerugian',
                        data: [
                            potentialYield - year3ago,
                            potentialYield - year2ago,
                            potentialYield - year1ago
                        ],
                        borderColor: 'rgba(239, 68, 68, 1)',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 4,
                        pointRadius: 7,
                        pointHoverRadius: 10,
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: {
                        labels: {
                            color: 'white',
                            font: { size: 14, weight: 'bold' },
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) label += ': ';
                                label += context.parsed.y.toFixed(2) + ' Ton/Ha';
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { 
                            color: 'white', 
                            font: { size: 14, weight: 'bold' } 
                        },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    y: {
                        title: { 
                            display: true, 
                            text: 'Produksi (Ton/Ha)', 
                            color: 'white', 
                            font: { size: 16, weight: 'bold' } 
                        },
                        ticks: { 
                            color: 'white', 
                            font: { size: 13, weight: 'bold' },
                            callback: function(value) {
                                return value.toFixed(1) + ' Ton/Ha';
                            }
                        },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        beginAtZero: false
                    }
                }
            }
        });
    }

    // ESC key to close yield modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !document.getElementById('yieldTrendModal').classList.contains('hidden')) {
            closeYieldTrendModal();
        }
    });

    // ====== AUTO-RUN ======'''

# Insert before AUTO-RUN marker
content = content.replace('        // ====== AUTO-RUN ======', modal_js)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated production trend chart:")
print("   - Period: 2023-2025 (removed 2026)")
print("   - Added '🔍 Perbesar' zoom button")
print("   - Created fullscreen zoom modal")
print("   - Added data table in modal")
print("   - Added disclaimer about calculated data")
print("\n⚠️  DATA DISCLAIMER:")
print("   Chart shows CALCULATED trend from 2025 census data")
print("   Real historical data (2023-2024) not available in BLOCKS_DATA")
