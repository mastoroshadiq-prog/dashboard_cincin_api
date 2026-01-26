import os

# SOURCES
V8_FILE = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_v8_final.html'
# OUTPUT
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

# --- HTML SNIPPETS ---

# 1. STYLE & CSS
ISO_STYLE = '''
<style>
    /* ISO 31000 Badges */
    .iso-badge {
        position: absolute; top: 1.5rem; right: 1.5rem;
        padding: 0.35rem 0.85rem; border-radius: 9999px;
        font-size: 0.6rem; font-weight: 900; text-transform: uppercase;
        letter-spacing: 0.15em; z-index: 50; backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        pointer-events: none;
    }
    .iso-phase-1 { background: rgba(99, 102, 241, 0.85); color: white; }
    .iso-phase-2 { background: rgba(59, 130, 246, 0.85); color: white; }
    .iso-phase-3 { background: rgba(245, 158, 11, 0.85); color: white; }
    .iso-phase-4 { background: rgba(16, 185, 129, 0.85); color: white; }
    .iso-phase-5 { background: rgba(100, 116, 139, 0.85); color: white; }

    /* Animation */
    .animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
'''

# 2. NAV BAR
NAV_BAR = '''
<div class="sticky top-[72px] z-40 bg-slate-50/95 backdrop-blur border-y border-slate-200 mb-6 py-2 shadow-sm transition-all" id="isoNavBar">
    <div class="max-w-7xl mx-auto px-4 flex overflow-x-auto no-scrollbar gap-2 md:justify-center">
        <button onclick="switchIsoTab(1)" id="tab-btn-1" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase text-indigo-600 bg-indigo-50 border border-indigo-200 transition-all hover:shadow-md ring-2 ring-indigo-500/0 active:scale-95">
            <span class="w-6 h-6 rounded bg-indigo-600 text-white flex items-center justify-center text-xs">1</span><span>Identification</span>
        </button>
        <button onclick="switchIsoTab(2)" id="tab-btn-2" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-blue-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">2</span><span>Analysis</span>
        </button>
        <button onclick="switchIsoTab(3)" id="tab-btn-3" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-amber-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">3</span><span>Evaluation</span>
        </button>
        <button onclick="switchIsoTab(4)" id="tab-btn-4" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-emerald-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">4</span><span>Treatment</span>
        </button>
        <button onclick="switchIsoTab(5)" id="tab-btn-5" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-slate-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">5</span><span>Monitoring</span>
        </button>
    </div>
</div>
'''

# 3. HEADERS PER PHASE
HEADERS = {
    1: '<div class="mb-8 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-black">1</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK IDENTIFICATION</h2><p class="text-xs text-slate-500 font-bold">Identifikasi Sumber & Sebaran Risiko</p></div></div>',
    2: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black">2</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK ANALYSIS</h2><p class="text-xs text-slate-500 font-bold">Analisis Dampak Finansial & Probabilitas</p></div></div>',
    3: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-amber-600 rounded-lg flex items-center justify-center text-white font-black">3</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK EVALUATION</h2><p class="text-xs text-slate-500 font-bold">Evaluasi Level Risiko & Prioritas</p></div></div>',
    4: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-black">4</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK TREATMENT</h2><p class="text-xs text-slate-500 font-bold">Protokol Mitigasi & Pengendalian</p></div></div>',
    5: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center text-white font-black">5</div><div><h2 class="text-xl font-black text-slate-800 uppercase">MONITORING & REVIEW</h2><p class="text-xs text-slate-500 font-bold">Pemantauan Berkelanjutan</p></div></div>'
}

