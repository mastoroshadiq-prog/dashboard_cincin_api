"""
Add fullscreen modal and expand button
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add expand button to chart header
old_header = '''                        <h4 class="text-white text-xs font-bold mb-3 flex items-center gap-2">
                            📉 Degradation Timeline (No Treatment)
                        </h4>'''

new_header = '''                        <div class="flex justify-between items-center mb-3">
                            <h4 class="text-white text-xs font-bold flex items-center gap-2">
                                📉 Degradation Timeline (No Treatment)
                            </h4>
                            <button onclick="openAnalysisModal()" 
                                class="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg border border-indigo-400 transition-all flex items-center gap-1">
                                🔍 Analisa Lengkap
                            </button>
                        </div>'''

content = content.replace(old_header, new_header)

# 2. Add modal HTML before FEATURE 1
modal_html = '''
        <!-- FULLSCREEN ANALYSIS MODAL -->
        <div id="analysisModal" class="hidden fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-8">
            <div class="w-full h-full max-w-7xl bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border-2 border-indigo-500/50 shadow-2xl overflow-hidden flex flex-col">
                
                <!-- Modal Header -->
                <div class="flex justify-between items-center p-6 border-b border-white/10 bg-slate-900/50">
                    <div>
                        <h2 class="text-2xl font-black text-white">Advanced Analysis: Treatment Comparison</h2>
                        <p class="text-sm text-slate-400 mt-1">Block: <span id="modalBlockCode" class="text-indigo-400 font-bold">--</span></p>
                    </div>
                    <button onclick="closeAnalysisModal()" 
                        class="w-10 h-10 rounded-lg bg-red-600/20 hover:bg-red-600 border border-red-500/50 text-white font-bold text-xl transition-all">
                        ×
                    </button>
                </div>

                <!-- Modal Content -->
                <div class="flex-1 overflow-y-auto p-6">
                    
                    <!-- Comparison Metrics -->
                    <div class="grid grid-cols-4 gap-4 mb-6">
                        <div class="bg-red-900/30 p-4 rounded-xl border border-red-500/30">
                            <div class="text-xs text-red-300 uppercase mb-1">3-Year Loss (No Treatment)</div>
                            <div class="text-2xl font-black text-white" id="modalNoTreatmentLoss">--</div>
                        </div>
                        <div class="bg-emerald-900/30 p-4 rounded-xl border border-emerald-500/30">
                            <div class="text-xs text-emerald-300 uppercase mb-1">Treatment Cost</div>
                            <div class="text-2xl font-black text-white" id="modalTreatmentCost">--</div>
                        </div>
                        <div class="bg-blue-900/30 p-4 rounded-xl border border-blue-500/30">
                            <div class="text-xs text-blue-300 uppercase mb-1">Savings (70%)</div>
                            <div class="text-2xl font-black text-white" id="modalSavings">--</div>
                        </div>
                        <div class="bg-cyan-900/30 p-4 rounded-xl border border-cyan-500/30">
                            <div class="text-xs text-cyan-300 uppercase mb-1">Net Benefit</div>
                            <div class="text-2xl font-black text-white" id="modalNetBenefit">--</div>
                        </div>
                    </div>

                    <!-- Side-by-Side Charts -->
                    <div class="grid grid-cols-2 gap-6">
                        
                        <!-- NO TREATMENT -->
                        <div class="bg-red-900/10 p-6 rounded-xl border-2 border-red-500/30">
                            <h3 class="text-lg font-bold text-red-400 mb-4">❌ No Treatment</h3>
                            <div style="height: 400px;">
                                <canvas id="modalNoTreatmentChart"></canvas>
                            </div>
                        </div>

                        <!-- WITH TREATMENT -->
                        <div class="bg-emerald-900/10 p-6 rounded-xl border-2 border-emerald-500/30">
                            <h3 class="text-lg font-bold text-emerald-400 mb-4">✅ With Treatment</h3>
                            <div style="height: 400px;">
                                <canvas id="modalWithTreatmentChart"></canvas>
                            </div>
                        </div>

                    </div>

                </div>

            </div>
        </div>

'''

# Insert modal before FEATURE 1
feature1_marker = '        <!-- FEATURE 1: Treatment Comparison Chart -->'
content = content.replace(feature1_marker, modal_html + feature1_marker)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added expand button to chart header")
print("✅ Added fullscreen modal HTML")
print("✅ Modal includes: side-by-side charts + metrics")
print("\nNEXT: Add JavaScript for modal functions and chart rendering")
