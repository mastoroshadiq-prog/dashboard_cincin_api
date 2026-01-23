
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\tbm_stats_data.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    tbm_data = json.load(f)

# 1. INJECT DATA JSON
tbm_data_script = f"\n            const TBM_STATS_DATA = {json.dumps(tbm_data)};\n"
# Cari posisi setelah const HISTORICAL_YIELDS = { ... };
# Karena regex susah untuk nested braces, kita cari pattern penutup blok json historical yield
# Asumsi: HISTORICAL_YIELDS didefinisikan secara literal "const HISTORICAL_YIELDS = {"
# Kita cari deklarasi variabel berikutnya atau akhir script
pattern_insert_data = r'(const BLOCKS_DATA = \{)'
if 'const TBM_STATS_DATA' not in html_content:
    html_content = re.sub(pattern_insert_data, lambda m: tbm_data_script + m.group(1), html_content, count=1)
    print("Data TBM injected.")


# 2. CREATE TBM DETAIL PANEL HTML
tbm_panel_html = """
    <!-- TBM DETAIL STATISTICS MODAL (NEW) -->
    <div id="tbmDetailPanel" class="hidden fixed inset-0 bg-black/80 z-[70] flex items-center justify-center p-4">
        <div class="bg-gradient-to-br from-emerald-900 to-slate-900 rounded-2xl max-w-2xl w-full border-2 border-emerald-500/50 shadow-2xl overflow-hidden transform transition-all">
            
            <!-- Header -->
            <div class="bg-gradient-to-r from-emerald-800 to-green-900 p-6 flex justify-between items-start border-b border-emerald-500/30">
                <div>
                    <div class="flex items-center gap-3 mb-2">
                        <div class="p-2 bg-emerald-500/20 rounded-lg border border-emerald-400/30">
                            <span class="text-2xl">🌱</span>
                        </div>
                        <div>
                            <h2 class="text-3xl font-black text-white tracking-tight" id="tbmDetailTitle">BLOK ???</h2>
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">TBM STATISTICS</span>
                                <span class="text-emerald-200/60 text-sm">Tanaman Belum Menghasilkan</span>
                            </div>
                        </div>
                    </div>
                </div>
                <button onclick="closeTBMDetail()" class="p-2 hover:bg-white/10 rounded-lg transition-colors group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400 group-hover:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Content -->
            <div class="p-6 space-y-6">
                
                <!-- Info Grid -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-black/30 p-4 rounded-xl border border-white/10">
                        <div class="text-xs text-slate-400 uppercase font-bold mb-1">Tahun Tanam</div>
                        <div class="text-3xl font-black text-yellow-400" id="tbmPlantingYear">----</div>
                    </div>
                    <div class="bg-black/30 p-4 rounded-xl border border-white/10">
                        <div class="text-xs text-slate-400 uppercase font-bold mb-1">Total Tanaman (Pokok)</div>
                        <div class="text-3xl font-black text-emerald-400" id="tbmTotalPokok">----</div>
                    </div>
                </div>

                <!-- 3-Year Chart Section -->
                <div class="bg-slate-800/50 rounded-xl p-6 border border-white/5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-white flex items-center gap-2">
                            <span>📊</span> Populasi TBM (2023 - 2025)
                        </h3>
                        <span class="text-xs text-slate-400 italic">*Data populasi historis disimulasikan dari data terkini</span>
                    </div>
                    <div class="h-64 w-full">
                        <canvas id="tbmStatsChart"></canvas>
                    </div>
                </div>

                <!-- Footer Info -->
                <div class="bg-emerald-500/10 p-4 rounded-lg border border-emerald-500/20 text-center">
                    <p class="text-sm text-emerald-200">
                        <strong>Status:</strong> Blok kategori Tanaman Belum Menghasilkan (TBM). Tidak ada data produksi yield.
                    </p>
                </div>
            </div>
        </div>
    </div>
"""

# Inject panel HTML before the end of body
if 'id="tbmDetailPanel"' not in html_content:
    html_content = html_content.replace('</body>', tbm_panel_html + '\n</body>')
    print("Panel HTML injected.")


