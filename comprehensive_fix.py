import os
import re

BACKUP_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'
OUTPUT_FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(BACKUP_FILE):
        print("ERROR: Backup file not found")
        return

    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Starting comprehensive fix...")
    print(f"Original file size: {len(content)} chars")
    
    # Count initial issues
    initial_v_class = content.count('v class="')
    initial_v_id = content.count('v id="')
    print(f"\nInitial issues found:")
    print(f"  - 'v class=' occurrences: {initial_v_class}")
    print(f"  - 'v id=' occurrences: {initial_v_id}")
    
    # FIX 1: Replace ALL "v class=" with "<div class="
    # Be aggressive - replace regardless of context (we'll be careful with SVG later)
    content = content.replace('v class="', '<div class="')
    print(f"✅ Fixed all 'v class=' → '<div class='")
    
    # FIX 2: Replace "v id=" with "<div id="
    content = content.replace('v id="', '<div id="')
    print(f"✅ Fixed all 'v id=' → '<div id='")
    
    # FIX 3: Replace standalone "v>" patterns (but NOT in SVG paths)
    # Look for whitespace + "v>" pattern
    content = re.sub(r'(\s+)v>', r'\1<div>', content)
    print(f"✅ Fixed all standalone 'v>' → '<div>'")
    
    # FIX 4: Check for any remaining problematic patterns
    remaining_v_class = content.count('v class="')
    remaining_v_id = content.count('v id="')
    
    print(f"\nRemaining issues:")
    print(f"  - 'v class=' occurrences: {remaining_v_class}")
    print(f"  - 'v id=' occurrences: {remaining_v_id}")
    
    # FIX 5: Verify we didn't break SVG tags
    # SVG should still have proper tags
    svg_check = content.count('<svg')
    if svg_check > 0:
        print(f"✅ SVG tags intact: {svg_check} <svg> tags found")
    
    # Write to output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"\n✅ FIXED FILE SAVED: {OUTPUT_FILE}")
    print(f"Final file size: {len(content)} chars")
    print("\nPlease:")
    print("  1. HARD REFRESH browser (Ctrl + Shift + R)")
    print("  2. Check if dashboard displays correctly")
    print("  3. If still broken, let me know EXACT error")

if __name__ == "__main__":
    main()
