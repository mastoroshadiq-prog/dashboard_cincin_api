with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find modal header section
old = '''                <div class="flex justify-between items-center p-6 border-b border-white/10 bg-slate-900/50">
                    <div>
                        <h2 class="text-2xl font-black text-white">Advanced Analysis: Treatment Comparison</h2>
                        <p class="text-sm text-slate-400 mt-1">Block: <span id="modalBlockCode"
                                class="text-indigo-400 font-bold">--</span></p>
                    </div>
                    <button onclick="closeAnalysisModal()" 
                        class="w-10 h-10 rounded-lg bg-red-600/20 hover:bg-red-600 border border-red-500/50 text-white font-bold text-xl transition-all">
                        ×
                    </button>
                </div>'''

new = '''                <div class="p-6 border-b border-white/10 bg-slate-900/50">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h2 class="text-2xl font-black text-white">Advanced Analysis: Treatment Comparison</h2>
                            <p class="text-sm text-slate-400 mt-1">Block: <span id="modalBlockCode" class="text-indigo-400 font-bold">--</span></p>
                        </div>
                        <button onclick="closeAnalysisModal()" class="w-10 h-10 rounded-lg bg-red-600/20 hover:bg-red-600 border border-red-500/50 text-white font-bold text-xl transition-all">×</button>
                    </div>
                    <div class="flex items-center gap-4 bg-slate-800/50 p-3 rounded-lg">
                        <div class="flex items-center gap-2">
                            <span class="text-xs text-slate-400 font-bold uppercase">View:</span>
                            <button onclick="switchViewMode('per-blok')" id="viewPerBlok" class="px-4 py-2 rounded-lg text-sm font-bold bg-indigo-600 text-white border-2 border-indigo-400">Per-Blok</button>
                            <button onclick="switchViewMode('total')" id="viewTotal" class="px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">Total 8 Blok</button>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-xs text-slate-400 font-bold uppercase">Select:</span>
                            <select id="blockSelector" onchange="switchBlock(this.value)" class="px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-white border-2 border-slate-600"></select>
                        </div>
                    </div>
                </div>'''

c = c.replace(old, new)
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('✅ Added dropdown and toggle to modal!')
