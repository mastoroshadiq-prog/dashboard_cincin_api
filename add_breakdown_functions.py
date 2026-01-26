"""
ADD JavaScript functions for Block Breakdown Modal
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find insertion point (after closePaparanRisikoModal function)
marker = "function closePaparanRisikoModal() {"
marker_idx = content.find(marker)

# Find end of the function (next function start or script end)
next_function_idx = content.find("function sortModalChart", marker_idx)

# Insert our new functions before sortModalChart
insert_point = next_function_idx

js_functions = '''
            // ========================================
            // BLOCK BREAKDOWN MODAL FUNCTIONS
            // ========================================

            let categoryDistributionChart = null;

            function openBlockBreakdownModal() {
                const divisionCode = window.currentDivision || 'AME02';
                console.log('[BREAKDOWN] Opening for division:', divisionCode);

                // Calculate breakdown using calculateDivisionMetrics
                const metrics = calculateDivisionMetrics(divisionCode);
                if (!metrics) {
                    alert(`No data for division: ${divisionCode}`);
                    return;
                }

                // Get all blocks for this division
                const allBlocks = Object.values(BLOCKS_DATA);
                const divisionBlocks = allBlocks.filter(block => block.division === divisionCode);

                // Categorize blocks by stadium
                const categories = {
                    critical: [], // Stadium 4
                    high: [],     // Stadium 3
                    medium: [],   // Stadium 2
                    low: []       // Stadium 1
                };

                divisionBlocks.forEach(block => {
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

                // Calculate multi-factor analysis for CRITICAL blocks
                const criticalBlocks = categories.critical;
                if (criticalBlocks.length > 0) {
                    const avgAR = criticalBlocks.reduce((sum, b) => sum + (parseFloat(b.attack_rate) || 0), 0) / criticalBlocks.length;
                    const avgSPH = criticalBlocks.reduce((sum, b) => sum + (parseFloat(b.sph) || 0), 0) / criticalBlocks.length;
                    const avgGap = criticalBlocks.reduce((sum, b) => sum + Math.abs(parseFloat(b.gap_pct) || 0), 0) / criticalBlocks.length;
                    const totalArea = criticalBlocks.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

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
            }

            function closeBlockBreakdownModal() {
                const modal = document.getElementById('blockBreakdownModal');
                modal.classList.add('hidden');
                modal.classList.remove('flex');

                // Destroy chart
                if (categoryDistributionChart) {
                    categoryDistributionChart.destroy();
                    categoryDistributionChart = null;
                }
            }

            function renderCategoryDistributionChart(categories) {
                const ctx = document.getElementById('categoryDistributionChart');
                if (!ctx) return;

                // Destroy existing chart
                if (categoryDistributionChart) {
                    categoryDistributionChart.destroy();
                }

                const data = {
                    labels: ['🔴 Critical', '🟠 High', '🟡 Medium', '🟢 Low'],
                    datasets: [{
                        label: 'Number of Blocks',
                        data: [
                            categories.critical.length,
                            categories.high.length,
                            categories.medium.length,
                            categories.low.length
                        ],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',
                            'rgba(251, 146, 60, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(34, 197, 94, 0.8)'
                        ],
                        borderColor: [
                            'rgb(239, 68, 68)',
                            'rgb(251, 146, 60)',
                            'rgb(251, 191, 36)',
                            'rgb(34, 197, 94)'
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
                                    font: {size: 14, weight: 'bold'},
                                    padding: 15
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        const label = context.label || '';
                                        const value = context.parsed || 0;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return `${label}: ${value} blocks (${percentage}%)`;
                                    }
                                }
                            }
                        }
                    }
                });

                console.log('[BREAKDOWN] Chart rendered');
            }

            '''

# Insert the functions
new_content = content[:insert_point] + js_functions + '\n' + content[insert_point:]

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ JavaScript functions added!")
print("   - openBlockBreakdownModal()")
print("   - closeBlockBreakdownModal()")
print("   - renderCategoryDistributionChart()")
print("\n✅ READY TO TEST!")
print("   Click 'Total Blocks' card in Division Overview")
