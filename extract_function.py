"""
Extract renderPaparanRisk function
"""

def extract_function():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_idx = content.find('function renderPaparanRisk')
    if start_idx == -1:
        print("[ERROR] Function not found")
        return
    
    # Find end of function (next function or closing script tag)
    # Look for next 'function ' or '</script>'
    search_area = content[start_idx:]
    next_function = search_area.find('function ', 50)  # Skip current function declaration
    script_end = search_area.find('</script>')
    
    if next_function != -1 and next_function < script_end:
        end_idx = start_idx + next_function
    else:
        end_idx = start_idx + script_end
    
    function_code = content[start_idx:end_idx]
    
    with open('renderPaparanRisk_function.js', 'w', encoding='utf-8') as f:
        f.write(function_code)
    
    print(f"[SAVED] Function to renderPaparanRisk_function.js")
    print(f"Function length: {len(function_code)} chars")
    print(f"Lines: {function_code.count(chr(10))}")

if __name__ == '__main__':
    extract_function()