# 4. NEW COMPONENTS (LIKELIHOOD, WATCHLIST - Pure V9 content)
LIKELIHOOD_COMP = '''
<div class="bg-gradient-to-br from-blue-900 to-blue-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden border border-blue-500/30">
    <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
    <h3 class="text-lg font-black text-blue-200 uppercase tracking-tight mb-6">Likelihood & Trend</h3>
    <div class="bg-black/30 rounded-2xl p-5 mb-4">
        <span class="text-xs font-black text-blue-300 uppercase block mb-3">Probability Score</span>
        <div class="flex items-baseline gap-2"><span class="text-5xl font-black text-white" id="likelihoodScore">--</span><span class="text-xl font-bold text-blue-400">%</span></div>
        <div class="mt-3 h-2 bg-slate-800 rounded-full overflow-hidden"><div id="likelihoodBar" class="h-full bg-gradient-to-r from-yellow-500 to-red-500" style="width: 0%"></div></div>
    </div>
    <div class="bg-black/30 rounded-2xl p-4">
        <div class="space-y-3">
            <div><div class="flex justify-between text-xs mb-1"><span class="text-blue-300 font-bold">AR Weight</span><span class="text-white font-black" id="arWeightValue">1.0x</span></div><input type="range" id="arWeightSlider" min="0.5" max="2.0" step="0.1" value="1.0" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"></div>
            <div><div class="flex justify-between text-xs mb-1"><span class="text-blue-300 font-bold">SPH Modifier</span><span class="text-white font-black" id="sphModifierValue">1.0x</span></div><input type="range" id="sphModifierSlider" min="0" max="2.0" step="0.1" value="1.0" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"></div>
            <button id="recalculateLikelihood" class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black uppercase rounded-lg">🔄 Recalculate</button>
        </div>
    </div>
    <div class="bg-black/30 rounded-2xl p-5 mt-4"><span class="text-xs font-black text-blue-300 uppercase block mb-3">Time to Critical</span><div class="flex items-baseline gap-2"><span class="text-4xl font-black text-white" id="timeToCritical">--</span><span class="text-lg font-bold text-blue-400">Bulan</span></div></div>
</div>
'''

WATCHLIST_COMP = '''
<div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 mb-8 mx-1 relative overflow-hidden">
    <span class="iso-badge iso-phase-5">5. MONITORING</span>
    <h3 class="text-xl font-black text-slate-800 uppercase tracking-tight mb-4">Watchlist Evaluation</h3>
    <div class="overflow-x-auto">
        <table class="w-full text-xs text-left text-slate-600">
            <thead class="bg-slate-50 text-slate-900 font-bold uppercase"><tr><th class="px-3 py-2">Blok</th><th class="px-3 py-2">Status</th><th class="px-3 py-2">Risk Level</th><th class="px-3 py-2">Recommendation</th></tr></thead>
            <tbody id="monitoringTableBody"><tr class="border-b border-slate-100"><td class="px-3 py-2 font-bold">LOADING...</td></tr></tbody>
        </table>
    </div>
</div>
'''

