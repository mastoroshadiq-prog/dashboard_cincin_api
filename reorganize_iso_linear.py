"""
REORGANIZE DASHBOARD - ISO 31000 LINEAR FLOW
Phase 1: Risk Identification
Phase 2: Risk Analysis (+ Likelihood component)
Phase 3: Risk Evaluation
Phase 4: Risk Treatment
Phase 5: Monitoring & Review
"""
import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'
OUTPUT = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_REORGANIZED.html'

# Phase section headers
PHASE_HEADERS = {
    1: '''
    <!-- ======================================= -->
    <!-- PHASE 1: RISK IDENTIFICATION           -->
    <!-- ======================================= -->
    <div class="mb-8">
        <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-indigo-600 text-white flex items-center justify-center font-black text-2xl shadow-lg">1</div>
            <div>
                <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight">RISK IDENTIFICATION</h2>
                <p class="text-slate-600 font-bold">Deteksi Sumber Risiko & Vektor Penularan</p>
            </div>
        </div>
    </div>
    ''',
    2: '''
    <!-- ======================================= -->
    <!-- PHASE 2: RISK ANALYSIS                 -->
    <!-- ======================================= -->
    <div class="mb-8 mt-16">
        <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-blue-600 text-white flex items-center justify-center font-black text-2xl shadow-lg">2</div>
            <div>
                <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight">RISK ANALYSIS</h2>
                <p class="text-slate-600 font-bold">Analisis Dampak, Likelihood & Proyeksi</p>
            </div>
        </div>
    </div>
    ''',
    3: '''
    <!-- ======================================= -->
    <!-- PHASE 3: RISK EVALUATION               -->
    <!-- ======================================= -->
    <div class="mb-8 mt-16">
        <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-amber-600 text-white flex items-center justify-center font-black text-2xl shadow-lg">3</div>
            <div>
                <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight">RISK EVALUATION</h2>
                <p class="text-slate-600 font-bold">Evaluasi Level Risiko & Prioritas</p>
            </div>
        </div>
    </div>
    ''',
    4: '''
    <!-- ======================================= -->
    <!-- PHASE 4: RISK TREATMENT                -->
    <!-- ======================================= -->
    <div class="mb-8 mt-16">
        <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center font-black text-2xl shadow-lg">4</div>
            <div>
                <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight">RISK TREATMENT</h2>
                <p class="text-slate-600 font-bold">Protokol Mitigasi & Action Plan</p>
            </div>
        </div>
    </div>
    ''',
    5: '''
    <!-- ======================================= -->
    <!-- PHASE 5: MONITORING & REVIEW           -->
    <!-- ======================================= -->
    <div class="mb-8 mt-16">
        <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-slate-600 text-white flex items-center justify-center font-black text-2xl shadow-lg">5</div>
            <div>
                <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight">MONITORING & REVIEW</h2>
                <p class="text-slate-600 font-bold">Watchlist & Continuous Tracking</p>
            </div>
        </div>
    </div>
    '''
}

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        original = f.read()
    
    print("REORGANIZING Dashboard by ISO 31000 Phases...")
    
    # Start with header/nav up to main content
    main_content_start = original.find('<!-- MAIN DASHBOARD CONTENT -->')
    if main_content_start == -1:
        print("ERROR: Main content marker not found")
        return
    
    header_section = original[:main_content_start]
    
    # Close main content wrapper at the end
    body_close = original.rfind('</body>')
    if body_close == -1:
        print("ERROR: Body close not found")
        return
    
