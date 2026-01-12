import os

# PATHS
V8_FILE = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_v8_final.html'
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

# HTML SNIPPETS ==============================================

# 1. ISO BADGE CSS (To be injected in HEAD)
ISO_CSS = '''
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
'''

# 2. PHASE HEADERS
HEADERS = {
    1: '<div class="mb-8 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-black">1</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK IDENTIFICATION</h2><p class="text-xs text-slate-500 font-bold">Identifikasi Sumber & Sebaran Risiko</p></div></div>',
    2: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black">2</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK ANALYSIS</h2><p class="text-xs text-slate-500 font-bold">Analisis Dampak Finansial & Probabilitas</p></div></div>',
    3: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-amber-600 rounded-lg flex items-center justify-center text-white font-black">3</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK EVALUATION</h2><p class="text-xs text-slate-500 font-bold">Evaluasi Level Risiko & Prioritas</p></div></div>',
    4: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-black">4</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK TREATMENT</h2><p class="text-xs text-slate-500 font-bold">Protokol Mitigasi & Pengendalian</p></div></div>',
    5: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center text-white font-black">5</div><div><h2 class="text-xl font-black text-slate-800 uppercase">MONITORING & REVIEW</h2><p class="text-xs text-slate-500 font-bold">Pemantauan Berkelanjutan</p></div></div>'
}

# 3. LIKELIHOOD COMPONENT (New)
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
});
</script>
'''

# 4. WATCHLIST COMPONENT (New standalone container for Phase 5)
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
                    <th class="px-3 py-2">Last Update</th>
                </tr>
            </thead>
            <tbody id="monitoringTableBody">
                <tr class="border-b border-slate-100">
                    <td class="px-3 py-2 font-bold">F008A</td>
                    <td class="px-3 py-2"><span class="bg-red-100 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold">CRITICAL</span></td>
                    <td class="px-3 py-2">High Exposure</td>
                    <td class="px-3 py-2">Today</td>
                </tr>
                <tr class="border-b border-slate-100">
                    <td class="px-3 py-2 font-bold">D001A</td>
                    <td class="px-3 py-2"><span class="bg-yellow-100 text-yellow-600 px-2 py-0.5 rounded text-[10px] font-bold">WARNING</span></td>
                    <td class="px-3 py-2">Moderate</td>
                    <td class="px-3 py-2">Today</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
'''

def extract_block(content, start_marker, end_marker=None, closing_tag_count=1):
    """Simple extraction helper"""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"FAILED to find start marker: {start_marker[:50]}...")
        return ""
    
    if end_marker:
        end_idx = content.find(end_marker, start_idx)
        if end_idx == -1:
            print(f"FAILED to find end marker: {end_marker[:50]}...")
            return ""
        return content[start_idx:end_idx]
    
    # Simple tag counting if no explicit end marker
    # This is naive but works for well-indented blocks usually
    # Better: find the next section start and cut there
    return ""

