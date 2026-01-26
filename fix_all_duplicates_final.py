"""
COMPREHENSIVE FIX: Remove ALL duplicate currentDivision declarations
Keep only ONE declaration
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find ALL lines with 'let currentDivision'
duplicates = []
for i, line in enumerate(lines):
    if 'let currentDivision' in line:
        duplicates.append(i + 1)  # 1-indexed line number
        print(f"Line {i+1}: {line.strip()}")

print(f"\n{'='*70}")
print(f"Found {len(duplicates)} declarations of 'let currentDivision'")
print(f"Lines: {duplicates}")
print(f"{'='*70}\n")

if len(duplicates) > 1:
    print("FIXING: Keeping LAST declaration (most recent), removing others\n")
    
    # Keep the LAST one (most recent functional version)
    # Remove all others by commenting them out
    keep_line = duplicates[-1] - 1  # 0-indexed
    
    for dup_line_1indexed in duplicates[:-1]:  # All except last
        line_idx = dup_line_1indexed - 1
        # Comment out the duplicate
        lines[line_idx] = '        // REMOVED DUPLICATE: ' + lines[line_idx].strip() + '\n'
        print(f"  ✅ Removed duplicate at line {dup_line_1indexed}")
    
    print(f"  ✅ Kept declaration at line {duplicates[-1]}")
    
    # Write back
    with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n{'='*70}")
    print("✅ ALL DUPLICATES FIXED!")
    print(f"{'='*70}")
else:
    print("✅ No duplicates found - already fixed!")
