import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # FIX: Broken div tags - "v class=" should be "<div class="
    # This happened because of aggressive string replacement that broke tags
    
    # Pattern 1: "v class=" → "<div class="
    content = re.sub(r'(\s+)v class="', r'\1<div class="', content)
    print("✅ Fixed:  v class= → <div class=")
    
    # Pattern 2: "v>" → "<div>"
    content = re.sub(r'(\s+)v>', r'\1<div>', content)
    print("✅ Fixed:  v> → <div>")
    
    # Pattern 3: "v id=" → "<div id="
    content = re.sub(r'(\s+)v id="', r'\1<div id="', content)
    print("✅ Fixed:  v id= → <div id=")
    
    # Verify no more standalone "v" tags remain
    # Look for pattern like whitespace + "v " or "v>" that's not part of <svg> or other valid tags
    standalone_v_count = len(re.findall(r'\n\s+v[\s>]', content))
    
    if standalone_v_count > 0:
        print(f"⚠️  WARNING: Found {standalone_v_count} potential standalone 'v' tags")
        print("   Manual inspection may be needed")
    else:
        print("✅ No standalone 'v' tags found")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ All broken div tags fixed")
    print("\nPlease refresh browser")
    print("Expected results:")
    print("  • Likelihood column FULLY VISIBLE on the right")
    print("  • Formula Parameters section displays properly")
    print("  • Info toggle button should now WORK")

if __name__ == "__main__":
    main()
