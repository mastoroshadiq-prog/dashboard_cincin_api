"""
List all field names in BLOCKS_DATA
"""

import re

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find BLOCKS_DATA
idx = content.find('const BLOCKS_DATA = {')
if idx == -1:
    idx = content.find('const COMPLETE_BLOCKS_DATA = {')

section = content[idx:idx+30000]

# Find all field names
fields = set(re.findall(r'"([a-z_0-9]+)":', section))

print("All fields found in BLOCKS_DATA:")
for field in sorted(fields):
    print(f"  - {field}")

# Check specifically for 'stadium' or 'kritis' or 'risk' or 'severity'
print("\n" + "="*60)
print("Fields containing 'stad', 'krit', 'risk', 'sever', 'loss':")
print("="*60)
for field in sorted(fields):
    if any(keyword in field.lower() for keyword in ['stad', 'krit', 'risk', 'sever', 'loss', 'grade', 'level']):
        print(f"  ✓ {field}")
