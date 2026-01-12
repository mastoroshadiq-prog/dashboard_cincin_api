import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def audit_phases():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define Phases Containers using Regex
    # We look for <div id="phase-X" ...> until the next <div id="phase-Y"
    
    # Split content by phase IDs
    # Phase 1
    p1_start = content.find('id="phase-1"')
    p2_start = content.find('id="phase-2"')
    p3_start = content.find('id="phase-3"')
    p4_start = content.find('id="phase-4"')
    p5_start = content.find('id="phase-5"')
    
    phases = [
        (1, p1_start, p2_start),
        (2, p2_start, p3_start),
        (3, p3_start, p4_start),
        (4, p4_start, p5_start),
        (5, p5_start, len(content)) # Until end
    ]
    
    print("--- BADGE AUDIT REPORT ---")
    
    for p_num, start, end in phases:
        if start == -1:
            print(f"Phase {p_num} Container: MISSING!")
            continue
            
        block = content[start:end]
        
        # Find all badges in this block
        # Pattern: iso-phase-(\d)
        badges = re.findall(r'iso-phase-(\d)', block)
        
        # Filter expected vs unexpected
        expected = str(p_num)
        unexpected = [b for b in badges if b != expected]
        
        if unexpected:
            print(f"⚠️  [PHASE {p_num}] CONTAINS WRONG COMPONENTS!")
            print(f"    Found Badges for Pillars: {set(unexpected)}")
            # Advanced: Find semantic pointers (Titles/Keywords) to identify WHAT component it is
            if '2' in unexpected:
                if 'Financial' in block: print("    -> Detected 'Financial' component leaking here.")
                if 'Likelihood' in block: print("    -> Detected 'Likelihood' component leaking here.")
        else:
            print(f"✅ [PHASE {p_num}] CLEAN. (Contains {len(badges)} correct items)")

if __name__ == "__main__":
    audit_phases()
