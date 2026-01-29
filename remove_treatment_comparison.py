"""
Remove Treatment Impact Analysis section (Before/After Treatment Comparison)
This redundant section is now covered by 5-Year Trend Analysis with scenario toggles
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Treatment Impact Analysis section: lines 217-388 (inclusive, 1-indexed)
section_start = 217 - 1  # Convert to 0-indexed
section_end = 389  # Exclusive in Python slicing (includes line 388)

print(f"\n🗑️ Removing Treatment Impact Analysis section:")
print(f"   Lines: {section_start+1} - {section_end-1}")
print(f"   Total: {section_end - section_start} lines")

# Build new content without this section
new_lines = lines[:section_start] + lines[section_end:]

print(f"\n📊 Line count change:")
print(f"   Before: {len(lines)} lines")
print(f"   After: {len(new_lines)} lines")
print(f"   Removed: {len(lines) - len(new_lines)} lines")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ TREATMENT IMPACT ANALYSIS SECTION REMOVED!")
print(f"   Removed 'FEATURE 1: Before/After Treatment Comparison'")
print(f"   Removed:")
print(f"   • 3-Year Financial Impact Analysis")
print(f"   • No Treatment vs With Treatment comparison chart")
print(f"   • Savings Highlight")
print(f"   • 3-Year Degradation Model Chart (hidden)")
print(f"\n   Reason: Redundant with 5-Year Trend Analysis (scenario toggles)")
print(f"   Benefits: Cleaner UI, no duplication, better performance")
