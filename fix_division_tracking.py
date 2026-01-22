"""
Add currentSelectedDivision update to updateDivisionSummary function
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find updateDivisionSummary function and add the assignment
old_func = "function updateDivisionSummary(divisionCode) {"
new_func = """function updateDivisionSummary(divisionCode) {
                // Update global current division for modal
                currentSelectedDivision = divisionCode;"""

if old_func in content:
    # Check if already modified
    if "currentSelectedDivision = divisionCode" not in content[content.find(old_func):content.find(old_func)+300]:
        content = content.replace(old_func, new_func)
        print("✅ Added currentSelectedDivision update to updateDivisionSummary")
    else:
        print("✅ Already has currentSelectedDivision update")
else:
    print("⚠️ updateDivisionSummary function not found")

# Also update openPaparanRisikoModal to use dynamic division if needed
old_paparan = "openPaparanRisikoModal('AME02')"
new_paparan = "openPaparanRisikoModal(currentSelectedDivision || 'AME02')"
if old_paparan in content:
    content = content.replace(old_paparan, new_paparan)
    print("✅ Updated openPaparanRisikoModal to use dynamic division")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
