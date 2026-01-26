import os

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

# The missing logic
TAB_LOGIC = '''
<script>
// ISO 31000 TAB MANAGER
function switchIsoTab(phaseNum) {
    console.log("Switching to Phase:", phaseNum);
    
    // 1. Hide all Content
    document.querySelectorAll('.iso-phase-content').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('animate-fade-in');
    });
    
    // 2. Show Selected Content
    const target = document.getElementById('phase-' + phaseNum);
    if(target) {
        target.classList.remove('hidden');
        target.classList.add('animate-fade-in'); // Add animation class if exists
    }
    
    // 3. Update Buttons State
    document.querySelectorAll('.iso-tab-btn').forEach(btn => {
        // Reset to default inactive style
        btn.className = "iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white border border-transparent hover:border-slate-200 transition-all active:scale-95";
        
        // Reset badge inside
        const badge = btn.querySelector('span:first-child');
        badge.className = "w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs";
    });
    
    // 4. Style Active Button
    const activeBtn = document.getElementById('tab-btn-' + phaseNum);
    const colors = {
        1: ['indigo', 'bg-indigo-600', 'text-indigo-600', 'bg-indigo-50', 'border-indigo-200'],
        2: ['blue', 'bg-blue-600', 'text-blue-600', 'bg-blue-50', 'border-blue-200'],
        3: ['amber', 'bg-amber-600', 'text-amber-600', 'bg-amber-50', 'border-amber-200'],
        4: ['emerald', 'bg-emerald-600', 'text-emerald-600', 'bg-emerald-50', 'border-emerald-200'],
        5: ['slate', 'bg-slate-600', 'text-slate-600', 'bg-slate-50', 'border-slate-200']
    };
    
    if (activeBtn) {
        const c = colors[phaseNum];
        activeBtn.className = `iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase ${c[2]} ${c[3]} ${c[4]} transition-all shadow-sm ring-2 ring-${c[0]}-500/10`;
        
        const activeBadge = activeBtn.querySelector('span:first-child');
        if(activeBadge) {
            activeBadge.className = `w-6 h-6 rounded ${c[1]} text-white flex items-center justify-center text-xs`;
        }
    }
    
    // 5. Force Map Resize if entering Phase 1 (Leaflet glitch fix)
    if(phaseNum === 1 && window.map) {
        setTimeout(() => { map.invalidateSize(); }, 200);
    }
}

// Likelihood Analysis Logic (Also missing?)
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

// Init on Load
document.addEventListener('DOMContentLoaded', () => {
    switchIsoTab(1); // Start at Phase 1
    
    // Init Sliders logic
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
    
     // Attach listener to global selector
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

<style>
.animate-fade-in {
    animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
'''

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', TAB_LOGIC + '\n</body>')
    else:
        new_content = content + TAB_LOGIC # Append if no body tag found
        
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ RESTORED: Tabs and Likelihood Logic Scripts.")

if __name__ == "__main__":
    main()
