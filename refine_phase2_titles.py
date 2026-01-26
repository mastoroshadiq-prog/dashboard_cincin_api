import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. RENAME "Financial Exposure" COMPONENT to "Financial Impact Metrics"
    # Locate the unique text "Total Potensi Loss (Est)" which is the first item in that card.
    unique_metric_label = 'Total Potensi Loss (Est)</p>'
    
    # We want to inject a Header BEFORE this label's parent div or just before it.
    # The structure is simple text inside the card. We want to add a proper Section Header inside the card.
    
    header_html = '''
    <div class="border-b border-indigo-500/30 pb-4 mb-6">
        <h3 class="text-xl font-black text-white uppercase tracking-tight">Financial Impact Metrics</h3>
        <p class="text-[10px] text-indigo-300 font-bold uppercase tracking-widest">Estimasi Kerugian & Budgeting</p>
    </div>
    '''
    
    # We look for the Start of the Inner Content for "Left Financial"
    # It starts with: <div class="bg-gradient-to-br from-indigo-900 to-slate-900 ...">
    # Then some Badge / Decor divs.
    # Then <div class="relative z-10"> (Likely wrapper for content)
    # Then <div class="absolute ..."> (Decor) -> No.
    
    # Let's search for the "Total Potensi Loss" line and prepend the header to its container.
    # The line is: <p class="text-indigo-300 font-bold mb-1 uppercase tracking-widest text-xs">Total Potensi Loss (Est)</p>
    
    target_str = '<p class="text-indigo-300 font-bold mb-1 uppercase tracking-widest text-xs">Total Potensi Loss (Est)</p>'
    
    if target_str in content:
        # Check if already injected
        if 'Financial Impact Metrics' not in content:
            content = content.replace(target_str, header_html + '\n' + target_str)
            print("Injected 'Financial Impact Metrics' Header")
        else:
            print("Header 'Financial Impact Metrics' might already exist.")
            
    else:
        print("Warning: Could not locate 'Total Potensi Loss' label.")

    # 2. UPDATE "Vanishing Yield" CARD TITLE
    # Current Title: <h3 class="font-bold text-slate-700 mb-2">The "Silent Killer" Effect</h3>
    # User wants: "Vanishing Yield Analysis"
    # We can keep "Silent Killer" as subtitle/description.
    
    old_vanish_title = '<h3 class="font-bold text-slate-700 mb-2">The "Silent Killer" Effect</h3>'
    new_vanish_header = '''
    <div class="mb-4 border-b border-slate-200 pb-2">
        <h3 class="text-2xl font-black text-slate-800 uppercase tracking-tighter">Vanishing Yield Analysis</h3>
        <p class="text-slate-500 text-xs font-bold uppercase tracking-widest">The "Silent Killer" Effect</p>
    </div>
    '''
    
    if old_vanish_title in content:
        # We replace the old H3 with our new Header Block.
        # But wait, the H3 is inside the card content immediately.
        content = content.replace(old_vanish_title, new_vanish_header)
        print("Updated Vanishing Yield Title")
    else:
        print("Warning: Vanishing Yield H3 not found")

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Phase 2 Titles Refined.")

if __name__ == "__main__":
    main()
