"""
Remove Critical Blocks metric card from DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html
This removes the 4th card in the Quick Metrics Grid
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Critical Blocks card section: lines 198-215 (1-indexed, inclusive)
# This is the 4th card in the grid
section_start = 198 - 1  # Convert to 0-indexed  
section_end = 215  # Exclusive in Python slicing

print(f"\n🗑️ Removing Critical Blocks metric card:")
print(f"   Lines: {section_start+1} - {section_end-1}")
print(f"   Total: {section_end - section_start} lines")

# Verify we're removing the right section
print(f"\n📋 Preview of section to remove:")
for i in range(section_start, min(section_start+5, section_end)):
    print(f"   Line {i+1}: {lines[i][:70].rstrip()}")

# Build new content without this section
new_lines = lines[:section_start] + lines[section_end:]

# Also need to change grid from "grid-cols-4" to "grid-cols-3" since we're removing 1 card
# Find the Quick Metrics Grid line
for i, line in enumerate(new_lines):
    if 'Quick Metrics Grid' in line and i < 200:
        # Check next few lines for grid-cols-4
        for j in range(i, min(i+5, len(new_lines))):
            if 'grid-cols-4' in new_lines[j]:
                new_lines[j] = new_lines[j].replace('grid-cols-4', 'grid-cols-3')
                print(f"\n✅ Changed grid from 4 to 3 columns at line {j+1}")
                break
        break

print(f"\n📊 Line count change:")
print(f"   Before: {len(lines)} lines")
print(f"   After: {len(new_lines)} lines")
print(f"   Removed: {len(lines) - len(new_lines)} lines")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ CRITICAL BLOCKS CARD REMOVED!")
print(f"   Removed card showing 'Critical Blocks' metric")
print(f"   Changed grid layout from 4 columns to 3 columns")
print(f"   Dashboard now shows:")
print(f"   • Total Blocks")
print(f"   • Total Area")
print(f"   • Avg Yield 2025")
print(f"   ❌ Critical Blocks (REMOVED)")
