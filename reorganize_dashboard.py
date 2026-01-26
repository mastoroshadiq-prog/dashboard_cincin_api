#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk mereorganisasi komponen dashboard berdasarkan badge ISO Phase
"""

import re
from typing import List, Tuple, Dict

FILE_INPUT = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_ISO_TABBED_v10_REORGANIZED.html'

def extract_components_by_badge(content: str) -> Dict[int, List[str]]:
    """
    Ekstrak semua komponen berdasarkan badge ISO phase mereka
    """
    components = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    # Pattern untuk menemukan komponen dengan badge
    # Kita cari div yang memiliki badge iso-phase-X
    pattern = r'(<div[^>]*class="[^"]*(?:bg-gradient|bg-white)[^"]*"[^>]*>\s*<span class="iso-badge iso-phase-(\d)"[^>]*>[^<]+</span>.*?</div>(?:\s*</div>)*)'
    
    # Gunakan pendekatan yang lebih sederhana: cari berdasarkan marker unik
    # 1. Peta Cincin Api (Phase 1)
    peta_start = content.find('<!-- SECTION PETA CINCIN API -->')
    peta_end = content.find('<!-- Skenario Finansial', peta_start)
    if peta_start != -1 and peta_end != -1:
        components[1].append(content[peta_start:peta_end])
    
    # 2. Financial Simulator (Phase 2)
    fin_sim_start = content.find('<!-- Skenario Finansial Interaktif')
    fin_sim_end = content.find('<!-- Left Financial', fin_sim_start)
    if fin_sim_start != -1 and fin_sim_end != -1:
        components[2].append(content[fin_sim_start:fin_sim_end])
    
    # 3. Financial Impact (Phase 2)
    fin_impact_start = content.find('<!-- Left Financial (Blok A) -->')
    # Cari penutup div yang sesuai - ini tricky, kita cari div berikutnya
    if fin_impact_start != -1:
        # Cari dari posisi ini sampai menemukan komponen berikutnya
        search_pos = fin_impact_start
        div_count = 0
        in_component = False
        component_end = -1
        
        for i in range(search_pos, len(content)):
            if content[i:i+4] == '<div':
                div_count += 1
                in_component = True
            elif content[i:i+6] == '</div>':
                div_count -= 1
                if in_component and div_count == 0:
                    component_end = i + 6
                    break
        
        if component_end != -1:
            components[2].append(content[fin_impact_start:component_end])
    
    # 4. Likelihood & Trend (Phase 2)
    likelihood_start = content.find('<div class="bg-gradient-to-br from-blue-900 to-blue-950')
    if likelihood_start != -1:
        # Cari penutupnya
        search_pos = likelihood_start
        div_count = 0
        for i in range(search_pos, len(content)):
            if content[i:i+4] == '<div':
                div_count += 1
            elif content[i:i+6] == '</div>':
                div_count -= 1
                if div_count == 0:
                    components[2].append(content[likelihood_start:i+6])
                    break
    
    # 5. Vanishing Yield (Phase 2)
    vanishing_start = content.find('VANISHING YIELD ANALYSIS')
    if vanishing_start != -1:
        # Backtrack untuk menemukan opening div
        div_start = content.rfind('<div class="bg-gradient-to-r from-slate-900', 0, vanishing_start)
        if div_start != -1:
            # Cari penutupnya
            div_count = 0
            for i in range(div_start, len(content)):
                if content[i:i+4] == '<div':
                    div_count += 1
                elif content[i:i+6] == '</div>':
                    div_count -= 1
                    if div_count == 0:
                        components[2].append(content[div_start:i+6])
                        break
    
    # 6. Risk Matrix (Phase 3)
    matrix_start = content.find('<!-- 3. RISK MATRIX')
    if matrix_start != -1:
        # Cari sampai komponen berikutnya
        next_component = content.find('<!-- Risk Control Tower', matrix_start)
        if next_component != -1:
            components[3].append(content[matrix_start:next_component])
    
    # 7. Risk Control Tower (Phase 3)
    tower_start = content.find('<!-- Risk Control Tower')
    if tower_start != -1:
        next_component = content.find('<!-- Warning for Estate', tower_start)
        if next_component != -1:
            components[3].append(content[tower_start:next_component])
    
    # 8. Estate Warning (Phase 3)
    warning_start = content.find('<!-- Warning for Estate Scale')
    if warning_start != -1:
        # Cari sampai phase berikutnya atau script
        next_phase = content.find('<div id="phase-4"', warning_start)
        if next_phase == -1:
            next_phase = content.find('<!-- ISO 31000 PROTOCOLS', warning_start)
        if next_phase != -1:
            components[3].append(content[warning_start:next_phase])
    
    # 9. Treatment Protocols (Phase 4)
    protocols_start = content.find('<!-- ISO 31000 PROTOCOLS')
    if protocols_start != -1:
        # Cari sampai script atau phase berikutnya
        next_section = content.find('<script>', protocols_start)
        phase_5 = content.find('<div id="phase-5"', protocols_start)
        if phase_5 != -1 and phase_5 < next_section:
            next_section = phase_5
        if next_section != -1:
            components[4].append(content[protocols_start:next_section])
    
    # 10. Watchlist/Monitoring (Phase 5)
    # Cari komponen dengan badge phase-5
    watchlist_pattern = r'(<div[^>]*>\s*<span class="iso-badge iso-phase-5"[^>]*>.*?</div>)'
    for match in re.finditer(watchlist_pattern, content, re.DOTALL):
        components[5].append(match.group(1))
    
    return components

def rebuild_dashboard(content: str) -> str:
    """
    Rebuild dashboard dengan komponen yang sudah diorganisir
    """
    # Ekstrak bagian header (sampai tab-overview)
    header_end = content.find('<div id="tab-overview"')
    if header_end == -1:
        print("ERROR: Tidak dapat menemukan tab-overview container")
        return content
    
    header = content[:header_end]
    header += '<div id="tab-overview" class="max-w-7xl mx-auto space-y-6">\n'
    
    # Ekstrak komponen
    components = extract_components_by_badge(content)
    
    # Headers untuk setiap phase
    phase_headers = {
        1: '<div class="mb-8 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-black">1</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK IDENTIFICATION</h2><p class="text-xs text-slate-500 font-bold">Identifikasi Sumber & Sebaran Risiko</p></div></div>',
        2: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black">2</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK ANALYSIS</h2><p class="text-xs text-slate-500 font-bold">Analisis Dampak Finansial & Probabilitas</p></div></div>',
        3: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-amber-600 rounded-lg flex items-center justify-center text-white font-black">3</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK EVALUATION</h2><p class="text-xs text-slate-500 font-bold">Evaluasi Level Risiko & Prioritas</p></div></div>',
        4: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-black">4</div><div><h2 class="text-xl font-black text-slate-800 uppercase">RISK TREATMENT</h2><p class="text-xs text-slate-500 font-bold">Protokol Mitigasi & Pengendalian</p></div></div>',
        5: '<div class="mb-8 mt-12 p-4 bg-slate-100 rounded-xl border border-slate-200 flex items-center gap-4"><div class="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center text-white font-black">5</div><div><h2 class="text-xl font-black text-slate-800 uppercase">MONITORING & REVIEW</h2><p class="text-xs text-slate-500 font-bold">Pemantauan Berkelanjutan</p></div></div>'
    }
    
    # Build setiap phase
    new_body = header
    
    for phase_num in range(1, 6):
        hidden = "" if phase_num == 1 else " hidden"
        new_body += f'\n<div id="phase-{phase_num}" class="iso-phase-content{hidden}">\n'
        new_body += phase_headers[phase_num] + '\n'
        
        # Tambahkan semua komponen untuk phase ini
        for component in components[phase_num]:
            new_body += component + '\n'
        
        new_body += '</div>\n'
    
    new_body += '</div> <!-- End tab-overview -->\n'
    
    # Ekstrak scripts dari file asli
    script_start = content.find('<script>')
    if script_start != -1:
        scripts = content[script_start:]
        new_body += scripts
    
    return new_body

def main():
    print("Membaca file dashboard...")
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Mereorganisasi komponen berdasarkan badge ISO Phase...")
    new_content = rebuild_dashboard(content)
    
    print(f"Menulis hasil ke {FILE_OUTPUT}...")
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ SELESAI! Dashboard telah direorganisasi.")
    print(f"   File output: {FILE_OUTPUT}")
    print("\nSilakan review file output dan jika sudah OK, rename menjadi v10.html")

if __name__ == "__main__":
    main()
