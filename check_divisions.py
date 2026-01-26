"""
Quick test to see what division codes exist in BLOCKS_DATA
"""

import re

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all division values in BLOCKS_DATA section
# Look for "division": "XXX"
divisions = re.findall(r'"division":\s*"([^"]+)"', content)

unique_divisions = sorted(set(divisions))
print(f"Found {len(unique_divisions)} unique divisions:")
for div in unique_divisions:
    count = divisions.count(div)
    print(f"  {div}: {count} blocks")

# Check if AME_II or AME_IV exist
print("\nDivision format check:")
print(f"  AME_II exists: {'AME_II' in unique_divisions}")
print(f"  AME_IV exists: {'AME_IV' in unique_divisions}")
print(f"  AME02 exists: {'AME02' in unique_divisions}")

# Show sample division codes
print(f"\nSample division codes:")
for div in unique_divisions[:5]:
    print(f"  - {div}")
