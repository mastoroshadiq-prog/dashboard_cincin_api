"""
Script untuk extract PAPARAN RISIKO section
"""

def extract_paparan_section():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find PAPARAN RISIKO section
    start_idx = content.find('PAPARAN RISIKO')
    if start_idx == -1:
        print("[ERROR] PAPARAN RISIKO not found")
        return
    
    # Get more context
    section_start = max(0, start_idx - 500)
    section_end = min(len(content), start_idx + 5000)
    
    section = content[section_start:section_end]
    
    # Save to file
    with open('paparan_risiko_section.html', 'w', encoding='utf-8') as f:
        f.write(section)
    
    print(f"[SAVED] PAPARAN RISIKO section to paparan_risiko_section.html")
    print(f"Section starts at position: {start_idx}")
    
    # Also look for chart canvas elements
    if 'canvas' in section:
        print("[FOUND] Canvas element exists in section")
    else:
        print("[INFO] No canvas element found - need to add chart")

if __name__ == '__main__':
    extract_paparan_section()
