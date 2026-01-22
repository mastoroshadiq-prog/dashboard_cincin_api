"""
Menambahkan:
1. Chart visualisasi tren produksi per blok (2023-2025)
2. Fitur klik pada blok untuk detail lebih lanjut
"""

import re

# Read the HTML file
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Find and update the modal HTML to add chart and make blocks clickable
# Find the current block lists section and add chart above it

old_block_lists = '''                    <!-- Two Column Layout: Block Lists -->
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
                    </div>'''

new_block_lists = '''                    <!-- Production Trend Chart per Block -->
                    <div class="bg-black/20 rounded-xl p-4 border border-cyan-700/30 mb-6">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            📊 Tren Produksi Per Blok (2023-2025)
                            <span class="text-xs text-slate-400 font-normal ml-2">Klik blok untuk detail</span>
                        </h3>
                        <div style="height: 300px;">
                            <canvas id="blockTrendChart"></canvas>
                        </div>
                    </div>

                    <!-- Two Column Layout: Block Lists -->
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <!-- DECLINING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                            <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                📉 Blok dengan Penurunan Produksi
                                <span class="text-xs text-slate-400 font-normal">(klik untuk detail)</span>
                            </h3>
                            <div id="decliningBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                <div class="text-slate-500 text-center py-4">Loading...</div>
                            </div>
                        </div>

                        <!-- INCREASING BLOCKS LIST -->
                        <div class="bg-black/20 rounded-xl p-4 border border-green-700/30">
                            <h3 class="text-lg font-bold text-green-400 mb-3 flex items-center gap-2">
                                📈 Blok dengan Kenaikan Produksi
                                <span class="text-xs text-slate-400 font-normal">(klik untuk detail)</span>
                            </h3>
                            <div id="increasingBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                <div class="text-slate-500 text-center py-4">Loading...</div>
                            </div>
                        </div>
                    </div>

                    <!-- Block Detail Panel (hidden by default) -->
                    <div id="blockDetailPanel" class="hidden bg-gradient-to-br from-slate-800/90 to-slate-900/90 rounded-xl p-6 border-2 border-cyan-500/50 mb-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold text-white flex items-center gap-2">
                                <span class="text-2xl">🔍</span>
                                <span id="detailBlockCode">-</span>
                            </h3>
                            <button onclick="closeBlockDetail()" class="text-slate-400 hover:text-white transition-colors">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        </div>
                        
                        <!-- Block Info Grid -->
                        <div class="grid grid-cols-4 gap-4 mb-4">
                            <div class="bg-slate-700/50 rounded-lg p-3">
                                <div class="text-xs text-slate-400 mb-1">Luas</div>
                                <div class="text-xl font-bold text-white" id="detailLuas">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3">
                                <div class="text-xs text-slate-400 mb-1">Produksi 2023</div>
                                <div class="text-xl font-bold text-cyan-400" id="detailProd2023">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3">
                                <div class="text-xs text-slate-400 mb-1">Produksi 2025</div>
                                <div class="text-xl font-bold text-cyan-400" id="detailProd2025">-</div>
                            </div>
                            <div class="bg-slate-700/50 rounded-lg p-3">
                                <div class="text-xs text-slate-400 mb-1">Perubahan</div>
                                <div class="text-xl font-bold" id="detailChange">-</div>
                            </div>
                        </div>

                        <!-- Detail Chart -->
                        <div class="bg-black/30 rounded-lg p-4">
                            <div style="height: 200px;">
                                <canvas id="blockDetailChart"></canvas>
                            </div>
                        </div>
                    </div>'''

content = content.replace(old_block_lists, new_block_lists)

# 2. Add JavaScript functions for the new features
# Find the populateBlockTrendLists function and update it to make blocks clickable

old_populate_function = '''            // NEW: Populate block trend lists
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
                console.log('[PRODUCTION TREND] Block lists populated');
            }'''

