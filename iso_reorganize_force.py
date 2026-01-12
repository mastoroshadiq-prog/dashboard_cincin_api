import os

# CONFIG
SOURCE_FILE = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_v8_final.html'
TARGET_FILE_1 = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'
TARGET_FILE_2 = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'

# HTML SNIPPETS
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
    .iso-phase-1 { background: rgba(99, 102, 241, 0.85); color: white; } /* Indigo */
    .iso-phase-2 { background: rgba(59, 130, 246, 0.85); color: white; } /* Blue */
    .iso-phase-3 { background: rgba(245, 158, 11, 0.85); color: white; } /* Amber */
    .iso-phase-4 { background: rgba(16, 185, 129, 0.85); color: white; } /* Emerald */
    .iso-phase-5 { background: rgba(100, 116, 139, 0.85); color: white; } /* Slate */
</style>
'''

HEADERS = {
    1: '<div class="mb-8 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-black">1</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK IDENTIFICATION</h2><p class="text-xs text-slate-500 font-bold">Identifikasi Sumber & Sebaran Risiko</p></div></div>',
    2: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black">2</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK ANALYSIS</h2><p class="text-xs text-slate-500 font-bold">Analisis Dampak Finansial & Probabilitas</p></div></div>',
    3: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-amber-600 rounded-lg flex items-center justify-center text-white font-black">3</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK EVALUATION</h2><p class="text-xs text-slate-500 font-bold">Evaluasi Level Risiko & Prioritas</p></div></div>',
    4: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-black">4</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK TREATMENT</h2><p class="text-xs text-slate-500 font-bold">Protokol Mitigasi & Pengendalian</p></div></div>',
    5: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center text-white font-black">5</div><div><h2 class="text-xl font-black text-slate-800 uppercase">MONITORING & REVIEW</h2><p class="text-xs text-slate-500 font-bold">Pemantauan Berkelanjutan</p></div></div>'
}

LIKELIHOOD_COMP = '''
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
'''

VANISHING_YIELD_COMP = '''
<div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem] p-10 border border-slate-800 relative overflow-hidden shadow-2xl mb-8">
    <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
    <h2 class="text-3xl font-black text-white tracking-tighter uppercase mb-2">VANISHING YIELD ANALYSIS</h2>
    <p class="text-slate-400 font-bold text-lg">Analisis Kesenjangan Produksi vs Potensi Biologis</p>
</div>
'''

WATCHLIST_COMP = '''
<div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 mb-8 mx-1 relative overflow-hidden">
    <span class="iso-badge iso-phase-5">5. MONITORING</span>
    <h3 class="text-xl font-black text-slate-800 uppercase tracking-tight mb-4">Watchlist Evaluation</h3>
    <div class="overflow-x-auto">
        <table class="w-full text-xs text-left text-slate-600">
            <thead class="bg-slate-50 text-slate-900 font-bold uppercase">
                <tr>
                    <th class="px-3 py-2">Blok</th>
                    <th class="px-3 py-2">Status</th>
                    <th class="px-3 py-2">Risk Level</th>
                    <th class="px-3 py-2">Recommendation</th>
                </tr>
            </thead>
            <tbody id="monitoringTableBody">
                <tr class="border-b border-slate-100">
                    <td class="px-3 py-2 font-bold">F008A</td>
                    <td class="px-3 py-2"><span class="bg-red-100 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold">CRITICAL</span></td>
                    <td class="px-3 py-2">High Exposure (Rp 29M)</td>
                    <td class="px-3 py-2">Isolasi Immediately</td>
                </tr>
                <tr class="border-b border-slate-100">
                    <td class="px-3 py-2 font-bold">D001A</td>
                    <td class="px-3 py-2"><span class="bg-yellow-100 text-yellow-600 px-2 py-0.5 rounded text-[10px] font-bold">WARNING</span></td>
                    <td class="px-3 py-2">Moderate</td>
                    <td class="px-3 py-2">Monitor Monthly</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
