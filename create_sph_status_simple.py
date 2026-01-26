#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk membuat komponen Status Kerapatan SPH yang sederhana
Hanya menampilkan status/kategori SPH, bukan angka (karena sudah ada di atas)
"""

import re

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_SPH_STATUS.html'

# Komponen Status SPH yang sederhana
SPH_STATUS_COMPONENT = '''
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

# JavaScript function untuk update SPH status
SPH_STATUS_FUNCTION = '''
    // ============================================
    // SPH STATUS UPDATE FUNCTION
    // ============================================
    function updateSPHStatus(blockData, side = 'Left') {
        if (!blockData) return;
        
        const sphActual = blockData.sph || 0;
        const sphStandard = 136;
        const sphPercentage = (sphActual / sphStandard) * 100;
        
        // Determine status and color
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
        
        // Update status badge
        const badgeElement = document.getElementById(`sphStatusBadge${side}`);
        if (badgeElement) {
            badgeElement.textContent = statusText;
            badgeElement.className = `text-xs font-black ${statusColor}`;
        }
        
        // Update progress bar
        const progressElement = document.getElementById(`sphProgress${side}`);
        if (progressElement) {
            const clampedPercentage = Math.min(Math.max(sphPercentage, 0), 100);
            progressElement.style.width = `${clampedPercentage}%`;
            progressElement.className = `h-full transition-all duration-500 rounded-full ${progressColor}`;
        }
    }
'''

def create_sph_status():
    print("Membaca file dashboard...")
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Tambahkan komponen SPH Status di Estimasi Kerugian (Blok A)
    marker_pattern = r'(<div id="finSymptomLagLeft"[^>]*>[^<]*--[^<]*</div>\s*</div>\s*</div>\s*</div>)'
    matches = list(re.finditer(marker_pattern, content, re.DOTALL))
    
    if matches:
        insert_pos = matches[0].end()
        content = content[:insert_pos] + '\n' + SPH_STATUS_COMPONENT + '\n' + content[insert_pos:]
        print("✓ Komponen SPH Status ditambahkan di Estimasi Kerugian")
    else:
        print("⚠️  Tidak dapat menemukan lokasi untuk insert SPH Status")
    
    # 2. Tambahkan JavaScript function
    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + '\n' + SPH_STATUS_FUNCTION + '\n' + content[last_script_close:]
        print("✓ JavaScript function updateSPHStatus ditambahkan")
    
    # 3. Tambahkan call ke updateSPHStatus di updateFinancialPanel
    fin_loss_pattern = r'(document\.getElementById\(["\']finLossLeft["\']\)\.textContent\s*=\s*[^;]+;)'
    matches = list(re.finditer(fin_loss_pattern, content))
    
    if matches:
        insert_pos = matches[0].end()
        sph_call = '\n        updateSPHStatus(blockData, "Left");'
        content = content[:insert_pos] + sph_call + content[insert_pos:]
        print("✓ Auto-call updateSPHStatus ditambahkan")
    
    # 4. Tambahkan call di Risk Watchlist click handler
    # Cari fungsi yang handle click pada watchlist item
    watchlist_pattern = r'(function\s+loadBlockToPanel\([^)]*\)\s*{)'
    matches = list(re.finditer(watchlist_pattern, content))
    
    if matches:
        # Cari di dalam fungsi ini, tambahkan call setelah updateFinancialPanel
        func_start = matches[0].end()
        # Cari updateFinancialPanel call
        search_area = content[func_start:func_start+2000]
        update_fin_match = re.search(r'(updateFinancialPanel\([^)]+\);)', search_area)
        if update_fin_match:
            insert_pos = func_start + update_fin_match.end()
            sph_call = '\n        updateSPHStatus(blockData, "Left");'
            content = content[:insert_pos] + sph_call + content[insert_pos:]
            print("✓ Auto-call updateSPHStatus ditambahkan di loadBlockToPanel")
    
    # Tulis output
    print(f"\nMenulis ke {FILE_OUTPUT}...")
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "="*70)
    print("✅ SELESAI!")
    print("="*70)
    print("\nKomponen Status Kerapatan SPH telah ditambahkan:")
    print("  📍 Lokasi: Di bawah container Estimasi Kerugian (Blok A)")
    print("  🎯 Fitur:")
    print("     - Status badge dengan emoji (🔴🟠🟡🟢🔵)")
    print("     - Progress bar dengan warna dinamis")
    print("     - Update otomatis dari dropdown DAN watchlist")
    print("\n  📊 Kategori Status:")
    print("     🔴 KRITIS  : SPH < 100")
    print("     🟠 RENDAH  : SPH 100-120")
    print("     🟡 SEDANG  : SPH 120-130")
    print("     🟢 OPTIMAL : SPH 130-140")
    print("     🔵 TINGGI  : SPH > 140")
    print(f"\n  📁 File: {FILE_OUTPUT}")

if __name__ == "__main__":
    create_sph_status()
