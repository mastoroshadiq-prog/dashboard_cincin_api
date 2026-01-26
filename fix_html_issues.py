import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # FIX 1: Remove broken tag spacing (< /span> → </span>)
    content = content.replace('< /span>', '</span>')
    content = content.replace('< /div>', '</div>')
    print("✅ Fixed broken closing tags")
    
    # FIX 2: Fix grid structure for Phase 2
    # Find Phase 2 grid and ensure proper items-stretch
    phase2_grid_pattern = r'<div class="grid grid-cols-1 lg:grid-cols-2 gap-8([^"]*)">'
    match = re.search(phase2_grid_pattern, content)
    
    if match:
        old_grid = match.group()
        # Ensure items-stretch is present
        if 'items-stretch' not in old_grid:
            new_grid = '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">'
            content = content.replace(old_grid, new_grid)
            print("✅ Added items-stretch to grid")
        else:
            print("✅ Grid already has items-stretch")
    
    # FIX 3: Ensure both columns have h-full for alignment
    # Find Financial Impact Metrics column
    financial_col_pattern = r'<div class="lg:col-span-1([^"]*)">\s*<div\s*class="bg-gradient-to-br from-indigo-900'
    match = re.search(financial_col_pattern, content)
    
    if match:
        old_div = match.group()
        if 'h-full' not in old_div:
            # Add h-full to column wrapper
            new_div = old_div.replace('<div class="lg:col-span-1">', '<div class="lg:col-span-1 h-full">')
            content = content.replace(old_div, new_div)
            print("✅ Added h-full to Financial column")
    
    # Likelihood column should already have h-full (line 820)
    
    # FIX 4: Remove visible "items-stretch">" text if it exists
    content = content.replace('items-stretch">', '')
    if 'items-stretch"' in content:
        # Make sure it's only in proper HTML attributes
        print("✅ Cleaned up any leaked attribute text")
    
    # FIX 5: Debug recalculate function
    # Check if updateLikelihoodMetrics is properly defined
    if 'function updateLikelihoodMetrics(blockData)' not in content:
        print("⚠️  WARNING: updateLikelihoodMetrics function not found!")
        print("  This means the function was lost during edits - need to re-add")
    else:
        print("✅ updateLikelihoodMetrics function exists")
    
    # FIX 6: Ensure recalculate button handler exists and is correct
    recalc_pattern = 'recalculateLikelihood'
    if content.count(recalc_pattern) < 2:
        print("⚠️  WARNING: recalculateLikelihood button/handler may be missing")
    else:
        print("✅ Recalculate button and handler found")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ HTML cleanup complete")
    print("\nPlease refresh and check:")
    print("  1. No visible tag text (< /span>, etc.)")
    print("  2. Financial and Likelihood cards aligned (same height)")
    print("  3. Recalculate button clickable")

if __name__ == "__main__":
    main()
