import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. INJECT TITLE: "Financial Impact Metrics" (Left Financial Panel)
    # Target Wrapper: bg-gradient-to-br from-indigo-900 to-slate-900
    wrapper_marker = 'from-indigo-900 to-slate-900'
    idx_wrapper = content.find(wrapper_marker)
    
    if idx_wrapper != -1:
        # Find the content container <div class="relative z-10"> within this wrapper
        z10_marker = '<div class="relative z-10">'
        idx_z10 = content.find(z10_marker, idx_wrapper)
        
        if idx_z10 != -1:
            header_html = '''
            <div class="border-b border-indigo-500/30 pb-4 mb-6">
                <h3 class="text-xl font-black text-white uppercase tracking-tight">Financial Impact Metrics</h3>
                <p class="text-[10px] text-indigo-300 font-bold uppercase tracking-widest">Estimasi Kerugian & Budgeting</p>
            </div>
            '''
            
            # We insert it right after the opening tag
            insert_pos = idx_z10 + len(z10_marker)
            
            # Safety check: avoid double injection
            nearby_content = content[insert_pos:insert_pos+200]
            if 'Financial Impact Metrics' not in nearby_content:
                content = content[:insert_pos] + '\n' + header_html + content[insert_pos:]
                print("Injected Financial Impact Metrics Header")
            else:
                print("Header already present.")
        else:
            print("Error: Inner content div (z-10) not found in Left Fin.")
    else:
        print("Error: Left Financial wrapper not found.")

    # 2. RENAME "VANISHING YIELD" -> "VANISHING YIELD ANALYSIS"
    # Target: The H2 text
    # Use exact match case sensitive just to be safe it's the title
    if 'VANISHING YIELD' in content:
        # Replace only the title occurrence which is likely uppercase in H2
        # But global replace is fine if consistent
        content = content.replace('>VANISHING YIELD<', '>VANISHING YIELD ANALYSIS<')
        content = content.replace('>VANISHING YIELD\n', '>VANISHING YIELD ANALYSIS\n') # Handle newline
        print("Updated Vanishing Yield Title")

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Phase 2 Refinement Complete.")

if __name__ == "__main__":
    main()