# 5. JS LOGIC (Tabs + Likelihood)
JS_CORE = '''
<script>
// TABS
function switchIsoTab(phaseNum) {
    document.querySelectorAll('.iso-phase-content').forEach(el => { el.classList.add('hidden'); el.classList.remove('animate-fade-in'); });
    const target = document.getElementById('phase-' + phaseNum);
    if(target) { target.classList.remove('hidden'); target.classList.add('animate-fade-in'); }
    
    document.querySelectorAll('.iso-tab-btn').forEach(btn => {
        btn.className = "iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white border border-transparent hover:border-slate-200 transition-all active:scale-95";
        btn.querySelector('span:first-child').className = "w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs";
    });
    
    const activeBtn = document.getElementById('tab-btn-' + phaseNum);
    const colors = {
        1: ['indigo', 'bg-indigo-600', 'text-indigo-600', 'bg-indigo-50', 'border-indigo-200'],
        2: ['blue', 'bg-blue-600', 'text-blue-600', 'bg-blue-50', 'border-blue-200'],
        3: ['amber', 'bg-amber-600', 'text-amber-600', 'bg-amber-50', 'border-amber-200'],
        4: ['emerald', 'bg-emerald-600', 'text-emerald-600', 'bg-emerald-50', 'border-emerald-200'],
        5: ['slate', 'bg-slate-600', 'text-slate-600', 'bg-slate-50', 'border-slate-200']
    };
    const c = colors[phaseNum];
    activeBtn.className = `iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase ${c[2]} ${c[3]} ${c[4]} transition-all shadow-sm ring-2 ring-${c[0]}-500/10`;
    activeBtn.querySelector('span:first-child').className = `w-6 h-6 rounded ${c[1]} text-white flex items-center justify-center text-xs`;
    
    if(phaseNum === 1 && window.map) setTimeout(() => { map.invalidateSize(); }, 200);
}

// LIKELIHOOD
function updateLikelihoodMetrics(blockData) {
    if (!blockData) return;
    const ar = blockData.arNdre || 0;
    const sph = blockData.sph || 0;
    const arSlider = document.getElementById('arWeightSlider');
    const sphSlider = document.getElementById('sphModifierSlider');
    const arWeight = arSlider ? parseFloat(arSlider.value) : 1.0;
    const sphModifier = sphSlider ? parseFloat(sphSlider.value) : 1.0;
    
    let score = (ar >= 5) ? (75 + (ar-5)*5) : ((ar >= 2) ? (40 + (ar-2)*10) : (ar*20));
    score = Math.min(95, Math.max(0, (score * arWeight) + ((sph > 130 ? 10 : (sph > 120 ? 5 : 0)) * sphModifier)));
    
    document.getElementById('likelihoodScore').textContent = Math.round(score);
    document.getElementById('likelihoodBar').style.width = score + '%';
    
    let months = 0;
    if (sph > 100) { months = Math.ceil((sph - 100) / Math.max(ar * 0.5, 0.1)); }
    document.getElementById('timeToCritical').textContent = Math.max(1, Math.min(36, months));
}

document.addEventListener('DOMContentLoaded', () => {
    switchIsoTab(1);
    
    const arSlider = document.getElementById('arWeightSlider');
    if(arSlider) arSlider.addEventListener('input', function() { document.getElementById('arWeightValue').textContent = parseFloat(this.value).toFixed(1) + 'x'; });
    
    const sphSlider = document.getElementById('sphModifierSlider');
    if(sphSlider) sphSlider.addEventListener('input', function() { document.getElementById('sphModifierValue').textContent = parseFloat(this.value).toFixed(1) + 'x'; });
    
    document.getElementById('recalculateLikelihood')?.addEventListener('click', function() {
        const sel = document.getElementById('globalSelectorLeft');
        if (sel && sel.value && typeof BLOCKS_DATA !== 'undefined') updateLikelihoodMetrics(BLOCKS_DATA[sel.value]);
    });
    
    const sel = document.getElementById('globalSelectorLeft');
    if (sel) sel.addEventListener('change', function() { if(this.value && typeof BLOCKS_DATA !== 'undefined') updateLikelihoodMetrics(BLOCKS_DATA[this.value]); });
});
</script>
'''

def extract_block(content, start_marker, end_marker):
    start = content.find(start_marker)
    if start == -1: return ""
    end = content.find(end_marker, start)
    if end == -1: return ""
    return content[start:end]

