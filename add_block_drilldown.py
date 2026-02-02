"""
Add Block Drill-Down Feature to Production Trend Modal
When user clicks on a specific block, show detailed modal with:
1. 3-year production trend chart (2023-2025)
2. Gap yield metrics per year
3. Risk metrics: Attack rate, Stadium ganoderma, SPH
"""

block_drilldown_html = '''
        <!-- BLOCK DETAIL DRILL-DOWN MODAL -->
        <div id="blockDetailModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden items-center justify-center z-[9999]" 
             onclick="closeBlockDetailModal()">
            <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-3xl border-2 border-cyan-500/50 shadow-2xl w-[90%] max-w-6xl max-h-[90vh] overflow-y-auto custom-scrollbar"
                 onclick="event.stopPropagation()">
                
                <!-- Header -->
                <div class="bg-gradient-to-r from-cyan-900/50 to-blue-900/50 p-6 border-b-2 border-cyan-500/30 sticky top-0 z-10">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <div class="text-5xl">📊</div>
                            <div>
                                <h2 class="text-3xl font-black text-white mb-1">
                                    <span id="blockDetailName">-</span> - Analisis Detail
                                </h2>
                                <p class="text-cyan-300 text-sm">
                                    Trend Produksi 3 Tahun (2023-2025) + Metriks Risiko
                                </p>
                            </div>
                        </div>
                        <button onclick="closeBlockDetailModal()" 
                                class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-bold transition-all">
                            ✕ Tutup
                        </button>
                    </div>
                </div>

                <!-- Content -->
                <div class="p-8 space-y-6">
                    
                    <!-- 3-YEAR PRODUCTION TREND CHART -->
                    <div class="bg-gradient-to-br from-indigo-900/30 to-purple-900/30 rounded-2xl border-2 border-indigo-500/40 p-6">
                        <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            📈 Trend Produksi 2023-2025
                        </h3>
                        <div style="height: 300px;">
                            <canvas id="blockDetailTrendChart"></canvas>
                        </div>
                        <div class="mt-4 grid grid-cols-3 gap-3">
                            <div class="bg-black/30 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">2023 (Baseline)</div>
                                <div class="text-2xl font-black text-yellow-400" id="block_yield_2023">-</div>
                                <div class="text-xs text-slate-500">T/Ha</div>
                            </div>
                            <div class="bg-black/30 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">2024</div>
                                <div class="text-2xl font-black text-cyan-400" id="block_yield_2024">-</div>
                                <div class="text-xs text-slate-500">T/Ha</div>
                            </div>
                            <div class="bg-black/30 rounded-lg p-3 text-center">
                                <div class="text-xs text-slate-400 mb-1">2025 (Current)</div>
                                <div class="text-2xl font-black text-white" id="block_yield_2025">-</div>
                                <div class="text-xs text-slate-500">T/Ha</div>
                            </div>
                        </div>
                    </div>

                    <!-- GAP YIELD METRICS PER YEAR -->
                    <div class="bg-gradient-to-br from-orange-900/30 to-red-900/30 rounded-2xl border-2 border-orange-500/40 p-6">
                        <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            📊 Gap Yield per Tahun
                        </h3>
                        <div class="grid grid-cols-3 gap-4">
                            <div class="bg-black/30 rounded-xl p-4 border border-orange-500/20">
                                <div class="text-xs text-orange-300 uppercase mb-2">Gap 2023</div>
                                <div class="text-3xl font-black text-orange-400" id="block_gap_2023">-</div>
                                <div class="text-xs text-slate-400 mt-1">% from potential</div>
                            </div>
                            <div class="bg-black/30 rounded-xl p-4 border border-orange-500/20">
                                <div class="text-xs text-orange-300 uppercase mb-2">Gap 2024</div>
                                <div class="text-3xl font-black text-orange-400" id="block_gap_2024">-</div>
                                <div class="text-xs text-slate-400 mt-1">% from potential</div>
                            </div>
                            <div class="bg-black/30 rounded-xl p-4 border border-orange-500/20">
                                <div class="text-xs text-orange-300 uppercase mb-2">Gap 2025</div>
                                <div class="text-3xl font-black text-orange-400" id="block_gap_2025">-</div>
                                <div class="text-xs text-slate-400 mt-1">% from potential</div>
                            </div>
                        </div>
                    </div>

                    <!-- RISK METRICS -->
                    <div class="grid grid-cols-3 gap-4">
                        
                        <!-- Attack Rate -->
                        <div class="bg-gradient-to-br from-red-900/30 to-pink-900/30 rounded-2xl border-2 border-red-500/40 p-6">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="text-3xl">🔴</div>
                                <h3 class="text-lg font-bold text-white">Attack Rate</h3>
                            </div>
                            <div class="text-5xl font-black text-red-400 mb-2" id="block_attack_rate">-</div>
                            <div class="text-sm text-slate-400">% infected area (NDRE)</div>
                            <div class="mt-3 text-xs text-red-200/70">
                                <span class="font-bold">Stadium:</span> 
                                <span id="block_ganoderma_stadium">-</span>
                            </div>
                        </div>

                        <!-- Ganoderma Stadium -->
                        <div class="bg-gradient-to-br from-purple-900/30 to-violet-900/30 rounded-2xl border-2 border-purple-500/40 p-6">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="text-3xl">🍄</div>
                                <h3 class="text-lg font-bold text-white">Ganoderma Detail</h3>
                            </div>
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Stadium I:</span>
                                    <span class="font-bold text-yellow-400" id="block_stadium_i">-</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Stadium II:</span>
                                    <span class="font-bold text-orange-400" id="block_stadium_ii">-</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Stadium III:</span>
                                    <span class="font-bold text-red-400" id="block_stadium_iii">-</span>
                                </div>
                            </div>
                        </div>

                        <!-- SPH (Trees per Hectare) -->
                        <div class="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-2xl border-2 border-blue-500/40 p-6">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="text-3xl">🌴</div>
                                <h3 class="text-lg font-bold text-white">SPH Status</h3>
                            </div>
                            <div class="text-5xl font-black text-blue-400 mb-2" id="block_sph">-</div>
                            <div class="text-sm text-slate-400 mb-3">pohon/Ha</div>
                            <div class="text-xs text-blue-200/70">
                                <span class="font-bold">Standard:</span> 130-143 pohon/Ha
                            </div>
                            <div class="mt-2 text-xs font-bold" id="block_sph_status">
                                <!-- Status akan diisi JS -->
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
'''

