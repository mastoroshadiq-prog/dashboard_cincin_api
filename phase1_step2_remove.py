"""
Phase 1 Step 2: Remove sections from popup
Replace with comments to keep structure clean
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Calculate new line numbers after insertion (added 406 lines at line 467)
# Original popup sections were at:
#   Visual: 18697-18773
#   Loss: 18776-18985  
#   Trend: 18987-19086
# After insertion of 406 lines, they shifted to:
shift = 406
visual_start = 18697 + shift - 1  # 0-indexed
visual_end = 18773 + shift
loss_start = 18776 + shift - 1
loss_end = 18985 + shift
trend_start = 18987 + shift - 1
trend_end = 19086 + shift

print(f"\n📍 Adjusted line numbers (after +{shift} line shift):")
print(f"   Visual Analysis: {visual_start+1} - {visual_end}")
print(f"   Loss Analysis: {loss_start+1} - {loss_end}")
print(f"   5-Year Trend: {trend_start+1} - {trend_end}")

# Replace sections with comments
replacement_visual = [
    '                    <!-- ================================================ -->\n',
    '                    <!-- VISUAL ANALYSIS - Moved to Main Dashboard -->\n',
    '                    <!-- See lines ~467-543 on main dashboard -->\n',
    '                    <!-- ================================================ -->\n',
    '\n'
]

replacement_loss = [
    '                    <!-- ================================================ -->\n',
    '                    <!-- LOSS ANALYSIS - Moved to Main Dashboard -->\n',
    '                    <!-- See lines ~550-759 on main dashboard -->\n',
    '                    <!-- ================================================ -->\n',
    '\n'
]

replacement_trend = [
    '                    <!-- ================================================ -->\n',
    '                    <!-- 5-YEAR TREND ANALYSIS - Moved to Main Dashboard -->\n',
    '                    <!-- See lines ~766-865 on main dashboard -->\n',
    '                    <!-- ================================================ -->\n',
    '\n'
]

# Build new content
new_lines = []
new_lines.extend(lines[:visual_start])
new_lines.extend(replacement_visual)
new_lines.extend(lines[visual_end:loss_start])
new_lines.extend(replacement_loss)
new_lines.extend(lines[loss_end:trend_start])
new_lines.extend(replacement_trend)
new_lines.extend(lines[trend_end:])

print(f"\n✅ Replaced sections with comments")
print(f"   Visual: {len(lines[visual_start:visual_end])} lines → {len(replacement_visual)} lines")
print(f"   Loss: {len(lines[loss_start:loss_end])} lines → {len(replacement_loss)} lines")
print(f"   Trend: {len(lines[trend_start:trend_end])} lines → {len(replacement_trend)} lines")

removed_lines = len(lines) - len(new_lines)
print(f"\n📊 Line count change:")
print(f"   Before: {len(lines)} lines")
print(f"   After: {len(new_lines)} lines")
print(f"   Removed: {removed_lines} lines")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ PHASE 1 STEP 2 COMPLETE!")
print(f"   Removed 3 sections from popup")
print(f"   Replaced with comments indicating new locations")
print(f"   Popup is now simplified and lightweight")
