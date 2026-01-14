"""
COMPREHENSIVE FIX:
1. Fix grid structure (both panels inside grid)
2. Add onclick handlers to blocks
3. Add function to populate ESTIMASI panel when block clicked
"""

import re

# Read demo
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("COMPREHENSIVE FIXES...")

# PROBLEM: Line 108 closes the first div, line 110 starts second div
# They're SEQUENTIAL not PARALLEL!

# FIX 1: Remove the closing tag at line 107 (before RIGHT panel comment)
# Find the section
old_structure_pattern = r'</div>\s*<-- RIGHT: STATISTIK BLOK'
if '</div>' in demo and '<!-- RIGHT: STATISTIK BLOK' in demo:
    # Remove that closing div
    demo = demo.replace('</div>\r\n\r\n                <!-- RIGHT: STATISTIK BLOK', '\r\n\r\n                <!-- RIGHT: STATISTIK BLOK')
    print("✅ Removed premature closing div")

# FIX 2: Add onclick to blocks in renderPaparanRisk function
# Find the function and update it
old_render = '''html += `
                    <div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer">
                        <div class="flex justify-between items-center">
                            <div>
                                <span class="text-white font-bold text-sm">${code}</span>
                                <span class="text-rose-300 text-xs ml-2">AR: ${ar.toFixed(1)}%</span>
                            </div>
                            <span class="text-rose-200 text-sm">Rp ${loss.toFixed(1)} Jt</span>
                        </div>
                    </div>
                `;'''

new_render = '''html += `
                    <div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer" onclick="loadBlockData('${code}')">
                        <div class="flex justify-between items-center">
                            <div>
                                <span class="text-white font-bold text-sm">${code}</span>
                                <span class="text-rose-300 text-xs ml-2">AR: ${ar.toFixed(1)}%</span>
                            </div>
                            <span class="text-rose-200 text-sm">Rp ${loss.toFixed(1)} Jt</span>
                        </div>
                    </div>
                `;'''

demo = demo.replace(old_render, new_render)
print("✅ Added onclick handlers to blocks")

# FIX 3: Add loadBlockData function
load_function = '''
        // Load block data into ESTIMASI panel
        function loadBlockData(code) {
            if (!BLOCKS_DATA[code]) return;
            
            const data = BLOCKS_DATA[code];
            
            // Update block name
            document.getElementById('finTitleLeft').textContent = code;
            
            // Update loss value
            document.getElementById('finLossLeft').textContent = Math.round(data.loss_value_juta || 0);
            
            // Update Potensi & Realisasi
            document.getElementById('finPotLeft').textContent = (data.potensi_ton_ha || 0).toFixed(2);
            document.getElementById('finRealLeft').textContent = (data.realisasi_ton_ha || 0).toFixed(2);
            
            // Update Gap
            const gap = Math.abs(data.gap_ton_ha || 0);
            document.getElementById('finGapTonLeft').textContent = gap.toFixed(2);
            
            const gapPct = Math.abs(data.gap_pct || 0);
            const gapPctEl = document.getElementById('finGapPctLeft');
            gapPctEl.textContent = gapPct.toFixed(0) + '%';
            gapPctEl.className = gapPct > 20 ? 'text-red-400 text-3xl font-black' : 'text-emerald-400 text-3xl font-black';
            
            // Update Footer Stats
            document.getElementById('finLuasLeft').textContent = (data.luas_ha || 0).toFixed(1) + ' Ha';
            document.getElementById('finSphLeft').textContent = data.sph || 0;
            document.getElementById('finTTLeft').textContent = data.tt || '--';
            document.getElementById('finARLeft').textContent = (data.attack_rate || 0).toFixed(1) + '%';
            document.getElementById('finCensusRateLeft').textContent = (data.census_rate_pct || 0).toFixed(2) + '%';
            document.getElementById('finMitigasiLeft').textContent = 'Rp ' + (data.mitigation_cost_juta || 0).toFixed(1) + ' Jt';
            
            // Update status
            const statusEl = document.getElementById('finSymptomLagLeft');
            const narrative = data.status_narrative || '--';
            statusEl.textContent = narrative;
            statusEl.className = narrative.includes('STABIL') || narrative.includes('MONITORING') 
                ? 'inline-block px-2 py-1 rounded bg-green-800 border border-green-600 text-[10px] font-bold text-green-200'
                : 'inline-block px-2 py-1 rounded bg-red-800 border border-red-600 text-[10px] font-bold text-red-200';
        }
'''

# Add before window.addEventListener
if 'function loadBlockData' not in demo:
    demo = demo.replace(
        '        // Auto-run on load',
        load_function + '\n        // Auto-run on load'
    )
    print("✅ Added loadBlockData function")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print(f"\n✅ ALL COMPREHENSIVE FIXES APPLIED!")
print(f"   File size: {len(demo)} chars")
print("\nCHANGES:")
print("  1.  Structure: Fixed div nesting (panels inside grid)")
print("  2. Click handlers: Added onclick to all blocks")
print("  3. Load function: Populate ESTIMASI panel on click")
