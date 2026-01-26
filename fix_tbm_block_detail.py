"""
Fix TBM Block Detail Panel:
1. Remove the incorrect TBM stats section from modal
2. Modify showBlockDetail function to show planting year info for TBM blocks
"""

import re
import json

# Read the HTML file
html_file = r'data\output\DASHBOARD_DEMO_FEATURES.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# 1. Remove the TBM stats section that was incorrectly added to modal
tbm_stats_pattern = r'<!-- TBM PLANTING YEAR STATISTICS -->[\s\S]*?id="recentTbmList"[\s\S]*?</div>\s*</div>\s*</div>'
content = re.sub(tbm_stats_pattern, '', content)
print(f"✓ Removed TBM stats section from modal (if existed)")

# 2. Remove the call to renderTbmPlantingYearStats
content = re.sub(r'\s*renderTbmPlantingYearStats\(tbmBlocks\);', '', content)
print("✓ Removed renderTbmPlantingYearStats call")

# 3. Remove the renderTbmPlantingYearStats function
func_pattern = r'// TBM Planting Year Chart instance[\s\S]*?function renderTbmPlantingYearStats\(tbmBlocks\)[\s\S]*?\}\s*\}'
content = re.sub(func_pattern, '', content)
print("✓ Removed renderTbmPlantingYearStats function")

# 4. Now modify showBlockDetail to handle TBM blocks differently
# Find the showBlockDetail function and add TBM-specific rendering

# First, let's find and view the current showBlockDetail function
show_block_detail_pattern = r'function showBlockDetail\(blockCode\)'
match = re.search(show_block_detail_pattern, content)
if match:
    print(f"Found showBlockDetail at position {match.start()}")
    
    # Find where we check for block data and render the panel
    # We need to add logic to detect TBM blocks and show different content
    
    # Add TBM detection logic after getting yield data
    # Look for where blockData is retrieved
    
    # Replace the chart and stats rendering for TBM blocks
    old_render_pattern = r"(const blockData = HISTORICAL_YIELDS\[blockCode\];[\s\S]*?)(// Render trend chart)"
    
    new_render_code = '''const blockData = HISTORICAL_YIELDS[blockCode];
        
        // Check if this is a TBM block (no historical yield data OR planting year >= 2021)
        const plantingYear = PLANTING_YEAR_DATA[blockCode] || 0;
        const isTBM = !blockData || (plantingYear >= 2021);
        
        if (isTBM) {
            // Show TBM-specific content instead of production chart
            renderTbmBlockDetail(blockCode, plantingYear, blockData);
            return;
        }
        
        // Non-TBM blocks continue with normal rendering
        '''
    
    content = re.sub(old_render_pattern, new_render_code + '\\2', content)
    print("✓ Added TBM detection logic to showBlockDetail")