# 3. INJECT JS FUNCTIONS
js_functions = """
            // --- TBM STATISTICS FEATURE ---
            let tbmChartInstance = null;

            window.showTBMStatistics = function(blockCode) {
                const data = TBM_STATS_DATA[blockCode];
                if (!data) {
                    alert('Data TBM tidak ditemukan untuk blok ' + blockCode);
                    return;
                }

                // Populate Info
                document.getElementById('tbmDetailTitle').textContent = 'BLOK ' + blockCode;
                document.getElementById('tbmPlantingYear').textContent = data.year || '-';
                document.getElementById('tbmTotalPokok').textContent = data.pokok ? data.pokok.toLocaleString() : '0';

                // Show Modal
                const panel = document.getElementById('tbmDetailPanel');
                panel.classList.remove('hidden');

                // Render Chart
                const ctx = document.getElementById('tbmStatsChart').getContext('2d');
                
                if (tbmChartInstance) {
                    tbmChartInstance.destroy();
                }

                // Simulate historical data (flat or slightly varying)
                const currentPokok = data.pokok || 0;
                // Asumsi: Populasi 2023 & 2024 sama dengan 2025 (stabil)
                const chartData = [currentPokok, currentPokok, currentPokok];

                tbmChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['2023', '2024', '2025'],
                        datasets: [{
                            label: 'Jumlah Pokok TBM',
                            data: chartData,
                            backgroundColor: [
                                'rgba(16, 185, 129, 0.6)', // Emerald
                                'rgba(16, 185, 129, 0.7)',
                                'rgba(16, 185, 129, 0.9)'
                            ],
                            borderColor: 'rgba(16, 185, 129, 1)',
                            borderWidth: 2,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return context.raw.toLocaleString() + ' Pokok';
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: '#94a3b8' }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { color: '#ffff', font: { weight: 'bold' } }
                            }
                        }
                    }
                });
            };

            window.closeTBMDetail = function() {
                document.getElementById('tbmDetailPanel').classList.add('hidden');
            };
"""

# Inject JS before closing script tag (assumed at end of body)
# Or just before generic helper functions
if 'window.showTBMStatistics' not in html_content:
    html_content = html_content.replace('function closeBlockDetail() {', js_functions + '\n\n            function closeBlockDetail() {')
    print("JS Functions injected.")


# 4. UPDATE ONCLICK HANDLER
# Cari bagian pembuatan list TBM di fungsi populateBlockTrendLists
# Pattern: onclick="showBlockDetail('${block.block_code}')" ... >${block.reason ...
# Kita harus spesifik mengganti yang ada di loop TBM

# Karena populateBlockTrendLists mungkin panjang, kita gunakan replace string yang unik untuk bagian TBM list generation
# Biasanya ada blok kode: categories.nodata.forEach(...)

# Mari kita cari string unik di loop rendering TBM
target_str_old = "onclick=\"showBlockDetail('${block.block_code}')\""
# Kita tidak bisa replace all karena blok lain tetap pakai showBlockDetail.
# Kita perlu replace HANYA di bagian render kategori 'nodata' / 'tbm'

# Asumsi kodenya seperti:
# ... categories.nodata.sort(...) ...
# ... html += `... onclick="showBlockDetail(...) ...`
# ... tbmListEl.innerHTML = html;

# Kita coba approach Regex untuk menemukan loop kategori NODATA/TBM
# Atau lebih simpel: Kita ubah fungsi `populateBlockTrendLists` secara masif? Riskan.

# Alternatif aman: Ubah definisi `showBlockDetail` untuk mendeteksi apakah blok tersebut TBM.
# Jika TBM, alihkan ke `showTBMStatistics`. Ini lebih minim intrusi ke HTML rendering logic.

override_logic = """
            // OVERRIDE: Redirect TBM blocks to new modal
            const originalShowBlockDetail = showBlockDetail;
            showBlockDetail = function(blockCode) {
                // Check if block is in TBM data list
                if (TBM_STATS_DATA[blockCode]) {
                    showTBMStatistics(blockCode);
                } else {
                    // Fallback to original logic for TM blocks
                    originalShowBlockDetail(blockCode);
                }
            };
"""

# Insert override logic at the end of script
if 'const originalShowBlockDetail' not in html_content:
    html_content = html_content.replace('// Initialize Chart instances', override_logic + '\n            // Initialize Chart instances')
    print("JS Override logic injected.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML Update Complete!")
