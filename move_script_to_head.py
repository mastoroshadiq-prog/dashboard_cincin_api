import os

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # REMOVE OLD SCRIPT AT BOTTOM IF EXISTS
    # Look for: // ISO 31000 TAB MANAGER
    old_script_start = content.rfind('// ISO 31000 TAB MANAGER')
    if old_script_start != -1:
        # Find the <script> tag before it
        script_tag_open = content.rfind('<script', 0, old_script_start)
        # Find the closing tag
        script_tag_close = content.find('</script>', old_script_start)
        
        if script_tag_open != -1 and script_tag_close != -1:
            print("Removing old script from bottom...")
            # We cut it out
            content = content[:script_tag_open] + content[script_tag_close+9:]

    # PREPARE NEW HEAD SCRIPT
    HEAD_SCRIPT = '''
    <script>
    // ISO 31000 TAB MANAGER (HEAD Version)
    function switchIsoTab(phaseNum) {
        console.log("Switching to Phase:", phaseNum);
        
        // 1. Hide all Content
        const allPhases = document.querySelectorAll('.iso-phase-content');
        allPhases.forEach(el => {
            el.classList.add('hidden');
            el.classList.remove('animate-fade-in');
        });
        
        // 2. Show Selected Content
        const targetId = 'phase-' + phaseNum;
        const target = document.getElementById(targetId);
        if(target) {
            target.classList.remove('hidden');
            target.classList.add('animate-fade-in'); 
        } else {
            console.error("Target Phase Not Found:", targetId);
        }
        
        // 3. Update Buttons State
        document.querySelectorAll('.iso-tab-btn').forEach(btn => {
            btn.className = "iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white border border-transparent hover:border-slate-200 transition-all active:scale-95";
            const badge = btn.querySelector('span:first-child');
            if(badge) badge.className = "w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs";
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
            if(activeBadge) activeBadge.className = `w-6 h-6 rounded ${c[1]} text-white flex items-center justify-center text-xs`;
        }
        
        // 5. Force Map Resize
        if(phaseNum === 1 && window.map) {
            setTimeout(() => { map.invalidateSize(); }, 200);
        }
    }
    
    // Init on Load
    document.addEventListener('DOMContentLoaded', () => {
        // Ensure Phase 1 is forced active
        switchIsoTab(1);
    });
    </script>
    '''
    
    # INJECT INTO HEAD
    # Find </head>
    head_end = content.find('</head>')
    if head_end != -1:
        new_content = content[:head_end] + HEAD_SCRIPT + '\n' + content[head_end:]
        
        with open(FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Script moved to HEAD for priority execution.")
    else:
        print("Could not find </head> tag.")

if __name__ == "__main__":
    main()
