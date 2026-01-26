"""
Update openBlockBreakdownModal function to use production trend logic instead of stadium categories
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the categorization logic
old_categories = '''// Categorize blocks by stadium
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
                });'''

new_categories = '''// Categorize blocks by PRODUCTION TREND (2023-2025)
                const trendCategories = {
                    declining: [], // Produksi turun > 5%
                    stable: [],    // Perubahan -5% s/d +5%
                    increasing: [], // Produksi naik > 5%
                    nodata: []     // Tidak ada data historis
                };

                mergedBlocks.forEach(block => {
                    const blockCode = block.block_code;
                    const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                    
                    if (!historical || !historical.yields) {
                        trendCategories.nodata.push({...block, prodChangePct: 0, prod2023: 0, prod2025: 0});
                        return;
                    }
                    
                    const y2023 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y2025 = historical.yields[2025] || historical.yields['2025'] || {};
                    const prod2023 = y2023.real_ton_ha || 0;
                    const prod2025 = y2025.real_ton_ha || 0;
                    
                    if (prod2023 === 0 && prod2025 === 0) {
                        trendCategories.nodata.push({...block, prodChangePct: 0, prod2023: 0, prod2025: 0});
                        return;
                    }
                    
                    const changePct = prod2023 > 0 ? ((prod2025 - prod2023) / prod2023) * 100 : 0;
                    const enrichedBlock = {...block, prodChangePct: changePct, prod2023, prod2025};
                    
                    if (changePct < -5) {
                        trendCategories.declining.push(enrichedBlock);
                    } else if (changePct > 5) {
                        trendCategories.increasing.push(enrichedBlock);
                    } else {
                        trendCategories.stable.push(enrichedBlock);
                    }
                });

                // Sort by change percentage
                trendCategories.declining.sort((a, b) => a.prodChangePct - b.prodChangePct);
                trendCategories.increasing.sort((a, b) => b.prodChangePct - a.prodChangePct);

                console.log('[BREAKDOWN] Production Trend Categories:', {
                    declining: trendCategories.declining.length,
                    stable: trendCategories.stable.length,
                    increasing: trendCategories.increasing.length,
                    nodata: trendCategories.nodata.length
                });'''

if old_categories in content:
    content = content.replace(old_categories, new_categories)
    print("✅ Updated categorization logic to production trends")
else:
    print("⚠️ Could not find old categories pattern")

# Update the UI updates section
old_ui_update = '''// Update modal content
                document.getElementById('breakdownDivisionSubtitle').textContent =
                    `${divisionCode} Division - ${metrics.totalBlocks} blok total`;

                // Update category counts
                document.getElementById('categoryCount_critical').textContent = categories.critical.length;
                document.getElementById('categoryCount_high').textContent = categories.high.length;
                document.getElementById('categoryCount_medium').textContent = categories.medium.length;
                document.getElementById('categoryCount_low').textContent = categories.low.length;'''

new_ui_update = '''// Update modal content
                document.getElementById('breakdownDivisionSubtitle').textContent =
                    `${divisionCode} Division - ${metrics.totalBlocks} blok total - TREN PRODUKSI 2023-2025`;

                // Update category counts (now using trend IDs)
                document.getElementById('categoryCount_declining').textContent = trendCategories.declining.length;
                document.getElementById('categoryCount_stable').textContent = trendCategories.stable.length;
                document.getElementById('categoryCount_increasing').textContent = trendCategories.increasing.length;
                document.getElementById('categoryCount_nodata').textContent = trendCategories.nodata.length;'''

if old_ui_update in content:
    content = content.replace(old_ui_update, new_ui_update)
    print("✅ Updated UI element IDs")
else:
    print("⚠️ Could not find old UI update pattern")

# Update the multi-factor analysis to show declining stats
old_analysis = '''// Calculate multi-factor analysis for CRITICAL + HIGH blocks (Stadium 3+)
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
                    document.getElementById('avgAR_critical').textContent = '0%';'''

new_analysis = '''// Calculate stats for DECLINING BLOCKS
                const decliningBlocks = trendCategories.declining;

                console.log('[BREAKDOWN] Declining blocks:', decliningBlocks.length);
                if (decliningBlocks.length > 0) {
                    console.log('[BREAKDOWN] Sample declining block:', decliningBlocks[0]);
                }

                if (decliningBlocks.length > 0) {
                    const avgChange = decliningBlocks.reduce((sum, b) => sum + (b.prodChangePct || 0), 0) / decliningBlocks.length;
                    const avgProd2023 = decliningBlocks.reduce((sum, b) => sum + (b.prod2023 || 0), 0) / decliningBlocks.length;
                    const avgProd2025 = decliningBlocks.reduce((sum, b) => sum + (b.prod2025 || 0), 0) / decliningBlocks.length;
                    const totalArea = decliningBlocks.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

                    console.log('[BREAKDOWN] Avg change:', avgChange);
                    console.log('[BREAKDOWN] Total area:', totalArea);

                    document.getElementById('avgChange_declining').textContent = avgChange.toFixed(1) + '%';
                    document.getElementById('avgProd2023_declining').textContent = avgProd2023.toFixed(1) + ' T/Ha';
                    document.getElementById('avgProd2025_declining').textContent = avgProd2025.toFixed(1) + ' T/Ha';
                    document.getElementById('totalArea_declining').textContent = totalArea.toFixed(1) + ' Ha';
                } else {
                    document.getElementById('avgChange_declining').textContent = '0%';'''

if old_analysis in content:
    content = content.replace(old_analysis, new_analysis)
    print("✅ Updated analysis section for declining blocks")
else:
    print("⚠️ Could not find old analysis pattern")

# Update the remaining else block
old_else = '''document.getElementById('avgSPH_critical').textContent = '0';
                    document.getElementById('avgGap_critical').textContent = '0%';
                    document.getElementById('totalAreaRisk').textContent = '0 Ha';
                }'''

new_else = '''document.getElementById('avgProd2023_declining').textContent = '0 T/Ha';
                    document.getElementById('avgProd2025_declining').textContent = '0 T/Ha';
                    document.getElementById('totalArea_declining').textContent = '0 Ha';
                }
                
                // Populate declining and increasing block lists
                populateBlockTrendLists(trendCategories);'''

if old_else in content:
    content = content.replace(old_else, new_else)
    print("✅ Updated else block and added populateBlockTrendLists call")
else:
    print("⚠️ Could not find old else pattern")

# Add populateBlockTrendLists function if not exists
if 'function populateBlockTrendLists' not in content:
    # Find position before closing </script> near end
    insert_marker = '// ============================================\n            // BLOCK TREND BAR CHART'
    if insert_marker not in content:
        # Insert before last </script>
        last_script = content.rfind('</script>')
        if last_script > 0:
            populate_function = '''
            // Populate block trend lists
            function populateBlockTrendLists(trendCategories) {
                // Update declining blocks list
                const decliningList = document.getElementById('decliningBlocksList');
                if (decliningList && trendCategories.declining.length > 0) {
                    let html = trendCategories.declining.slice(0, 10).map(b => 
                        `<div onclick="showBlockDetail('${b.block_code}')" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer hover:bg-red-900/40 transition-all border border-transparent hover:border-red-500/50">
                            <span class="text-white font-medium">${b.block_code}</span>
                            <span class="text-red-400 font-bold">${b.prodChangePct.toFixed(1)}%</span>
                            <span class="text-slate-400 text-sm">${b.prod2023.toFixed(1)} → ${b.prod2025.toFixed(1)} T/Ha</span>
                        </div>`
                    ).join('');
                    if (trendCategories.declining.length > 10) {
                        html += `<div class="text-slate-400 text-sm text-center mt-2">+${trendCategories.declining.length - 10} blok lainnya...</div>`;
                    }
                    decliningList.innerHTML = html;
                } else if (decliningList) {
                    decliningList.innerHTML = '<div class="text-slate-500 text-center py-4">Tidak ada blok dengan tren penurunan signifikan</div>';
                }

                // Update increasing blocks list
                const increasingList = document.getElementById('increasingBlocksList');
                if (increasingList && trendCategories.increasing.length > 0) {
                    let html = trendCategories.increasing.slice(0, 10).map(b => 
                        `<div onclick="showBlockDetail('${b.block_code}')" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer hover:bg-green-900/40 transition-all border border-transparent hover:border-green-500/50">
                            <span class="text-white font-medium">${b.block_code}</span>
                            <span class="text-green-400 font-bold">+${b.prodChangePct.toFixed(1)}%</span>
                            <span class="text-slate-400 text-sm">${b.prod2023.toFixed(1)} → ${b.prod2025.toFixed(1)} T/Ha</span>
                        </div>`
                    ).join('');
                    if (trendCategories.increasing.length > 10) {
                        html += `<div class="text-slate-400 text-sm text-center mt-2">+${trendCategories.increasing.length - 10} blok lainnya...</div>`;
                    }
                    increasingList.innerHTML = html;
                } else if (increasingList) {
                    increasingList.innerHTML = '<div class="text-slate-500 text-center py-4">Tidak ada blok dengan tren kenaikan signifikan</div>';
                }

                // Render distribution chart
                renderTrendDistributionChart(trendCategories);
                console.log('[PRODUCTION TREND] Block lists populated');
            }

            // Render trend distribution doughnut chart
            function renderTrendDistributionChart(trendCategories) {
                const ctx = document.getElementById('categoryDistributionChart');
                if (!ctx) return;

                // Destroy existing chart if any
                if (window.categoryDistChart) {
                    window.categoryDistChart.destroy();
                }

                window.categoryDistChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Penurunan', 'Stabil', 'Kenaikan', 'No Data'],
                        datasets: [{
                            data: [
                                trendCategories.declining.length,
                                trendCategories.stable.length,
                                trendCategories.increasing.length,
                                trendCategories.nodata.length
                            ],
                            backgroundColor: [
                                'rgba(239, 68, 68, 0.8)',
                                'rgba(251, 191, 36, 0.8)',
                                'rgba(34, 197, 94, 0.8)',
                                'rgba(100, 116, 139, 0.8)'
                            ],
                            borderColor: [
                                'rgb(239, 68, 68)',
                                'rgb(251, 191, 36)',
                                'rgb(34, 197, 94)',
                                'rgb(100, 116, 139)'
                            ],
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: { color: '#fff', font: { size: 12 } }
                            }
                        }
                    }
                });
            }

            // Show block detail (placeholder)
            function showBlockDetail(blockCode) {
                console.log('[DETAIL] Block clicked:', blockCode);
                const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                if (historical) {
                    const y23 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y25 = historical.yields[2025] || historical.yields['2025'] || {};
                    alert(`Blok: ${blockCode}\\nLuas: ${historical.luas_ha} Ha\\n2023: ${(y23.real_ton_ha || 0).toFixed(1)} T/Ha\\n2025: ${(y25.real_ton_ha || 0).toFixed(1)} T/Ha`);
                }
            }

'''
            content = content[:last_script] + populate_function + content[last_script:]
            print("✅ Added populateBlockTrendLists function")
else:
    print("✅ populateBlockTrendLists already exists")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
