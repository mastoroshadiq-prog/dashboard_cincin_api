"""
Make the Block Breakdown Modal dynamic based on selected division
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace hardcoded 'AME02' in onclick with dynamic currentSelectedDivision
old_onclick = "openBlockBreakdownModal('AME02')"
new_onclick = "openBlockBreakdownModal(currentSelectedDivision || 'AME02')"

if old_onclick in content:
    content = content.replace(old_onclick, new_onclick)
    print("✅ Updated onclick to use currentSelectedDivision")
else:
    print("⚠️ Could not find hardcoded AME02 onclick")

# 2. Add currentSelectedDivision initialization in the main script block
# Find where the script starts and add the variable
init_marker = "// =============================================\n            // GLOBAL VARIABLES"
if init_marker in content:
    # Already has global variables section
    if 'currentSelectedDivision' not in content:
        content = content.replace(
            init_marker,
            init_marker + "\n            let currentSelectedDivision = 'AME02'; // Default to AME02"
        )
        print("✅ Added currentSelectedDivision initialization")
    else:
        print("✅ currentSelectedDivision already exists")
else:
    # Need to find first script block after style and add init
    script_start = content.find('<script>', content.find('</style>'))
    if script_start > 0:
        insert_pos = content.find('\n', script_start) + 1
        init_code = "            // Global variable for current division\n            let currentSelectedDivision = 'AME02';\n\n"
        content = content[:insert_pos] + init_code + content[insert_pos:]
        print("✅ Added currentSelectedDivision at script start")

# 3. Find division change handlers (like showDivisionOverview) and update currentSelectedDivision
# Look for showDivisionOverview function
show_div_func = "function showDivisionOverview("
func_pos = content.find(show_div_func)

if func_pos > 0:
    # Find opening brace
    brace_pos = content.find('{', func_pos)
    if brace_pos > 0:
        # Insert currentSelectedDivision update right after opening brace
        update_line = "\n                // Update current selected division\n                currentSelectedDivision = divisionCode;\n"
        
        # Check if already added
        check_area = content[brace_pos:brace_pos+200]
        if 'currentSelectedDivision = divisionCode' not in check_area:
            content = content[:brace_pos+1] + update_line + content[brace_pos+1:]
            print("✅ Added division update in showDivisionOverview")
        else:
            print("✅ Division update already exists in showDivisionOverview")
else:
    print("⚠️ showDivisionOverview function not found")

# 4. Also check if there's a selectDivision or similar function
select_div_patterns = ['function selectDivision', 'function changeDivision', 'function onDivisionChange']
for pattern in select_div_patterns:
    if pattern in content:
        print(f"  Found: {pattern}")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
