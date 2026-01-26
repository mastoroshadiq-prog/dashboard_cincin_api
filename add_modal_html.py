"""
ADD PAPARAN RISIKO MODAL HTML to the dashboard
Insert before closing </body> tag
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Modal HTML
modal_html = '''
    <!-- ====== PAPARAN RISIKO KRITIS MODAL ====== -->
    <div id="paparanRisikoModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden border-2 border-red-500/30 shadow-2xl shadow-red-500/20">
            
            <!-- Header -->
            <div class="bg-gradient-to-r from-red-900 to-rose-800 p-6 border-b-2 border-red-500/30 flex justify-between items-center">
                <div>
                    <h2 class="text-3xl font-black text-white flex items-center gap-3">
                        <span class="text-4xl">🚨</span>
                        PAPARAN RISIKO KRITIS
                    </h2>
                    <p class="text-red-200 text-sm mt-1" id="modalDivisionSubtitle">Loading...</p>
                </div>
                <button onclick="closePaparanRisikoModal()" class="text-white hover:text-red-200 transition-colors">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <!-- Content -->
            <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                
                <!-- Summary Cards -->
                <div class="grid grid-cols-3 gap-4 mb-6">
                    <!-- Total Potensi Kerugian -->
                    <div class="bg-black/30 rounded-xl p-6 border border-red-500/30">
                        <div class="text-red-300 text-xs font-bold uppercase mb-2">Total Potensi Kerugian</div>
                        <div class="text-5xl font-black text-red-400" id="modalTotalLoss">Rp 0.0 M</div>
                    </div>

                    <!-- Blok Kritis -->
                    <div class="bg-black/30 rounded-xl p-6 border border-orange-500/30">
                        <div class="text-orange-300 text-xs font-bold uppercase mb-2">Blok Kritis</div>
                        <div class="text-5xl font-black text-white" id="modalCriticalCount">0 Blok</div>
                    </div>

                    <!-- Area Berisiko -->
                    <div class="bg-black/30 rounded-xl p-6 border border-yellow-500/30">
                        <div class="text-yellow-300 text-xs font-bold uppercase mb-2">Area Berisiko</div>
                        <div class="text-5xl font-black text-yellow-400" id="modalRiskArea">0.0 Ha</div>
                    </div>
                </div>

                <!-- Chart Section -->
                <div class="bg-black/20 rounded-xl p-6 border border-slate-700">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xl font-bold text-white">Distribusi Risiko per Blok</h3>
                        <div class="flex gap-2">
                            <button onclick="sortModalChart('ar')" id="sortModalBy_ar" 
                                class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-600 text-white border-2 border-rose-400">
                                AR %
                            </button>
                            <button onclick="sortModalChart('loss')" id="sortModalBy_loss"
                                class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-700 text-slate-300 border border-slate-600">
                                Loss (Rp)
                            </button>
                        </div>
                    </div>

                    <!-- Chart Canvas -->
                    <div class="bg-slate-900/50 rounded-lg p-4" style="height: 400px;">
                        <canvas id="modalRiskChart"></canvas>
                    </div>

                    <!-- Legend -->
                    <div class="mt-4 flex justify-center gap-6 text-sm">
                        <div class="flex items-center gap-2">
                            <div class="w-4 h-4 bg-red-500 rounded"></div>
                            <span class="text-slate-300">Attack Rate (%)</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="w-4 h-4 bg-yellow-500 rounded"></div>
                            <span class="text-slate-300">Loss (Miliar Rp)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
'''

# Find closing body tag
body_close_idx = content.rfind('</body>')
if body_close_idx == -1:
    print("ERROR: Could not find </body> tag")
    exit(1)

# Insert modal before </body>
new_content = content[:body_close_idx] + modal_html + '\n' + content[body_close_idx:]

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ PAPARAN RISIKO MODAL HTML added successfully!")
print("   - Modal ID: paparanRisikoModal")
print("   - Canvas ID: modalRiskChart")
print("   - Close function: closePaparanRisikoModal()")
print("   - Sort buttons: sortModalChart('ar' | 'loss')")
