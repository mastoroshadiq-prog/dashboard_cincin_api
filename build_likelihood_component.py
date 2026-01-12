import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

# COMPLETE LIKELIHOOD COMPONENT HTML
LIKELIHOOD_HTML = '''
                    <div class="lg:col-span-1 h-full">
                        <!-- LIKELIHOOD & TREND ANALYSIS -->
                        <div class="bg-gradient-to-br from-blue-900 to-blue-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden group border border-blue-500/30 h-full flex flex-col">
                            <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
                            
                            <!-- Header -->
                            <div class="mb-6 relative z-10 border-b border-blue-500/30 pb-4">
                                <h3 class="text-lg font-black text-blue-200 uppercase tracking-tight mb-1">Likelihood & Trend</h3>
                                <p class="text-blue-300 text-xs font-bold">Analisis Probabilitas & Proyeksi</p>
                            </div>
                            
                            <div class="space-y-6 relative z-10 flex-grow">
                                <!-- PROBABILITY SCORE -->
                                <div class="bg-black/30 rounded-2xl p-5 border border-blue-500/20">
                                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest block mb-3">Probability Score</span>
                                    <div class="flex items-baseline gap-2">
                                        <span class="text-5xl font-black text-white" id="likelihoodScore">--</span>
                                        <span class="text-xl font-bold text-blue-400">%</span>
                                    </div>
                                    <p class="text-xs text-blue-300 italic mt-2">Probabilitas mencapai Critical State</p>
                                    <div class="mt-3 h-2 bg-slate-800 rounded-full overflow-hidden">
                                        <div id="likelihoodBar" class="h-full bg-gradient-to-r from-yellow-500 to-red-500" style="width: 0%"></div>
                                    </div>
                                </div>
                                
                                <!-- FORMULA PARAMETERS -->
                                <div class="bg-black/30 rounded-2xl p-4 border border-blue-500/20">
                                    <div class="flex items-center justify-between mb-3">
                                        <span class="text-xs font-black text-blue-300 uppercase tracking-widest">Formula Parameters</span>
                                        <button id="toggleFormulaInfo" class="text-xs text-blue-400 hover:text-blue-200 underline">ℹ️ Info</button>
                                    </div>
                                    
                                    <div id="formulaExplanation" class="hidden mb-4 p-3 bg-slate-900/50 rounded-lg border border-blue-500/20">
                                        <p class="text-xs text-blue-200 leading-relaxed mb-2"><strong>Formula Basis:</strong> Likelihood dihitung dari:</p>
                                        <ul class="text-xs text-blue-300 space-y-1 ml-4">
                                            <li>• <strong>Attack Rate (AR):</strong> Primary indicator (40-95%)</li>
                                            <li>• <strong>SPH Density:</strong> Spread risk modifier (+5-10%)</li>
                                        </ul>
                                        <p class="text-xs text-yellow-300 mt-2 italic">⚠️ Formula ini estimasi empiris. Nilai aktual bergantung pada <strong>domain expert</strong>.</p>
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
                                        
                                        <button id="recalculateLikelihood" class="w-full mt-2 px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black uppercase rounded-lg transition-colors">🔄 Recalculate</button>
                                    </div>
                                </div>
                                
                                <!-- TIME TO CRITICAL -->
                                <div class="bg-black/30 rounded-2xl p-5 border border-blue-500/20">
                                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest block mb-3">Time to Critical (SPH <100)</span>
                                    <div class="flex items-baseline gap-2 mb-2">
                                        <span class="text-4xl font-black text-white" id="timeToCritical">--</span>
                                        <span class="text-lg font-bold text-blue-400">Bulan</span>
                                    </div>
                                    <p class="text-xs text-blue-300 italic">Proyeksi jika trend continues</p>
                                    <div class="mt-4 h-2 bg-slate-800 rounded-full overflow-hidden">
                                        <div id="timelineBar" class="h-full bg-gradient-to-r from-emerald-500 via-yellow-500 to-red-500" style="width: 60%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
'''

