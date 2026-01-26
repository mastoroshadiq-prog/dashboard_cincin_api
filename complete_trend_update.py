"""
Script yang lebih aman untuk:
1. Update HISTORICAL_YIELDS dengan data lengkap
2. Menambahkan bar chart & click feature ke modal TANPA merusak HTML
"""

import json
import re

print("=== STEP 1: Load complete yields data ===")
with open('complete_historical_yields.json', 'r') as f:
    complete_data = json.load(f)
print(f"Loaded {len(complete_data)} blocks")

print("\n=== STEP 2: Read HTML file ===")
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()
print(f"File size: {len(content)} bytes")

# STEP 3: Find and replace HISTORICAL_YIELDS carefully
print("\n=== STEP 3: Update HISTORICAL_YIELDS ===")
start_marker = "const HISTORICAL_YIELDS = {"
start_pos = content.find(start_marker)

if start_pos == -1:
    print("ERROR: HISTORICAL_YIELDS not found!")
    exit(1)

print(f"Found at position {start_pos}")

# Count braces to find end
brace_count = 0
end_pos = start_pos
for i in range(start_pos, min(start_pos + 50000, len(content))):
    if content[i] == '{':
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end_pos = i + 1
            # Include semicolon if present
            if i + 1 < len(content) and content[i + 1] == ';':
                end_pos = i + 2
            break

print(f"Ends at position {end_pos} (length: {end_pos - start_pos})")

# Build new HISTORICAL_YIELDS
historical_yields = {}
for block_code, block_data in complete_data.items():
    yields = block_data.get('yields', {})
    historical_yields[block_code] = {
        'luas_ha': block_data.get('luas_ha', 0),
        'division': block_data.get('division', ''),
        'yields': {
            2023: yields.get('2023', {}),
            2024: yields.get('2024', {}),
            2025: yields.get('2025', {})
        }
    }

# Format as JavaScript - use proper indentation
js_lines = ["const HISTORICAL_YIELDS = {"]
for block_code, data in historical_yields.items():
    js_lines.append(f"                '{block_code}': {{")
    js_lines.append(f"                    luas_ha: {data['luas_ha']},")
    js_lines.append(f"                    division: '{data['division']}',")
    js_lines.append(f"                    yields: {{")
    for year in [2023, 2024, 2025]:
        y = data['yields'].get(year, {})
        js_lines.append(f"                        {year}: {{")
        js_lines.append(f"                            real_ton_ha: {y.get('real_ton_ha', 0)},")
        js_lines.append(f"                            poten_ton_ha: {y.get('poten_ton_ha', 0)},")
        js_lines.append(f"                            gap_pct: {y.get('gap_pct', 0)}")
        js_lines.append(f"                        }},")
    js_lines.append(f"                    }}")
    js_lines.append(f"                }},")
js_lines.append("            };")

new_historical = "\n".join(js_lines)
print(f"New HISTORICAL_YIELDS size: {len(new_historical)} bytes")

# Replace in content
content = content[:start_pos] + new_historical + content[end_pos:]

# STEP 4: Add bar chart canvas BEFORE the two-column block lists
print("\n=== STEP 4: Add bar chart HTML ===")

# Find the declining blocks list section
declining_pattern = r'(<!-- [^>]*DECLINING[^>]* -->[\s\r\n]*<div[^>]*border-red[^>]*>)'
match = re.search(declining_pattern, content, re.IGNORECASE)

if match:
    insert_pos = match.start()
    
    bar_chart_html = '''<!-- Block Trend Bar Chart -->
                    <div class="bg-black/20 rounded-xl p-4 border border-cyan-700/30 mb-6">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            📊 Perbandingan Tren Produksi Per Blok
                            <span class="text-xs text-slate-400 font-normal ml-2">(Klik bar untuk detail)</span>
                        </h3>
                        <div style="height: 280px;">
                            <canvas id="blockTrendBarChart"></canvas>
                        </div>
                    </div>

                    <!-- Block Detail Panel -->
                    <div id="blockDetailPanel" class="hidden bg-gradient-to-br from-slate-800/90 to-slate-900/90 rounded-xl p-5 border-2 border-cyan-500/50 mb-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold text-white flex items-center gap-2">
                                🔍 <span id="detailBlockCode">-</span>
                            </h3>
                            <button onclick="closeBlockDetail()" class="text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg p-1 transition-all">✕</button>
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
                            <div style="height: 180px;"><canvas id="blockDetailLineChart"></canvas></div>
                        </div>
                    </div>

                    '''
    
    content = content[:insert_pos] + bar_chart_html + content[insert_pos:]
    print("✅ Added bar chart HTML")
