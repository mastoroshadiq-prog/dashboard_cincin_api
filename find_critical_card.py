"""
Script untuk menemukan dan memperbaiki CRITICAL BLOCKS card
"""

def find_and_fix_critical_card():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Searching for CRITICAL BLOCKS card...")
    
    # Try various search patterns
    patterns = [
        'Critical Blocks',
        'CRITICAL BLOCKS',
        'divCriticalBlocks',
        'divMetric_critical',
        'orange-500/50',  # Card border color
    ]
    
    for pattern in patterns:
        if pattern in content:
            idx = content.find(pattern)
            print(f"\n[FOUND] '{pattern}' at position {idx}")
            # Show context
            start = max(0, idx - 500)
            end = min(len(content), idx + 500)
            print("Context:")
            print(content[start:end])
            print("\n" + "="*80)
    
    # Try to find by looking for the 4-card grid in Division Overview
    search_start = content.find('DIVISION OVERVIEW')
    if search_start != -1:
        print(f"\n[FOUND] DIVISION OVERVIEW at position {search_start}")
        
        # Look for the grid section after it
        grid_search = content[search_start:search_start+5000]
        
        # Save section to file for inspection
        with open('division_overview_section.html', 'w', encoding='utf-8') as f:
            f.write(grid_search)
        print("[SAVED] Division overview section to division_overview_section.html for inspection")

if __name__ == '__main__':
    find_and_fix_critical_card()
