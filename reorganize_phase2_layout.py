import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find Phase 2 grid container
    # Look for the grid that contains Financial + Likelihood
    grid_marker = '<!-- Grid: Financial & Vanishing -->'
    idx_grid_comment = content.find(grid_marker)
    
    if idx_grid_comment == -1:
        print("⚠️  Grid marker not found, searching by alternative method...")
        # Search for grid cols pattern in Phase 2
        # After Financial Simulator, there should be a grid
        simulator_end = content.find('</div>\n\n<!-- Grid: Financial')
        if simulator_end == -1:
            print("ERROR: Cannot find grid structure")
            return
        idx_grid_comment = simulator_end + 7
    
    # Find the grid div opening after the comment
    idx_search_start = idx_grid_comment
    grid_pattern = r'<div class="grid grid-cols-1 lg:grid-cols-\d+ gap-8'
    match = re.search(grid_pattern, content[idx_search_start:idx_search_start+500])
    
    if not match:
        print("ERROR: Grid div not found")
        return
    
    idx_grid_div = idx_search_start + match.start()
    grid_opening = match.group()
    
    print(f"Found grid: {grid_opening}")
    
    # Change to 2 columns (if not already)
    new_grid = '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">'
    content = content[:idx_grid_div] + new_grid + content[idx_grid_div+len(grid_opening):]
    print("✅ Changed grid to 2 columns")
    
    # Now find Vanishing Yield component
    # Search for unique text in Vanishing Yield
    vanishing_text_markers = [
        'Silent Infection',
        'Root Degradation', 
        'Cryptic Collapse',
        'Insolvency'
    ]
    
    # Find where Vanishing Yield starts - look for its container
    # It should be inside a lg:col-span div
    idx_vanishing_start = -1
    
    # Search for the container that has all 4 phases
    for marker in vanishing_text_markers:
        idx_test = content.find(marker, idx_grid_div)
        if idx_test != -1:
            # Found a phase, now backtrack to find the container opening
            # Look backwards for '<div class="lg:col-span-'
            search_back = content[idx_grid_div:idx_test]
            col_span_pattern = r'<div class="lg:col-span-\d+ h-full">'
            matches = list(re.finditer(col_span_pattern, search_back))
            if matches:
                # Get the LAST match before the marker (closest parent)
                last_match = matches[-1]
                idx_vanishing_start = idx_grid_div + last_match.start()
                print(f"Found Vanishing container at position {idx_vanishing_start}")
                break
    
    if idx_vanishing_start == -1:
        print("ERROR: Cannot find Vanishing Yield container")
        return
    
    # Find the closing div for Vanishing container
    # Count div balance from start
    def find_matching_closing_div(text, start_pos):
        balance = 0
        i = start_pos
        while i < len(text):
            if text[i:i+4] == '<div':
                balance += 1
                # Skip to end of tag
                while i < len(text) and text[i] != '>':
                    i += 1
            elif text[i:i+6] == '</div>':
                balance -= 1
                if balance == 0:
                    return i + 6
                i += 6
                continue
            i += 1
        return -1
    
    idx_vanishing_end = find_matching_closing_div(content, idx_vanishing_start)
    
    if idx_vanishing_end == -1:
        print("ERROR: Cannot find Vanishing Yield closing div")
        return
    
    # Extract Vanishing Yield component
    vanishing_component = content[idx_vanishing_start:idx_vanishing_end]
    print(f"Extracted Vanishing component ({len(vanishing_component)} chars)")
    
    # Remove from current position
    content = content[:idx_vanishing_start] + content[idx_vanishing_end:]
    
    # Find the closing of the 2-column grid
    # After removing Vanishing, the grid should only have 2 items (Financial + Likelihood)
    # Find the grid closing </div>
    
    # Search for </div></div></div> pattern after grid (closes: grid items → grid → section)
    idx_after_removal = idx_vanishing_start
    grid_close_pattern = '</div>\n</div></div>'
    idx_grid_close = content.find(grid_close_pattern, idx_after_removal)
    
    if idx_grid_close == -1:
        # Try alternative pattern
        print("⚠️  Standard close pattern not found, trying alternative...")
        idx_grid_close = content.find('</div>\n\n        <div class="relative border-t', idx_after_removal)
    
    if idx_grid_close == -1:
        print("ERROR: Cannot find grid closing")
        return
    
    # Insert Vanishing AFTER grid, with full width wrapper
    vanishing_full_width = f'''

<!-- Vanishing Yield Analysis - Full Width Below -->
<div class="w-full">
    {vanishing_component}
</div>
'''
    
    # Remove the col-span class from vanishing component (make it full width)
    vanishing_full_width = vanishing_full_width.replace('class="lg:col-span-1 h-full"', 'class="w-full"')
    
    insert_pos = idx_grid_close + len(grid_close_pattern)
    content = content[:insert_pos] + vanishing_full_width + content[insert_pos:]
    
    print("✅ Moved Vanishing Yield to bottom (full width)")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Layout reorganization complete!")
    print("\nNew Phase 2 Structure:")
    print("  [Top] Financial Simulator (full width)")
    print("  [Middle] Grid 2 columns:")
    print("    - Left: Financial Impact Metrics")
    print("    - Right: Likelihood & Trend Analysis")
    print("  [Bottom] Vanishing Yield Analysis (full width)")
    print("\nPlease refresh browser to see new layout")

if __name__ == "__main__":
    main()
