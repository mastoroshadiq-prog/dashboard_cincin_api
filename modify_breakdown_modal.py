"""
Script untuk memodifikasi popup Block Breakdown menjadi menampilkan:
1. TREN PENURUNAN - blok dengan produksi menurun 2023-2025
2. TREN KENAIKAN - blok dengan produksi meningkat 2023-2025
"""

import re

# Read the HTML file
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify the openBlockBreakdownModal function
# Find and replace the function with new logic

old_function_start = '''            function openBlockBreakdownModal(divisionCode) {
                divisionCode = divisionCode || window.currentDivision || 'AME02';
                console.log('[BREAKDOWN] Opening for division:', divisionCode);

                // Map division code format (button uses AME_II, data uses AME02)
                const divisionMap = {
                    'AME_I': 'AME01',
                    'AME_II': 'AME02',
                    'AME_III': 'AME03',
                    'OLE_I': 'OLE01',
                    'OLE_II': 'OLE02'
                };
                const mappedCode = divisionMap[divisionCode] || divisionCode;
                console.log('[BREAKDOWN] Mapped division code:', mappedCode);

                // Calculate breakdown using calculateDivisionMetrics
                const metrics = calculateDivisionMetrics(mappedCode);
                if (!metrics) {
                    alert(`No data for division: ${divisionCode}`);
                    return;
                }

                // Get all blocks for this division
                // COMPLETE_BLOCKS_DATA has 'division' field
                // BLOCKS_DATA has 'attack_rate', 'sph' fields
                // We need to merge both using block_code as key

                if (typeof COMPLETE_BLOCKS_DATA === 'undefined' || typeof BLOCKS_DATA === 'undefined') {
                    alert('Block data not available. Please refresh the page.');
                    return;
                }

                const completeBlocks = Object.values(COMPLETE_BLOCKS_DATA);
                const blocksData = BLOCKS_DATA; // keyed by block_code

                // Filter by division from COMPLETE_BLOCKS_DATA
                const divisionBlocks = completeBlocks.filter(block => block.division === mappedCode);
                console.log('[BREAKDOWN] Division blocks from COMPLETE_BLOCKS_DATA:', divisionBlocks.length);

                // Merge with BLOCKS_DATA to get attack_rate, sph, etc.
                const mergedBlocks = divisionBlocks.map(block => {
                    const blockCode = block.block_code;
                    const riskData = blocksData[blockCode] || {};
                    return {
                        ...block,
                        attack_rate: riskData.attack_rate || 0,
                        sph: riskData.sph || 0,
                        loss_value_juta: riskData.loss_value_juta || 0
                    };
                });

                console.log('[BREAKDOWN] Merged blocks sample:', mergedBlocks[0]);

                // Categorize blocks by stadium
                const categories = {
                    critical: [], // Stadium 4
                    high: [],     // Stadium 3
                    medium: [],   // Stadium 2
                    low: []       // Stadium 1
                };

                mergedBlocks.forEach(block => {
                    const attackRate = parseFloat(block.attack_rate) || 0;
                    const gapPct = Math.abs(parseFloat(block.gap_pct) || 0);

                    // Stadium classification (inline logic)
                    if (attackRate >= 30 || gapPct >= 40) {
                        categories.critical.push(block);
                    } else if (attackRate >= 15 || gapPct >= 20) {
                        categories.high.push(block);
                    } else if (attackRate >= 5 || gapPct >= 10) {
                        categories.medium.push(block);
                    } else {
                        categories.low.push(block);
                    }
                });

                console.log('[BREAKDOWN] Categories:', {
                    critical: categories.critical.length,
                    high: categories.high.length,
                    medium: categories.medium.length,
                    low: categories.low.length
                });

                // Update modal content
                document.getElementById('breakdownDivisionSubtitle').textContent =
                    `${divisionCode} Division - ${metrics.totalBlocks} blok total`;

                // Update category counts
                document.getElementById('categoryCount_critical').textContent = categories.critical.length;
                document.getElementById('categoryCount_high').textContent = categories.high.length;
                document.getElementById('categoryCount_medium').textContent = categories.medium.length;
                document.getElementById('categoryCount_low').textContent = categories.low.length;

                // Calculate multi-factor analysis for CRITICAL + HIGH blocks (Stadium 3+)
                // This matches Division Overview "Critical Blocks" count
                const stadium3Plus = [...categories.critical, ...categories.high];

                console.log('[BREAKDOWN] Stadium 3+ blocks:', stadium3Plus.length);
                if (stadium3Plus.length > 0) {
                    console.log('[BREAKDOWN] Sample block fields:', stadium3Plus[0]);
                    console.log('[BREAKDOWN] ALL KEYS:', Object.keys(stadium3Plus[0]));
                }

                if (stadium3Plus.length > 0) {
                    const avgAR = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.attack_rate) || 0), 0) / stadium3Plus.length;
                    const avgSPH = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.sph) || 0), 0) / stadium3Plus.length;
                    const avgGap = stadium3Plus.reduce((sum, b) => sum + Math.abs(parseFloat(b.gap_pct) || 0), 0) / stadium3Plus.length;
                    const totalArea = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

                    console.log('[BREAKDOWN] Calculated avgAR:', avgAR);
                    console.log('[BREAKDOWN] Calculated avgSPH:', avgSPH);
                    console.log('[BREAKDOWN] Calculated avgGap:', avgGap);

                    document.getElementById('avgAR_critical').textContent = avgAR.toFixed(1) + '%';
                    document.getElementById('avgSPH_critical').textContent = Math.round(avgSPH);
                    document.getElementById('avgGap_critical').textContent = avgGap.toFixed(1) + '%';
                    document.getElementById('totalAreaRisk').textContent = totalArea.toFixed(1) + ' Ha';
                } else {
                    document.getElementById('avgAR_critical').textContent = '0%';
                    document.getElementById('avgSPH_critical').textContent = '0';
                    document.getElementById('avgGap_critical').textContent = '0%';
                    document.getElementById('totalAreaRisk').textContent = '0 Ha';
                }

                // Render distribution chart
                renderCategoryDistributionChart(categories);

                // Show modal
                const modal = document.getElementById('blockBreakdownModal');
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }'''

