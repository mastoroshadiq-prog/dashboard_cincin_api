"""
Fix duplicate currentDivision declarations
Keep only the FIRST one, remove others
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all lines with 'let currentDivision'
declaration_lines = []
for i, line in enumerate(lines):
    if 'let currentDivision' in line:
        declaration_lines.append(i + 1)  # 1-indexed

print(f"Found {len(declaration_lines)} declarations at lines: {declaration_lines}")

if len(declaration_lines) > 1:
    # Keep the LAST one (most recent), remove others
    # Change 'let' to just assignment for duplicates
    for line_num in declaration_lines[:-1]:  # All except last
        idx = line_num - 1  # Convert to 0-indexed
        # Replace 'let currentDivision' with just the comment or remove
        if 'let currentDivision' in lines[idx]:
            # Just remove the 'let ' keyword
            lines[idx] = lines[idx].replace('let currentDivision', '// Removed duplicate: currentDivision')
            print(f"  Fixed line {line_num}")
    
    # Write back
    with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n✅ Fixed! Kept declaration at line {declaration_lines[-1]}, removed {len(declaration_lines)-1} duplicates")
else:
    print("✅ No duplicates found")