new_populate_function = '''            // Store current trend data for chart
            let currentTrendCategories = null;
            let blockTrendChart = null;
            let blockDetailChart = null;

            // NEW: Populate block trend lists with clickable items
            function populateBlockTrendLists(trendCategories) {
                currentTrendCategories = trendCategories;

                // Update declining blocks list with clickable items
                const decliningList = document.getElementById('decliningBlocksList');
                if (decliningList) {
                    if (trendCategories.declining.length > 0) {
                        let html = trendCategories.declining.slice(0, 10).map(b => 
                            `<div onclick="showBlockDetail('${b.block_code}')" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer hover:bg-red-900/40 hover:scale-102 transition-all duration-200 border border-transparent hover:border-red-500/50">
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

                // Update increasing blocks list with clickable items
                const increasingList = document.getElementById('increasingBlocksList');
                if (increasingList) {
                    if (trendCategories.increasing.length > 0) {
                        let html = trendCategories.increasing.slice(0, 10).map(b => 
                            `<div onclick="showBlockDetail('${b.block_code}')" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer hover:bg-green-900/40 hover:scale-102 transition-all duration-200 border border-transparent hover:border-green-500/50">
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

                // Render the block trend chart
                renderBlockTrendChart(trendCategories);
                console.log('[PRODUCTION TREND] Block lists populated with click handlers');
            }

            // NEW: Render block trend chart (bar chart showing all blocks)
            function renderBlockTrendChart(trendCategories) {
                const ctx = document.getElementById('blockTrendChart');
                if (!ctx) return;

                // Destroy existing chart
                if (blockTrendChart) {
                    blockTrendChart.destroy();
                }

                // Combine all blocks and sort by change %
                const allBlocks = [
                    ...trendCategories.declining,
                    ...trendCategories.stable,
                    ...trendCategories.increasing
                ].sort((a, b) => a.prodChangePct - b.prodChangePct);

                // Take top 15 declining and top 15 increasing for display
                const displayBlocks = [
                    ...allBlocks.slice(0, 8),  // Most declining
                    ...allBlocks.slice(-8)      // Most increasing
                ];

                const labels = displayBlocks.map(b => b.block_code);
                const changeData = displayBlocks.map(b => b.prodChangePct);
                const colors = displayBlocks.map(b => 
                    b.prodChangePct < -5 ? 'rgba(239, 68, 68, 0.8)' :
                    b.prodChangePct > 5 ? 'rgba(34, 197, 94, 0.8)' :
                    'rgba(251, 191, 36, 0.8)'
                );
                const borderColors = displayBlocks.map(b =>
                    b.prodChangePct < -5 ? 'rgb(239, 68, 68)' :
                    b.prodChangePct > 5 ? 'rgb(34, 197, 94)' :
                    'rgb(251, 191, 36)'
                );

                blockTrendChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Perubahan Produksi (%)',
                            data: changeData,
                            backgroundColor: colors,
                            borderColor: borderColors,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        onClick: (event, elements) => {
                            if (elements.length > 0) {
                                const index = elements[0].index;
                                const blockCode = labels[index];
                                showBlockDetail(blockCode);
                            }
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const block = displayBlocks[context.dataIndex];
                                        return [
                                            `Perubahan: ${block.prodChangePct.toFixed(1)}%`,
                                            `2023: ${block.prod2023.toFixed(1)} T/Ha`,
                                            `2025: ${block.prod2025.toFixed(1)} T/Ha`
                                        ];
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { 
                                    color: '#94a3b8',
                                    callback: function(value) { return value + '%'; }
                                },
                                title: {
                                    display: true,
                                    text: 'Perubahan (%)',
                                    color: '#94a3b8'
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { 
                                    color: '#94a3b8',
                                    maxRotation: 45,
                                    minRotation: 45
                                }
                            }
                        }
                    }
                });
                console.log('[PRODUCTION TREND] Block trend chart rendered');
            }

            // NEW: Show block detail panel
            function showBlockDetail(blockCode) {
                const historical = HISTORICAL_YIELDS[blockCode];
                if (!historical) {
                    console.log('[BLOCK DETAIL] No data for:', blockCode);
                    return;
                }

                // Update detail panel content
                document.getElementById('detailBlockCode').textContent = `Detail Blok: ${blockCode}`;
                document.getElementById('detailLuas').textContent = `${historical.luas_ha.toFixed(1)} Ha`;

                const y2023 = historical.yields['2023'] || historical.yields[2023];
                const y2024 = historical.yields['2024'] || historical.yields[2024];
                const y2025 = historical.yields['2025'] || historical.yields[2025];

                const prod2023 = y2023 ? y2023.real_ton_ha : 0;
                const prod2024 = y2024 ? y2024.real_ton_ha : 0;
                const prod2025 = y2025 ? y2025.real_ton_ha : 0;

                document.getElementById('detailProd2023').textContent = `${prod2023.toFixed(1)} T/Ha`;
                document.getElementById('detailProd2025').textContent = `${prod2025.toFixed(1)} T/Ha`;

                const changePct = prod2023 > 0 ? ((prod2025 - prod2023) / prod2023) * 100 : 0;
                const changeEl = document.getElementById('detailChange');
                changeEl.textContent = `${changePct >= 0 ? '+' : ''}${changePct.toFixed(1)}%`;
                changeEl.className = `text-xl font-bold ${changePct < -5 ? 'text-red-400' : changePct > 5 ? 'text-green-400' : 'text-yellow-400'}`;

                // Show detail panel
                document.getElementById('blockDetailPanel').classList.remove('hidden');

                // Render detail chart
                renderBlockDetailChart(blockCode, prod2023, prod2024, prod2025, y2023, y2024, y2025);

                // Scroll to detail panel
                document.getElementById('blockDetailPanel').scrollIntoView({ behavior: 'smooth', block: 'center' });

                console.log('[BLOCK DETAIL] Showing detail for:', blockCode);
            }

            // NEW: Close block detail panel
            function closeBlockDetail() {
                document.getElementById('blockDetailPanel').classList.add('hidden');
                if (blockDetailChart) {
                    blockDetailChart.destroy();
                    blockDetailChart = null;
                }
            }

            // NEW: Render block detail chart
            function renderBlockDetailChart(blockCode, prod2023, prod2024, prod2025, y2023, y2024, y2025) {
                const ctx = document.getElementById('blockDetailChart');
                if (!ctx) return;

                // Destroy existing chart
                if (blockDetailChart) {
                    blockDetailChart.destroy();
                }

                const poten2023 = y2023 ? y2023.poten_ton_ha : 0;
                const poten2024 = y2024 ? y2024.poten_ton_ha : 0;
                const poten2025 = y2025 ? y2025.poten_ton_ha : 0;

                blockDetailChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [
                            {
                                label: 'Produksi Aktual (T/Ha)',
                                data: [prod2023, prod2024, prod2025],
                                borderColor: 'rgb(34, 211, 238)',
                                backgroundColor: 'rgba(34, 211, 238, 0.2)',
                                fill: true,
                                tension: 0.3,
                                pointRadius: 6,
                                pointHoverRadius: 8,
                                borderWidth: 3
                            },
                            {
                                label: 'Potensi (T/Ha)',
                                data: [poten2023, poten2024, poten2025],
                                borderColor: 'rgb(251, 191, 36)',
                                backgroundColor: 'rgba(251, 191, 36, 0.1)',
                                fill: false,
                                tension: 0.3,
                                pointRadius: 4,
                                borderWidth: 2,
                                borderDash: [5, 5]
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#fff',
                                    font: { size: 12 },
                                    usePointStyle: true
                                }
                            },
                            title: {
                                display: true,
                                text: `Tren Produksi ${blockCode} (2023-2025)`,
                                color: '#fff',
                                font: { size: 14, weight: 'bold' }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `${context.dataset.label}: ${context.raw.toFixed(1)} T/Ha`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { color: '#94a3b8' },
                                title: {
                                    display: true,
                                    text: 'Ton/Ha',
                                    color: '#94a3b8'
                                }
                            },
                            x: {
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { color: '#94a3b8' }
                            }
                        }
                    }
                });
                console.log('[BLOCK DETAIL] Detail chart rendered for:', blockCode);
            }'''

content = content.replace(old_populate_function, new_populate_function)

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully added:")
print("1. Block Trend Chart - Bar chart showing production changes for all blocks")
print("2. Clickable block items in declining/increasing lists")
print("3. Block Detail Panel - Shows when clicking a block")
print("4. Block Detail Chart - Line chart showing 2023-2025 trend with potential comparison")
