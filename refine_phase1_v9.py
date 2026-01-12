import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Read {len(content)} chars.")
    
    # 1. UPDATE SPH TITLE & SUBTITLE
    old_sph_title = 'Analisis Kerapatan (SPH)'
    new_sph_title = 'Identifikasi Densitas & Vektor (SPH)'
    
    old_sph_sub = 'The "Density Paradox": Hubungan SPH, Attack Rate & Efisiensi Biaya'
    new_sph_sub = 'Identifikasi Sumber Risiko: Densitas Tinggi Sebagai Vektor Penularan Utama'
    
    if old_sph_title in content:
        content = content.replace(old_sph_title, new_sph_title)
        print("Updated SPH Title")
    else:
        print("Warning: SPH Title not found")
        
    if old_sph_sub in content:
        content = content.replace(old_sph_sub, new_sph_sub)
        print("Updated SPH Subtitle")

    # 2. INJECT STATS HEADER (ASSET RISK PROFILE)
    # Target: The grid stats inside the newly moved right column
    target_grid = '<div class="grid grid-cols-2 gap-3 mb-4">'
    
    count_grid = content.count(target_grid)
    print(f"Found {count_grid} occurrences of stats grid.")
    
    header_html = '''
    <div class="mb-6 border-b border-indigo-50 pb-4 relative z-10">
        <div class="flex items-center justify-between">
             <div>
                <h3 class="text-2xl font-black text-slate-800 uppercase tracking-tighter">Asset Risk Profile</h3>
                <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Status Kesehatan Blok A</p>
             </div>
             <div class="bg-indigo-50 p-2 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
             </div>
        </div>
    </div>
    '''
    
    # We want to keep the original grid div but add header BEFORE it.
    # And maybe make grid relative z-10.
    new_grid_div = '<div class="grid grid-cols-2 gap-3 mb-4 relative z-10">'
    
    if count_grid == 1:
        content = content.replace(target_grid, header_html + '\n' + new_grid_div)
        print("Injected Stats Header")
    else:
        # Fallback: Determine which one is the Phase 1 stats.
        # It is the one inside the wrapper we created: 'class="bg-white rounded-3xl p-8 border-4 border-slate-100'
        # Let's search relative to that wrapper.
        wrapper_frag = 'class="bg-white rounded-3xl p-8 border-4 border-slate-100'
        idx_wrapper = content.find(wrapper_frag)
        if idx_wrapper != -1:
            # Search grid after wrapper
            idx_grid = content.find(target_grid, idx_wrapper)
            if idx_grid != -1:
                pre = content[:idx_grid]
                post = content[idx_grid + len(target_grid):]
                content = pre + header_html + '\n' + new_grid_div + post
                print("Injected Stats Header (Targeted)")
            else:
                print("Error: Grid not found inside wrapper")
        else:
            print("Error: Wrapper not found")

    # 3. RENAME ANALISIS SPASIAL
    old_spatial = '>Analisis Spasial:</p>'
    new_spatial = '>Identifikasi Pola Sebaran:</p>'
    
    if old_spatial in content:
        content = content.replace(old_spatial, new_spatial)
        print("Renamed Analisis Spasial")
    else:
        print("Warning: Analisis Spasial label not found")

    # WRITE
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Phase 1 Refinement Complete.")

if __name__ == "__main__":
    main()
