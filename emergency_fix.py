import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'
BACKUP = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9_BACKUP_EMERGENCY.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create emergency backup
    with open(BACKUP, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Emergency backup created: {BACKUP}")
    
    # COMPREHENSIVE FIX for all broken tags
    
    # Fix ALL forms of broken div tags
    fixes_applied = []
    
    # Pattern 1: Standalone "v class=" at line start with indentation
    if 'v class="' in content:
        content = re.sub(r'([\n\r]\s*)v\s+class="', r'\1<div class="', content)
        fixes_applied.append("v class= → <div class=")
    
    # Pattern 2: Standalone "v>" 
    if re.search(r'([\n\r]\s*)v\s*>', content):
        content = re.sub(r'([\n\r]\s*)v\s*>', r'\1<div>', content)
        fixes_applied.append("v> → <div>")
    
    # Pattern 3: "v id="
    if 'v id="' in content:
        content = re.sub(r'([\n\r]\s*)v\s+id="', r'\1<div id="', content)
        fixes_applied.append("v id= → <div id=")
    
    # Check if there are still standalone v tags that are NOT in valid contexts
    # Valid: <svg>, viewBox, stroke, etc.
    # Invalid: line starting with whitespace + "v " + attribute
    
    test_pattern = r'^\s+v\s+[a-z]+='
    remaining_issues = re.findall(test_pattern, content, re.MULTILINE)
    
    if remaining_issues:
        print(f"⚠️  WARNING: {len(remaining_issues)} potential issues remain:")
        for issue in remaining_issues[:5]:  # Show first 5
            print(f"  - {repr(issue)}")
    
    # Write fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"\n✅ Applied {len(fixes_applied)} fixes:")
    for fix in fixes_applied:
        print(f"  • {fix}")
    
    print("\n⚠️  IMPORTANT:")
    print(f"  • Backup saved to: {BACKUP}")
    print("  • Please HARD REFRESH browser (Ctrl + Shift + R)")
    print("  • If still broken, we should restore from v8_final and start clean")

if __name__ == "__main__":
    main()
