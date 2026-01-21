"""
Check OLE01 blocks and stadium_kritis field
"""

import re
import json

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find BLOCKS_DATA section
start_idx = content.find('const BLOCKS_DATA = {')
if start_idx == -1:
    start_idx = content.find('const COMPLETE_BLOCKS_DATA = {')
    
# Extract a portion to analyze
section = content[start_idx:start_idx+100000]

# Find OLE01 blocks
ole01_blocks = []
lines = section.split('\n')
current_block = {}
in_block = False
block_code = None

for i, line in enumerate(lines):
    # Look for block code
    if '"block_code":' in line:
        match = re.search(r'"block_code":\s*"([^"]+)"', line)
        if match:
            block_code = match.group(1)
            if 'OLE01' in block_code:
                in_block = True
                current_block = {'block_code': block_code}
    
    if in_block:
        # Get division
        if '"division":' in line:
            match = re.search(r'"division":\s*"([^"]+)"', line)
            if match:
                current_block['division'] = match.group(1)
        
        # Get stadium_kritis - THIS IS KEY!
        if '"stadium_kritis"' in line or '"stadium"' in line or '"kritis"' in line:
            print(f"FOUND STADIUM LINE: {line.strip()}")
            match = re.search(r'"([^"]*stadium[^"]*)":\s*([^,\n]+)', line, re.IGNORECASE)
            if match:
                current_block['stadium_field'] = match.group(1)
                current_block['stadium_value'] = match.group(2).strip()
        
        # Get loss
        if '"ganoderma_loss' in line or '"loss' in line:
            match = re.search(r'"([^"]*loss[^"]*)":\s*([^,\n]+)', line)
            if match:
                current_block['loss_field'] = match.group(1)
                current_block['loss_value'] = match.group(2).strip()
        
        # End of block
        if '},' in line and current_block:
            ole01_blocks.append(current_block)
            in_block = False
            current_block = {}
            if len(ole01_blocks) >= 3:  # Get first 3 blocks
                break

print("="*60)
print(f"OLE01 Sample Blocks (first {len(ole01_blocks)}):")
print("="*60)
for i, block in enumerate(ole01_blocks, 1):
    print(f"\nBlock {i}:")
    for key, value in block.items():
        print(f"  {key}: {value}")

# Also check what fields exist
print("\n" + "="*60)
print("Searching for 'stadium' or 'kritis' field names...")
print("="*60)
stadium_fields = set(re.findall(r'"([^"]*(?:stadium|kritis|stage|grade)[^"]*)":', section, re.IGNORECASE))
print("Found fields:", stadium_fields)