block_drilldown_js = '''
        // ===== BLOCK DRILL-DOWN FEATURE =====
        
        let blockDetailChart = null;

        /**
         * Open block detail modal with 3-year trend and risk metrics
         */
        function openBlockDetail(blockCode, divisionCode) {
            console.log(`[BLOCK DETAIL] Opening detail for ${blockCode} in ${divisionCode}`);
            
            // Get block data
            const blockData = window.ALL_BLOCKS_DATA.find(b => b.block_code === blockCode);
            if (!blockData) {
                console.error(`[BLOCK DETAIL] Block not found: ${blockCode}`);
                return;
            }

            // Update modal title
            document.getElementById('blockDetailName').textContent = blockCode;

            // Update 3-year yield data
            const yield2023 = blockData.yield_2023 || 0;
            const yield2024 = blockData.yield_2024 || 0;
            const yield2025 = blockData.yield_real_2025 || 0;
            
            document.getElementById('block_yield_2023').textContent = yield2023.toFixed(2);
            document.getElementById('block_yield_2024').textContent = yield2024.toFixed(2);
            document.getElementById('block_yield_2025').textContent = yield2025.toFixed(2);

            // Update gap yield data
            const potential2025 = blockData.yield_pot_2025 || 0;
            const gap2023 = potential2025 > 0 ? ((potential2025 - yield2023) / potential2025 * 100) : 0;
            const gap2024 = potential2025 > 0 ? ((potential2025 - yield2024) / potential2025 * 100) : 0;
            const gap2025 = blockData.gap_pct || 0;
            
            document.getElementById('block_gap_2023').textContent = gap2023.toFixed(1) + '%';
            document.getElementById('block_gap_2024').textContent = gap2024.toFixed(1) + '%';
            document.getElementById('block_gap_2025').textContent = gap2025.toFixed(1) + '%';

            // Update risk metrics
            const attackRate = blockData.attack_rate_pct || 0;
            document.getElementById('block_attack_rate').textContent = attackRate.toFixed(1) + '%';
            
            // Ganoderma stadium
            const stadiumI = blockData.stadium_i_pct || 0;
            const stadiumII = blockData.stadium_ii_pct || 0;
            const stadiumIII = blockData.stadium_iii_pct || 0;
            document.getElementById('block_ganoderma_stadium').textContent = 
                stadiumIII > 10 ? 'Stadium III (Kritis)' : 
                stadiumII > 10 ? 'Stadium II (Sedang)' : 
                'Stadium I (Ringan)';
            
            document.getElementById('block_stadium_i').textContent = stadiumI.toFixed(1) + '%';
            document.getElementById('block_stadium_ii').textContent = stadiumII.toFixed(1) + '%';
            document.getElementById('block_stadium_iii').textContent = stadiumIII.toFixed(1) + '%';

            // SPH
            const sph = blockData.sph || 0;
            document.getElementById('block_sph').textContent = sph;
            
            const sphStatus = document.getElementById('block_sph_status');
            if (sph < 130) {
                sphStatus.innerHTML = '<span class="text-red-400">⚠️ Below Standard</span>';
            } else if (sph >= 130 && sph <= 143) {
                sphStatus.innerHTML = '<span class="text-green-400">✅ Within Standard</span>';
            } else {
                sphStatus.innerHTML = '<span class="text-blue-400">📈 Above Standard</span>';
            }

            // Render 3-year trend chart
            renderBlockTrendChart(yield2023, yield2024, yield2025);

            // Show modal
            document.getElementById('blockDetailModal').classList.remove('hidden');
            document.getElementById('blockDetailModal').classList.add('flex');
        }

        /**
         * Close block detail modal
         */
        function closeBlockDetailModal() {
            document.getElementById('blockDetailModal').classList.add('hidden');
            document.getElementById('blockDetailModal').classList.remove('flex');
            
            // Destroy chart
            if (blockDetailChart) {
                blockDetailChart.destroy();
                blockDetailChart = null;
            }
        }

        /**
         * Render 3-year production trend chart for specific block
         */
        function renderBlockTrendChart(yield2023, yield2024, yield2025) {
            const ctx = document.getElementById('blockDetailTrendChart');
            if (!ctx) return;

            // Destroy existing chart
            if (blockDetailChart) {
                blockDetailChart.destroy();
            }

            blockDetailChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['2023', '2024', '2025'],
                    datasets: [{
                        label: 'Yield (T/Ha)',
                        data: [yield2023, yield2024, yield2025],
                        borderColor: '#22d3ee',
                        backgroundColor: 'rgba(34, 211, 238, 0.1)',
                        borderWidth: 3,
                        pointRadius: 6,
                        pointBackgroundColor: '#22d3ee',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#22d3ee',
                            bodyColor: '#fff',
                            borderColor: '#22d3ee',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return 'Yield: ' + context.parsed.y.toFixed(2) + ' T/Ha';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: '#94a3b8',
                                font: { weight: 'bold' },
                                callback: function(value) {
                                    return value.toFixed(1);
                                }
                            },
                            grid: {
                                color: 'rgba(148, 163, 184, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#94a3b8',
                                font: { weight: 'bold', size: 14 }
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
'''

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Insert modal HTML before </body>
body_end = content.rfind('</body>')
if body_end != -1:
    content = content[:body_end] + block_drilldown_html + '\n' + content[body_end:]
    print(f"✅ Inserted block detail modal HTML before </body>")
else:
    print(f"❌ Could not find </body> tag")

# Insert JavaScript before closing </script> or before </body>
# Find the last </script> tag
script_end = content.rfind('</script>')
if script_end != -1:
    content = content[:script_end] + block_drilldown_js + '\n' + content[script_end:]
    print(f"✅ Inserted block drill-down JavaScript")
else:
    print(f"❌ Could not find </script> tag")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ BLOCK DRILL-DOWN FEATURE ADDED!")
print(f"   Modal: Block detail modal with 3-year trend chart")
print(f"   Charts: Production trend 2023-2025")
print(f"   Metrics: Gap yield, Attack rate, Stadium, SPH")
print(f"\n📝 Next: Need to update block item rendering to add click handlers")
print(f"   Each block should call: openBlockDetail('D010A', 'AME02')")
