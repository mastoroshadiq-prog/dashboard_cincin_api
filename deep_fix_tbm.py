
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\tbm_stats_real.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    tbm_data = json.load(f)

# 1. INJECT DATA JSON
tbm_data_script = f"\n            const TBM_REAL_STATS = {json.dumps(tbm_data)};\n"
if 'const TBM_REAL_STATS' not in html_content:
    # Inject sebelum HISTORICAL_YIELDS atau di awal script
    # Cari HISTORICAL_YIELDS dan taruh sebelumnya
    if 'const HISTORICAL_YIELDS' in html_content:
        html_content = html_content.replace('const HISTORICAL_YIELDS', tbm_data_script + 'const HISTORICAL_YIELDS')
    # Backup: jika tidak ketemu, taruh setelah <body>
    elif '<script>' in html_content:
        html_content = html_content.replace('<script>', '<script>' + tbm_data_script, 1)
    
    print("Data TBM REAL injected.")


# 2. INJECT HTML MODAL
modal_html = """
    <!-- TBM STATISTICS MODAL (REAL DATA) -->
    <div id="tbmStatsModal" class="hidden fixed inset-0 bg-black/90 z-[80] flex items-center justify-center p-4 backdrop-blur-sm">
        <div class="bg-gradient-to-b from-slate-900 to-black rounded-2xl max-w-2xl w-full border border-emerald-500/50 shadow-[0_0_50px_rgba(16,185,129,0.2)] overflow-hidden">
            
            <!-- Header -->
            <div class="bg-gradient-to-r from-emerald-900/80 to-slate-900 p-6 flex justify-between items-center border-b border-emerald-500/30">
                <div class="flex items-center gap-4">
                    <div class="p-3 bg-emerald-500/20 rounded-xl border border-emerald-500/30 shadow-inner">
                        <span class="text-3xl">🌱</span>
                    </div>
                    <div>
                        <h2 class="text-2xl font-black text-white tracking-tight leading-none mb-1" id="tbmModalTitle">BLOK ???</h2>
                        <div class="flex items-center gap-2">
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 tracking-wider">TBM STATISTICS</span>
                        </div>
                    </div>
                </div>
                <button onclick="closeTbmStatsModal()" class="group p-2 rounded-lg hover:bg-white/5 transition-colors">
                    <div class="text-slate-500 group-hover:text-white transition-colors">✕</div>
                </button>
            </div>

            <!-- Content -->
            <div class="p-6 space-y-6">
                
                <!-- Info Grid -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-slate-800/50 p-4 rounded-xl border border-white/5 relative overflow-hidden group">
                        <div class="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
                            <span class="text-4xl">🗓️</span>
                        </div>
                        <div class="text-[10px] text-slate-400 uppercase font-bold tracking-wider mb-1">Tahun Tanam</div>
                        <div class="text-3xl font-black text-white" id="tbmModalYear">----</div>
                    </div>
                    <div class="bg-slate-800/50 p-4 rounded-xl border border-white/5 relative overflow-hidden group">
                        <div class="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
                            <span class="text-4xl">🌲</span>
                        </div>
                        <div class="text-[10px] text-slate-400 uppercase font-bold tracking-wider mb-1">Total Tanam (3 Tahun)</div>
                        <div class="text-3xl font-black text-emerald-400" id="tbmModalTotal">----</div>
                    </div>
                </div>

                <!-- Chart container -->
                <div class="bg-slate-800/30 rounded-xl p-5 border border-white/5">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="font-bold text-white flex items-center gap-2 text-sm">
                            Statistik Penanaman TBM (2023 - 2025)
                        </h3>
                    </div>
                    <div class="h-64 w-full relative">
                        <canvas id="tbmRealChart"></canvas>
                    </div>
                </div>
                
                <div class="text-center text-[10px] text-slate-500">
                    *Data bersumber dari Laporan Realisasi Tanam (Kolom C038, C041, C045)
                </div>
            </div>
        </div>
    </div>
"""

if 'id="tbmStatsModal"' not in html_content:
    # Inject sebelum penutup body
    html_content = html_content.replace('</body>', modal_html + '\n</body>')
    print("Modal HTML injected.")


# 3. INJECT JS LOGIC WITH SAFE INTERCEPTION
js_logic = """
            // --- TBM FEATURES (REAL DATA) ---
            let tbmRealChartInstance = null;

            window.openTbmStatsModal = function(blockCode) {
                const data = TBM_REAL_STATS[blockCode];
                if (!data) {
                    console.warn('No TBM data available for', blockCode);
                    // Fallback to old modal if no data found? Or alerting?
                    // Better to just show modal with zeros
                }
                
                // Populate data
                const year = (data && data.year) ? data.year : '-';
                const total = (data && data.total_tbm_3th) ? data.total_tbm_3th : 0;
                
                document.getElementById('tbmModalTitle').textContent = 'BLOK ' + blockCode;
                document.getElementById('tbmModalYear').textContent = year;
                document.getElementById('tbmModalTotal').textContent = total.toLocaleString();
                
                document.getElementById('tbmStatsModal').classList.remove('hidden');
                
                const ctx = document.getElementById('tbmRealChart').getContext('2d');
                if (tbmRealChartInstance) tbmRealChartInstance.destroy();
                
                const val2023 = (data && data.tanam_2023) ? data.tanam_2023 : 0;
                const val2024 = (data && data.tanam_2024) ? data.tanam_2024 : 0;
                const val2025 = (data && data.tanam_2025) ? data.tanam_2025 : 0;
                
                tbmRealChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [{
                            label: 'Jumlah Pokok Tanam',
                            data: [val2023, val2024, val2025],
                            backgroundColor: '#10b981',
                            borderRadius: 4,
                            barThickness: 40
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: 'rgba(0,0,0,0.9)',
                                titleColor: '#10b981',
                                callbacks: {
                                    label: function(ctx) { return ctx.raw.toLocaleString() + ' Pokok'; }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.05)' },
                                ticks: { color: '#64748b', font: {size: 10} }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { color: '#fff', font: {weight: 'bold'} }
                            }
                        }
                    }
                });
            }

            window.closeTbmStatsModal = function() {
                document.getElementById('tbmStatsModal').classList.add('hidden');
            }

            // SAFE INTERCEPTION
            // Store original function
            if (!window.originalShowBlockDetail) {
                window.originalShowBlockDetail = window.showBlockDetail;
            }
            
            // Override with redirection logic
            window.showBlockDetail = function(blockCode) {
                // Check if this block should use the new TBM modal
                // Condition: data exists AND (has TBM activity > 0 OR Recent Planting Year >= 2021)
                const tbmData = TBM_REAL_STATS[blockCode];
                const isTbmCandidate = tbmData && (tbmData.total_tbm_3th > 0 || tbmData.year >= 2021);
                
                if (isTbmCandidate) {
                    openTbmStatsModal(blockCode);
                } else {
                    // Call original function for everything else
                    if (window.originalShowBlockDetail) window.originalShowBlockDetail(blockCode);
                }
            }
"""

if 'window.openTbmStatsModal' not in html_content:
    # Inject di akhir script sebelum tutup
    html_content = html_content.replace('// Initialize Chart instances', js_logic + '\n            // Initialize Chart instances')
    print("JS Logic injected.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML updated successfully.")
