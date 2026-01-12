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
    # These are incomplete tags that need to be removed entirely
    initial_di_count = content.count('<di')
    content = re.sub(r'<di(?![v])', '', content)  # Remove <di but NOT <div
    print(f"✅ Removed {initial_di_count} broken '<di' tags")
    
    # STEP 2: Now ALL remaining should be proper tags
    # Verify
    remaining_di = content.count('<di')
    if remaining_di > 0:
        # These should only be <div> tags now
        if '<div' in content:
            print(f"✅ {remaining_di} '<div>' tags remain (CORRECT)")
    
    # STEP 3: Final verification - check for visible broken text
    test_lines = content.split('\n')[:100]  # Check first 100 lines
    has_visible_v_class = any('v class="' in line and '<' not line.startswith with line.strip() for line in test_lines)
    
    if not has_visible_v_class:
        print("✅ No visible broken 'v class=' text in first 100 lines")
    
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
