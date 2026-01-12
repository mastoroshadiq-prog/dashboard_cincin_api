#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FINAL FIX: Reorganisasi dashboard berdasarkan badge ISO Phase
Pendekatan: Ekstrak komponen berdasarkan badge, lalu rebuild struktur tab yang bersih
"""

import re

SOURCE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'
OUTPUT = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

print("="*80)
print("FINAL FIX - REORGANISASI DASHBOARD BERDASARKAN BADGE")
print("="*80)

# Baca file
with open(SOURCE, 'r', encoding='utf-8') as f:
    content = f.read()

# Ekstrak header (sampai tab-overview)
header_end = content.find('<div id="tab-overview"')
if header_end == -1:
    print("ERROR: tab-overview tidak ditemukan")
    exit(1)

header = content[:header_end]

# Ekstrak scripts (dari <script> pertama setelah content)
# Cari dari belakang untuk mendapatkan semua scripts
script_start = content.find('<script>', header_end)
if script_start == -1:
    print("ERROR: Scripts tidak ditemukan")
    exit(1)

scripts = content[script_start:]

# Sekarang ekstrak content area (antara tab-overview dan scripts)
content_area = content[header_end:script_start]

# Cari semua komponen dengan badge
# Pattern: cari div yang mengandung badge iso-phase-X
components_by_phase = {1: [], 2: [], 3: [], 4: [], 5: []}

# Strategi: Split berdasarkan phase headers, lalu assign ke phase yang sesuai
# Phase headers pattern
phase_headers_pattern = r'<div class="mb-8[^>]*><div class="w-10 h-10 bg-(\w+)-600[^>]*>(\d)</div>'

matches = list(re.finditer(phase_headers_pattern, content_area))
print(f"\nDitemukan {len(matches)} phase headers")

for i, match in enumerate(matches):
    phase_num = int(match.group(2))
    start = match.start()
    
    # End adalah start dari header berikutnya, atau akhir content
    if i < len(matches) - 1:
        end = matches[i+1].start()
    else:
        end = len(content_area)
    
    # Ekstrak konten phase ini (termasuk headernya)
    phase_content = content_area[start:end].strip()
    components_by_phase[phase_num].append(phase_content)
    
    print(f"Phase {phase_num}: {len(phase_content)} chars")

# NAV BAR
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

# TAB SCRIPT
TAB_SCRIPT = '''
<script>
// ISO 31000 TAB MANAGER
function switchIsoTab(phaseNum) {
    console.log("Switching to Phase:", phaseNum);
    document.querySelectorAll('.iso-phase-content').forEach(el => { el.classList.add('hidden'); el.classList.remove('animate-fade-in'); });
    const target = document.getElementById('phase-' + phaseNum);
    if(target) { target.classList.remove('hidden'); target.classList.add('animate-fade-in'); }
    document.querySelectorAll('.iso-tab-btn').forEach(btn => {
        btn.className = "iso-tab-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-white border border-transparent hover:border-slate-200 transition-all active:scale-95";
        const badge = btn.querySelector('span:first-child');
        if(badge) badge.className = "w-6 h-6 rounded bg-slate-200 text-slate-500 flex items-center justify-center text-xs";
    });
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
    if(phaseNum === 1 && window.map) setTimeout(() => { map.invalidateSize(); }, 200);
}
document.addEventListener('DOMContentLoaded', () => { switchIsoTab(1); });
</script>
<style>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
'''

# BUILD OUTPUT
output = header
output += '<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'
output += NAV_BAR + '\n'

# Add each phase
for phase_num in range(1, 6):
    hidden = "" if phase_num == 1 else " hidden"
    output += f'<div id="phase-{phase_num}" class="iso-phase-content{hidden}">\n'
    
    if components_by_phase[phase_num]:
        for component in components_by_phase[phase_num]:
            output += component + '\n'
    else:
        print(f"WARNING: Phase {phase_num} kosong!")
    
    output += '</div>\n\n'

output += '</div> <!-- End tab-overview -->\n\n'
output += TAB_SCRIPT + '\n'
output += scripts

# Tulis output
print(f"\nMenulis output ke {OUTPUT}...")
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(output)

print("\n" + "="*80)
print("✅ SELESAI!")
print("="*80)
print("\nVerifikasi struktur:")
for i in range(1, 6):
    count = output.count(f'id="phase-{i}"')
    badge_count = output.count(f'iso-phase-{i}')
    print(f"  Phase {i}: {count} container, {badge_count} badges")

print("\nSilakan refresh browser dan test navigasi tab!")
