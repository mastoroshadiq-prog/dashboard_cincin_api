#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Konversi Dashboard V9 Linear (yang sudah benar) menjadi V10 Tabbed
dengan memastikan setiap komponen tetap di phase yang sesuai dengan badge-nya
"""

import re

SOURCE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'
OUTPUT = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

# Navigation Bar HTML
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

# Tab Controller Script
TAB_SCRIPT = '''
    <script>
    // ISO 31000 TAB MANAGER
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
        switchIsoTab(1);
    });
    </script>
    
    <style>
    .animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
'''

def convert_to_tabs():
    print("Membaca V9 Linear source...")
    with open(SOURCE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cari phase headers untuk menentukan batas setiap phase
    # Pattern: <div class="mb-8 ... >X</div> ... RISK ...
    phase_pattern = r'<div class="mb-8[^>]*><div class="w-10 h-10 bg-\w+-600[^>]*>(\d)</div><div><h2[^>]*>RISK [^<]*</h2>'
    
    matches = list(re.finditer(phase_pattern, content))
    print(f"Ditemukan {len(matches)} phase headers")
    
    if len(matches) < 5:
        print("ERROR: Tidak menemukan semua 5 phase headers!")
        return
    
    # Ekstrak bagian sebelum phase pertama (header, nav, dll)
    first_phase_start = matches[0].start()
    pre_content = content[:first_phase_start]
    
    # Inject navigation bar sebelum content phases
    # Cari <div id="tab-overview"
    tab_overview_pos = pre_content.find('<div id="tab-overview"')
    if tab_overview_pos != -1:
        # Insert nav bar setelah tag overview tapi sebelum content
        overview_tag_end = pre_content.find('>', tab_overview_pos) + 1
        pre_content = pre_content[:overview_tag_end] + '\n' + NAV_BAR + '\n' + pre_content[overview_tag_end:]
    
    # Ekstrak content untuk setiap phase
    phase_contents = {}
    for i, match in enumerate(matches):
        phase_num = int(match.group(1))
        start_pos = match.start()
        
        # End position adalah start dari phase berikutnya, atau akhir content
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            # Phase terakhir, cari sampai </div> <!-- End Overview -->
            end_marker = content.find('</div> <!-- End Overview -->', start_pos)
            if end_marker == -1:
                end_marker = content.find('</div>\n\n    <script>', start_pos)
            if end_marker == -1:
                end_marker = content.find('<script>', start_pos)
            end_pos = end_marker if end_marker != -1 else len(content)
        
        phase_contents[phase_num] = content[start_pos:end_pos].strip()
        print(f"Phase {phase_num}: {len(phase_contents[phase_num])} characters")
    
    # Rebuild dengan tab structure
    new_content = pre_content
    
    for phase_num in range(1, 6):
        if phase_num not in phase_contents:
            print(f"WARNING: Phase {phase_num} tidak ditemukan!")
            continue
        
        hidden_class = "" if phase_num == 1 else " hidden"
        new_content += f'\n<div id="phase-{phase_num}" class="iso-phase-content{hidden_class}">\n'
        new_content += phase_contents[phase_num]
        new_content += '\n</div>\n'
    
    new_content += '\n</div> <!-- End tab-overview -->\n'
    
    # Ekstrak scripts dari file asli
    script_start = content.find('<script>')
    if script_start != -1:
        scripts = content[script_start:]
        # Inject tab script sebelum scripts lainnya
        new_content += TAB_SCRIPT + '\n' + scripts
    
    # Tulis output
    print(f"\nMenulis output ke {OUTPUT}...")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ SELESAI!")
    print("\nVerifikasi:")
    for phase_num in range(1, 6):
        count = new_content.count(f'id="phase-{phase_num}"')
        print(f"  Phase {phase_num} container: {count} instance(s)")

if __name__ == "__main__":
    convert_to_tabs()
