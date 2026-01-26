"""
Add TBM Planting Year Statistics to Block Breakdown Modal
- Add a section showing planting year distribution chart for TBM blocks
- Display statistics: oldest/newest, count per year group
"""

import re
import json

# Read the HTML file
html_file = r'data\output\DASHBOARD_DEMO_FEATURES.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Read planting year data
with open('planting_year_data.json', 'r') as f:
    planting_data = json.load(f)

# Create PLANTING_YEAR_DATA JavaScript object
planting_year_js = "const PLANTING_YEAR_DATA = " + json.dumps({p['block_code']: p['planting_year'] for p in planting_data}, indent=2) + ";"

# Find where to add the TBM statistics section (after TBM block list)
# Look for the tbmBlocksList div and add after it

tbm_stats_html = '''
                    <!-- TBM PLANTING YEAR STATISTICS -->
                    <div id="tbmStatsSection" class="mt-6 bg-gradient-to-br from-slate-800/50 to-slate-700/30 rounded-xl p-6 border border-slate-600/50">
                        <h4 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <span class="text-2xl">🌱</span>
                            Statistik Tahun Tanam TBM
                        </h4>
                        
                        <!-- Stats Summary -->
                        <div class="grid grid-cols-4 gap-3 mb-4">
                            <div class="bg-slate-800/50 rounded-lg p-3 text-center border border-slate-600/30">
                                <div class="text-xs text-slate-400 mb-1">Total TBM</div>
                                <div class="text-2xl font-bold text-cyan-400" id="tbmTotalStats">0</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-3 text-center border border-slate-600/30">
                                <div class="text-xs text-slate-400 mb-1">Tanam 2023</div>
                                <div class="text-2xl font-bold text-emerald-400" id="tbm2023Stats">0</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-3 text-center border border-slate-600/30">
                                <div class="text-xs text-slate-400 mb-1">Tanam 2024</div>
                                <div class="text-2xl font-bold text-blue-400" id="tbm2024Stats">0</div>
                            </div>
                            <div class="bg-slate-800/50 rounded-lg p-3 text-center border border-slate-600/30">
                                <div class="text-xs text-slate-400 mb-1">Tanam 2025</div>
                                <div class="text-2xl font-bold text-purple-400" id="tbm2025Stats">0</div>
                            </div>
                        </div>
                        
                        <!-- Chart Container -->
                        <div class="bg-slate-900/50 rounded-lg p-4">
                            <canvas id="tbmPlantingYearChart" height="200"></canvas>
                        </div>
                        
                        <!-- Recent TBM Blocks List -->
                        <div class="mt-4">
                            <div class="text-sm font-semibold text-slate-300 mb-2">📋 Blok TBM Terbaru (2023-2025)</div>
                            <div id="recentTbmList" class="grid grid-cols-3 gap-2 max-h-32 overflow-y-auto">
                                <!-- Filled dynamically -->
                            </div>
                        </div>
                    </div>
'''

# Find the closing div of tbmBlocksList section and add after it
# Look for pattern: id="tbmBlocksList" ... </div> ... </div>
pattern_tbm_list = r'(<div id="tbmBlocksList"[^>]*>[\s\S]*?</div>\s*</div>)'

# Find the TBM column closing and add stats section
# Actually, let's add it after the grid of 4 columns
pattern_grid_end = r'(<!-- TBM Column -->\s*<div class="bg-slate-800/30[^>]*>[\s\S]*?id="tbmBlocksList"[\s\S]*?</div>\s*</div>\s*</div>)\s*(</div>)'

match = re.search(pattern_grid_end, content)
if match:
    print(f"Found TBM column end at position {match.start()}")
    # Insert stats section before the closing grid div
    content = content[:match.end(1)] + '\n\n' + tbm_stats_html + '\n                ' + content[match.end(1):]
    print("✓ Added TBM statistics HTML section")
else:
    # Try simpler approach - find tbmBlocksList and add after parent div
    print("Looking for simpler pattern...")
    pattern_simple = r'(id="tbmBlocksList"[\s\S]*?</div>\s*</div>\s*</div>\s*</div>)'
    match2 = re.search(pattern_simple, content)
    if match2:
        print(f"Found at position {match2.start()}")
        insert_pos = match2.end()
        content = content[:insert_pos] + '\n\n' + tbm_stats_html + '\n' + content[insert_pos:]
        print("✓ Added TBM statistics HTML section (simpler)")
    else:
        print("Could not find insertion point for TBM stats section")

# Add PLANTING_YEAR_DATA to the script section
# Find where other data constants are defined
pattern_data = r'(const HISTORICAL_YIELDS = \{)'
if re.search(pattern_data, content):
    content = re.sub(pattern_data, planting_year_js + '\n\n            \\1', content)
    print("✓ Added PLANTING_YEAR_DATA constant")

