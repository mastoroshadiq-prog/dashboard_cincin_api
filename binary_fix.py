import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    # Read as BINARY to avoid encoding issues
    with open(FILE, 'rb') as f:
        content = f.read()

    print("BINARY-LEVEL FIX...")
    
    # Count initial
    initial_count = content.count(b'<di')
    print(f"Initial <di patterns: {initial_count}")
    
    # REPLACE AS BYTES
    # Pattern 1: <di><div → <div
    content = content.replace(b'<di><div', b'<div')
    
    # Pattern 2: <di>< → <
    content = content.replace(b'<di><', b'<')
    
    # Pattern 3: <di> → empty
    content = content.replace(b'<di>', b'')
    
    # Pattern 4: <di followed by space
    content = content.replace(b'<di ', b'')
    
    # Pattern 5: <di followed by newline
    content = content.replace(b'<di\r', b'')
    content = content.replace(b'<di\n', b'')
    
    # Count final
    final_count = content.count(b'<di')
    print(f"Final <di patterns: {final_count}")
    
    if final_count == 0:
        print("✅ ALL <di patterns REMOVED!")
    else:
        print(f"⚠️ {final_count} patterns still remain")
    
    # Write back as binary
    with open(FILE, 'wb') as f:
        f.write(content)
    
    print("\n✅ FILE SAVED (binary mode)")
    print("🔄 REFRESH BROWSER NOW!")

if __name__ == "__main__":
    main()