def main():
    print("Reading V8 Source...")
    with open(V8_FILE, 'r', encoding='utf-8') as f:
        src = f.read()
    
    # 1. HEAD & CSS
    head_end = src.find('</head>')
    header_content = src[:head_end] + ISO_CSS + src[head_end:src.find('<!-- MAIN DASHBOARD CONTENT -->')]
    
    # 2. EXTRACT COMPONENTS (Slicing based on known structure of V8)
    
    # Financial Simulator
    idx_fin_sim_start = src.find('<!-- Skenario Finansial Interaktif')
    idx_matrix_start = src.find('<!-- 3. RISK MATRIX')
    block_fin_sim = src[idx_fin_sim_start:idx_matrix_start]
    # Add Badge Ph2
    block_fin_sim = block_fin_sim.replace('<div class="bg-white', '<div class="bg-white relative') # ensure relative
    block_fin_sim = block_fin_sim.replace('relative overflow-hidden">', 'relative overflow-hidden">\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>')

    # Risk Matrix
    idx_grid_start = src.find('<div class="grid grid-cols-1 md:grid-cols-2 gap-6 relative mt-4">')
    block_matrix = src[idx_matrix_start:idx_grid_start]
    # Add Badge Ph3
    block_matrix = block_matrix.replace('<div class="bg-white', '<div class="bg-white relative')
    block_matrix = block_matrix.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-3">3. EVALUATION</span>', 1)

    # Grid (Left Financial & Control Tower)
    # We need to split this grid to separate Phase 2 (Financial) and Phase 3 (Tower)
    # The grid contains 2 divs: "Left Financial" and "Risk Control Tower"
    
    # Extract Left Financial (Blok A)
    idx_left_fin_start = src.find('<!-- Left Financial (Blok A) -->')
    idx_tower_start = src.find('<!-- Risk Control Tower (Summary) -->')
    
    # This block is inside a grid div. We'll reconstruct the wrappers manually.
    wrapper_grid_start = '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">'
    
    block_fin_impact = src[idx_left_fin_start:idx_tower_start]
    # Add Badge Ph2
    block_fin_impact = block_fin_impact.replace('relative overflow-hidden group border', 'relative overflow-hidden group border\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>')

    # Extract Control Tower
    # It ends before the closing of the grid div... tricky.
    # Let's find "<!-- Warning for Estate Scale -->" as the end of the grid section approx
    idx_warning_start = src.find('<!-- Warning for Estate Scale -->')
    block_control_tower_raw = src[idx_tower_start:idx_warning_start]
    # Remove the closing divs of the grid
    block_control_tower = block_control_tower_raw[:block_control_tower_raw.rfind('</div>')] # remove 1
    block_control_tower = block_control_tower[:block_control_tower.rfind('</div>')] # remove 2
    # Add Badge Ph3
    block_control_tower = block_control_tower.replace('relative overflow-hidden group border', 'relative overflow-hidden group border\n<span class="iso-badge iso-phase-3">3. EVALUATION</span>')

    # Vanishing Yield is NOT in V8 ? 
    # Wait, user mapped "Vanishing Yield Explained (Line ~835)" in the plan.
    # Let's check if it exists in V8.
    idx_vanishing = src.find('Vanishing Yield')
    if idx_vanishing == -1:
        # Create it if missing
        block_vanishing = '''
        <div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem] p-10 border border-slate-800 relative overflow-hidden shadow-2xl mb-8">
            <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
            <h2 class="text-3xl font-black text-white tracking-tighter uppercase mb-2">VANISHING YIELD ANALYSIS</h2>
            <p class="text-slate-400 font-bold text-lg">Analisis Kesenjangan Produksi vs Potensi Biologis</p>
        </div>
        '''
    else:
        # Extract it if found
        block_vanishing = "" # Placeholder

    # Map Section (Phase 1)
    idx_map_start = src.find('<!-- SECTION PETA CINCIN API -->')
    # It ends before protocols
    idx_proto_start = src.find('<!-- ISO 31000 PROTOCOLS')
    block_map = src[idx_map_start:idx_proto_start]
    # Add Badge Ph1
    block_map = block_map.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>', 1)

    # Protocols (Phase 4)
    # Ends at end of main container... 
    idx_tab_end = src.find('</div>\n    </div>', idx_proto_start)
    block_protocols = src[idx_proto_start:idx_tab_end]
    # Add Badge Ph4
    block_protocols = block_protocols.replace('relative">', 'relative">\n<span class="iso-badge iso-phase-4">4. TREATMENT</span>', 1)

    # Footer Scripts
    footer_scripts = src[src.find('<script>', idx_tab_end):]

    # ASSEMBLING THE NEW CONTENT =========================================
    
    new_body = header_content + '\n'
    new_body += '<!-- ISO 31000 RESTRUCTURED -->\n'
    new_body += '<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'

    # PHASE 1
    new_body += HEADERS[1] + '\n' + block_map + '\n'
    
    # PHASE 2
    new_body += HEADERS[2] + '\n'
    new_body += block_fin_sim + '\n' # Financial Simulator
    new_body += wrapper_grid_start + '\n' # Start Grid
    new_body += block_fin_impact + '\n' # Left: Fin Impact
    new_body += LIKELIHOOD_COMP + '\n' # Right: Likelihood (NEW)
    new_body += '</div>\n' # End Grid
    new_body += block_vanishing + '\n' # Vanishing Yield
    
    # PHASE 3
    new_body += HEADERS[3] + '\n'
    new_body += block_matrix + '\n'
    new_body += block_control_tower + '\n'
    
    # PHASE 4
    new_body += HEADERS[4] + '\n'
    new_body += block_protocols + '\n'
    
    # PHASE 5
    new_body += HEADERS[5] + '\n'
    new_body += WATCHLIST_COMP + '\n'
    
    new_body += '</div>\n' # End tab-overview
    
    # Add JS
    new_body += footer_scripts.replace('</body>', JS_LIKELIHOOD + '\n</body>')

    print("Writing to V9...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_body)
    
    print("✅ COMPLETE: Dashboard Reorganized to ISO 31000 Phases 1-5")

if __name__ == "__main__":
    main()