'''

JS_LIKELIHOOD = '''
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
    console.log("ISO 31000 Dashboard Logic Loaded");
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
        if (sel && sel.value && typeof BLOCKS_DATA !== 'undefined') updateLikelihoodMetrics(BLOCKS_DATA[sel.value]);
    });
    
    // Attach listener to global selector to trigger likelihood update as well
    const sel = document.getElementById('globalSelectorLeft');
    if (sel) {
        sel.addEventListener('change', function() {
            if (this.value && typeof BLOCKS_DATA !== 'undefined') {
                updateLikelihoodMetrics(BLOCKS_DATA[this.value]);
            }
        });
    }
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
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        src = f.read()
    
    # --- EXTRACT COMPONENTS ---
    
    # Header Section (Top of file until Main Content)
    # We find where main content starts. Usually "<!-- MAIN DASHBOARD CONTENT -->"
    idx_main_start = src.find("<!-- MAIN DASHBOARD CONTENT -->")
    header_section = src[:idx_main_start]
    # Inject ISO CSS into HEAD
    header_section = header_section.replace('</style>', ISO_STYLE + '\n</style>')
    
    # Financial Simulator (Block 2 in Orig)
    # Starts at "<!-- Skenario Finansial" -> Ends at "<!-- 3. RISK MATRIX"
    fin_sim = extract_block(src, "<!-- Skenario Finansial Interaktif", "<!-- 3. RISK MATRIX")
    fin_sim = fin_sim.replace('<div class="bg-white p-6', '<div class="bg-white p-6 relative')
    fin_sim = fin_sim.replace('relative overflow-hidden">', 'relative overflow-hidden">\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>', 1)

    # Risk Matrix (Block 3 in Orig)
    # Starts at "<!-- 3. RISK MATRIX" -> Ends at "<!-- Left Financial" BUT wait, in v8 it's a grid below...
    # The grid starts after matrix.
    # Matrix ends at: <div class="grid grid-cols-1 md:grid-cols-2 gap-6 relative mt-4">
    marker_grid_start = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6 relative mt-4">'
    risk_matrix = extract_block(src, "<!-- 3. RISK MATRIX", marker_grid_start)
    risk_matrix = risk_matrix.replace('<div class="bg-white p-6', '<div class="bg-white p-6 relative')
    risk_matrix = risk_matrix.replace('mx-1 relative">', 'mx-1 relative">\n<span class="iso-badge iso-phase-3">3. EVALUATION</span>', 1)

    # Left Financial (Inside Grid)
    idx_left_fin = src.find("<!-- Left Financial (Blok A) -->")
    # Finding end is tricky. It ends at "<!-- Risk Control Tower"
    fin_impact = extract_block(src, "<!-- Left Financial (Blok A) -->", "<!-- Risk Control Tower")
    fin_impact = fin_impact.replace("group border border-indigo-500/30", "group border border-indigo-500/30\n<span class=\"iso-badge iso-phase-2\">2. ANALYSIS</span>")

    # Risk Control Tower
    idx_tower = src.find("<!-- Risk Control Tower")
    # Ends at "<!-- Warning for Estate Scale"
    control_tower_raw = extract_block(src, "<!-- Risk Control Tower", "<!-- Warning for Estate Scale")
    # Cleanup closing divs from raw grid extract (last 2 divs usually)
    control_tower = control_tower_raw # Use as is, but be careful of closing tags. 
    # In V8 it's inside a grid column... we will wrap it in a new grid col logic if needed.
    # Add Badge
    control_tower = control_tower.replace("border-rose-500/30", "border-rose-500/30\n<span class=\"iso-badge iso-phase-3\">3. EVALUATION</span>")
    
    # Estate Warning (Keep it)
    estate_warning = extract_block(src, "<!-- Warning for Estate Scale", "<!-- SECTION PETA CINCIN API")

    # Map (Block 1 in ISO)
    # Starts "<!-- SECTION PETA CINCIN API" -> Ends "<!-- ISO 31000 PROTOCOLS"
    map_comp = extract_block(src, "<!-- SECTION PETA CINCIN API", "<!-- ISO 31000 PROTOCOLS")
    map_comp = map_comp.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>', 1)

    # Protocols
    protocols = extract_block(src, "<!-- ISO 31000 PROTOCOLS", "</div>\n    </div>\n    \n    <script>")
    # If extract fails, try shorter end marker
    if not protocols:
        # Try finding the script tag
        idx_proto = src.find("<!-- ISO 31000 PROTOCOLS")
        idx_script = src.find("<script>", idx_proto)
        # Scan back for the closing div of the main container
        protocols = src[idx_proto:idx_script].rpartition("</div>")[0].rpartition("</div>")[0]
        
    protocols = protocols.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-4">4. TREATMENT</span>', 1)

    # Footer/Scripts
    scripts = src[src.find("<script>", src.find("<!-- ISO 31000 PROTOCOLS")):]
    scripts = scripts.replace("</body>", JS_LIKELIHOOD + "\n</body>")

    # --- ASSEMBLE ---
    
    body = header_section + '\n'
    body += '<!-- ISO 31000 LINEAR DASHBOARD v9 -->\n'
    body += '<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'
    
    # Phase 1
    body += HEADERS[1] + '\n'
    body += map_comp + '\n'
    
    # Phase 2
    body += HEADERS[2] + '\n'
    body += fin_sim + '\n'
    body += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">\n' # New Grid for Impact vs Likelihood
    body += fin_impact + '\n'
    body += LIKELIHOOD_COMP + '\n'
    body += '</div>\n'
    body += VANISHING_YIELD_COMP + '\n'
    
    # Phase 3
    body += HEADERS[3] + '\n'
    body += risk_matrix + '\n'
    body += control_tower + '\n'
    body += estate_warning + '\n'
    
    # Phase 4
    body += HEADERS[4] + '\n'
    body += protocols + '\n'
    
    # Phase 5
    body += HEADERS[5] + '\n'
    body += WATCHLIST_COMP + '\n'
    
    body += '</div> <!-- End Overview -->\n'
    body += scripts
    
    # WRITE
    print(f"Writing to {TARGET_FILE_1}...")
    with open(TARGET_FILE_1, 'w', encoding='utf-8') as f:
        f.write(body)
        
    print(f"Writing to {TARGET_FILE_2}...")
    with open(TARGET_FILE_2, 'w', encoding='utf-8') as f:
        f.write(body)

if __name__ == "__main__":
    main()
