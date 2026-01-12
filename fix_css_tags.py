import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Fixing exposed CSS text...")
    
    # 1. Identify the raw CSS start and end
    # The raw css started with "/* ISO 31000 Badges */" and ended with the last curly brace of .iso-phase-5
    
    start_marker = "/* ISO 31000 Badges */"
    # Identify unique string at the end of the CSS block I injected
    end_marker = ".iso-phase-5 { background: rgba(100, 116, 139, 0.85); color: white; } /* Slate */"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("CSS block not found. formatting might be different.")
        # Try to find it without the comment if needed, or maybe it lays differently
        return

    end_idx = content.find(end_marker)
    if end_idx == -1:
        print("End of CSS block not found.")
        return
        
    end_idx += len(end_marker)
    
    # Check if already wrapped
    # Look back from start_idx for <style>
    if "<style>" in content[max(0, start_idx-20):start_idx]:
        print("CSS already wrapped in <style>. No details to fix.")
        return

    # WRAP IT
    css_content = content[start_idx:end_idx]
    new_css_block = f"\n<style>\n{css_content}\n</style>\n"
    
    # Replace
    new_full_content = content[:start_idx] + new_css_block + content[end_idx:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_full_content)
        
    print("✅ FIXED: Raw CSS text is now properly hidden inside <style> tags.")
    print("🔄 Refresh dashboard to see clean header.")

if __name__ == "__main__":
    main()
