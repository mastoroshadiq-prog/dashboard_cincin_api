import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ISSUE 1: Malformed Class Attribute with Badge injection
    # Detected: class="... <span class="iso-badge...</span>">
    
    # Regex to find this pattern
    # It looks like: class="[^"]+\n<span
    
    pattern = re.compile(r'(class="[^"]+)\n(<span class="iso-badge[^>]+>.*?</span>)">', re.DOTALL)
    
    # We want to change it to: class="..." > \n <span...>
    
    def replacer(match):
        print("Found malformed class injection!")
        cls_attr = match.group(1) + '"'
        badge = match.group(2)
        return cls_attr + '>\n' + badge

    new_content, count = pattern.subn(replacer, content)
    
    if count == 0:
        print("Regex didn't trigger. Trying strict string replacement for the specific case seen.")
        # The specific case from view_file:
        # border-indigo-500/30\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>">
        
        broken_str = 'border-indigo-500/30\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>">'
        fixed_str = 'border-indigo-500/30">\n<span class="iso-badge iso-phase-2">2. ANALYSIS</span>'
        
        if broken_str in content:
            print("Found specific broken string. Fixing...")
            new_content = content.replace(broken_str, fixed_str)
        else:
            print("Could not find the broken string either. Check file content manually.")
            
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ HTML Attribute Fix applied.")

if __name__ == "__main__":
    main()
