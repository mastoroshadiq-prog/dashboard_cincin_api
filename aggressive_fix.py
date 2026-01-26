import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("ERROR: File not found")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("AGGRESSIVE FIX - Replacing ALL 'v class=' patterns...")
    
    # Count initial occurrences
    initial_count = content.count('v class="')
    print(f"Found {initial_count} instances of 'v class=\"'")
    
    # AGGRESSIVE REPLACEMENT - Replace ALL instances
    content = content.replace('v class="', '<div class="')
    
    # Verify
    remaining = content.count('v class="')
    print(f"Remaining: {remaining} (should be 0)")
    
    if remaining == 0:
        print("✅ ALL 'v class=' patterns fixed!")
    else:
        print(f"⚠️  {remaining} patterns still remain - manual check needed")
    
    # Write back
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ FILE SAVED")
    print("🔄 HARD REFRESH BROWSER NOW: Ctrl + Shift + R")

if __name__ == "__main__":
    main()
