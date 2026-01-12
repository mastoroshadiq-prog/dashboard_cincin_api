import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    # Read as BINARY
    with open(FILE, 'rb') as f:
        content = f.read()

    print("CORRECT PATTERN FIX...")
    
    # Count initial
    initial_count = content.count(b'<di')
    print(f"Initial <di patterns: {initial_count}")
    
    # FIX: Use regex to match <di><div (with any character after div)
    # Replace <di><div with just <div
    content = re.sub(b'<di><div', b'<div', content)
    print("✅ Fixed <di><div → <div")
    
    # Also fix <di><d (incomplete div tags)
    content = content.replace(b'<di><d', b'<d')
    
    # Fix <di>< (any tag after)
    content = re.sub(b'<di><', b'<', content)
    print("✅ Fixed <di>< → <")
    
    # Remove standalone <di>
    content = content.replace(b'<di>', b'')
    
    # Remove <di with whitespace
    content = re.sub(b'<di\\s', b'', content)
    
    # Count final
    final_count = content.count(b'<di')
    print(f"Final <di patterns: {final_count}")
    
    if final_count == 0:
        print("✅ ALL <di patterns COMPLETELY REMOVED!")
    else:
        print(f"⚠️ {final_count} patterns still remain - checking...")
        # Show sample
        matches = re.findall(b'.{0,10}<di.{0,10}', content)
        if matches:
            print("  Remaining patterns:")
            for i, m in enumerate(matches[:5]):
                print(f"    {i+1}. {repr(m)}")
    
    # Write back
    with open(FILE, 'wb') as f:
        f.write(content)
    
    print("\n✅ FILE SAVED")
    print("\n🔄 HARD REFRESH BROWSER: Ctrl + Shift + R")
    print("\nDashboard should NOW be COMPLETELY CLEAN!")

if __name__ == "__main__":
    main()
