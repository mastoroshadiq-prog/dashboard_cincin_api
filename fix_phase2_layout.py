import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def get_end_of_div(full, start_idx):
    balance = 0
    p = start_idx
    while p < len(full):
        if full.startswith('<div', p):
            balance += 1
            p += 4
        elif full.startswith('</div', p):
            balance -= 1
            p += 5
            if balance == 0:
                return full.find('>', p-1) + 1
        else:
            p += 1
    return -1

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CLEAN GARBAGE
    garbage = "VANISHING YIELD EXPLAINED (PENGGANTI SYMPTOM LAG)"
    if garbage in content:
        content = content.replace(garbage, "")
        print("Removed garbage text.")

    # Remove lingering comments artifacts like '================'
    # Use simple replace for known artifacts
    # The artifact appears around line 887: "========================================================================= -->"
    # Let's clean it defensively
    content = content.replace("========================================================================= -->", "")


    # 2. EXTRACT COMPONENTS
    # Simulator
    sim_marker = '<!-- Skenario Finansial Interaktif (What-If) -->'
    idx_sim_start = content.find(sim_marker)
    if idx_sim_start == -1: 
        print("Sim marker not found")
        return
        
    idx_sim_div_start = content.find('<div', idx_sim_start)
    idx_sim_end = get_end_of_div(content, idx_sim_div_start)
    sim_html = content[idx_sim_start:idx_sim_end]

    # Vanishing Yield
    # Marker class: "bg-gradient-to-r from-slate-900 to-slate-950"
    # Find div with this class
    vanish_class = 'bg-gradient-to-r from-slate-900 to-slate-950'
    idx_vanish_class = content.find(vanish_class)
    if idx_vanish_class == -1:
        print("Vanishing yield not found")
        return
        
    # Backtrack to <div
    idx_vanish_div_start = content.rfind('<div', 0, idx_vanish_class)
    idx_vanish_end = get_end_of_div(content, idx_vanish_div_start)
    vanish_html = content[idx_vanish_div_start:idx_vanish_end]
    
    # Financial Metrics
    fin_marker = '<!-- Left Financial (Blok A) -->'
    idx_fin_start = content.find(fin_marker)
    if idx_fin_start == -1:
         print("Left Fin not found")
         return
    
    idx_fin_div_start = content.find('<div', idx_fin_start)
    idx_fin_end = get_end_of_div(content, idx_fin_div_start)
    fin_html = content[idx_fin_start:idx_fin_end]

    # 3. LOCATE TARGET CONTAINER (PHASE 2)
    # Search for "Risk Analysis" header
    h2_str = '>Risk Analysis</h2>'
    idx_h2 = content.find(h2_str)
    if idx_h2 == -1:
        print("Phase 2 Header not found")
        return
        
    # Find <div class="space-y-8"> following it
    space_marker = '<div class="space-y-8">'
    idx_container_start = content.find(space_marker, idx_h2)
    idx_container_end = get_end_of_div(content, idx_container_start)
    
    # 4. REBUILD CONTENT
    # Make Vanishing Yield h-full to match Financial height in grid
    if 'h-full' not in vanish_html:
        vanish_html = vanish_html.replace('rounded-[3rem]', 'rounded-[3rem] h-full flex flex-col justify-center')

    new_content = []
    # Simulator Top
    new_content.append(sim_html)
    
    # Grid Bottom
    new_content.append('\n<!-- Grid: Financial & Vanishing -->')
    new_content.append('<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">')
    
    # Col 1: Financial (1/3)
    new_content.append(f'<div class="lg:col-span-1 h-full">{fin_html}</div>')
    
    # Col 2: Vanishing (2/3)
    new_content.append(f'<div class="lg:col-span-2 h-full">{vanish_html}</div>')
    
    new_content.append('</div>') # End Grid
    
    final_html = '<div class="space-y-8">\n' + '\n'.join(new_content) + '\n</div>'
    
    # 5. REPLACE
    # Safe Replace: Cut out the old container content and insert new
    full_new_content = content[:idx_container_start] + final_html + content[idx_container_end:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(full_new_content)
        
    print("✅ Phase 2 Layout Fixed: Simulator Top, Split Bottom.")

if __name__ == "__main__":
    main()
