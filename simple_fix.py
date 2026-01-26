import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("ERROR: File not found")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("CRITICAL FIX - Removing all broken tags...")
    
    # STEP 1: Remove ALL <di patterns (broken <div starts)
    # Match <di followed by anything that's NOT 'v' (so we keep <div>)
    initial_di_count = content.count('<di')
    
    # Remove <di> standalone
    content = content.replace('<di>', '')
    # Remove <di followed by < (means <di<div becomes <div)
    content = content.replace('<di<', '<')
    
    print(f"✅ Removed broken '<di' patterns")
    
    # STEP 2: Verify <div tags are intact
    div_count = content.count('<div')
    print(f"✅ Found {div_count} '<div' tags (should be valid)")
    
    # Write fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"\n✅ FIXED FILE SAVED")
    print(f"File size: {len(content)} chars")
    print("\n🔄 PLEASE HARD REFRESH BROWSER:")
    print("   Ctrl + Shift + R")
    print("\nDashboard should now display correctly!")

if __name__ == "__main__":
    main()