def main():
    print("Reading V8 Source...")
    with open(V8_FILE, 'r', encoding='utf-8') as f:
        src = f.read()

    # EXTRACT COMPONENTS (Same as Force V9, but safe)
    idx_main_start = src.find("<!-- MAIN DASHBOARD CONTENT -->")
    header_section = src[:idx_main_start].replace('</style>', ISO_STYLE + '\n</style>')

    # 1. PETA
    map_comp = extract_block(src, "<!-- SECTION PETA CINCIN API", "<!-- ISO 31000 PROTOCOLS")
    map_comp = map_comp.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>', 1)

    # 2. ANALYSIS
    fin_sim = extract_block(src, "<!-- Skenario Finansial Interaktif", "<!-- 3. RISK MATRIX")
    fin_sim = fin_sim.replace('<div class="bg-white p-6', '<div class="bg-white p-6 relative')
    fin_sim = fin_sim.replace('relative overflow-hidden">', 'relative overflow-hidden">\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>', 1)
    
    fin_impact = extract_block(src, "<!-- Left Financial (Blok A) -->", "<!-- Risk Control Tower")
    # FIX BAD ATTRIBUTE INJECTION RISK FROM PREVIOUS ATTEMPTS (Explicitly clean string)
    fin_impact = fin_impact.replace('border-indigo-500/30', 'border-indigo-500/30') 
    # Add badge carefully
    fin_impact = fin_impact.replace('border-indigo-500/30', 'border-indigo-500/30">\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>')
    # Remove the quoted closing > if replace added it? No, raw string replace is safer.
    
    yield_loss = '<div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem] p-10 border border-slate-800 relative overflow-hidden shadow-2xl mb-8"><span class="iso-badge iso-phase-2">2. ANALYSIS</span><h2 class="text-3xl font-black text-white tracking-tighter uppercase mb-2">VANISHING YIELD ANALYSIS</h2><p class="text-slate-400 font-bold text-lg">Analisis Kesenjangan Produksi vs Potensi Biologis</p></div>'

    # 3. EVALUATION
    # Get Risk Matrix Logic
    risk_matrix = extract_block(src, "<!-- 3. RISK MATRIX", '<div class="grid grid-cols-1 md:grid-cols-2 gap-6 relative mt-4">')
    risk_matrix = risk_matrix.replace('<div class="bg-white p-6', '<div class="bg-white p-6 relative')
    risk_matrix = risk_matrix.replace('mx-1 relative">', 'mx-1 relative">\n<span class="iso-badge iso-phase-3">3. EVALUATION</span>', 1)

    control_tower = extract_block(src, "<!-- Risk Control Tower", "<!-- Warning for Estate Scale")
    control_tower = control_tower.replace("border-rose-500/30", "border-rose-500/30\">\n<span class=\"iso-badge iso-phase-3\">3. EVALUATION</span>")

    estate_warning = extract_block(src, "<!-- Warning for Estate Scale", "<!-- SECTION PETA CINCIN API")
    
    # 4. TREATMENT
    protocols = extract_block(src, "<!-- ISO 31000 PROTOCOLS", "</div>\n    </div>\n    \n    <script>")
    if not protocols: # Fallback extraction
        idx_proto = src.find("<!-- ISO 31000 PROTOCOLS")
        idx_script = src.find("<script>", idx_proto)
        protocols = src[idx_proto:idx_script].rpartition("</div>")[0].rpartition("</div>")[0]
    protocols = protocols.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-4">4. TREATMENT</span>', 1)

    # SCRIPTS
    scripts = src[src.find("<script>", src.find("<!-- ISO 31000 PROTOCOLS")):]
    scripts = scripts.replace("</body>", JS_CORE + "\n</body>")

    # --- ASSEMBLY (TABBED) ---
    body = header_section + '\n' + NAV_BAR
    
    body += '<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'
    
    body += '<div id="phase-1" class="iso-phase-content">\n' + HEADERS[1] + '\n' + map_comp + '\n</div>'
    
    body += '<div id="phase-2" class="iso-phase-content hidden">\n' + HEADERS[2] + '\n' + fin_sim + '\n'
    body += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">\n' + fin_impact + '\n' + LIKELIHOOD_COMP + '\n</div>\n' + yield_loss + '\n</div>'
    
    body += '<div id="phase-3" class="iso-phase-content hidden">\n' + HEADERS[3] + '\n' + risk_matrix + '\n' + control_tower + '\n' + estate_warning + '\n</div>'
    
    body += '<div id="phase-4" class="iso-phase-content hidden">\n' + HEADERS[4] + '\n' + protocols + '\n</div>'
    
    body += '<div id="phase-5" class="iso-phase-content hidden">\n' + HEADERS[5] + '\n' + WATCHLIST_COMP + '\n</div>'
    
    body += '</div> <!-- End Overview -->\n'
    body += scripts
    
    print(f"Writing CLEAN V10 to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(body)

if __name__ == "__main__":
    main()
