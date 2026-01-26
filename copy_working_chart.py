"""
COPY renderPaparanRisk logic to renderModalChart - EXACTLY!
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find renderModalChart function
start_marker = "function renderModalChart(blocks, sortBy) {"
end_marker = "function closePaparanRisikoModal()"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find function markers")
    exit(1)

# Extract before and after
before = content[:start_idx]
after = content[end_idx:]

# NEW renderModalChart - COPIED from renderPaparanRisk!
new_function = """function renderModalChart(blocks, sortBy) {
                console.log('[renderModalChart] Called with', blocks.length, 'blocks, sortBy:', sortBy);
                
                const ctx = document.getElementById('modalRiskChart');
                if (!ctx) {
                    console.error('[renderModalChart] Canvas not found!');
                    return;
                }

                // Destroy existing chart
                if (modalRiskChart) {
                    modalRiskChart.destroy();
                }

                // FFB Price for loss calculation
                const FFB_PRICE_PER_TON_JUTA = 2.5;

                // Calculate loss for each block (COPIED from renderPaparanRisk)
                const blocksWithLoss = blocks.map(block => {
                    const gapTonHa = Math.abs(block.gap_ton_ha || 0);
                    const area = block.luas_ha || 0;
                    const attackRate = block.attack_rate || 0;
                    const gapPct = Math.abs(block.gap_pct || 0);

                    // Calculate loss from gap if not available
                    let blockLoss = block.loss_value_juta || 0;
                    if (blockLoss === 0 && gapTonHa > 0 && area > 0) {
                        blockLoss = gapTonHa * area * FFB_PRICE_PER_TON_JUTA;
                    }

                    return {
                        code: block.block_code,
                        attack_rate: attackRate,
                        gap_pct: gapPct,
                        calculated_loss: blockLoss,
                        luas_ha: area
                    };
                });

                // Sort by attack rate or loss (COPIED from renderPaparanRisk)
                blocksWithLoss.sort((a, b) => {
                    if (sortBy === 'ar') {
                        return (b.attack_rate || 0) - (a.attack_rate || 0);
                    } else {
                        return (b.calculated_loss || 0) - (a.calculated_loss || 0);
                    }
                });

                // Prepare chart data (COPIED from renderPaparanRisk)
                const labels = blocksWithLoss.map(block => 
                    `${block.code} • AR: ${(block.attack_rate || 0).toFixed(1)}% • Gap: ${(block.gap_pct || 0).toFixed(0)}%`
                );
                const arData = blocksWithLoss.map(block => block.attack_rate || 0);
                const lossDataMiliar = blocksWithLoss.map(block => (block.calculated_loss || 0) / 1000);

                console.log('[renderModalChart] Labels:', labels.length);
                console.log('[renderModalChart] AR data:', arData);
                console.log('[renderModalChart] Loss data:', lossDataMiliar);

                // Create chart (EXACT COPY from renderPaparanRisk)
                modalRiskChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Attack Rate (%)',
                                data: arData,
                                backgroundColor: 'rgba(239, 68, 68, 0.8)',
                                borderColor: 'rgb(239, 68, 68)',
                                borderWidth: 2,
                                yAxisID: 'y',
                                barThickness: 'flex',
                                maxBarThickness: 30
                            },
                            {
                                label: 'Loss (Miliar Rp)',
                                data: lossDataMiliar,
                                backgroundColor: 'rgba(251, 191, 36, 0.8)',
                                borderColor: 'rgb(251, 191, 36)',
                                borderWidth: 2,
                                yAxisID: 'y1',
                                barThickness: 'flex',
                                maxBarThickness: 30
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: 'index',
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    color: '#fff',
                                    font: { size: 12, weight: 'bold' }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                                titleColor: '#fff',
                                bodyColor: '#fff',
                                borderColor: 'rgba(239, 68, 68, 0.5)',
                                borderWidth: 1,
                                callbacks: {
                                    label: function (context) {
                                        const label = context.dataset.label || '';
                                        const value = context.parsed.y;
                                        if (label.includes('Attack Rate')) {
                                            return `${label}: ${value.toFixed(1)}%`;
                                        } else {
                                            return `${label}: Rp ${value.toFixed(2)} M`;
                                        }
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                ticks: {color: '#fff', font: {size: 10}},
                                grid: {color: 'rgba(255, 255, 255, 0.1)'}
                            },
                            y: {
                                type: 'linear',
                                position: 'left',
                                ticks: {
                                    color: 'rgb(239, 68, 68)',
                                    callback: function (value) {
                                        return value.toFixed(0) + '%';
                                    }
                                },
                                grid: {color: 'rgba(239, 68, 68, 0.2)'},
                                title: {
                                    display: true,
                                    text: 'Attack Rate (%)',
                                    color: 'rgb(239, 68, 68)',
                                    font: {weight: 'bold'}
                                }
                            },
                            y1: {
                                type: 'linear',
                                position: 'right',
                                ticks: {
                                    color: 'rgb(251, 191, 36)',
                                    callback: function (value) {
                                        return 'Rp ' + value.toFixed(2) + ' M';
                                    }
                                },
                                grid: {display: false},
                                title: {
                                    display: true,
                                    text: 'Loss (Miliar Rp)',
                                    color: 'rgb(251, 191, 36)',
                                    font: {weight: 'bold'}
                                }
                            }
                        }
                    }
                });

                console.log('[renderModalChart] Chart created successfully!');
            }

            """

new_content = before + new_function + after

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ renderModalChart REPLACED with EXACT COPY from renderPaparanRisk!")
print("   This is the WORKING chart function!")
print("   Should display bars now!")