# 5. Add new function to render TBM block details
tbm_block_detail_func = '''
            // Render TBM block detail (for blocks without production history)
            function renderTbmBlockDetail(blockCode, plantingYear, blockData) {
                const panel = document.getElementById('blockDetailPanel');
                if (!panel) return;
                
                // Calculate age of plantation
                const currentYear = 2025;
                const age = plantingYear > 0 ? (currentYear - plantingYear) : 'N/A';
                const yearsToProduction = plantingYear > 0 ? Math.max(0, 4 - (currentYear - plantingYear)) : 'N/A';
                
                // Determine TBM stage
                let tbmStage = 'TBM-0';
                let stageDesc = 'Baru tanam';
                let stageColor = 'text-emerald-400';
                
                if (plantingYear > 0) {
                    const ageYears = currentYear - plantingYear;
                    if (ageYears === 0) { tbmStage = 'TBM-0'; stageDesc = 'Baru tanam (tahun ini)'; stageColor = 'text-emerald-400'; }
                    else if (ageYears === 1) { tbmStage = 'TBM-1'; stageDesc = 'Tahun pertama pertumbuhan'; stageColor = 'text-green-400'; }
                    else if (ageYears === 2) { tbmStage = 'TBM-2'; stageDesc = 'Tahun kedua pertumbuhan'; stageColor = 'text-lime-400'; }
                    else if (ageYears === 3) { tbmStage = 'TBM-3'; stageDesc = 'Tahun ketiga, menjelang produksi'; stageColor = 'text-yellow-400'; }
                    else { tbmStage = 'Transisi'; stageDesc = 'Mulai berproduksi'; stageColor = 'text-orange-400'; }
                }
                
                // Get area if available from blockData
                const area = blockData?.luas_ha || 'N/A';
                
                // Update header
                document.getElementById('detailBlockCode').textContent = blockCode;
                document.getElementById('detailDivision').textContent = blockData?.division || 'N/A';
                
                // Replace chart container with TBM info
                const chartContainer = document.getElementById('blockTrendChartContainer');
                if (chartContainer) {
                    chartContainer.innerHTML = `
                        <div class="bg-gradient-to-br from-emerald-900/30 to-green-800/20 rounded-xl p-6 border border-emerald-500/30">
                            <div class="text-center mb-6">
                                <div class="text-6xl mb-3">🌱</div>
                                <div class="text-2xl font-bold text-emerald-400">Tanaman Belum Menghasilkan</div>
                                <div class="text-sm text-slate-400 mt-1">${stageDesc}</div>
                            </div>
                            
                            <!-- TBM Stats Grid -->
                            <div class="grid grid-cols-2 gap-4 mb-6">
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-600/30">
                                    <div class="text-xs text-slate-400 mb-1">📅 Tahun Tanam</div>
                                    <div class="text-3xl font-bold text-cyan-400">${plantingYear > 0 ? plantingYear : 'N/A'}</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-600/30">
                                    <div class="text-xs text-slate-400 mb-1">🌴 Umur Tanaman</div>
                                    <div class="text-3xl font-bold text-amber-400">${age} ${age !== 'N/A' ? 'tahun' : ''}</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-600/30">
                                    <div class="text-xs text-slate-400 mb-1">🏷️ Stadium</div>
                                    <div class="text-2xl font-bold ${stageColor}">${tbmStage}</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-600/30">
                                    <div class="text-xs text-slate-400 mb-1">⏳ Estimasi Produksi</div>
                                    <div class="text-2xl font-bold text-purple-400">${yearsToProduction} ${yearsToProduction !== 'N/A' ? 'tahun lagi' : ''}</div>
                                </div>
                            </div>
                            
                            <!-- TBM Growth Timeline -->
                            <div class="bg-slate-900/50 rounded-lg p-4">
                                <div class="text-sm font-semibold text-slate-300 mb-3">📈 Timeline Pertumbuhan</div>
                                <div class="flex items-center justify-between">
                                    ${[0, 1, 2, 3, 4].map(yr => {
                                        const targetYear = plantingYear > 0 ? plantingYear + yr : 2025 + yr;
                                        const isComplete = plantingYear > 0 && (currentYear - plantingYear) >= yr;
                                        const isCurrent = plantingYear > 0 && (currentYear - plantingYear) === yr;
                                        const label = yr === 0 ? 'Tanam' : yr === 4 ? 'Produksi' : 'TBM-' + yr;
                                        return \`
                                            <div class="flex flex-col items-center">
                                                <div class="\${isCurrent ? 'w-8 h-8 bg-emerald-500 animate-pulse' : isComplete ? 'w-6 h-6 bg-emerald-600' : 'w-6 h-6 bg-slate-600'} rounded-full flex items-center justify-center text-xs text-white font-bold">
                                                    \${isComplete ? '✓' : yr}
                                                </div>
                                                <div class="text-xs text-slate-400 mt-1">\${label}</div>
                                                <div class="text-xs text-slate-500">\${targetYear}</div>
                                            </div>
                                        \`;
                                    }).join('<div class="flex-1 h-1 bg-slate-700 mx-1"></div>')}
                                </div>
                            </div>
                        </div>
                    `;
                }
                
                // Update info metrics for TBM
                document.getElementById('detailLuas').textContent = area !== 'N/A' ? area.toFixed(2) + ' Ha' : 'N/A';
                document.getElementById('detailYield2023').textContent = '-';
                if (document.getElementById('detailYield2024')) {
                    document.getElementById('detailYield2024').textContent = '-';
                }
                document.getElementById('detailYield2025').textContent = '-';
                document.getElementById('detailChange').textContent = 'TBM';
                document.getElementById('detailChange').className = 'text-xl font-bold text-emerald-400';
                
                // Update risk metrics
                document.getElementById('detailAttackRate').textContent = '-';
                document.getElementById('detailStadium').textContent = tbmStage;
                document.getElementById('detailSPH').textContent = '-';
                document.getElementById('detailLoss').textContent = '-';
                
                // Update yield gap for TBM
                document.getElementById('gapPotential').textContent = '-';
                document.getElementById('gapActual').textContent = '-';
                document.getElementById('gapPercent').textContent = 'TBM';
                
                // Show panel
                panel.classList.remove('hidden');
                panel.classList.add('flex');
            }
'''

# Find where to insert the function - after showBlockDetail function
pattern_insert = r'(function closeBlockDetail\(\))'
match_insert = re.search(pattern_insert, content)
if match_insert:
    content = content[:match_insert.start()] + tbm_block_detail_func + '\n\n            ' + content[match_insert.start():]
    print("✓ Added renderTbmBlockDetail function")

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nFile size: {original_len} -> {new_len} bytes")
print("\n✅ TBM Block Detail Panel updated successfully!")
print("Now when you click a TBM block, it will show:")
print("  - Planting year")
print("  - Age of plantation")
print("  - TBM stage (TBM-0, TBM-1, TBM-2, TBM-3)")
print("  - Estimated years to production")
print("  - Growth timeline visualization")