else:
    print("⚠️ Could not find declining blocks section, trying alternative...")
    # Try finding "Blok dengan Penurunan"
    alt_pos = content.find("Blok dengan Penurunan Produksi")
    if alt_pos > 0:
        # Go back to find the parent div
        # ...
        print("Found 'Blok dengan Penurunan' - manual insertion needed")

# STEP 5: Add JavaScript functions BEFORE the closing </script> before </body>
print("\n=== STEP 5: Add JavaScript functions ===")

js_functions = '''
            // ============================================
            // BLOCK TREND BAR CHART & DETAIL FUNCTIONS
            // ============================================
            var blockTrendBarChartInstance = null;
            var blockDetailLineChartInstance = null;

            function renderBlockTrendBarChart(trendCategories) {
                var ctx = document.getElementById('blockTrendBarChart');
                if (!ctx) { console.log('[TREND] Canvas not found'); return; }
                if (blockTrendBarChartInstance) blockTrendBarChartInstance.destroy();

                var allBlocks = trendCategories.declining.concat(trendCategories.stable, trendCategories.increasing);
                allBlocks.sort(function(a, b) { return a.prodChangePct - b.prodChangePct; });

                var displayBlocks = allBlocks.filter(function(b) { return b.prodChangePct < -5; }).slice(0, 8)
                    .concat(allBlocks.filter(function(b) { return b.prodChangePct > 5; }).slice(-8).reverse());

                if (displayBlocks.length === 0) return;

                var labels = displayBlocks.map(function(b) { return b.block_code; });
                var changeData = displayBlocks.map(function(b) { return b.prodChangePct; });
                var colors = displayBlocks.map(function(b) {
                    return b.prodChangePct < -5 ? 'rgba(239, 68, 68, 0.8)' :
                           b.prodChangePct > 5 ? 'rgba(34, 197, 94, 0.8)' : 'rgba(251, 191, 36, 0.8)';
                });

                blockTrendBarChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ label: 'Perubahan (%)', data: changeData, backgroundColor: colors, borderWidth: 1 }] },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        onClick: function(event, elements) {
                            if (elements.length > 0) showBlockDetail(displayBlocks[elements[0].index].block_code);
                        },
                        plugins: { legend: { display: false } },
                        scales: { y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8', callback: function(v) { return v + '%'; } } },
                                  x: { grid: { display: false }, ticks: { color: '#94a3b8', maxRotation: 45 } } }
                    }
                });
                console.log('[TREND] Bar chart rendered');
            }

            function showBlockDetail(blockCode) {
                var data = HISTORICAL_YIELDS[blockCode];
                if (!data) return;

                document.getElementById('detailBlockCode').textContent = 'Detail: ' + blockCode;
                document.getElementById('detailLuas').textContent = (data.luas_ha || 0).toFixed(1) + ' Ha';

                var y23 = data.yields[2023] || data.yields['2023'] || {};
                var y24 = data.yields[2024] || data.yields['2024'] || {};
                var y25 = data.yields[2025] || data.yields['2025'] || {};

                var p23 = y23.real_ton_ha || 0, p24 = y24.real_ton_ha || 0, p25 = y25.real_ton_ha || 0;
                document.getElementById('detailProd2023').textContent = p23.toFixed(1) + ' T/Ha';
                document.getElementById('detailProd2025').textContent = p25.toFixed(1) + ' T/Ha';

                var chg = p23 > 0 ? ((p25 - p23) / p23) * 100 : 0;
                var chgEl = document.getElementById('detailChange');
                chgEl.textContent = (chg >= 0 ? '+' : '') + chg.toFixed(1) + '%';
                chgEl.className = 'text-lg font-bold ' + (chg < -5 ? 'text-red-400' : (chg > 5 ? 'text-green-400' : 'text-yellow-400'));

                document.getElementById('blockDetailPanel').classList.remove('hidden');
                renderBlockDetailLineChart(blockCode, p23, p24, p25, y23, y24, y25);
                document.getElementById('blockDetailPanel').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            function closeBlockDetail() {
                document.getElementById('blockDetailPanel').classList.add('hidden');
                if (blockDetailLineChartInstance) { blockDetailLineChartInstance.destroy(); blockDetailLineChartInstance = null; }
            }

            function renderBlockDetailLineChart(blockCode, p23, p24, p25, y23, y24, y25) {
                var ctx = document.getElementById('blockDetailLineChart');
                if (!ctx) return;
                if (blockDetailLineChartInstance) blockDetailLineChartInstance.destroy();

                blockDetailLineChartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [
                            { label: 'Aktual (T/Ha)', data: [p23, p24, p25], borderColor: 'rgb(34, 211, 238)', backgroundColor: 'rgba(34, 211, 238, 0.2)', fill: true, tension: 0.3, pointRadius: 6, borderWidth: 3 },
                            { label: 'Potensi (T/Ha)', data: [y23.poten_ton_ha || 0, y24.poten_ton_ha || 0, y25.poten_ton_ha || 0], borderColor: 'rgb(251, 191, 36)', borderDash: [5, 5], fill: false, tension: 0.3, pointRadius: 4, borderWidth: 2 }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: { legend: { position: 'top', labels: { color: '#fff' } }, title: { display: true, text: 'Tren ' + blockCode, color: '#fff' } },
                        scales: { y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8' } }, x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8' } } }
                    }
                });
            }

            // Enhance populateBlockTrendLists with click handlers
            (function() {
                var origFn = typeof populateBlockTrendLists === 'function' ? populateBlockTrendLists : null;
                window.populateBlockTrendLists = function(trendCategories) {
                    if (origFn) origFn(trendCategories);

                    var decList = document.getElementById('decliningBlocksList');
                    if (decList && trendCategories.declining.length > 0) {
                        var html = '';
                        trendCategories.declining.slice(0, 10).forEach(function(b) {
                            html += '<div onclick="showBlockDetail(\\''+b.block_code+'\\')\" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer hover:bg-red-900/40 transition-all border border-transparent hover:border-red-500/50">' +
                                '<span class="text-white font-medium">' + b.block_code + '</span>' +
                                '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                                '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span></div>';
                        });
                        if (trendCategories.declining.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (trendCategories.declining.length - 10) + ' lainnya...</div>';
                        decList.innerHTML = html;
                    }

                    var incList = document.getElementById('increasingBlocksList');
                    if (incList && trendCategories.increasing.length > 0) {
                        var html = '';
                        trendCategories.increasing.slice(0, 10).forEach(function(b) {
                            html += '<div onclick="showBlockDetail(\\''+b.block_code+'\\')\" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer hover:bg-green-900/40 transition-all border border-transparent hover:border-green-500/50">' +
                                '<span class="text-white font-medium">' + b.block_code + '</span>' +
                                '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                                '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span></div>';
                        });
                        if (trendCategories.increasing.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (trendCategories.increasing.length - 10) + ' lainnya...</div>';
                        incList.innerHTML = html;
                    }

                    renderBlockTrendBarChart(trendCategories);
                };
            })();
'''

# Find the last </script> before </body>
body_close = content.rfind('</body>')
if body_close > 0:
    script_close = content.rfind('</script>', 0, body_close)
    if script_close > 0:
        content = content[:script_close] + js_functions + "\n        </script>" + content[script_close + 9:]
        print("✅ Added JavaScript functions")
    else:
        print("⚠️ Could not find </script> before </body>")
else:
    print("⚠️ Could not find </body>")

# Write back
print("\n=== STEP 6: Write file ===")
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ File written: {len(content)} bytes")