# COMPLETE JAVASCRIPT
LIKELIHOOD_JS = '''
<script>
// LIKELIHOOD ANALYSIS LOGIC
function updateLikelihoodMetrics(blockData) {
    if (!blockData) return;
    
    const ar = blockData.arNdre || 0;
    const sph = blockData.sph || 0;
    const arSlider = document.getElementById('arWeightSlider');
    const sphSlider = document.getElementById('sphModifierSlider');
    const arWeight = arSlider ? parseFloat(arSlider.value) : 1.0;
    const sphModifier = sphSlider ? parseFloat(sphSlider.value) : 1.0;
    
    // Calculate likelihood
    let score = 0;
    if (ar >= 5) score = 75 + (ar - 5) * 5;
    else if (ar >= 2) score = 40 + (ar - 2) * 10;
    else score = ar * 20;
    
    score = score * arWeight;
    let sphBonus = (sph > 130 ? 10 : (sph > 120 ? 5 : 0)) * sphModifier;
    score = Math.min(95, Math.max(0, score + sphBonus));
    
    // Update UI
    const scoreEl = document.getElementById('likelihoodScore');
    const barEl = document.getElementById('likelihoodBar');
    if (scoreEl) scoreEl.textContent = Math.round(score);
    if (barEl) barEl.style.width = score + '%';
    
    // Time to critical
    let months = 0;
    if (sph > 100) {
        const deficit = sph - 100;
        const decline = Math.max(ar * 0.5, 0.1);
        months = Math.ceil(deficit / decline);
    }
    months = Math.max(1, Math.min(36, months));
    
    const timeEl = document.getElementById('timeToCritical');
    const timelineEl = document.getElementById('timelineBar');
    if (timeEl) timeEl.textContent = months;
    if (timelineEl) timelineEl.style.width = Math.max(0, 100 - (months * 2.5)) + '%';
}

// Event handlers
window.addEventListener('load', function() {
    // Toggle info
    const toggleBtn = document.getElementById('toggleFormulaInfo');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const exp = document.getElementById('formulaExplanation');
            if (exp) exp.classList.toggle('hidden');
        });
    }
    
    // Sliders
    const arSlider = document.getElementById('arWeightSlider');
    if (arSlider) {
        arSlider.addEventListener('input', function() {
            const val = document.getElementById('arWeightValue');
            if (val) val.textContent = parseFloat(this.value).toFixed(1) + 'x';
        });
    }
    
    const sphSlider = document.getElementById('sphModifierSlider');
    if (sphSlider) {
        sphSlider.addEventListener('input', function() {
            const val = document.getElementById('sphModifierValue');
            if (val) val.textContent = parseFloat(this.value).toFixed(1) + 'x';
        });
    }
    
    // Recalculate
    const recalcBtn = document.getElementById('recalculateLikelihood');
    if (recalcBtn) {
        recalcBtn.addEventListener('click', function() {
            const sel = document.getElementById('globalSelectorLeft');
            if (sel && sel.value && BLOCKS_DATA) {
                updateLikelihoodMetrics(BLOCKS_DATA[sel.value]);
            }
        });
    }
    
    // Hook block selection
    const sel = document.getElementById('globalSelectorLeft');
    if (sel) {
        sel.addEventListener('change', function() {
            if (this.value && BLOCKS_DATA) {
                updateLikelihoodMetrics(BLOCKS_DATA[this.value]);
            }
        });
    }
});
</script>
'''

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Adding Likelihood component...")
    
    # 1. Find Financial column closing and add Likelihood after
    financial_end = content.find('</div>\n                    </div>\n\n                    <!-- Removed: Vanishing Yield column')
    if financial_end == -1:
        # Try alternative pattern
        financial_end = content.find('</div>\n                </div>\n\n                <!-- Vanishing Yield Analysis')
    
    if financial_end != -1:
        insert_point = content.find('\n', financial_end) + 1
        content = content[:insert_point] + LIKELIHOOD_HTML + '\n' + content[insert_point:]
        print("✅ Likelihood HTML added")
    else:
        print("⚠️ Could not find insertion point - trying alternative")
        # Find grid closing
        grid_close = content.find('</div>\n</div></div>')
        if grid_close != -1:
            content = content[:grid_close] + LIKELIHOOD_HTML + '\n' + content[grid_close:]
            print("✅ Likelihood HTML added (alternative)")
    
    # 2. Add JavaScript before </body>
    body_close = content.rfind('</body>')
    if body_close != -1:
        content = content[:body_close] + LIKELIHOOD_JS + '\n' + content[body_close:]
        print("✅ Likelihood JavaScript added")
    
    # 3. Write
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ COMPLETE! Dashboard rebuilt with Likelihood component")
    print("🔄 Refresh browser and test!")

if __name__ == "__main__":
    main()