scripts_section = original[body_close-5000:body_close]  # Get last part with scripts
    
    # BUILD NEW CONTENT IN ISO ORDER
    new_content = header_section + '<!-- MAIN DASHBOARD CONTENT -->\n<div id="tab-overview" class="space-y-6">\n\n'
    
    # PHASE 1: Map + SPH
    new_content += PHASE_HEADERS[1]
    new_content += '''
    <!-- Map Container -->
    <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-[2rem] p-8 text-white shadow-2xl border border-white/10 relative">
        <span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>
        <div class="flex items-start justify-between mb-6">
            <div class="flex items-center gap-6">
                <div class="bg-gradient-to-br from-red-600 to-red-900 w-20 h-20 rounded-3xl flex items-center justify-center shadow-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                </div>
                <div>
                    <h2 class="text-4xl font-black text-white tracking-tighter uppercase mb-2">🔥 PETA KLUSTER CINCIN API</h2>
                    <p class="text-slate-400 font-bold text-lg max-w-2xl">Identifikasi spasial sumber risiko Ganoderma per blok</p>
                </div>
            </div>
        </div>
        <div class="h-[500px] bg-slate-800 rounded-2xl" id="mapContainerLeft"></div>
    </div>
'''
    
    # PHASE 2: Financial Simulator + Financial Impact + Likelihood + Vanishing Yield
    new_content += PHASE_HEADERS[2]
    new_content += '''
    <!-- Financial Simulator -->
    <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 mb-8 relative overflow-hidden">
        <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
        <div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div class="flex items-start gap-4">
                <div class="bg-indigo-600 text-white p-3 rounded-2xl shadow-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect width="20" height="14" x="2" y="5" rx="2"/>
                        <line x1="2" x2="22" y1="10" y2="10"/>
                    </svg>
                </div>
                <div>
                    <h3 class="text-lg font-black text-slate-800 uppercase tracking-tight">Financial Simulator</h3>
                    <p class="text-slate-500 text-sm font-medium">Sesuaikan Harga TBS untuk proyeksi real-time</p>
                </div>
            </div>
            <div class="flex items-center gap-6 w-full md:w-auto bg-slate-50 p-4 rounded-2xl">
                <div class="flex-1 min-w-[200px]">
                    <input type="range" id="priceSlider" min="1500" max="4000" step="50" value="2500" class="w-full h-3 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                </div>
                <div class="bg-white border-2 border-indigo-100 px-5 py-2 rounded-xl text-center min-w-[120px]">
                    <span class="text-[10px] font-black uppercase text-slate-400 block mb-1">Harga TBS</span>
                    <div class="text-xl font-black text-indigo-700">Rp <span id="priceDisplay">2.500</span></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 2-Column Grid: Financial Impact + Likelihood -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Financial Impact Metrics -->
        <div class="bg-gradient-to-br from-indigo-900 to-indigo-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden border border-indigo-500/30">
            <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
            <h3 class="text-lg font-black text-indigo-200 uppercase tracking-tight mb-6">Financial Impact Metrics</h3>
            <div class="space-y-4">
                <div class="bg-black/30 rounded-2xl p-5">
                    <span class="text-xs font-black text-indigo-300 uppercase block mb-2">Total Kerugian</span>
                    <div class="text-4xl font-black text-white" id="finTotalLossLeft">Rp 0</div>
                </div>
            </div>
        </div>
        
        <!-- Likelihood & Trend Analysis -->
        <div class="bg-gradient-to-br from-blue-900 to-blue-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden border border-blue-500/30">
            <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
            <h3 class="text-lg font-black text-blue-200 uppercase tracking-tight mb-6">Likelihood & Trend</h3>
            
            <!-- Probability Score -->
            <div class="bg-black/30 rounded-2xl p-5 mb-4">
                <span class="text-xs font-black text-blue-300 uppercase block mb-3">Probability Score</span>
                <div class="flex items-baseline gap-2">
                    <span class="text-5xl font-black text-white" id="likelihoodScore">--</span>
                    <span class="text-xl font-bold text-blue-400">%</span>
                </div>
                <div class="mt-3 h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div id="likelihoodBar" class="h-full bg-gradient-to-r from-yellow-500 to-red-500" style="width: 0%"></div>
                </div>
            </div>
            
            <!-- Sliders -->
            <div class="bg-black/30 rounded-2xl p-4">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-black text-blue-300 uppercase">Formula Parameters</span>
                    <button id="toggleFormulaInfo" class="text-xs text-blue-400 hover:text-blue-200 underline">ℹ️ Info</button>
                </div>
                <div id="formulaExplanation" class="hidden mb-4 p-3 bg-slate-900/50 rounded-lg">
                    <p class="text-xs text-blue-200"><strong>Formula:</strong> AR (40-95%) + SPH modifier</p>
                </div>
                <div class="space-y-3">
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">AR Weight</span>
                            <span class="text-white font-black" id="arWeightValue">1.0x</span>
                        </div>
                        <input type="range" id="arWeightSlider" min="0.5" max="2.0" step="0.1" value="1.0" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">SPH Modifier</span>
                            <span class="text-white font-black" id="sphModifierValue">1.0x</span>
                        </div>
                        <input type="range" id="sphModifierSlider" min="0" max="2.0" step="0.1" value="1.0" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    <button id="recalculateLikelihood" class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black uppercase rounded-lg">🔄 Recalculate</button>
                </div>
            </div>
            
            <!-- Time to Critical -->
            <div class="bg-black/30 rounded-2xl p-5 mt-4">
                <span class="text-xs font-black text-blue-300 uppercase block mb-3">Time to Critical</span>
                <div class="flex items-baseline gap-2">
                    <span class="text-4xl font-black text-white" id="timeToCritical">--</span>
                    <span class="text-lg font-bold text-blue-400">Bulan</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Vanishing Yield (Full Width) -->
    <div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem] p-10 border border-slate-800 relative overflow-hidden shadow-2xl">
        <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
        <h2 class="text-4xl font-black text-white tracking-tighter uppercase mb-2">VANISHING YIELD ANALYSIS</h2>
        <p class="text-slate-400 font-bold text-lg">Mengapa produksi "menghilang" padahal pohon terlihat sehat?</p>
    </div>
'''
    
    # PHASE 3: Risk Matrix + Control Tower
    new_content += PHASE_HEADERS[3]
    new_content += '''
    <!-- Risk Control Tower -->
    <div class="bg-gradient-to-br from-slate-900 via-rose-950 to-slate-900 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden border border-rose-500/30">
        <span class="iso-badge iso-phase-3">3. EVALUATION</span>
        <h3 class="text-2xl font-black text-rose-200 uppercase tracking-tight mb-6">🚨 RISK CONTROL TOWER</h3>
        <div class="grid grid-cols-2 gap-4">
            <div class="bg-black/30 rounded-2xl p-5">
                <span class="text-xs font-black text-rose-300 uppercase block mb-2">Total Loss</span>
                <div class="text-3xl font-black text-white" id="totalLossDisplay">Rp 0</div>
            </div>
            <div class="bg-black/30 rounded-2xl p-5">
                <span class="text-xs font-black text-rose-300 uppercase block mb-2">Critical Blocks</span>
                <div class="text-3xl font-black text-red-400" id="criticalCountDisplay">0</div>
            </div>
        </div>
    </div>
'''
    
    # PHASE 4: Standard Protocols
    new_content += PHASE_HEADERS[4]
    new_content += '''
    <!-- Standard Protocols -->
    <div class="bg-gradient-to-br from-slate-900 to-emerald-950 text-white p-8 rounded-3xl shadow-2xl relative overflow-hidden border border-emerald-500/30">
        <span class="iso-badge iso-phase-4">4. TREATMENT</span>
        <h2 class="text-3xl font-black text-emerald-200 uppercase tracking-tight mb-4">📋 STANDARD PROTOCOLS</h2>
        <p class="text-slate-400 font-bold text-lg mb-6">Protokol mitigasi berdasarkan severity level</p>
    </div>
'''
    
    # PHASE 5: Watchlist
    new_content += PHASE_HEADERS[5]
    new_content += '''
    <!-- Watchlist -->
    <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
        <span class="iso-badge iso-phase-5">5. MONITORING</span>
        <h2 class="text-2xl font-black text-slate-900 uppercase tracking-tight mb-4">📊 WATCHLIST</h2>
        <p class="text-slate-600 font-bold mb-6">Continuous monitoring blok prioritas</p>
    </div>
'''
    
    new_content += '\n</div><!-- End tab-overview -->\n\n'
    
    # Add scripts section
    new_content += '''
<script>
// Likelihood Analysis Logic
function updateLikelihoodMetrics(blockData) {
    if (!blockData) return;
    const ar = blockData.arNdre || 0;
    const sph = blockData.sph || 0;
    const arSlider = document.getElementById('arWeightSlider');
    const sphSlider = document.getElementById('sphModifierSlider');
    const arWeight = arSlider ? parseFloat(arSlider.value) : 1.0;
    const sphModifier = sphSlider ? parseFloat(sphSlider.value) : 1.0;
    
    let score = 0;
    if (ar >= 5) score = 75 + (ar - 5) * 5;
    else if (ar >= 2) score = 40 + (ar - 2) * 10;
    else score = ar * 20;
    score = score * arWeight;
    let sphBonus = (sph > 130 ? 10 : (sph > 120 ? 5 : 0)) * sphModifier;
    score = Math.min(95, Math.max(0, score + sphBonus));
    
    const scoreEl = document.getElementById('likelihoodScore');
    const barEl = document.getElementById('likelihoodBar');
    if (scoreEl) scoreEl.textContent = Math.round(score);
    if (barEl) barEl.style.width = score + '%';
    
    let months = 0;
    if (sph > 100) {
        const deficit = sph - 100;
        const decline = Math.max(ar * 0.5, 0.1);
        months = Math.ceil(deficit / decline);
    }
    months = Math.max(1, Math.min(36, months));
    const timeEl = document.getElementById('timeToCritical');
    if (timeEl) timeEl.textContent = months;
}

window.addEventListener('load', function() {
    const toggleBtn = document.getElementById('toggleFormulaInfo');
    if (toggleBtn) toggleBtn.addEventListener('click', () => document.getElementById('formulaExplanation').classList.toggle('hidden'));
    
    const arSlider = document.getElementById('arWeightSlider');
    if (arSlider) arSlider.addEventListener('input', function() {
        const val = document.getElementById('arWeightValue');
        if (val) val.textContent = parseFloat(this.value).toFixed(1) + 'x';
    });
    
    const sphSlider = document.getElementById('sphModifierSlider');
    if (sphSlider) sphSlider.addEventListener('input', function() {
        const val = document.getElementById('sphModifierValue');
        if (val) val.textContent = parseFloat(this.value).toFixed(1) + 'x';
    });
    
    const recalcBtn = document.getElementById('recalculateLikelihood');
    if (recalcBtn) recalcBtn.addEventListener('click', function() {
        const sel = document.getElementById('globalSelectorLeft');
        if (sel && sel.value && BLOCKS_DATA) updateLikelihoodMetrics(BLOCKS_DATA[sel.value]);
    });
});
</script>
'''
    
    new_content += '\n</body>\n</html>'
    
    # Write
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Also update main file
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n✅ DASHBOARD REORGANIZED!")
    print("\nNEW STRUCTURE:")
    print("  PHASE 1: Map (Identification)")
    print("  PHASE 2: Financial Simulator + Financial Impact + LIKELIHOOD + Vanishing Yield (Analysis)")
    print("  PHASE 3: Risk Control Tower (Evaluation)")
    print("  PHASE 4: Standard Protocols (Treatment)")
    print("  PHASE 5: Watchlist (Monitoring)")
    print("\n🔄 REFRESH BROWSER NOW!")

if __name__ == "__main__":
    main()
