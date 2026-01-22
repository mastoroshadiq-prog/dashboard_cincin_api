"""
Menambahkan fitur tren chart dan click handler untuk block detail.
Script ini menambahkan kode BARU tanpa menghapus yang sudah ada.
"""

import re

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Find and add blockTrendChart canvas to the modal
# Look for the section before "Two Column Layout: Block Lists"
old_two_column = '''                    <!-- Two Column Layout: Block Lists -->
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <!-- DECLINING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                            <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                📉 Blok dengan Penurunan Produksi
                            </h3>'''

new_chart_and_lists = '''                    <!-- Block Trend Bar Chart -->
                    <div class="bg-black/20 rounded-xl p-4 border border-cyan-700/30 mb-6">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            📊 Perbandingan Tren Produksi Per Blok
                            <span class="text-xs text-slate-400 font-normal ml-2">(Klik bar untuk detail)</span>
                        </h3>
                        <div style="height: 280px;">
                            <canvas id="blockTrendBarChart"></canvas>
                        </div>
                    </div>

                    <!-- Block Detail Panel (hidden by default) -->
                    <div id="blockDetailPanel" class="hidden bg-gradient-to-br from-slate-800/90 to-slate-900/90 rounded-xl p-5 border-2 border-cyan-500/50 mb-6 animate-fade-in">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold text-white flex items-center gap-2">
                                🔍 <span id="detailBlockCode">-</span>
                            </h3>
                            <button onclick="closeBlockDetail()" class="text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg p-1 transition-all">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        </div>
                        <div class="grid grid-cols-4 gap-3 mb-4">
                            <div class="bg-slate-700/50 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">Luas</div>
                                <div class="text-lg font-bold text-white" id="detailLuas">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">Produksi 2023</div>
                                <div class="text-lg font-bold text-cyan-400" id="detailProd2023">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">Produksi 2025</div>
                                <div class="text-lg font-bold text-cyan-400" id="detailProd2025">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">Perubahan</div>
                                <div class="text-lg font-bold" id="detailChange">-</div>
                            </div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-4">
                            <div style="height: 180px;">
                                <canvas id="blockDetailLineChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <!-- Two Column Layout: Block Lists -->
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <!-- DECLINING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                            <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                📉 Blok dengan Penurunan Produksi
                                <span class="text-xs text-slate-400 font-normal">(klik untuk detail)</span>
                            </h3>'''

if old_two_column in content:
    content = content.replace(old_two_column, new_chart_and_lists)
    print("✅ Added chart canvas and detail panel to modal HTML")
else:
    print("⚠️ Could not find exact match for Two Column Layout section")

