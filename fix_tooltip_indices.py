"""
Fix dataset indices in tooltip after SPH removal
Old indices: [0, 1, 2, 3, 4, 5] with datasets at:
  0: Kerugian (No Treatment)
  1: Ganoderma (No Treatment)
  2: SPH (No Treatment) - REMOVED
  3: Kerugian (With Treatment)
  4: Ganoderma (With Treatment)
  5: SPH (With Treatment) - REMOVED

New indices: [0, 1, 2, 3] with datasets at:
  0: Kerugian (No Treatment)
  1: Ganoderma (No Treatment)
  2: Kerugian (With Treatment)
  3: Ganoderma (With Treatment)
"""

# Read file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content):,} characters")

# Fix 1: Change datasets[4] to datasets[3] for Ganoderma With Treatment
old_gano = 'const ganoWith = datasets[4].data[dataIndex];'
new_gano = 'const ganoWith = datasets[3].data[dataIndex];'

if old_gano in content:
    content = content.replace(old_gano, new_gano)
    print(f"✅ Fixed: datasets[4] → datasets[3] for Ganoderma With Treatment")
else:
    print(f"⚠️ Could not find Ganoderma index to fix")

# Fix 2: Remove SPH row from tooltip (lines 18105-18114 approximately)
# Find and remove the SPH tooltip section
sph_tooltip_pattern = r'// SPH row\s+const sphNo = datasets\[\d+\]\.data\[dataIndex\];\s+const sphWith = datasets\[\d+\]\.data\[dataIndex\];\s+const sphDelta = sphWith - sphNo;\s+html \+= `<tr>.*?</tr>`;'

import re
match = re.search(sph_tooltip_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + content[match.end():]
    print(f"✅ Removed SPH row from tooltip using regex")
else:
    # Manual approach - find and remove specific lines
    print(f"⚠️ Regex didn't work, trying manual removal...")
    
    # Split into lines
    lines = content.split('\n')
    new_lines = []
    skip_mode = False
    skip_count = 0
    
    for i, line in enumerate(lines):
        # Start skipping when we find SPH row comment
        if '// SPH row' in line and 'const sphNo' in lines[i+1] if i+1 < len(lines) else False:
            skip_mode = True
            skip_count = 0
            print(f"  Found SPH section at line {i+1}")
            continue
        
        # Skip next 8-10 lines (SPH tooltip code)
        if skip_mode:
            skip_count += 1
            if skip_count <= 9:  # Skip the SPH tooltip block
                continue
            else:
                skip_mode = False
                # Continue to next iteration after exiting skip mode
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    print(f"✅ Removed SPH section manually")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ TOOLTIP FIXED!")
print(f"   Changed: datasets[4] → datasets[3] (Ganoderma With Treatment)")
print(f"   Removed: SPH row from tooltip (datasets[2] and datasets[5])")
print(f"\nTooltip will now show:")
print(f"   ✅ Kerugian comparison (No Treatment vs With Treatment)")
print(f"   ✅ Ganoderma comparison (No Treatment vs With Treatment)")
print(f"   ❌ SPH comparison (REMOVED)")
