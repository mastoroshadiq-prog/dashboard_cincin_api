#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FINAL FIX - SPH Status Component dengan posisi yang benar
"""

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_SPH_FINAL.html'

with open(FILE_INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))

# STEP 1: Cari lokasi yang tepat - setelah grid cols-3 selesai
# Cari finSymptomLagLeft (elemen terakhir di grid)
marker = 'id="finSymptomLagLeft"'
pos = content.find(marker)

if pos == -1:
    print("ERROR: Marker tidak ditemukan!")
    exit(1)

print(f"Found marker at position {pos}")

# Dari posisi ini, cari 4 closing divs untuk keluar dari grid cols-3
closes = []
search_pos = pos
for i in range(10):
    next_close = content.find('</div>', search_pos)
    if next_close == -1:
        break
    closes.append(next_close)
    search_pos = next_close + 6

print(f"Found {len(closes)} closing divs")

# Insert setelah closing div ke-4
if len(closes) >= 4:
    insert_pos = closes[3] + 6
    
    sph_html = '''
                <!-- SPH STATUS INDICATOR -->
                <div class="mt-6 pt-6 border-t border-indigo-500/20 relative z-10">
                    <div class="bg-black/30 p-4 rounded-xl border border-indigo-500/20">
                        <div class="flex items-center justify-between mb-3">
                            <div class="flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-indigo-400">
                                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                                </svg>
                                <span class="text-[9px] font-bold text-indigo-200/60 uppercase">Status Kerapatan</span>
                            </div>
                            <span class="text-xs font-black" id="sphStatusBadgeLeft">--</span>
                        </div>
                        <div class="relative h-3 bg-slate-800 rounded-full overflow-hidden mb-2">
                            <div id="sphProgressLeft" class="h-full transition-all duration-500 rounded-full" style="width: 0%"></div>
                        </div>
                        <div class="flex justify-between text-[8px] text-slate-500">
                            <span>Kritis (&lt;100)</span>
                            <span>Optimal (130-140)</span>
                        </div>
                    </div>
                </div>
'''
    
    content = content[:insert_pos] + sph_html + content[insert_pos:]
    print(f"✓ HTML inserted at position {insert_pos}")

# STEP 2: Add JavaScript
js_code = '''
    function updateSPHStatus(blockData, side) {
        if (!blockData || !blockData.sph) return;
        const sph = parseFloat(blockData.sph);
        const pct = (sph / 136) * 100;
        let status, color, prog;
        if (sph < 100) { status = '🔴 KRITIS'; color = 'text-red-400'; prog = 'bg-gradient-to-r from-red-600 to-red-500'; }
        else if (sph < 120) { status = '🟠 RENDAH'; color = 'text-orange-400'; prog = 'bg-gradient-to-r from-orange-600 to-orange-500'; }
        else if (sph < 130) { status = '🟡 SEDANG'; color = 'text-yellow-400'; prog = 'bg-gradient-to-r from-yellow-600 to-yellow-500'; }
        else if (sph <= 140) { status = '🟢 OPTIMAL'; color = 'text-emerald-400'; prog = 'bg-gradient-to-r from-emerald-600 to-emerald-500'; }
        else { status = '🔵 TINGGI'; color = 'text-blue-400'; prog = 'bg-gradient-to-r from-blue-600 to-blue-500'; }
        const badge = document.getElementById('sphStatusBadge' + side);
        if (badge) { badge.textContent = status; badge.className = 'text-xs font-black ' + color; }
        const bar = document.getElementById('sphProgress' + side);
        if (bar) { bar.style.width = Math.min(pct, 100) + '%'; bar.className = 'h-full transition-all duration-500 rounded-full ' + prog; }
    }
'''

last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + js_code + '\n' + content[last_script:]
    print("✓ JavaScript added")

# STEP 3: Add function call
# Cari di mana finSphLeft di-update
pattern = 'document.getElementById("finSphLeft").textContent'
pos = content.find(pattern)
if pos != -1:
    # Cari akhir baris (semicolon)
    end_pos = content.find(';', pos) + 1
    call = '\n        updateSPHStatus(blockData, "Left");'
    content = content[:end_pos] + call + content[end_pos:]
    print("✓ Function call added")

# Save
with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ DONE: {FILE_OUTPUT}")
print("\nSilakan test file ini di browser!")
