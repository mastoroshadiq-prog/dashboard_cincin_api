import os
import re

# CONFIG
SOURCE_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

# HTML COMPONENTS

# 1. NAVIGATION BAR
NAV_BAR = '''
<!-- ISO 31000 NAVIGATION TABS -->
<div class="sticky top-[72px] z-40 bg-slate-50/95 backdrop-blur border-y border-slate-200 mb-6 py-2 shadow-sm transition-all" id="isoNavBar">
    <div class="max-w-7xl mx-auto px-4 flex overflow-x-auto no-scrollbar gap-2 md:justify-center">
        <!-- Tab 1 -->
        <button onclick="switchIsoTab(1)" id="tab-btn-1" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase text-indigo-600 bg-indigo-50 border border-indigo-200 transition-all hover:shadow-md ring-2 ring-indigo-500/0 active:scale-95">
            <span class="w-6 h-6 rounded bg-indigo-600 text-white flex items-center justify-center text-xs">1</span>
            <span>Identification</span>
        </button>
        <!-- Tab 2 -->
        <button onclick="switchIsoTab(2)" id="tab-btn-2" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-blue-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">2</span>
            <span>Analysis</span>
        </button>
        <!-- Tab 3 -->
        <button onclick="switchIsoTab(3)" id="tab-btn-3" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-amber-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">3</span>
            <span>Evaluation</span>
        </button>
        <!-- Tab 4 -->
        <button onclick="switchIsoTab(4)" id="tab-btn-4" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-emerald-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">4</span>
            <span>Treatment</span>
        </button>
        <!-- Tab 5 -->
        <button onclick="switchIsoTab(5)" id="tab-btn-5" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-slate-600 border border-transparent hover:border-slate-200 transition-all active:scale-95">
            <span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">5</span>
            <span>Monitoring</span>
        </button>
    </div>
</div>
'''

# 2. JS LOGIC FOR TABS
TAB_SCRIPT = '''
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
    
    const c = colors[phaseNum];
    activeBtn.className = `iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase ${c[2]} ${c[3]} ${c[4]} transition-all shadow-sm ring-2 ring-${c[0]}-500/10`;
    
    const activeBadge = activeBtn.querySelector('span:first-child');
    activeBadge.className = `w-6 h-6 rounded ${c[1]} text-white flex items-center justify-center text-xs`;
    
    // 5. Scroll to top of content (optional)
    // window.scrollTo({top: 0, behavior: 'smooth'});
    
    // 6. Force Map Resize if entering Phase 1 (Leaflet glitch fix)
    if(phaseNum === 1 && window.map) {
        setTimeout(() => { map.invalidateSize(); }, 200);
    }
}

// Init on Load
document.addEventListener('DOMContentLoaded', () => {
    switchIsoTab(1); // Start at Phase 1
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
    print("Reading V9 Linear Source...")
    if not os.path.exists(SOURCE_FILE):
        print("ERROR: Source file not found.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        src = f.read()

    # SECTION IDENTIFICATION PATTERNS
    # We will split the content based on the PHASE HEADERS we injected previously.
    # Pattern: 1</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK IDENTIFICATION</h2>
    
    # Let's find the split points using the phase number headers
    # Phase 1 header
    idx_p1 = src.find('">1</div>')
    # Phase 2 header
    idx_p2 = src.find('">2</div>')
    # Phase 3 header
    idx_p3 = src.find('">3</div>')
    # Phase 4 header
    idx_p4 = src.find('">4</div>')
    # Phase 5 header
    idx_p5 = src.find('">5</div>')
    
    # End of content
    idx_end = src.find('</div> <!-- End Overview -->')
    
    if -1 in [idx_p1, idx_p2, idx_p3, idx_p4, idx_p5]:
        print("ERROR: Could not find all phase headers. Layout mismatch.")
        return

    # Backtrack to start of the div container for headers (approx 100 chars back)
    # The header string starts with <div class="mb-8 ...
    def find_div_start(idx, content):
        return content.rfind('<div class="mb-8', 0, idx)

    start_p1 = find_div_start(idx_p1, src)
    start_p2 = find_div_start(idx_p2, src)
    start_p3 = find_div_start(idx_p3, src)
    start_p4 = find_div_start(idx_p4, src)
    start_p5 = find_div_start(idx_p5, src)

    # SEGMENTATION
    # Content BEFORE P1 (Header, Top Bar, Disclaimer)
    # Note: We need to locate where "tab-overview" starts.
    idx_tab_overview = src.find('<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">')
    if idx_tab_overview == -1:
        print("ERROR: tab-overview container not found")
        return
    
    pre_content = src[:idx_tab_overview + len('<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">')]
    
    # PHASE CONTENT EXTRACTION
    # Phase 1: From start_p1 to start_p2
    content_p1 = src[start_p1:start_p2]
    # Phase 2: From start_p2 to start_p3
    content_p2 = src[start_p2:start_p3]
    # Phase 3: From start_p3 to start_p4
    content_p3 = src[start_p3:start_p4]
    # Phase 4: From start_p4 to start_p5
    content_p4 = src[start_p4:start_p5]
    # Phase 5: From start_p5 to idx_end
    content_p5 = src[start_p5:idx_end]
    
    post_content = src[idx_end:] # Closing divs + Scripts

    # WRAPPING
    def wrap_phase(content, phase_num):
        # We strip the "Header" itself if we want a cleaner look, or keep it.
        # Strategy: Keep the header as it serves as a nice title inside the tab.
        return f'\n<!-- PHASE {phase_num} WRAPPER -->\n<div id="phase-{phase_num}" class="iso-phase-content hidden">\n{content}\n</div>'

    new_p1 = wrap_phase(content_p1, 1)
    new_p2 = wrap_phase(content_p2, 2)
    new_p3 = wrap_phase(content_p3, 3)
    new_p4 = wrap_phase(content_p4, 4)
    new_p5 = wrap_phase(content_p5, 5)
    
    # INJECTION
    # Insert Nav Bar after the Estate Warning or near the top of tab-overview?
    # Better to insert it RIGHT AFTER the `pre_content` start.
    
    final_html = pre_content + '\n' + NAV_BAR + '\n' + new_p1 + new_p2 + new_p3 + new_p4 + new_p5 + '\n' + post_content
    
    # Inject Script before closing body
    final_html = final_html.replace('</body>', TAB_SCRIPT + '\n</body>')

    print("Writing V10 Tabbed Dashboard...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("✅ SUCCESS: ISO 31000 Tabbed Dashboard (v10) created.")

if __name__ == "__main__":
    main()
