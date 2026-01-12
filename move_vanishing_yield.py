import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def move_yield():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # IDENTIFY VANISHING YIELD BLOCK
    # It has text "VANISHING YIELD ANALYSIS" inside a H2
    # We find the parent div.
    # Pattern: <div class="bg-gradient-to-r ... VANISHING YIELD ... </div>
    
    # Let's locate uniqueness.
    # Start: <div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem]
    # End: </div> (Hopefully correctly matched)
    
    start_marker = '<div class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem]'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("Vanishing Yield Block not found!")
        return
        
    # Find matching closing div... tough without parser.
    # But usually it's just one block closing </div>
    # Let's verify context.
    
    # Is it inside Phase 2?
    p2_start = content.find('id="phase-2"')
    p3_start = content.find('id="phase-3"')
    
    if start_idx > p2_start and start_idx < p3_start:
        print("Vanishing Yield IS already inside Phase 2 boundary.")
        # Is it "orphaned" by an early closing div?
        # Check if there is a </div> between p2_start and start_idx?
        
        # Let's verify if there is a </div> immediately before it.
        pre_content = content[p2_start:start_idx]
        if pre_content.strip().endswith('</div>'):
             print("WARNING: Found a closing div right before Yield block! It's orphaned.")
             # REMOVE that closing div
             # We need to find the specific </div> index in global content
             # It is pre_content.rfind('</div>') + p2_start
             
             split_point = content.rfind('</div>', p2_start, start_idx)
             if split_point != -1:
                 print(f"Removing premature closing div at {split_point}")
                 # Remove </div> (6 chars)
                 new_content = content[:split_point] + content[split_point+6:]
                 
                 # Now we must add a closing div AFTER the Yield block to close P2 properly.
                 # Find Yield block end.
                 # Yield block starts at 'start_idx' (shifted by -6 now).
                 shift_start_idx = start_idx - 6
                 
                 # Where does Yield block end? It ends before <div id="phase-3"> (hopefully)
                 # Actually, let's just insert </div> right before <div id="phase-3">
                 
                 # But wait, we removed ONE </div>. We need to put ONE </div> back.
                 # Where? At the end of Phase 2.
                 # Phase 2 ends before Phase 3 starts.
                 
                 # So we find phase-3 start in new_content
                 new_p3_start = new_content.find('id="phase-3"')
                 # Insert </div> before the <div id="phase-3"> tag (which is usually on new line)
                 # Search backwards for <div id="phase-3"
                 div_p3_idx = new_content.rfind('<div' , 0, new_p3_start) 
                 
                 final_content = new_content[:div_p3_idx] + '\n</div>\n' + new_content[div_p3_idx:]
                 
                 with open(FILE, 'w', encoding='utf-8') as f:
                     f.write(final_content)
                 print("✅ FIXED: Removed premature close, added proper close after Yield.")
                 return

    print("Yield block seems fine or logic too complex to fix safely blindly.")

if __name__ == "__main__":
    move_yield()