new_function = '''            function openBlockBreakdownModal(divisionCode) {
                divisionCode = divisionCode || window.currentDivision || 'AME02';
                console.log('[PRODUCTION TREND] Opening for division:', divisionCode);

                // Map division code format (button uses AME_II, data uses AME02)
                const divisionMap = {
                    'AME_I': 'AME01',
                    'AME_II': 'AME02',
                    'AME_III': 'AME03',
                    'OLE_I': 'OLE01',
                    'OLE_II': 'OLE02'
                };
                const mappedCode = divisionMap[divisionCode] || divisionCode;
                console.log('[PRODUCTION TREND] Mapped division code:', mappedCode);

                // Calculate breakdown using calculateDivisionMetrics
                const metrics = calculateDivisionMetrics(mappedCode);
                if (!metrics) {
                    alert(`No data for division: ${divisionCode}`);
                    return;
                }

                // Get all blocks for this division
                if (typeof COMPLETE_BLOCKS_DATA === 'undefined' || typeof HISTORICAL_YIELDS === 'undefined') {
                    alert('Block data not available. Please refresh the page.');
                    return;
                }

                const completeBlocks = Object.values(COMPLETE_BLOCKS_DATA);
                
                // Filter by division from COMPLETE_BLOCKS_DATA
                const divisionBlocks = completeBlocks.filter(block => block.division === mappedCode);
                console.log('[PRODUCTION TREND] Division blocks from COMPLETE_BLOCKS_DATA:', divisionBlocks.length);

                // Categorize blocks by production trend (2023-2025)
                const trendCategories = {
                    declining: [],   // Production MENURUN
                    increasing: [],  // Production MENINGKAT
                    stable: [],      // Production STABIL
                    noData: []       // Tidak ada data historis
                };

                divisionBlocks.forEach(block => {
                    const blockCode = block.block_code;
                    const historical = HISTORICAL_YIELDS[blockCode];
                    
                    if (historical && historical.yields) {
                        const y2023 = historical.yields[2023];
                        const y2025 = historical.yields[2025];
                        
                        if (y2023 && y2025) {
                            const prod2023 = y2023.real_ton_ha || 0;
                            const prod2025 = y2025.real_ton_ha || 0;
                            const change = prod2025 - prod2023;
                            const changePct = prod2023 > 0 ? ((prod2025 - prod2023) / prod2023) * 100 : 0;
                            
                            // Add trend data to block
                            block.prod2023 = prod2023;
                            block.prod2025 = prod2025;
                            block.prodChange = change;
                            block.prodChangePct = changePct;
                            
                            // Categorize: >5% change = significant, else stable
                            if (changePct < -5) {
                                trendCategories.declining.push(block);
                            } else if (changePct > 5) {
                                trendCategories.increasing.push(block);
                            } else {
                                trendCategories.stable.push(block);
                            }
                        } else {
                            block.prod2023 = 0;
                            block.prod2025 = 0;
                            block.prodChange = 0;
                            block.prodChangePct = 0;
                            trendCategories.noData.push(block);
                        }
                    } else {
                        block.prod2023 = 0;
                        block.prod2025 = 0;
                        block.prodChange = 0;
                        block.prodChangePct = 0;
                        trendCategories.noData.push(block);
                    }
                });

                console.log('[PRODUCTION TREND] Categories:', {
                    declining: trendCategories.declining.length,
                    increasing: trendCategories.increasing.length,
                    stable: trendCategories.stable.length,
                    noData: trendCategories.noData.length
                });

                // Sort declining blocks by change % (most negative first)
                trendCategories.declining.sort((a, b) => a.prodChangePct - b.prodChangePct);
                // Sort increasing blocks by change % (most positive first)
                trendCategories.increasing.sort((a, b) => b.prodChangePct - a.prodChangePct);

                // Update modal content
                document.getElementById('breakdownDivisionSubtitle').textContent =
                    `${divisionCode} Division - ${metrics.totalBlocks} blok total - TREN PRODUKSI 2023-2025`;

                // Update category counts
                document.getElementById('categoryCount_critical').textContent = trendCategories.declining.length;
                document.getElementById('categoryCount_high').textContent = trendCategories.stable.length;
                document.getElementById('categoryCount_medium').textContent = trendCategories.increasing.length;
                document.getElementById('categoryCount_low').textContent = trendCategories.noData.length;

                // Calculate averages for DECLINING blocks
                if (trendCategories.declining.length > 0) {
                    const avgChange = trendCategories.declining.reduce((sum, b) => sum + b.prodChangePct, 0) / trendCategories.declining.length;
                    const avgProd2023 = trendCategories.declining.reduce((sum, b) => sum + b.prod2023, 0) / trendCategories.declining.length;
                    const avgProd2025 = trendCategories.declining.reduce((sum, b) => sum + b.prod2025, 0) / trendCategories.declining.length;
                    const totalArea = trendCategories.declining.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

                    document.getElementById('avgAR_critical').textContent = avgChange.toFixed(1) + '%';
                    document.getElementById('avgSPH_critical').textContent = avgProd2023.toFixed(1) + ' T/Ha';
                    document.getElementById('avgGap_critical').textContent = avgProd2025.toFixed(1) + ' T/Ha';
                    document.getElementById('totalAreaRisk').textContent = totalArea.toFixed(1) + ' Ha';
                } else {
                    document.getElementById('avgAR_critical').textContent = '0%';
                    document.getElementById('avgSPH_critical').textContent = '0 T/Ha';
                    document.getElementById('avgGap_critical').textContent = '0 T/Ha';
                    document.getElementById('totalAreaRisk').textContent = '0 Ha';
                }

                // Render production trend chart
                renderProductionTrendChart(trendCategories);

                // Populate block lists
                populateBlockTrendLists(trendCategories);

                // Show modal
                const modal = document.getElementById('blockBreakdownModal');
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }'''

