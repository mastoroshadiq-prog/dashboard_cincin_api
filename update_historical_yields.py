"""
Update HISTORICAL_YIELDS di dashboard HTML dengan data lengkap dari data_gabungan.xlsx
"""

import json
import re

# Load the complete yields data
with open('complete_historical_yields.json', 'r') as f:
    complete_data = json.load(f)

print(f"Total blocks in complete_data: {len(complete_data)}")

# Convert to format expected by dashboard (integer keys for years)
historical_yields = {}
for block_code, block_data in complete_data.items():
    yields = block_data.get('yields', {})
    historical_yields[block_code] = {
        'luas_ha': block_data.get('luas_ha', 0),
        'division': block_data.get('division', ''),
        'yields': {
            2023: {
                'real_ton_ha': yields.get('2023', {}).get('real_ton_ha', 0),
                'poten_ton_ha': yields.get('2023', {}).get('poten_ton_ha', 0),
                'gap_pct': yields.get('2023', {}).get('gap_pct', 0)
            },
            2024: {
                'real_ton_ha': yields.get('2024', {}).get('real_ton_ha', 0),
                'poten_ton_ha': yields.get('2024', {}).get('poten_ton_ha', 0),
                'gap_pct': yields.get('2024', {}).get('gap_pct', 0)
            },
            2025: {
                'real_ton_ha': yields.get('2025', {}).get('real_ton_ha', 0),
                'poten_ton_ha': yields.get('2025', {}).get('poten_ton_ha', 0),
                'gap_pct': yields.get('2025', {}).get('gap_pct', 0)
            }
        }
    }

# Convert to JavaScript object string
js_object = "const HISTORICAL_YIELDS = " + json.dumps(historical_yields, indent=4) + ";"

# Replace integer keys with unquoted keys for JavaScript
js_object = js_object.replace('"2023":', '2023:')
js_object = js_object.replace('"2024":', '2024:')
js_object = js_object.replace('"2025":', '2025:')

# Read the HTML file
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace HISTORICAL_YIELDS
# Pattern to match the existing HISTORICAL_YIELDS declaration
pattern = r'const HISTORICAL_YIELDS = \{[^}]+\};'
# Actually, the pattern is more complex because HISTORICAL_YIELDS has nested objects

# Better approach: find start and end
start_marker = 'const HISTORICAL_YIELDS = {'
end_marker_candidates = ['const BLOCKS_DATA', 'const DIVISIONS_META', 'function ']

start_pos = content.find(start_marker)
if start_pos == -1:
    print("ERROR: Could not find HISTORICAL_YIELDS in HTML")
    exit(1)

print(f"Found HISTORICAL_YIELDS at position {start_pos}")

# Find the end - look for the next const declaration or function
search_pos = start_pos + len(start_marker)
end_pos = len(content)

for marker in end_marker_candidates:
    pos = content.find(marker, search_pos)
    if pos != -1 and pos < end_pos:
        # Go back to find the semicolon and newlines before this marker
        # Actually let's count braces
        pass

# Better: count braces to find end
brace_count = 0
in_object = False
end_pos = start_pos

for i in range(start_pos, len(content)):
    char = content[i]
    if char == '{':
        brace_count += 1
        in_object = True
    elif char == '}':
        brace_count -= 1
        if in_object and brace_count == 0:
            end_pos = i + 1
            # Find the semicolon
            if content[i+1:i+2] == ';':
                end_pos = i + 2
            break

print(f"HISTORICAL_YIELDS ends at position {end_pos}")
print(f"Original size: {end_pos - start_pos} characters")

# Extract the old content for verification
old_content = content[start_pos:end_pos]
print(f"First 200 chars of old: {old_content[:200]}")

# Create new content
new_content = content[:start_pos] + js_object + content[end_pos:]

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ Updated HISTORICAL_YIELDS with {len(historical_yields)} blocks")
print(f"New size: {len(js_object)} characters")

# Show sample of updated data
print("\n=== SAMPLE AME02 DATA ===")
count = 0
for block_code, data in historical_yields.items():
    if data['division'] == 'AME02':
        print(f"{block_code}: 2023={data['yields'][2023]['real_ton_ha']:.1f} -> 2025={data['yields'][2025]['real_ton_ha']:.1f} T/Ha")
        count += 1
        if count >= 5:
            break
