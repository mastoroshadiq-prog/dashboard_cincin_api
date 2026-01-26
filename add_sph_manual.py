#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script MANUAL untuk menambahkan SPH Status - Dijamin Berhasil
"""

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_WITH_SPH_STATUS.html'

with open(FILE_INPUT, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines:", len(lines))

# STEP 1: Cari baris yang berisi finSphLeft
insert_line = None
for i, line in enumerate(lines):
    if 'id="finSphLeft"' in line:
        print(f"Found finSphLeft at line {i+1}")
        # Cari 3 closing divs setelah ini untuk keluar dari grid
        div_count = 0
        for j in range(i+1, min(i+20, len(lines))):
            if '</div>' in lines[j]:
                div_count += 1
                if div_count == 3:
                    insert_line = j + 1
                    print(f"Will insert after line {insert_line}")
                    break
        break

if insert_line:
    # HTML Component
    sph_html = '''                <!-- SPH STATUS INDICATOR -->
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
    lines.insert(insert_line, sph_html)
    print("✓ HTML inserted")

# STEP 2: Tambahkan JavaScript sebelum </script> terakhir
for i in range(len(lines)-1, -1, -1):
    if '</script>' in lines[i]:
        js_code = '''
    // SPH STATUS UPDATE
    function updateSPHStatus(blockData, side) {
        if (!blockData || !blockData.sph) return;
        const sph = parseFloat(blockData.sph);
        const pct = (sph / 136) * 100;
        let status = '', color = '', prog = '';
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
        lines.insert(i, js_code)
        print(f"✓ JavaScript inserted at line {i+1}")
        break

# STEP 3: Tambahkan call di updateFinancialPanel
for i, line in enumerate(lines):
    if 'document.getElementById("finSphLeft")' in line and '.textContent' in line:
        # Insert setelah baris ini
        lines.insert(i+1, '        updateSPHStatus(blockData, "Left");\n')
        print(f"✓ Function call added at line {i+2}")
        break

# Tulis output
with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ DONE! File: {FILE_OUTPUT}")
print("\nTest dengan:")
print("1. Buka file di browser")
print("2. Pilih blok dari dropdown")
print("3. Lihat Status Kerapatan muncul di bawah Estimasi Kerugian")