# Replace the function
content = content.replace(old_function_start, new_function)

# 2. Add the new renderProductionTrendChart function after renderCategoryDistributionChart
new_chart_function = '''
            // NEW: Render production trend chart
            function renderProductionTrendChart(trendCategories) {
                const ctx = document.getElementById('categoryDistributionChart');
                if (!ctx) return;

                // Destroy existing chart
                if (categoryDistributionChart) {
                    categoryDistributionChart.destroy();
                }

                const data = {
                    labels: ['📉 Penurunan', '➡️ Stabil', '📈 Kenaikan', '❓ No Data'],
                    datasets: [{
                        label: 'Number of Blocks',
                        data: [
                            trendCategories.declining.length,
                            trendCategories.stable.length,
                            trendCategories.increasing.length,
                            trendCategories.noData.length
                        ],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(34, 197, 94, 0.8)',
                            'rgba(148, 163, 184, 0.5)'
                        ],
                        borderColor: [
                            'rgb(239, 68, 68)',
                            'rgb(251, 191, 36)',
                            'rgb(34, 197, 94)',
                            'rgb(148, 163, 184)'
                        ],
                        borderWidth: 2
                    }]
                };

                categoryDistributionChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: data,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    color: '#fff',
                                    font: { size: 14, weight: 'bold' },
                                    padding: 15
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        const label = context.label || '';
                                        const value = context.raw;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const pct = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                        return `${label}: ${value} blok (${pct}%)`;
                                    }
                                }
                            }
                        }
                    }
                });
            }

            // NEW: Populate block trend lists
            function populateBlockTrendLists(trendCategories) {
                // Update declining blocks list
                const decliningList = document.getElementById('decliningBlocksList');
                if (decliningList) {
                    if (trendCategories.declining.length > 0) {
                        let html = trendCategories.declining.slice(0, 10).map(b => 
                            `<div class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1">
                                <span class="text-white font-medium">${b.block_code}</span>
                                <span class="text-red-400 font-bold">${b.prodChangePct.toFixed(1)}%</span>
                                <span class="text-slate-400 text-sm">${b.prod2023.toFixed(1)} → ${b.prod2025.toFixed(1)} T/Ha</span>
                            </div>`
                        ).join('');
                        if (trendCategories.declining.length > 10) {
                            html += `<div class="text-slate-400 text-sm text-center mt-2">+${trendCategories.declining.length - 10} blok lainnya...</div>`;
                        }
                        decliningList.innerHTML = html;
                    } else {
                        decliningList.innerHTML = '<div class="text-slate-500 text-center py-4">Tidak ada blok dengan tren penurunan signifikan</div>';
                    }
                }

                // Update increasing blocks list
                const increasingList = document.getElementById('increasingBlocksList');
                if (increasingList) {
                    if (trendCategories.increasing.length > 0) {
                        let html = trendCategories.increasing.slice(0, 10).map(b => 
                            `<div class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1">
                                <span class="text-white font-medium">${b.block_code}</span>
                                <span class="text-green-400 font-bold">+${b.prodChangePct.toFixed(1)}%</span>
                                <span class="text-slate-400 text-sm">${b.prod2023.toFixed(1)} → ${b.prod2025.toFixed(1)} T/Ha</span>
                            </div>`
                        ).join('');
                        if (trendCategories.increasing.length > 10) {
                            html += `<div class="text-slate-400 text-sm text-center mt-2">+${trendCategories.increasing.length - 10} blok lainnya...</div>`;
                        }
                        increasingList.innerHTML = html;
                    } else {
                        increasingList.innerHTML = '<div class="text-slate-500 text-center py-4">Tidak ada blok dengan tren kenaikan signifikan</div>';
                    }
                }
            }
'''

