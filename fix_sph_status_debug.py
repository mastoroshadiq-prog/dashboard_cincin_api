#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script FIXED untuk menambahkan Status Kerapatan SPH dengan debugging
"""

import re

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_SPH_FIXED.html'

print("="*70)
print("DEBUGGING & FIXING SPH STATUS COMPONENT")
print("="*70)

with open(FILE_INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"\n1. File size: {len(content)} characters")

# STEP 1: Cari lokasi untuk insert HTML component
# Cari finSphLeft (yang menampilkan SPH di footer stats)
sph_display_pattern = r'<span class="text-white font-black text-2xl" id="finSphLeft">--</span>'
matches = list(re.finditer(sph_display_pattern, content))

print(f"2. Found finSphLeft: {len(matches)} matches")

if not matches:
    print("   ERROR: finSphLeft tidak ditemukan!")
    print("   Mencoba pattern alternatif...")
    # Try alternative
    alt_pattern = r'id="finSphLeft"'
    matches = list(re.finditer(alt_pattern, content))
    print(f"   Alternative matches: {len(matches)}")

if matches:
    # Cari penutup dari grid cols-3 (footer stats)
    # Dari posisi finSphLeft, cari ke depan untuk menemukan penutup grid
    search_start = matches[0].end()
    
    # Cari 3 level penutup </div> untuk keluar dari grid-cols-3
    div_closes = []
    pos = search_start
    for i in range(10):  # Cari max 10 closing divs
        next_close = content.find('</div>', pos)
        if next_close == -1:
            break
        div_closes.append(next_close)
        pos = next_close + 6
    
    print(f"3. Found {len(div_closes)} closing divs after finSphLeft")
    
    if len(div_closes) >= 3:
        # Insert setelah closing div ke-3 (keluar dari grid)
        insert_pos = div_closes[2] + 6
        
        SPH_COMPONENT = '''
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
                        
                        <!-- Progress Bar -->
                        <div class="relative h-3 bg-slate-800 rounded-full overflow-hidden mb-2">
                            <div id="sphProgressLeft" class="h-full transition-all duration-500 rounded-full" style="width: 0%"></div>
                        </div>
                        
                        <!-- Markers -->
                        <div class="flex justify-between text-[8px] text-slate-500">
                            <span>Kritis (&lt;100)</span>
                            <span>Optimal (130-140)</span>
                        </div>
                    </div>
                </div>
'''
        
        content = content[:insert_pos] + '\n' + SPH_COMPONENT + '\n' + content[insert_pos:]
        print(f"4. ✓ HTML Component inserted at position {insert_pos}")
    else:
        print("4. ERROR: Tidak cukup closing divs ditemukan")

# STEP 2: Tambahkan JavaScript function
# Cari tag </script> terakhir
last_script = content.rfind('</script>')

if last_script != -1:
    JS_FUNCTION = '''
    
    // ============================================
    // SPH STATUS UPDATE FUNCTION
    // ============================================
    function updateSPHStatus(blockData, side) {
        console.log('updateSPHStatus called with:', blockData, side);
        
        if (!blockData || !blockData.sph) {
            console.warn('No SPH data available');
            return;
        }
        
        const sphActual = parseFloat(blockData.sph) || 0;
        const sphStandard = 136;
        const sphPercentage = (sphActual / sphStandard) * 100;
        
        console.log('SPH:', sphActual, 'Percentage:', sphPercentage);
        
        // Determine status
        let statusText = '';
        let statusColor = '';
        let progressColor = '';
        
        if (sphActual < 100) {
            statusText = '🔴 KRITIS';
            statusColor = 'text-red-400';
            progressColor = 'bg-gradient-to-r from-red-600 to-red-500';
        } else if (sphActual < 120) {
            statusText = '🟠 RENDAH';
            statusColor = 'text-orange-400';
            progressColor = 'bg-gradient-to-r from-orange-600 to-orange-500';
        } else if (sphActual < 130) {
            statusText = '🟡 SEDANG';
            statusColor = 'text-yellow-400';
            progressColor = 'bg-gradient-to-r from-yellow-600 to-yellow-500';
        } else if (sphActual <= 140) {
            statusText = '🟢 OPTIMAL';
            statusColor = 'text-emerald-400';
            progressColor = 'bg-gradient-to-r from-emerald-600 to-emerald-500';
        } else {
            statusText = '🔵 TINGGI';
            statusColor = 'text-blue-400';
            progressColor = 'bg-gradient-to-r from-blue-600 to-blue-500';
        }
        
        // Update badge
        const badgeId = 'sphStatusBadge' + side;
        const badgeElement = document.getElementById(badgeId);
        if (badgeElement) {
            badgeElement.textContent = statusText;
            badgeElement.className = 'text-xs font-black ' + statusColor;
            console.log('Badge updated:', statusText);
        } else {
            console.error('Badge element not found:', badgeId);
        }
        
        // Update progress bar
        const progressId = 'sphProgress' + side;
        const progressElement = document.getElementById(progressId);
        if (progressElement) {
            const clampedPercentage = Math.min(Math.max(sphPercentage, 0), 100);
            progressElement.style.width = clampedPercentage + '%';
            progressElement.className = 'h-full transition-all duration-500 rounded-full ' + progressColor;
            console.log('Progress updated:', clampedPercentage + '%');
        } else {
            console.error('Progress element not found:', progressId);
        }
    }
'''
    
    content = content[:last_script] + JS_FUNCTION + '\n' + content[last_script:]
    print(f"5. ✓ JavaScript function inserted before </script>")
else:
    print("5. ERROR: </script> tag tidak ditemukan")

# STEP 3: Tambahkan call di updateFinancialPanel
# Cari function updateFinancialPanel
update_panel_pattern = r'function updateFinancialPanel\('
match = re.search(update_panel_pattern, content)

if match:
    print(f"6. Found updateFinancialPanel at position {match.start()}")
    
    # Cari di dalam function ini, cari baris yang update finSphLeft
    func_start = match.start()
    func_area = content[func_start:func_start+5000]
    
    # Cari pattern: finSphLeft diupdate
    sph_update_pattern = r'(document\.getElementById\(["\']finSphLeft["\']\)[^;]+;)'
    sph_match = re.search(sph_update_pattern, func_area)
    
    if sph_match:
        insert_offset = func_start + sph_match.end()
        sph_call = '\n        updateSPHStatus(blockData, "Left");'
        content = content[:insert_offset] + sph_call + content[insert_offset:]
        print(f"7. ✓ updateSPHStatus call added in updateFinancialPanel")
    else:
        print("7. WARNING: finSphLeft update not found in updateFinancialPanel")
        print("   Searching for alternative insertion point...")
        
        # Alternative: cari finLossLeft update
        alt_pattern = r'(document\.getElementById\(["\']finLossLeft["\']\)[^;]+;)'
        alt_match = re.search(alt_pattern, func_area)
        if alt_match:
            insert_offset = func_start + alt_match.end()
            sph_call = '\n        updateSPHStatus(blockData, "Left");'
            content = content[:insert_offset] + sph_call + content[insert_offset:]
            print(f"7. ✓ updateSPHStatus call added after finLossLeft update")
else:
    print("6. ERROR: updateFinancialPanel function tidak ditemukan")

# Tulis output
with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n8. ✓ File written: {FILE_OUTPUT}")
print("\n" + "="*70)
print("SELESAI!")
print("="*70)
print("\nSilakan test file output:")
print(f"  {FILE_OUTPUT}")
print("\nBuka browser console (F12) untuk melihat log debug")
print("Jika masih tidak bekerja, screenshot console error-nya")
