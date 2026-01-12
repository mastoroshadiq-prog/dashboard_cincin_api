import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def intelligent_move():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dictionary to store content per phase
    # But checking entire blocks is hard with regex.
    # Instead, let's identify known unique components by their Title/Unique Text and FORCE them into the right phase structure.

    # DEFINISI MAP (Komponen -> Phase ID Target)
    # Phase 1
    # - Peta Kluster
    # Phase 2
    # - Financial Simulator
    # - Estimasi Kerugian (Blok A)
    # - Likelihood & Trend
    # - Vanishing Yield Analysis
    # Phase 3
    # - Risk Matrix
    # - Risk Control Tower
    # - Warning for Estate Scale
    # Phase 4
    # - Treatment Protocols / Risk Treatment
    # Phase 5
    # - Watchlist / Monitoring

    # We will EXTRACT these blocks using find boundaries, remove them from original text, and re-assemble structure.
    # This is safer than regex replace.
    
    # 1. PETA
    # Start: <!-- SECTION PETA CINCIN API -->
    # End: Be careful. Before Phase 2 header.
    p1_start = content.find('<!-- SECTION PETA CINCIN API -->')
    p1_end = content.find('<div id="phase-2"') 
    if p1_end == -1: p1_end = content.find('<!-- Skenario Finansial') # Fail safe
    
    # Phase 2 Header check
    # We need to preserve the HEADER inside the Phase div.
    
    # Let's simplify. I will rebuild the layout string using the snippets found in the file.
    
    def extract_snippet(start_str, end_str):
        s = content.find(start_str)
        if s == -1: return ""
        e = content.find(end_str, s)
        if e == -1: return content[s:] # Until end?
        return content[s:e]

    # COMPONENT 1: MAP (P1)
    map_block = extract_snippet('<!-- SECTION PETA CINCIN API -->', '<div id="phase-2"')
    # Clean trailing divs if any from previous mess
    if map_block.strip().endswith('</div></div>'): map_block = map_block.split('<div id="phase-2"')[0] 
    
    # COMPONENT 2: ANALYSIS (P2)
    # Getting everything between Phase 2 Header and Phase 3 Header
    # Markers might be messed up, so look for unique content.
    
    # Financial Simulator
    fin_sim = extract_snippet('<!-- Skenario Finansial', '<!-- Left Financial') 
    
    # Financial Impact (Blok A)
    fin_imp = extract_snippet('<!-- Left Financial', '<!-- Skenario Finansial') # Wait order?
    # Actually Fin Sim is first usually.
    # Let's look for specific divs.
    
    # Try Regex for Blocks based on ISO Badge?
    # No, risky. 
    
    # Let's just create a new CLEAN structure based on the file content we have.
    # We strip all phase wrappers first.
    
    raw_body = content
    # Remove existing wrappers to avoid duplication
    raw_body = raw_body.replace('<div id="phase-1" class="iso-phase-content">', '')
    raw_body = raw_body.replace('<div id="phase-2" class="iso-phase-content hidden">', '')
    raw_body = raw_body.replace('<div id="phase-3" class="iso-phase-content hidden">', '')
    raw_body = raw_body.replace('<div id="phase-4" class="iso-phase-content hidden">', '')
    raw_body = raw_body.replace('<div id="phase-5" class="iso-phase-content hidden">', '')
    # Remove closing divs that were wrappers? Hard to know which ones.
    
    # OK, Plan B: Just ensure the HEADERS start the section.
    # We will inject the closing </div> BEFORE the next header starts.
    
    # 1. Find Header 2. Insert </div> before it.
    # Header 2: <h2 class="text-xl font-black text-slate-800 uppercase">RISK ANALYSIS</h2>
    # We need to find the DIV wrapping this header.
    # Pattern: <div class="mb-8 mt-12 ... >2</div>
    
    # We'll use the "Header Signature" to split.
    sigs = [
        '<div class="w-10 h-10 bg-indigo-600 rounded-lg', # 1
        '<div class="w-10 h-10 bg-blue-600 rounded-lg',   # 2
        '<div class="w-10 h-10 bg-amber-600 rounded-lg',  # 3
        '<div class="w-10 h-10 bg-emerald-600 rounded-lg',# 4
        '<div class="w-10 h-10 bg-slate-600 rounded-lg'   # 5
    ]
    
    # Find positions
    pos = []
    for s in sigs:
        p = content.find(s)
        # Scan back to find start of that container <div class="mb-8...
        if p != -1:
            start_div = content.rfind('<div', 0, p)
            pos.append(start_div)
        else:
            pos.append(-1)
            
    # Now we have split points.
    # Phase 1 is from pos[0] to pos[1]
    # Phase 2 is from pos[1] to pos[2]
    # ...
    
    # But we need to handle the "End of Phase 5".
    # It ends before "</div> <!-- End Overview -->"
    end_overview = content.find('<!-- End Overview -->')
    if end_overview != -1:
        # Backtrack to closing div
        end_pos = content.rfind('</div>', 0, end_overview)
        pos.append(end_pos)
    else:
        pos.append(content.find('</body>'))

    # Reconstruct
    new_content = content[:pos[0]] # Header stuff
    
    for i in range(5):
        if pos[i] == -1: continue # Skip missing phases?
        
        start = pos[i]
        end = pos[i+1] if i+1 < len(pos) else -1
        
        if end == -1: continue
        
        # Extract chunk
        # Note: The chunk currently contains MISMATCHED closing divs from previous attempts.
        # We should STRIP the wrapper divs if they exist in the chunk?
        # Or just Wrap blindly and assume browser fixes it? NO.
        
        chunk = content[start:end]
        
        # Clean the chunk of "orphan" </div> tags at the very end if they were the old wrapper closers?
        chunk = chunk.strip()
        
        # Remove old phase IDs references inside headers? No, headers don't have IDs.
        
        # WRAP
        phase_id = f"phase-{i+1}"
        hidden = " hidden" if i > 0 else ""
        
        # We need to be careful not to introduce double wrappers if I already wrapped them?
        # The file currently HAS wrappers. I should verify if pos[i] point TO THE WRAPPER or THE HEADER.
        
        # Current file: <div id="phase-1" ...> \n <div class="mb-8 ... header ...">
        # So pos[i] found the HEADER div. The WRAPPER div is before it.
        
        # Let's find the wrapper based on ID.
        wrapper_start = content.find(f'id="phase-{i+1}"')
        
        # If wrapper exists, we trust it?
        # User says components are MIXED.
        # This implies standard flow is broken.
        
        pass

    # Actually, simpler logic:
    # Just look for the BADGE in the blocks.
    # If a block has "iso-phase-2" badge but is between Header 1 and Header 2... wait...
    # That shouldn't happen if rebuilding was correct.
    
    # Let's assume the user wants stricter isolation.
    # I will verify headers order.
    
    print("Verifying Headers Order...")
    indices = [content.find(s) for s in sigs]
    sorted_indices = sorted([x for x in indices if x != -1])
    
    if indices != sorted_indices:
        print("CRITICAL: Headers are out of order! This explains mixing.")
        # If out of order, we must resort blocks.
        # But `rebuild_v10_clean.py` wrote them in order.
        return
    
    print("Headers are in correct order.")
    
if __name__ == "__main__":
    intelligent_move()