# Find the end of renderCategoryDistributionChart and insert after it
# Look for the closing of that function
insert_after = "                    }\n                });\n            }\n\n            function closeBlockBreakdownModal()"
insert_replacement = '''                    }
                });
            }
''' + new_chart_function + '''
            function closeBlockBreakdownModal()'''

content = content.replace(insert_after, insert_replacement)

# 3. Update the modal HTML structure
old_modal_content = '''                    <!-- Category Cards Grid -->
                    <div class="grid grid-cols-4 gap-4 mb-6">
                        <!-- CRITICAL -->
                        <div
                            class="bg-gradient-to-br from-red-900/40 to-red-800/20 rounded-xl p-6 border-2 border-red-500/40">
                            <div class="text-4xl mb-2">🔴</div>
                            <div class="text-red-200 text-xs font-bold uppercase mb-2">CRITICAL</div>
                            <div class="text-5xl font-black text-red-400 mb-2" id="categoryCount_critical">0</div>
                            <div class="text-xs text-red-300/70">Stadium 4 • AR ≥ 30%</div>
                        </div>

                        <!-- HIGH -->
                        <div
                            class="bg-gradient-to-br from-orange-900/40 to-orange-800/20 rounded-xl p-6 border-2 border-orange-500/40">
                            <div class="text-4xl mb-2">🟠</div>
                            <div class="text-orange-200 text-xs font-bold uppercase mb-2">HIGH</div>
                            <div class="text-5xl font-black text-orange-400 mb-2" id="categoryCount_high">0</div>
                            <div class="text-xs text-orange-300/70">Stadium 3 • AR 15-30%</div>
                        </div>

                        <!-- MEDIUM -->
                        <div
                            class="bg-gradient-to-br from-yellow-900/40 to-yellow-800/20 rounded-xl p-6 border-2 border-yellow-500/40">
                            <div class="text-4xl mb-2">🟡</div>
                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">MEDIUM</div>
                            <div class="text-5xl font-black text-yellow-400 mb-2" id="categoryCount_medium">0</div>
                            <div class="text-xs text-yellow-300/70">Stadium 2 • AR 5-15%</div>
                        </div>

                        <!-- LOW -->
                        <div
                            class="bg-gradient-to-br from-green-900/40 to-green-800/20 rounded-xl p-6 border-2 border-green-500/40">
                            <div class="text-4xl mb-2">🟢</div>
                            <div class="text-green-200 text-xs font-bold uppercase mb-2">LOW</div>
                            <div class="text-5xl font-black text-green-400 mb-2" id="categoryCount_low">0</div>
                            <div class="text-xs text-green-300/70">Stadium 1 • AR < 5%</div>
                            </div>
                        </div>

                        <!-- Multi-Factor Analysis -->
                        <div class="bg-black/20 rounded-xl p-6 border border-slate-700 mb-6">
                            <h3 class="text-xl font-bold text-white mb-4">📈 Multi-Factor Analysis Summary</h3>
                            <div class="grid grid-cols-2 gap-4">
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg Attack Rate (Critical)</div>
                                    <div class="text-2xl font-bold text-red-400" id="avgAR_critical">0%</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg SPH Decline (Critical)</div>
                                    <div class="text-2xl font-bold text-orange-400" id="avgSPH_critical">0</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg Yield Gap (Critical)</div>
                                    <div class="text-2xl font-bold text-yellow-400" id="avgGap_critical">0%</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Total Area at Risk</div>
                                    <div class="text-2xl font-bold text-cyan-400" id="totalAreaRisk">0 Ha</div>
                                </div>
                            </div>
                        </div>

                        <!-- Distribution Chart -->
                        <div class="bg-black/20 rounded-xl p-6 border border-slate-700">
                            <h3 class="text-xl font-bold text-white mb-4">📊 Category Distribution</h3>
                            <div style="height: 300px;">
                                <canvas id="categoryDistributionChart"></canvas>
                            </div>
                        </div>
                    </div>'''

