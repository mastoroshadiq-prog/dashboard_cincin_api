"""
ADD BLOCK CATEGORIZATION MODAL & FUNCTIONALITY
Triggered by clicking "Total Blocks" card in Division Overview
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# STEP 1: Add onclick handler to Total Blocks card
old_card = '''                        <div class="bg-black/30 rounded-xl p-4 border border-cyan-500/20">
                            <div class="text-xs text-cyan-300 font-bold uppercase mb-1">Total Blocks</div>
                            <div class="text-3xl font-black text-white" id="divMetric_totalBlocks">37</div>
                        </div>'''

new_card = '''                        <div onclick="openBlockBreakdownModal()" 
                            class="bg-black/30 rounded-xl p-4 border border-cyan-500/20 cursor-pointer hover:border-cyan-400 hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/20 transition-all duration-200 group">
                            <div class="text-xs text-cyan-300 font-bold uppercase mb-1 flex items-center gap-2">
                                Total Blocks
                                <span class="text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">📊</span>
                            </div>
                            <div class="text-3xl font-black text-white" id="divMetric_totalBlocks">37</div>
                            <div class="text-[10px] text-cyan-300/60 mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                Klik untuk breakdown kategorisasi
                            </div>
                        </div>'''

content = content.replace(old_card, new_card)

# STEP 2: Add modal HTML before </body>
modal_html = '''
    <!-- ====== BLOCK BREAKDOWN MODAL ====== -->
    <div id="blockBreakdownModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-gradient-to-br from-slate-900 via-cyan-900 to-slate-900 rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden border-2 border-cyan-500/30 shadow-2xl shadow-cyan-500/20">
            
            <!-- Header -->
            <div class="bg-gradient-to-r from-cyan-900 to-blue-800 p-6 border-b-2 border-cyan-500/30 flex justify-between items-center">
                <div>
                    <h2 class="text-3xl font-black text-white flex items-center gap-3">
                        <span class="text-4xl">📊</span>
                        BLOCK CATEGORIZATION
                    </h2>
                    <p class="text-cyan-200 text-sm mt-1" id="breakdownDivisionSubtitle">Loading...</p>
                </div>
                <button onclick="closeBlockBreakdownModal()" class="text-white hover:text-cyan-200 transition-colors">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <!-- Content -->
            <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                
                <!-- Category Cards Grid -->
                <div class="grid grid-cols-4 gap-4 mb-6">
                    <!-- CRITICAL -->
                    <div class="bg-gradient-to-br from-red-900/40 to-red-800/20 rounded-xl p-6 border-2 border-red-500/40">
                        <div class="text-4xl mb-2">🔴</div>
                        <div class="text-red-200 text-xs font-bold uppercase mb-2">CRITICAL</div>
                        <div class="text-5xl font-black text-red-400 mb-2" id="categoryCount_critical">0</div>
                        <div class="text-xs text-red-300/70">Stadium 4 • AR ≥ 30%</div>
                    </div>

                    <!-- HIGH -->
                    <div class="bg-gradient-to-br from-orange-900/40 to-orange-800/20 rounded-xl p-6 border-2 border-orange-500/40">
                        <div class="text-4xl mb-2">🟠</div>
                        <div class="text-orange-200 text-xs font-bold uppercase mb-2">HIGH</div>
                        <div class="text-5xl font-black text-orange-400 mb-2" id="categoryCount_high">0</div>
                        <div class="text-xs text-orange-300/70">Stadium 3 • AR 15-30%</div>
                    </div>

                    <!-- MEDIUM -->
                    <div class="bg-gradient-to-br from-yellow-900/40 to-yellow-800/20 rounded-xl p-6 border-2 border-yellow-500/40">
                        <div class="text-4xl mb-2">🟡</div>
                        <div class="text-yellow-200 text-xs font-bold uppercase mb-2">MEDIUM</div>
                        <div class="text-5xl font-black text-yellow-400 mb-2" id="categoryCount_medium">0</div>
                        <div class="text-xs text-yellow-300/70">Stadium 2 • AR 5-15%</div>
                    </div>

                    <!-- LOW -->
                    <div class="bg-gradient-to-br from-green-900/40 to-green-800/20 rounded-xl p-6 border-2 border-green-500/40">
                        <div class="text-4xl mb-2">🟢</div>
                        <div class="text-green-200 text-xs font-bold uppercase mb-2">LOW</div>
                        <div class="text-5xl font-black text-green-400 mb-2" id="categoryCount_low">0</div>
                        <div class="text-xs text-green-300/70">Stadium 1 • AR < 5%</div>
                    </div>
                </div>

                <!-- Multi-Factor Analysis -->
                <div class="bg-black/20 rounded-xl p-6 border border-slate-700 mb-6">
                    <h3 class="text-xl font-bold text-white mb-4">📈 Multi-Factor Analysis Summary</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-slate-800/50 rounded-lg p-4">
                            <div class="text-xs text-slate-400 mb-1">Avg Attack Rate (Critical)</div>
                            <div class="text-2xl font-bold text-red-400" id="avgAR_critical">0%</div>
                        </div>
                        <div class="bg-slate-800/50 rounded-lg p-4">
                            <div class="text-xs text-slate-400 mb-1">Avg SPH Decline (Critical)</div>
                            <div class="text-2xl font-bold text-orange-400" id="avgSPH_critical">0</div>
                        </div>
                        <div class="bg-slate-800/50 rounded-lg p-4">
                            <div class="text-xs text-slate-400 mb-1">Avg Yield Gap (Critical)</div>
                            <div class="text-2xl font-bold text-yellow-400" id="avgGap_critical">0%</div>
                        </div>
                        <div class="bg-slate-800/50 rounded-lg p-4">
                            <div class="text-xs text-slate-400 mb-1">Total Area at Risk</div>
                            <div class="text-2xl font-bold text-cyan-400" id="totalAreaRisk">0 Ha</div>
                        </div>
                    </div>
                </div>

                <!-- Distribution Chart -->
                <div class="bg-black/20 rounded-xl p-6 border border-slate-700">
                    <h3 class="text-xl font-bold text-white mb-4">📊 Category Distribution</h3>
                    <div style="height: 300px;">
                        <canvas id="categoryDistributionChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
'''

body_close_idx = content.rfind('</body>')
content = content[:body_close_idx] + modal_html + '\n' + content[body_close_idx:]

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Block Breakdown Modal HTML added!")
print("   - Total Blocks card now clickable")
print("   - Modal with 4 category cards (Critical/High/Medium/Low)")
print("   - Multi-factor analysis summary")
print("   - Distribution chart canvas")
print("\n⏭️  Next: Add JavaScript functions for modal logic")
