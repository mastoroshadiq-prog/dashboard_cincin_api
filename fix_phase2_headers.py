import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # PROBLEM: Line 758-761 has "Financial Impact Metrics" header INSIDE Vanishing Yield container
    # This is WRONG. We need to REMOVE it.
    
    # Target: The wrongly injected header block
    wrong_header = '''
            <div class="border-b border-indigo-500/30 pb-4 mb-6">
                <h3 class="text-xl font-black text-white uppercase tracking-tight">Financial Impact Metrics</h3>
                <p class="text-[10px] text-indigo-300 font-bold uppercase tracking-widest">Estimasi Kerugian & Budgeting</p>
            </div>
            '''
    
    if wrong_header.strip() in content:
        content = content.replace(wrong_header, '')
        print("✅ Removed wrong 'Financial Impact Metrics' header from Vanishing Yield panel")
    else:
        print("⚠️  Warning: Could not find exact wrong header match. Trying alternative...")
        # Try removing with different whitespace
        alt_target = '''<div class="border-b border-indigo-500/30 pb-4 mb-6">
                <h3 class="text-xl font-black text-white uppercase tracking-tight">Financial Impact Metrics</h3>
                <p class="text-[10px] text-indigo-300 font-bold uppercase tracking-widest">Estimasi Kerugian & Budgeting</p>
            </div>'''
        
        if alt_target in content:
            content = content.replace(alt_target, '')
            print("✅ Removed wrong header (alternative match)")

    # Now inject CORRECT header for Vanishing Yield Analysis
    # Find the Vanishing Yield H2 title
    vanish_title_marker = '<h2 class="text-4xl font-black text-white tracking-tighter uppercase mb-2">'
    vanish_h2_full = '''<h2 class="text-4xl font-black text-white tracking-tighter uppercase mb-2">
                                VANISHING YIELD
                            </h2>'''
    
    # We want to add a proper section header BEFORE the existing H2
    # But first, let's check if there's already a proper structure
    
    if 'VANISHING YIELD ANALYSIS' not in content:
        # Replace "VANISHING YIELD" with "VANISHING YIELD ANALYSIS"
        content = content.replace('>VANISHING YIELD<', '>VANISHING YIELD ANALYSIS<')
        print("✅ Updated Vanishing Yield title to 'VANISHING YIELD ANALYSIS'")

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Phase 2 headers fixed successfully.")

if __name__ == "__main__":
    main()
