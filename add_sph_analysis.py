#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk menambahkan Analisis Kerapatan SPH di container Estimasi Kerugian
"""

import re

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_WITH_SPH.html'

# Komponen Analisis SPH yang akan ditambahkan
SPH_ANALYSIS_COMPONENT = '''
                <!-- SPH DENSITY ANALYSIS -->
                <div class="mt-6 pt-6 border-t border-indigo-500/20 relative z-10">
                    <div class="mb-4">
                        <h4 class="text-indigo-200 text-xs font-black uppercase tracking-wider mb-2 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-indigo-400">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                                <line x1="12" y1="22.08" x2="12" y2="12"/>
                            </svg>
                            Analisis Kerapatan (SPH)
                        </h4>
                    </div>
                    
                    <!-- SPH Stats Grid -->
                    <div class="grid grid-cols-2 gap-3 mb-4">
                        <!-- Current SPH -->
                        <div class="bg-black/30 p-3 rounded-xl border border-indigo-500/20">
                            <span class="text-[9px] font-bold text-indigo-200/60 uppercase block mb-1">SPH Aktual</span>
                            <div class="flex items-baseline gap-1">
                                <span class="text-3xl font-black text-white" id="sphActualLeft">--</span>
                                <span class="text-xs text-slate-400">pohon/ha</span>
                            </div>
                        </div>
                        
                        <!-- Standard SPH -->
                        <div class="bg-black/30 p-3 rounded-xl border border-indigo-500/20">
                            <span class="text-[9px] font-bold text-indigo-200/60 uppercase block mb-1">SPH Standar</span>
                            <div class="flex items-baseline gap-1">
                                <span class="text-3xl font-black text-emerald-400" id="sphStandardLeft">136</span>
                                <span class="text-xs text-slate-400">pohon/ha</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- SPH Status Bar -->
                    <div class="bg-black/30 p-4 rounded-xl border border-indigo-500/20">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-[9px] font-bold text-indigo-200/60 uppercase">Status Kerapatan</span>
                            <span class="text-xs font-black" id="sphStatusTextLeft">--</span>
                        </div>
                        
                        <!-- Progress Bar -->
                        <div class="relative h-3 bg-slate-800 rounded-full overflow-hidden">
                            <div id="sphProgressLeft" class="h-full transition-all duration-500 rounded-full" style="width: 0%"></div>
                        </div>
                        
                        <!-- Markers -->
                        <div class="flex justify-between mt-1 text-[8px] text-slate-500">
                            <span>Kritis (&lt;100)</span>
                            <span>Optimal (130-140)</span>
                        </div>
                    </div>
                    
                    <!-- SPH Impact Analysis -->
                    <div class="mt-3 p-3 bg-indigo-950/50 rounded-lg border border-indigo-500/10">
                        <div class="flex items-start gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-indigo-400 mt-0.5 shrink-0">
                                <circle cx="12" cy="12" r="10"/>
                                <path d="M12 16v-4"/>
                                <path d="M12 8h.01"/>
                            </svg>
                            <p class="text-[10px] text-indigo-200 leading-relaxed" id="sphImpactLeft">
                                Memuat analisis dampak kerapatan...
                            </p>
                        </div>
                    </div>
                </div>
'''

def add_sph_analysis():
    print("Membaca file dashboard...")
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cari lokasi untuk insert SPH analysis
    # Kita akan insert setelah footer stats grid (setelah Col 3: Mitigasi & Status)
    # Pattern: cari penutup dari grid grid-cols-3 yang berisi Mitigasi & Status
    
    # Cari marker yang unik: "Status Indikasi" untuk panel kiri
    marker_pattern = r'(<div id="finSymptomLagLeft"[^>]*>[^<]*--[^<]*</div>\s*</div>\s*</div>\s*</div>)'
    
    matches = list(re.finditer(marker_pattern, content, re.DOTALL))
    
    if not matches:
        print("ERROR: Tidak dapat menemukan lokasi untuk insert SPH analysis")
        return
    
    print(f"Ditemukan {len(matches)} lokasi potensial")
    
    # Ambil match pertama (untuk panel kiri)
    insert_pos = matches[0].end()
    
    # Insert SPH analysis component
    new_content = content[:insert_pos] + '\n' + SPH_ANALYSIS_COMPONENT + '\n' + content[insert_pos:]
    
    # Tulis ke file output
    print(f"Menulis ke {FILE_OUTPUT}...")
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ SELESAI!")
    print("\nKomponen Analisis SPH telah ditambahkan ke container Estimasi Kerugian (Blok A)")
    print("\nCatatan:")
    print("- Komponen akan menampilkan SPH Aktual vs SPH Standar")
    print("- Progress bar menunjukkan status kerapatan")
    print("- Analisis dampak kerapatan ditampilkan di bagian bawah")
    print("\nAnda perlu menambahkan JavaScript untuk update data SPH secara dinamis")

if __name__ == "__main__":
    add_sph_analysis()
