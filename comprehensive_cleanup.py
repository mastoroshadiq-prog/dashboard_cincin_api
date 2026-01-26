import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("ERROR: File not found")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("COMPREHENSIVE CLEANUP...")
    
    # Count issues
    di_count = content.count('<di')
    print(f"Found {di_count} '<di' patterns")
    
    # AGGRESSIVE FIX - Remove ALL <di patterns
    # Pattern 1: <di><div becomes <div
    content = content.replace('<di><div', '<div')
    print("✅ Fixed <di><div → <div")
    
    # Pattern 2: <di>< becomes just <
    content = content.replace('<di><', '<')
    print("✅ Fixed <di>< → <")
    
    # Pattern 3: Standalone <di> (shouldn't exist but just in case)
    content = content.replace('<di>', '')
    print("✅ Removed standalone <di>")
    
    # Pattern 4: <di followed by space or newline
    content = re.sub(r'<di\s', '', content)
    print("✅ Removed <di with whitespace")
    
    # Verify no more <di
    remaining_di = content.count('<di')
    
    # But we should still have <div> tags
    div_count = content.count('<div')
    
    print(f"\nResults:")
    print(f"  <di patterns remaining: {remaining_di} (should be 0)")
    print(f"  <div tags found: {div_count} (should be >0)")
    
    # Write
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ FILE CLEANED AND SAVED")
    print("\n🔄 HARD REFRESH BROWSER: Ctrl + Shift + R")
    print("\nDashboard should now be CLEAN - no visible 'v class=' text!")

if __name__ == "__main__":
    main()
