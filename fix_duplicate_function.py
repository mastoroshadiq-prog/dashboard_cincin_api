"""
Remove OLD obsolete filterByDivision function
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove lines 1187-1220 (the old filter function)
# These are 0-indexed, so lines 1186-1219
start_line = 1186  # 0-indexed (line 1187)
end_line = 1220    # 0-indexed (line 1221)

# Remove the old function
new_lines = lines[:start_line] + ['        // OLD FILTER FUNCTION REMOVED - Using new functional version at end of script\n'] + lines[end_line:]

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("="*70)
print("✅ REMOVED OLD FILTER FUNCTION!")
print("="*70)
print(f"Deleted lines {start_line+1} to {end_line}")
print(f"File reduced from {len(lines)} to {len(new_lines)} lines")
print("\n🔧 This fixes:")
print("  ✅ Duplicate function declaration")
print("  ✅ References to non-existent buttons (divBtn_AME_II)")
print("\n🌐 REFRESH BROWSER - Errors should be gone!")
print("="*70)
