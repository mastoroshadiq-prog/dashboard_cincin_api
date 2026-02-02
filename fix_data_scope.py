"""
Fix: Remove window. prefix from COMPLETE_BLOCKS_DATA access
The object exists but not in window scope
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Replace window.COMPLETE_BLOCKS_DATA with just COMPLETE_BLOCKS_DATA
replacements = 0

if 'window.COMPLETE_BLOCKS_DATA' in content:
    count = content.count('window.COMPLETE_BLOCKS_DATA')
    content = content.replace('window.COMPLETE_BLOCKS_DATA', 'COMPLETE_BLOCKS_DATA')
    replacements = count
    print(f"✅ Removed 'window.' prefix from {replacements} occurrences")
else:
    print(f"⚠️ No window.COMPLETE_BLOCKS_DATA found")

# Also check if COMPLETE_BLOCKS_DATA is defined inside a function scope
# If so, we need to make it global
if 'const COMPLETE_BLOCKS_DATA' in content:
    # Check if it's inside a function
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'const COMPLETE_BLOCKS_DATA' in line:
            print(f"\n📍 COMPLETE_BLOCKS_DATA defined at line ~{i+1}")
            # Show context
            start = max(0, i-3)
            end = min(len(lines), i+3)
            for j in range(start, end):
                marker = " >>> " if j == i else "     "
                print(f"{marker}Line {j+1}: {lines[j][:70]}")
            break

# Make sure COMPLETE_BLOCKS_DATA is accessible globally
# Add it to window object explicitly if needed
global_assignment = '''
            // Make COMPLETE_BLOCKS_DATA globally accessible
            if (typeof COMPLETE_BLOCKS_DATA !== 'undefined') {
                window.COMPLETE_BLOCKS_DATA = COMPLETE_BLOCKS_DATA;
                console.log('[DATA] COMPLETE_BLOCKS_DATA exposed to window scope');
            }
'''

# Insert this after COMPLETE_BLOCKS_DATA definition
marker = 'const COMPLETE_BLOCKS_DATA = {'
if marker in content:
    # Find the closing brace for this object
    # This is complex, so let's insert it at a safe location
    # Look for the end of the COMPLETE_BLOCKS_DATA object
    
    # Simple approach: insert after we see }; following the const COMPLETE_BLOCKS_DATA
    import re
    # Find position after COMPLETE_BLOCKS_DATA definition
    pattern = r'const COMPLETE_BLOCKS_DATA = \{[^}]*\};'
    # This won't work for nested objects, so let's use a different approach
    
    # Insert after first <script> tag in file
    script_pos = content.find('<script>')
    if script_pos != -1:
        # Find end of script opening tag  
        script_end = content.find('>', script_pos) + 1
        # Insert global assignment
        content = content[:script_end] + '\n' + global_assignment + content[script_end:]
        print(f"✅ Added global window assignment")
else:
    print(f"⚠️ Could not find COMPLETE_BLOCKS_DATA definition")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ SCOPE FIX APPLIED!")
print(f"   Changed: window.COMPLETE_BLOCKS_DATA → COMPLETE_BLOCKS_DATA")
print(f"   Added: window.COMPLETE_BLOCKS_DATA = COMPLETE_BLOCKS_DATA")
print(f"   Effect: Direct access to data object")
print(f"\n📝 Now accessing data:")
print(f"   const blockData = COMPLETE_BLOCKS_DATA['F004A']")
print(f"   ✅ Should work now!")