# 2. Add new JavaScript functions before </script>
# Find the last </script> before </body>
js_functions = '''
            // ============================================
            // BLOCK TREND CHART & DETAIL FUNCTIONS
            // ============================================
            let blockTrendBarChartInstance = null;
            let blockDetailLineChartInstance = null;
            let currentTrendData = null;

            function renderBlockTrendBarChart(trendCategories) {
                const ctx = document.getElementById('blockTrendBarChart');
                if (!ctx) { console.log('[TREND] Canvas blockTrendBarChart not found'); return; }

                if (blockTrendBarChartInstance) {
                    blockTrendBarChartInstance.destroy();
                }

                currentTrendData = trendCategories;

                // Combine all blocks
                const allBlocks = [
                    ...trendCategories.declining,
                    ...trendCategories.stable,
                    ...trendCategories.increasing
                ].sort((a, b) => a.prodChangePct - b.prodChangePct);

                // Take top 8 declining and top 8 increasing
                const displayBlocks = [
                    ...allBlocks.filter(b => b.prodChangePct < -5).slice(0, 8),
                    ...allBlocks.filter(b => b.prodChangePct > 5).slice(-8).reverse()
                ];

                if (displayBlocks.length === 0) {
                    ctx.parentElement.innerHTML = '<div class="text-slate-400 text-center py-8">Tidak ada blok dengan perubahan signifikan</div>';
                    return;
                }

                const labels = displayBlocks.map(b => b.block_code);
                const changeData = displayBlocks.map(b => b.prodChangePct);
                const colors = displayBlocks.map(b => 
                    b.prodChangePct < -5 ? 'rgba(239, 68, 68, 0.8)' :
                    b.prodChangePct > 5 ? 'rgba(34, 197, 94, 0.8)' :
                    'rgba(251, 191, 36, 0.8)'
                );

                blockTrendBarChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Perubahan Produksi (%)',
                            data: changeData,
                            backgroundColor: colors,
                            borderColor: colors.map(c => c.replace('0.8', '1')),
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        onClick: (event, elements) => {
                            if (elements.length > 0) {
                                const idx = elements[0].index;
                                showBlockDetail(displayBlocks[idx].block_code);
                            }
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const block = displayBlocks[ctx.dataIndex];
                                        return [
                                            'Perubahan: ' + block.prodChangePct.toFixed(1) + '%',
                                            '2023: ' + block.prod2023.toFixed(1) + ' T/Ha',
                                            '2025: ' + block.prod2025.toFixed(1) + ' T/Ha'
                                        ];
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { color: '#94a3b8', callback: v => v + '%' }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45 }
                            }
                        }
                    }
                });
                console.log('[TREND] Bar chart rendered with', displayBlocks.length, 'blocks');
            }

            function showBlockDetail(blockCode) {
                const data = HISTORICAL_YIELDS[blockCode];
                if (!data) { console.log('[DETAIL] No data for', blockCode); return; }

                document.getElementById('detailBlockCode').textContent = 'Detail Blok: ' + blockCode;
                document.getElementById('detailLuas').textContent = (data.luas_ha || 0).toFixed(1) + ' Ha';

                const y23 = data.yields['2023'] || data.yields[2023] || {};
                const y24 = data.yields['2024'] || data.yields[2024] || {};
                const y25 = data.yields['2025'] || data.yields[2025] || {};

                const p23 = y23.real_ton_ha || 0;
                const p24 = y24.real_ton_ha || 0;
                const p25 = y25.real_ton_ha || 0;

                document.getElementById('detailProd2023').textContent = p23.toFixed(1) + ' T/Ha';
                document.getElementById('detailProd2025').textContent = p25.toFixed(1) + ' T/Ha';

                const chg = p23 > 0 ? ((p25 - p23) / p23) * 100 : 0;
                const chgEl = document.getElementById('detailChange');
                chgEl.textContent = (chg >= 0 ? '+' : '') + chg.toFixed(1) + '%';
                chgEl.className = 'text-lg font-bold ' + (chg < -5 ? 'text-red-400' : (chg > 5 ? 'text-green-400' : 'text-yellow-400'));

                document.getElementById('blockDetailPanel').classList.remove('hidden');
                renderBlockDetailLineChart(blockCode, p23, p24, p25, y23, y24, y25);
                document.getElementById('blockDetailPanel').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            function closeBlockDetail() {
                document.getElementById('blockDetailPanel').classList.add('hidden');
                if (blockDetailLineChartInstance) {
                    blockDetailLineChartInstance.destroy();
                    blockDetailLineChartInstance = null;
                }
            }

            function renderBlockDetailLineChart(blockCode, p23, p24, p25, y23, y24, y25) {
                const ctx = document.getElementById('blockDetailLineChart');
                if (!ctx) return;

                if (blockDetailLineChartInstance) blockDetailLineChartInstance.destroy();

                const pot23 = y23.poten_ton_ha || 0;
                const pot24 = y24.poten_ton_ha || 0;
                const pot25 = y25.poten_ton_ha || 0;

                blockDetailLineChartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [
                            {
                                label: 'Aktual (T/Ha)',
                                data: [p23, p24, p25],
                                borderColor: 'rgb(34, 211, 238)',
                                backgroundColor: 'rgba(34, 211, 238, 0.2)',
                                fill: true,
                                tension: 0.3,
                                pointRadius: 6,
                                borderWidth: 3
                            },
                            {
                                label: 'Potensi (T/Ha)',
                                data: [pot23, pot24, pot25],
                                borderColor: 'rgb(251, 191, 36)',
                                borderDash: [5, 5],
                                fill: false,
                                tension: 0.3,
                                pointRadius: 4,
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'top', labels: { color: '#fff', font: { size: 11 } } },
                            title: { display: true, text: 'Tren ' + blockCode + ' (2023-2025)', color: '#fff' }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8' } }
                        }
                    }
                });
            }

            // Override populateBlockTrendLists to add click handlers and render chart
            (function() {
                const origPopulate = window.populateBlockTrendLists;
                window.populateBlockTrendLists = function(trendCategories) {
                    // Call original if exists
                    if (typeof origPopulate === 'function') {
                        origPopulate(trendCategories);
                    }
                    
                    // Add click handlers to declining blocks
                    const decList = document.getElementById('decliningBlocksList');
                    if (decList && trendCategories.declining.length > 0) {
                        let html = trendCategories.declining.slice(0, 10).map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer hover:bg-red-900/40 hover:scale-[1.02] transition-all border border-transparent hover:border-red-500/50">' +
                                '<span class="text-white font-medium">' + b.block_code + '</span>' +
                                '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                                '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');
                        if (trendCategories.declining.length > 10) {
                            html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (trendCategories.declining.length - 10) + ' blok lainnya...</div>';
                        }
                        decList.innerHTML = html;
                    }
                    
                    // Add click handlers to increasing blocks
                    const incList = document.getElementById('increasingBlocksList');
                    if (incList && trendCategories.increasing.length > 0) {
                        let html = trendCategories.increasing.slice(0, 10).map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer hover:bg-green-900/40 hover:scale-[1.02] transition-all border border-transparent hover:border-green-500/50">' +
                                '<span class="text-white font-medium">' + b.block_code + '</span>' +
                                '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                                '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');
                        if (trendCategories.increasing.length > 10) {
                            html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (trendCategories.increasing.length - 10) + ' blok lainnya...</div>';
                        }
                        incList.innerHTML = html;
                    }

                    // Render the bar chart
                    renderBlockTrendBarChart(trendCategories);
                };
            })();

'''

# Insert before the last </script> tag that's before </body>
# Find closing </script> near the end
last_script_end = content.rfind('</script>')
if last_script_end > 0:
    content = content[:last_script_end] + js_functions + '\n        </script>'
    # Remove the old closing
    content = content[:last_script_end] + js_functions + content[last_script_end:]
    print("✅ Added JavaScript functions for chart and detail panel")
else:
    print("⚠️ Could not find </script> tag")

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Script completed. Added:")
print("   1. Block Trend Bar Chart canvas")
print("   2. Block Detail Panel HTML")
print("   3. JavaScript functions for chart rendering")
print("   4. Click handlers for block items")
