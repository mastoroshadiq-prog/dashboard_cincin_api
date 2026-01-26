"""
Add Block Detail Panel with:
1. Line chart showing production trend 2023-2025
2. Loss/kerugian information
3. Attack rate/stadium
4. SPH (Stands Per Hectare)
5. Yield (ton/ha)
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Block Detail Panel HTML before the closing modal div
# Find the distribution chart section (near end of modal content)
panel_html = '''
                        <!-- BLOCK DETAIL PANEL (Hidden by default) -->
                        <div id="blockDetailPanel" class="hidden fixed inset-0 bg-black/80 z-[60] flex items-center justify-center p-4">
                            <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border-2 border-cyan-500/30 shadow-2xl">
                                <!-- Header -->
                                <div class="bg-gradient-to-r from-cyan-900 to-blue-900 p-4 rounded-t-2xl flex justify-between items-center border-b border-cyan-500/30">
                                    <div>
                                        <h3 class="text-2xl font-black text-white flex items-center gap-2">
                                            📊 Detail Blok <span id="detailBlockCode" class="text-cyan-400">-</span>
                                        </h3>
                                        <p class="text-slate-300 text-sm">Analisis tren produksi dan risiko</p>
                                    </div>
                                    <button onclick="closeBlockDetail()" class="text-3xl text-slate-400 hover:text-white transition-colors">&times;</button>
                                </div>
                                
                                <!-- Content -->
                                <div class="p-6 space-y-6">
                                    <!-- Trend Chart -->
                                    <div class="bg-black/30 rounded-xl p-4 border border-cyan-700/30">
                                        <h4 class="text-lg font-bold text-cyan-400 mb-3">📈 Tren Produksi 2023-2025</h4>
                                        <div class="h-64">
                                            <canvas id="blockDetailChart"></canvas>
                                        </div>
                                    </div>
                                    
                                    <!-- Metrics Grid -->
                                    <div class="grid grid-cols-2 gap-4">
                                        <!-- Left Column: Production Metrics -->
                                        <div class="space-y-3">
                                            <h4 class="text-md font-bold text-white flex items-center gap-2">
                                                🌾 Metrik Produksi
                                            </h4>
                                            <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                                                <div class="text-xs text-slate-400">Luas Area</div>
                                                <div class="text-xl font-bold text-white" id="detailLuas">- Ha</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                                                <div class="text-xs text-slate-400">Yield 2023</div>
                                                <div class="text-xl font-bold text-cyan-400" id="detailYield2023">- T/Ha</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                                                <div class="text-xs text-slate-400">Yield 2025</div>
                                                <div class="text-xl font-bold text-cyan-400" id="detailYield2025">- T/Ha</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                                                <div class="text-xs text-slate-400">Perubahan Produksi</div>
                                                <div class="text-xl font-bold" id="detailChange">-%</div>
                                            </div>
                                        </div>
                                        
                                        <!-- Right Column: Risk Metrics -->
                                        <div class="space-y-3">
                                            <h4 class="text-md font-bold text-white flex items-center gap-2">
                                                ⚠️ Metrik Risiko
                                            </h4>
                                            <div class="bg-black/30 rounded-lg p-3 border border-red-700/30">
                                                <div class="text-xs text-slate-400">Attack Rate</div>
                                                <div class="text-xl font-bold text-red-400" id="detailAttackRate">- %</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-orange-700/30">
                                                <div class="text-xs text-slate-400">Stadium</div>
                                                <div class="text-xl font-bold text-orange-400" id="detailStadium">-</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-yellow-700/30">
                                                <div class="text-xs text-slate-400">SPH (Stands/Ha)</div>
                                                <div class="text-xl font-bold text-yellow-400" id="detailSPH">-</div>
                                            </div>
                                            <div class="bg-black/30 rounded-lg p-3 border border-rose-700/30">
                                                <div class="text-xs text-slate-400">Estimasi Kerugian</div>
                                                <div class="text-xl font-bold text-rose-400" id="detailLoss">Rp - Juta</div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Yield Gap Analysis -->
                                    <div class="bg-gradient-to-r from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-600">
                                        <h4 class="text-md font-bold text-white mb-3">📉 Analisis Gap Yield</h4>
                                        <div class="grid grid-cols-3 gap-4 text-center">
                                            <div>
                                                <div class="text-xs text-slate-400">Potensi</div>
                                                <div class="text-lg font-bold text-green-400" id="detailPotential">- T/Ha</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-400">Realisasi</div>
                                                <div class="text-lg font-bold text-blue-400" id="detailActual">- T/Ha</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-400">Gap</div>
                                                <div class="text-lg font-bold text-red-400" id="detailGap">- %</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
'''

# Find a good place to insert - after distribution chart section
dist_chart_end = content.find('categoryDistributionChart')
if dist_chart_end > 0:
    # Find the closing div of the distribution section
    modal_content_div = content.find('</div>\n                    </div>\n                </div>\n            </div>', dist_chart_end)
    if modal_content_div > 0:
        # Insert before modal closing
        insert_pos = modal_content_div + len('</div>')
        content = content[:insert_pos] + panel_html + content[insert_pos:]
        print("✅ Added Block Detail Panel HTML")
else:
    print("⚠️ Could not find distribution chart section")
    # Try alternative: find end of modal
    modal_end = content.find('id="blockBreakdownModal"')
    if modal_end > 0:
        # Find a suitable position
        end_divs = content.find('</div>\n            </div>\n        </div>', modal_end + 1000)
        if end_divs > 0:
            content = content[:end_divs] + panel_html + content[end_divs:]
            print("✅ Added Block Detail Panel HTML (alternative position)")

# 2. Add showBlockDetail and closeBlockDetail JavaScript functions
js_functions = '''
            // ============================================
            // BLOCK DETAIL FUNCTIONS
            // ============================================
            let blockDetailChart = null;
            
            function showBlockDetail(blockCode) {
                console.log('[BLOCK DETAIL] Opening for:', blockCode);
                
                // Get panel elements
                const panel = document.getElementById('blockDetailPanel');
                if (!panel) {
                    console.error('Block detail panel not found');
                    return;
                }
                
                // Set block code
                document.getElementById('detailBlockCode').textContent = blockCode;
                
                // Get historical data
                const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                
                // Get risk data from BLOCKS_DATA
                const riskData = typeof BLOCKS_DATA !== 'undefined' ? BLOCKS_DATA[blockCode] : null;
                
                // Calculate metrics
                let luas = 0, yield2023 = 0, yield2024 = 0, yield2025 = 0;
                let poten2023 = 0, poten2024 = 0, poten2025 = 0;
                let gap2025 = 0;
                
                if (historical) {
                    luas = historical.luas_ha || 0;
                    const y23 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y24 = historical.yields[2024] || historical.yields['2024'] || {};
                    const y25 = historical.yields[2025] || historical.yields['2025'] || {};
                    
                    yield2023 = y23.real_ton_ha || 0;
                    yield2024 = y24.real_ton_ha || 0;
                    yield2025 = y25.real_ton_ha || 0;
                    
                    poten2023 = y23.poten_ton_ha || 0;
                    poten2024 = y24.poten_ton_ha || 0;
                    poten2025 = y25.poten_ton_ha || 0;
                    
                    gap2025 = y25.gap_pct || 0;
                }
                
                const changePct = yield2023 > 0 ? ((yield2025 - yield2023) / yield2023) * 100 : 0;
                
                // Get risk metrics
                let attackRate = 0, stadium = '-', sph = 0, lossValue = 0;
                if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                    
                    // Determine stadium
                    if (attackRate >= 30) stadium = 'Stadium 4 (Kritis)';
                    else if (attackRate >= 15) stadium = 'Stadium 3 (Tinggi)';
                    else if (attackRate >= 5) stadium = 'Stadium 2 (Sedang)';
                    else stadium = 'Stadium 1 (Rendah)';
                }
                
                // Update UI
                document.getElementById('detailLuas').textContent = luas.toFixed(1) + ' Ha';
                document.getElementById('detailYield2023').textContent = yield2023.toFixed(1) + ' T/Ha';
                document.getElementById('detailYield2025').textContent = yield2025.toFixed(1) + ' T/Ha';
                
                const changeEl = document.getElementById('detailChange');
                changeEl.textContent = (changePct >= 0 ? '+' : '') + changePct.toFixed(1) + '%';
                changeEl.className = 'text-xl font-bold ' + (changePct >= 0 ? 'text-green-400' : 'text-red-400');
                
                document.getElementById('detailAttackRate').textContent = attackRate.toFixed(1) + ' %';
                document.getElementById('detailStadium').textContent = stadium;
                document.getElementById('detailSPH').textContent = Math.round(sph);
                document.getElementById('detailLoss').textContent = 'Rp ' + lossValue.toFixed(1) + ' Juta';
                
                document.getElementById('detailPotential').textContent = poten2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailActual').textContent = yield2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailGap').textContent = gap2025.toFixed(1) + '%';
                
                // Render chart
                renderBlockDetailChart(blockCode, yield2023, yield2024, yield2025, poten2023, poten2024, poten2025);
                
                // Show panel
                panel.classList.remove('hidden');
            }
            
            function closeBlockDetail() {
                const panel = document.getElementById('blockDetailPanel');
                if (panel) {
                    panel.classList.add('hidden');
                }
                if (blockDetailChart) {
                    blockDetailChart.destroy();
                    blockDetailChart = null;
                }
            }
            
            function renderBlockDetailChart(blockCode, y23, y24, y25, p23, p24, p25) {
                const ctx = document.getElementById('blockDetailChart');
                if (!ctx) return;
                
                // Destroy existing
                if (blockDetailChart) {
                    blockDetailChart.destroy();
                }
                
                blockDetailChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [
                            {
                                label: 'Realisasi (T/Ha)',
                                data: [y23, y24, y25],
                                borderColor: 'rgb(34, 211, 238)',
                                backgroundColor: 'rgba(34, 211, 238, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.3,
                                pointRadius: 6,
                                pointBackgroundColor: 'rgb(34, 211, 238)'
                            },
                            {
                                label: 'Potensi (T/Ha)',
                                data: [p23, p24, p25],
                                borderColor: 'rgb(34, 197, 94)',
                                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                fill: false,
                                tension: 0.3,
                                pointRadius: 4,
                                pointBackgroundColor: 'rgb(34, 197, 94)'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: { color: '#fff', font: { size: 12 } }
                            },
                            title: {
                                display: true,
                                text: 'Trend Produksi Blok ' + blockCode,
                                color: '#fff',
                                font: { size: 14, weight: 'bold' }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: false,
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { 
                                    color: '#fff',
                                    callback: function(value) { return value.toFixed(1) + ' T/Ha'; }
                                }
                            },
                            x: {
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                ticks: { color: '#fff' }
                            }
                        }
                    }
                });
            }
'''

# Find a good place to insert the JS - before the closing </script> near end
# Look for last </script> tag
last_script_end = content.rfind('</script>')
if last_script_end > 0:
    # Check if functions already exist
    if 'function showBlockDetail' not in content:
        content = content[:last_script_end] + js_functions + '\n        ' + content[last_script_end:]
        print("✅ Added showBlockDetail JavaScript functions")
    else:
        print("✅ showBlockDetail functions already exist")

# 3. Update the block list items to call showBlockDetail on click
# Find and update the declining blocks list rendering
old_declining_render = '''let html = decliningBlocks.slice(0, 10).map(b => 
                            '<div class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 border border-transparent hover:border-red-500/50">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                            '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');'''

new_declining_render = '''let html = decliningBlocks.slice(0, 10).map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer border border-transparent hover:border-red-500/50 hover:bg-red-900/40 transition-all">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                            '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');'''

if old_declining_render in content:
    content = content.replace(old_declining_render, new_declining_render)
    print("✅ Updated declining blocks with onclick")

# Similar for increasing blocks
old_increasing_render = '''let html = increasingBlocks.slice(0, 10).map(b => 
                        '<div class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 border border-transparent hover:border-green-500/50">' +
                        '<span class="text-white font-medium">' + b.block_code + '</span>' +
                        '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                        '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                        '</div>'
                    ).join('');'''

new_increasing_render = '''let html = increasingBlocks.slice(0, 10).map(b => 
                        '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer border border-transparent hover:border-green-500/50 hover:bg-green-900/40 transition-all">' +
                        '<span class="text-white font-medium">' + b.block_code + '</span>' +
                        '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                        '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                        '</div>'
                    ).join('');'''

if old_increasing_render in content:
    content = content.replace(old_increasing_render, new_increasing_render)
    print("✅ Updated increasing blocks with onclick")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
