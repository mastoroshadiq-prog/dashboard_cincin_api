"""
Remove Historical Trends & Projection chart section
This section is now redundant with the 5-Year Trend Analysis on main dashboard
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Historical Trends section to remove: lines 386-460 (inclusive, 1-indexed)
section_start = 386 - 1  # Convert to 0-indexed
section_end = 460  # Exclusive in Python slicing

print(f"\n🗑️ Removing Historical Trends section:")
print(f"   Lines: {section_start+1} - {section_end}")
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

print(f"\n✅ HISTORICAL TRENDS SECTION REMOVED!")
print(f"   Removed redundant 'Historical Trends & Projection' chart")
print(f"   Reason: Already have comprehensive 5-Year Trend Analysis on main dashboard")
print(f"   Benefits: Cleaner UI, no duplication, better performance")
