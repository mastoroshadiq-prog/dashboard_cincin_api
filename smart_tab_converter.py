import re

# CONFIG
SOURCE_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10_SMART.html'

# -- TEMPLATES --
NAV_BAR = '''
<div class="sticky top-[72px] z-40 bg-slate-50/95 backdrop-blur border-y border-slate-200 mb-6 py-2 shadow-sm transition-all" id="isoNavBar">
    <div class="max-w-7xl mx-auto px-4 flex overflow-x-auto no-scrollbar gap-2 md:justify-center">
        <button onclick="switchIsoTab(1)" id="tab-btn-1" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-black uppercase text-indigo-600 bg-indigo-50 border border-indigo-200 transition-all hover:shadow-md ring-2 ring-indigo-500/0 active:scale-95"><span class="w-6 h-6 rounded bg-indigo-600 text-white flex items-center justify-center text-xs">1</span><span>Identification</span></button>
        <button onclick="switchIsoTab(2)" id="tab-btn-2" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-blue-600 border border-transparent hover:border-slate-200 transition-all active:scale-95"><span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">2</span><span>Analysis</span></button>
        <button onclick="switchIsoTab(3)" id="tab-btn-3" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-amber-600 border border-transparent hover:border-slate-200 transition-all active:scale-95"><span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">3</span><span>Evaluation</span></button>
        <button onclick="switchIsoTab(4)" id="tab-btn-4" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-emerald-600 border border-transparent hover:border-slate-200 transition-all active:scale-95"><span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">4</span><span>Treatment</span></button>
        <button onclick="switchIsoTab(5)" id="tab-btn-5" class="iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white hover:text-slate-600 border border-transparent hover:border-slate-200 transition-all active:scale-95"><span class="w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs">5</span><span>Monitoring</span></button>
    </div>
</div>
'''

SCRIPT_LOGIC = '''
<script>
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

document.addEventListener('DOMContentLoaded', () => {
    switchIsoTab(1);
    // Init Sliders if needed
    const arSlider = document.getElementById('arWeightSlider');
    if(arSlider) arSlider.addEventListener('input', function() { document.getElementById('arWeightValue').textContent = parseFloat(this.value).toFixed(1) + 'x'; });
});
</script>
<style>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
'''

def main():
    print("Reading V9 Linear Source...")
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            src = f.read()
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found. Please ensure V9 Linear file exists.")
        return

    # STRATEGY: 
    # V9 Linear has clear headers we injected:
    # <div class="w-10 h-10 bg-indigo-600 ... >1</div> ... RISK IDENTIFICATION
    
    # We will use regex to find these split points reliably.
    
    # Split content by Phase Headers
    # Regex pattern to find the Phase Header Div
    # Pattern: <div[^>]*><div[^>]*>(\d)</div><div><h2[^>]*>RISK 
    
    pattern = re.compile(r'(<div[^>]*class="[^"]*mb-8[^"]*"[^>]*><div[^>]*class="[^"]*rounded-lg[^"]*">(\d)</div><div><h2[^>]*>RISK [^<]*</h2>)', re.DOTALL)
    
    matches = list(pattern.finditer(src))
    
    if len(matches) < 5:
        print(f"Warning: Found only {len(matches)} phase headers. Expected 5. Parsing might be incomplete.")
        
    # We reconstruct the body.
    # 1. Pre-Body (Header, disclaimer, etc)
    # The first match starts Phase 1. content before that is Pre.
    
    start_main_container = src.find('<div id="tab-overview"')
    if start_main_container == -1:
        print("Structure Error: tab-overview container not found.")
        return
        
    # Find closing of main container. It is usually before scripts.
    # We can assume the last </div> before <script> tag at end of file?
    # Or just wrap everything found between headers.
    
    # Header Part
    main_header = src[:start_main_container]
    
    # Insert Nav Bar into Header part, just before end
    # main_header += NAV_BAR # Better placement: inside the body wrapper?
    # No, usually navigation is outside the tab content container.
    
    new_body = main_header + NAV_BAR + '\n<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'
    
    # Process Phases
    for i in range(len(matches)):
        phase_num = int(matches[i].group(2))
        start_idx = matches[i].start()
        
        # End index is the start of next match, or End of Container for the last one.
        if i < len(matches) - 1:
            end_idx = matches[i+1].start()
        else:
            # Last phase. Finds where the main container ends.
            # Look for </div> <!-- End Overview --> if it exists from previous scripts?
            # Or just find the script tag start
            script_start = src.find('<script>', start_idx)
            end_idx = script_start
            
            # Walk back to remove the closing </div> of tab-overview
            temp_content = src[start_idx:end_idx]
            last_div = temp_content.rfind('</div>')
            if last_div != -1:
                # This logic is risky. Safe bet: Just take everything until script, and we manually close our wrapper.
                # Actually, V9 structure is: <div id="tab-overview"> ...content... </div> <script>...
                pass

        # Extract content
        content = src[start_idx:end_idx]
        
        # Cleanup: Remove the closing </div> of the main container which might be at the end of content P5
        if i == len(matches) - 1:
            content = content.strip()
            if content.endswith('</div>'):
                content = content[:-6]
            if content.endswith('<!-- End Overview -->'):
                content = content[:-len('<!-- End Overview -->')]
            content = content.strip()
            if content.endswith('</div>'): # Double check
                content = content[:-6]
                
        # Wrap
        new_body += f'<!-- PHASE {phase_num} -->\n<div id="phase-{phase_num}" class="iso-phase-content hidden">\n{content}\n</div>\n'

    new_body += '</div> <!-- End Tab Overview -->\n'
    
    # Post Body (Scripts)
    # Get scripts from V9
    script_start = src.find('<script>', matches[-1].end()) # Find script after last header
    # But wait, we used start_idx of last match above.
    # Actually, we can just grab everything from where we stopped parsing.
    
    # But simpler: Just inject clean script logic, ignoring old V9 scripts if they conflict?
    # V9 linear scripts logic is mostly for chart init. Tab logic needs to be added.
    
    # Let's take original scripts 
    scripts = src[src.find('<script>', 1000):] # Skip any head scripts
    
    # But we want to ensure we don't have duplicates or missing functions.
    # The safest way is to append our SCRIPT_LOGIC at the very end.
    
    new_body += scripts.replace('</body>', SCRIPT_LOGIC + '\n</body>')
    
    # Fix potential double </div> issues if parsing wasn't perfect? 
    # Browser is forgiving, but let's be neat.
    
    print(f"Writing Smart V10 to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_body)
        
    print("✅ Conversion Complete. Logic based on Phase Headers.")

if __name__ == "__main__":
    main()