new_modal_content = '''                    <!-- Production Trend Cards Grid -->
                    <div class="grid grid-cols-4 gap-4 mb-6">
                        <!-- DECLINING (PENURUNAN) -->
                        <div
                            class="bg-gradient-to-br from-red-900/40 to-red-800/20 rounded-xl p-6 border-2 border-red-500/40">
                            <div class="text-4xl mb-2">📉</div>
                            <div class="text-red-200 text-xs font-bold uppercase mb-2">TREN PENURUNAN</div>
                            <div class="text-5xl font-black text-red-400 mb-2" id="categoryCount_critical">0</div>
                            <div class="text-xs text-red-300/70">Produksi turun &gt;5%</div>
                        </div>

                        <!-- STABLE (STABIL) -->
                        <div
                            class="bg-gradient-to-br from-yellow-900/40 to-yellow-800/20 rounded-xl p-6 border-2 border-yellow-500/40">
                            <div class="text-4xl mb-2">➡️</div>
                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">TREN STABIL</div>
                            <div class="text-5xl font-black text-yellow-400 mb-2" id="categoryCount_high">0</div>
                            <div class="text-xs text-yellow-300/70">Perubahan -5% s/d +5%</div>
                        </div>

                        <!-- INCREASING (KENAIKAN) -->
                        <div
                            class="bg-gradient-to-br from-green-900/40 to-green-800/20 rounded-xl p-6 border-2 border-green-500/40">
                            <div class="text-4xl mb-2">📈</div>
                            <div class="text-green-200 text-xs font-bold uppercase mb-2">TREN KENAIKAN</div>
                            <div class="text-5xl font-black text-green-400 mb-2" id="categoryCount_medium">0</div>
                            <div class="text-xs text-green-300/70">Produksi naik &gt;5%</div>
                        </div>

                        <!-- NO DATA -->
                        <div
                            class="bg-gradient-to-br from-slate-800/40 to-slate-700/20 rounded-xl p-6 border-2 border-slate-500/40">
                            <div class="text-4xl mb-2">❓</div>
                            <div class="text-slate-300 text-xs font-bold uppercase mb-2">NO DATA</div>
                            <div class="text-5xl font-black text-slate-400 mb-2" id="categoryCount_low">0</div>
                            <div class="text-xs text-slate-400/70">Tidak ada data historis</div>
                        </div>
                    </div>

                    <!-- Analysis Summary for DECLINING blocks -->
                    <div class="bg-black/20 rounded-xl p-6 border border-red-700/50 mb-6">
                        <h3 class="text-xl font-bold text-red-400 mb-4">📉 Analisis Blok dengan Tren Penurunan</h3>
                        <div class="grid grid-cols-4 gap-4">
                            <div class="bg-slate-800/50 rounded-lg p-4">
                                <div class="text-xs text-slate-400 mb-1">Rata-rata Perubahan</div>
                                <div class="text-2xl font-bold text-red-400" id="avgAR_critical">0%</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-4">
                                <div class="text-xs text-slate-400 mb-1">Avg Produksi 2023</div>
                                <div class="text-2xl font-bold text-orange-400" id="avgSPH_critical">0 T/Ha</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-4">
                                <div class="text-xs text-slate-400 mb-1">Avg Produksi 2025</div>
                                <div class="text-2xl font-bold text-yellow-400" id="avgGap_critical">0 T/Ha</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-4">
                                <div class="text-xs text-slate-400 mb-1">Total Luas Terdampak</div>
                                <div class="text-2xl font-bold text-cyan-400" id="totalAreaRisk">0 Ha</div>
                            </div>
                        </div>
                    </div>

                    <!-- Two Column Layout: Block Lists -->
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <!-- DECLINING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                            <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                📉 Blok dengan Penurunan Produksi
                            </h3>
                            <div id="decliningBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                <div class="text-slate-500 text-center py-4">Loading...</div>
                            </div>
                        </div>

                        <!-- INCREASING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-green-700/30">
                            <h3 class="text-lg font-bold text-green-400 mb-3 flex items-center gap-2">
                                📈 Blok dengan Kenaikan Produksi
                            </h3>
                            <div id="increasingBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                <div class="text-slate-500 text-center py-4">Loading...</div>
                            </div>
                        </div>
                    </div>

                    <!-- Distribution Chart -->
                    <div class="bg-black/20 rounded-xl p-6 border border-slate-700">
                        <h3 class="text-xl font-bold text-white mb-4">📊 Distribusi Tren Produksi (2023-2025)</h3>
                        <div style="height: 300px;">
                            <canvas id="categoryDistributionChart"></canvas>
                        </div>
                    </div>
                </div>'''

content = content.replace(old_modal_content, new_modal_content)

# 4. Update modal header
old_header = '''                        <h2 class="text-3xl font-black text-white flex items-center gap-3">
                            <span class="text-4xl">📊</span>
                            BLOCK CATEGORIZATION
                        </h2>'''

new_header = '''                        <h2 class="text-3xl font-black text-white flex items-center gap-3">
                            <span class="text-4xl">📊</span>
                            TREN PRODUKSI PER BLOK
                        </h2>'''

content = content.replace(old_header, new_header)

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully modified Block Breakdown Modal to show Production Trends!")
print("Changes made:")
print("1. Modified openBlockBreakdownModal() to categorize by production trend")
print("2. Added renderProductionTrendChart() function")
print("3. Added populateBlockTrendLists() function")
print("4. Updated modal HTML with new layout for trend categories")
print("5. Updated modal header from 'BLOCK CATEGORIZATION' to 'TREN PRODUKSI PER BLOK'")
