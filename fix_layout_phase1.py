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
        print(f"Error: {FILE} not found")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original Size: {len(content)}")

    # 1. EXTRACT STATS WRAPPER FROM LEFT COL
    stats_start_str = '<div class="p-6 bg-slate-100 border-t-2 border-slate-200">'
    idx_stats_start = content.find(stats_start_str)
    
    if idx_stats_start == -1:
        print("Error: Could not find stats wrapper in Left Column")
        return # Safety abort

    idx_stats_end = get_end_of_div(content, idx_stats_start)
    if idx_stats_end == -1:
        print("Error: Could not parse stats wrapper end")
        return

    stats_html = content[idx_stats_start:idx_stats_end]
    print(f"Extracted Stats Block ({len(stats_html)} chars)")

    # 2. REMOVE STATS FROM LEFT (Clean Cut)
    # We remove the block from content. 
    # Be careful with string slicing.
    content_minus_stats = content[:idx_stats_start] + content[idx_stats_end:]

    # 3. LOCATE PROTOCOL BLOCK (RIGHT COL) & REPLACE
    proto_marker = '<!-- ISO 31000 PROTOCOLS (Replaces Right Map) -->'
    idx_proto_marker = content_minus_stats.find(proto_marker)
    
    if idx_proto_marker == -1:
        print("Error: Protocol marker not found")
        # Try finding simpler marker if comments drifted?
        # But we just generated it. Should be there.
        # Check if line breaks match.
        pass
    
    # Logic: From marker, find next <div which is the container start
    idx_proto_div_start = content_minus_stats.find('<div', idx_proto_marker)
    idx_proto_div_end = get_end_of_div(content_minus_stats, idx_proto_div_start)

    # 4. PREPARE NEW RIGHT CONTENT
    # User wants: Red/Orange/Yellow/Green stats + Analysis Text.
    # The extracted `stats_html` has exactly this.
    # We just need to re-style the wrapper to fit the Right Column aesthetics.
    # Old wrapper: p-6 bg-slate-100 border-t-2 ...
    # New wrapper: Let's use a nice card style.
    
    new_wrapper_class = 'class="bg-white rounded-3xl p-8 border-4 border-slate-100 h-full flex flex-col justify-center shadow-xl relative overflow-hidden"'
    
    # We allow the "Potensi Penyelamatan" rename here
    modified_stats_html = stats_html.replace(
        'class="p-6 bg-slate-100 border-t-2 border-slate-200"', 
        new_wrapper_class
    ).replace(
        'Rekomendasi Mitigasi:', 
        'Potensi Penyelamatan Aset:'
    )
    
    # Ensure badges or decorations?
    # Maybe add ISO 31000 badge for "1. IDENTIFICATION" here too? Or redundant?
    # Map already has it. This is part of Identification.
    # Let's add a decorative background to the Right Col stats.
    decor = '<div class="absolute top-0 right-0 w-64 h-64 bg-indigo-50 rounded-full blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>'
    
    # Inject decor inside the first div
    # find first >
    first_tag_close = modified_stats_html.find('>')
    modified_stats_html = modified_stats_html[:first_tag_close+1] + decor + modified_stats_html[first_tag_close+1:]

    # REPLACE PROTOCOL WITH STATS
    content_replaced = content_minus_stats[:idx_proto_marker] + \
                       '<!-- STATISTIK & ANALISIS SPASIAL (Right Col) -->\n' + \
                       modified_stats_html + \
                       content_minus_stats[idx_proto_div_end:]

    # 5. REMOVE HIDDEN OLD CONTENT
    # It might reside AFTER the extracted stats location in original file?
    # In `content_replaced`, we must find it.
    hidden_marker = '<!-- Hidden Old Content Wrapper -->'
    idx_hidden_start = content_replaced.find(hidden_marker)
    
    if idx_hidden_start != -1:
        # Find div start
        idx_hidden_div_start = content_replaced.find('<div', idx_hidden_start)
        idx_hidden_div_end = get_end_of_div(content_replaced, idx_hidden_div_start)
        
        content_final = content_replaced[:idx_hidden_start] + content_replaced[idx_hidden_div_end:]
        print("Removed Hidden Old Content")
    else:
        content_final = content_replaced
        print("Warning: Hidden Content not found (already clean?)")

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content_final)

    print("✅ Successfully updated Phase 1 Layout.")

if __name__ == "__main__":
    main()
