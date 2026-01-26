import os

INPUT_FILE = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_v8_final.html'
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def extract_outer_div_after_marker(content, marker_text):
    marker_pos = content.find(marker_text)
    if marker_pos == -1:
        print(f"Warning: Marker not found: {marker_text[:50]}...")
        return ""
    
    # Find first <div after marker
    div_start = content.find('<div', marker_pos)
    if div_start == -1: 
        print(f"Warning: No div found after marker {marker_text[:30]}")
        return ""
    
    # Robust parsing using nesting count
    balance = 0
    started = False
    
    cursor = div_start
    while cursor < len(content):
        if content.startswith('<div', cursor):
            balance += 1
            started = True
            cursor += 4
        elif content.startswith('</div', cursor):
            balance -= 1
            cursor += 5
            if started and balance == 0:
                # Found the closing tag!
                end_tag_pos = content.find('>', cursor-1)
                # Return content including comments/marker if needed? 
                # Better return just the component div to be clean.
                # But we might want the comment/marker too for context.
                # Let's return from marker_pos to end_tag_pos
                return content[marker_pos : end_tag_pos+1]
        else:
            cursor += 1
            
    print(f"Warning: Unbalanced div for marker {marker_text[:30]}")
    return ""

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw = f.read()

    print(f"Read {len(raw)} bytes from {INPUT_FILE}")

    # 1. EXTRACT COMPONENTS
    # Peta (Indentification)
    comp_map = extract_outer_div_after_marker(raw, '<!-- SECTION PETA CINCIN API -->')
    
    # SPH (Indentification)
    comp_sph = extract_outer_div_after_marker(raw, '<!-- SPH & EFFICIENCY ANALYSIS SECTION (NEW) -->')
    
    # Simulator (Analysis)
    comp_sim = extract_outer_div_after_marker(raw, '<!-- Skenario Finansial Interaktif (What-If) -->')
    
    # Vanishing (Analysis)
    comp_vanish = extract_outer_div_after_marker(raw, 'VANISHING YIELD EXPLAINED (PENGGANTI SYMPTOM LAG)')
    
    # Left Financial (Analysis)
    comp_left_fin = extract_outer_div_after_marker(raw, '<!-- Left Financial (Blok A) -->')
    
    # Matrix (Evaluation)
    comp_matrix = extract_outer_div_after_marker(raw, '<!-- 3. RISK MATRIX (ISO 31000 Strategic View) -->')
    
    # Tower (Evaluation)
    comp_tower = extract_outer_div_after_marker(raw, '<!-- Risk Control Tower (Summary) -->')
    
    # Protocol (Treatment)
    comp_protocol = extract_outer_div_after_marker(raw, '<!-- ISO 31000 PROTOCOLS (Replaces Right Map) -->')

    # 2. EXTRACT HEADER & TAIL
    # Header: 0 to <div id="tab-overview"> start
    header_end = raw.find('<div id="tab-overview"')
    if header_end == -1:
        print("Error: Could not find tab-overview")
        return
        
    head_part = raw[:header_end]
    
    # Scripts logic start
    # We use "<!-- Dynamic Modal Overlay -->" as anchor for tail.
    # But wait, Vanishing Yield & SPH are AFTER the main blocks in v8.
    # We must ensure we don't accidentally cut them off if we just take "tail" from end of list.
    # Actually, the components are extracted, so we can reconstruct body.
    # The "tail" should be everything AFTER the dashboard grid closes.
    # In v8, SPH is the last visible block (Line 1134).
    # Then <script> starts around 1396.
    # So "Tail" is from script start.
    
    script_start_marker = "<!-- Dynamic Modal Overlay -->"
    script_start = raw.find(script_start_marker)
    if script_start == -1:
        print("Error: Could not find script start marker")
        return
        
    tail_part = raw[script_start:]

    # 3. CONSTRUCT NEW LAYOUT
    html = []
    html.append(head_part)
    
    # Open new container
    html.append('<div id="tab-overview" class="space-y-16 pb-24">') # Increased space
    
    # Helper for Section Title
    def make_title(num, title, subtitle, color_bg, color_text):
        return f'''
        <div class="relative border-t border-slate-200 pt-12 first:border-0 first:pt-0">
            <div class="flex items-center gap-6 mb-8">
                <div class="w-16 h-16 rounded-2xl {color_bg} text-white flex items-center justify-center font-black text-3xl shadow-lg shadow-{color_text}-500/30 transform -rotate-3">{num}</div>
                <div>
                    <h2 class="text-4xl font-black text-slate-800 uppercase tracking-tighter">{title}</h2>
                    <p class="text-slate-500 font-bold text-sm uppercase tracking-widest mt-1">{subtitle}</p>
                </div>
            </div>
            <div class="space-y-8">
        '''

    def close_section():
        return '</div></div>' # Close content space and section

    # PHASE 1: IDENTIFICATION (Map + SPH)
    html.append(make_title(1, "Risk Identification", "Deteksi Sumber Risiko & Vektor Penularan", "bg-indigo-600", "indigo"))
    html.append(comp_map)
    html.append(comp_sph)
    html.append(close_section())

    # PHASE 2: ANALYSIS (Simulator + Vanishing + Fin Panel)
    html.append(make_title(2, "Risk Analysis", "Analisis Dampak Finansial & Proyeksi Kerugian", "bg-blue-600", "blue"))
    html.append(comp_sim)
    html.append(comp_vanish)
    html.append(f'<div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">{comp_left_fin}</div>') # Wrapped in Grid mostly for width control
    html.append(close_section())

    # PHASE 3: EVALUATION (Matrix + Tower)
    html.append(make_title(3, "Risk Evaluation", "Evaluasi Prioritas & Matriks Keputusan", "bg-amber-500", "amber"))
    html.append('<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">') 
    html.append(comp_matrix)
    html.append(comp_tower)
    html.append('</div>')
    html.append(close_section())

    # PHASE 4: TREATMENT (Protocol)
    html.append(make_title(4, "Risk Treatment", "Mitigasi & Standar Protokol (SOP)", "bg-emerald-500", "emerald"))
    # Protocol needs full width or centered? It was in col-span-1 before but looks like a card.
    # Better put it full width or centered.
    html.append('<div class="max-w-4xl mx-auto">') 
    html.append(comp_protocol)
    html.append('</div>')
    html.append(close_section())

    # PHASE 5: MONITORING
    html.append(make_title(5, "Monitoring & Review", "Pemantauan Berkelanjutan", "bg-slate-600", "slate"))
    html.append('''
    <div class="bg-gradient-to-br from-slate-100 to-white p-10 rounded-3xl border border-slate-200 text-center shadow-sm">
        <h3 class="text-2xl font-black text-slate-800 uppercase mb-4">Cycle Monitoring</h3>
        <p class="text-slate-500 max-w-2xl mx-auto text-lg">
            Pemantauan dilakukan secara real-time melalui <strong class="text-indigo-600">Priority Watchlist</strong> (Lihat Fase 3) 
            dan <strong class="text-indigo-600">Update Data Drone Harian</strong>. 
            Setiap perubahan parameter Attack Rate > 2% akan memicu notifikasi ulang.
        </p>
    </div>
    ''')
    html.append(close_section())

    html.append('</div>') # Close tab-overview
    html.append(tail_part) # Scripts

    # WRITE
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print(f"✅ Success! Created {OUTPUT_FILE} with ISO 31000 Layout.")

if __name__ == "__main__":
    main()