# Add JavaScript function to render TBM statistics
tbm_stats_js = '''
            // TBM Planting Year Chart instance
            let tbmPlantingYearChartInstance = null;
            
            function renderTbmPlantingYearStats(tbmBlocks) {
                // Count planting years for TBM blocks
                const yearCounts = {};
                const recentBlocks = [];
                
                tbmBlocks.forEach(block => {
                    const blockCode = block.block_code;
                    const plantingYear = PLANTING_YEAR_DATA[blockCode] || 0;
                    
                    if (plantingYear > 2000) {
                        yearCounts[plantingYear] = (yearCounts[plantingYear] || 0) + 1;
                        
                        // Collect recent blocks (2023-2025)
                        if (plantingYear >= 2023) {
                            recentBlocks.push({code: blockCode, year: plantingYear});
                        }
                    }
                });
                
                // Update stats badges
                document.getElementById('tbmTotalStats').textContent = tbmBlocks.length;
                document.getElementById('tbm2023Stats').textContent = yearCounts[2023] || 0;
                document.getElementById('tbm2024Stats').textContent = yearCounts[2024] || 0;
                document.getElementById('tbm2025Stats').textContent = yearCounts[2025] || 0;
                
                // Render chart
                const ctx = document.getElementById('tbmPlantingYearChart');
                if (!ctx) return;
                
                if (tbmPlantingYearChartInstance) {
                    tbmPlantingYearChartInstance.destroy();
                }
                
                // Sort years for chart
                const sortedYears = Object.keys(yearCounts).map(Number).sort();
                const data = sortedYears.map(y => yearCounts[y]);
                
                // Generate gradient colors based on year recency
                const colors = sortedYears.map(year => {
                    if (year >= 2023) return 'rgba(34, 197, 94, 0.8)';  // Green for recent
                    if (year >= 2020) return 'rgba(59, 130, 246, 0.8)'; // Blue for medium
                    if (year >= 2015) return 'rgba(251, 191, 36, 0.8)'; // Yellow for older
                    return 'rgba(100, 116, 139, 0.8)';  // Slate for oldest
                });
                
                tbmPlantingYearChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: sortedYears.map(y => y.toString()),
                        datasets: [{
                            label: 'Jumlah Blok',
                            data: data,
                            backgroundColor: colors,
                            borderColor: colors.map(c => c.replace('0.8', '1')),
                            borderWidth: 1,
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            title: {
                                display: true,
                                text: 'Distribusi Tahun Tanam TBM',
                                color: '#e2e8f0',
                                font: { size: 14, weight: 'bold' }
                            },
                            tooltip: {
                                callbacks: {
                                    label: (ctx) => `${ctx.parsed.y} blok`
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { color: 'rgba(100, 116, 139, 0.2)' },
                                ticks: { color: '#94a3b8' }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(100, 116, 139, 0.2)' },
                                ticks: { 
                                    color: '#94a3b8',
                                    stepSize: 1
                                }
                            }
                        }
                    }
                });
                
                // Render recent TBM blocks list
                const recentList = document.getElementById('recentTbmList');
                if (recentList) {
                    const sortedRecent = recentBlocks.sort((a, b) => b.year - a.year);
                    recentList.innerHTML = sortedRecent.map(b => 
                        `<div class="bg-slate-700/50 rounded px-2 py-1 text-xs flex justify-between items-center border border-slate-600/30">
                            <span class="text-white font-medium">${b.code}</span>
                            <span class="text-emerald-400">${b.year}</span>
                        </div>`
                    ).join('') || '<div class="text-slate-500 text-xs">Tidak ada blok TBM 2023-2025</div>';
                }
            }
'''

# Find the renderCategoryDistributionChart function and add our function after it
pattern_chart_func = r'(function renderCategoryDistributionChart\(categories\)[\s\S]*?categoryDistributionChart = new Chart[\s\S]*?\}\);[\s\S]*?\})'

match_func = re.search(pattern_chart_func, content)
if match_func:
    insert_pos = match_func.end()
    content = content[:insert_pos] + '\n\n' + tbm_stats_js + content[insert_pos:]
    print("✓ Added renderTbmPlantingYearStats function")

# Add call to renderTbmPlantingYearStats after populateBlockTrendLists
# Find where we populate TBM list and add the call
pattern_tbm_populate = r'(document\.getElementById\(\'tbmCount\'\)\.textContent = tbmBlocks\.length;)'
if re.search(pattern_tbm_populate, content):
    content = re.sub(pattern_tbm_populate, 
                     '\\1\n                renderTbmPlantingYearStats(tbmBlocks);', 
                     content)
    print("✓ Added call to renderTbmPlantingYearStats")

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ TBM Planting Year Statistics added successfully!")
print("Features added:")
print("  - Stats badges: Total TBM, 2023, 2024, 2025 counts")
print("  - Bar chart showing planting year distribution")
print("  - List of recent TBM blocks (2023-2025)")
