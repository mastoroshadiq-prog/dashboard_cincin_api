"""
Update Block Trend Modal:
1. Change "No Data" label to "TBM" 
2. Add TM vs TBM summary
3. Show TBM blocks list
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*60)
print("UPDATING BLOCK TREND MODAL FOR TBM")
print("="*60)

# 1. Find and update the category labels in JavaScript
# Look for nodata categorization
old_nodata = "nodata: []"
if old_nodata in content:
    content = content.replace(old_nodata, "tbm: []")
    print("✅ Changed 'nodata' to 'tbm' in categories object")

# 2. Update category count elements  
old_count = "categoryCount_nodata"
if old_count in content:
    content = content.replace(old_count, "categoryCount_tbm")
    print("✅ Changed categoryCount_nodata to categoryCount_tbm")

# 3. Update push to nodata -> tbm
old_push = "categories.nodata.push"
if old_push in content:
    content = content.replace(old_push, "categories.tbm.push")
    print("✅ Changed categories.nodata.push to categories.tbm.push")

# 4. Update chart labels
old_label = "'No Data'"
if old_label in content:
    content = content.replace(old_label, "'TBM'")
    print("✅ Changed 'No Data' label to 'TBM'")

# 5. Update chart data access for nodata
old_data = "categories.nodata.length"
if old_data in content:
    content = content.replace(old_data, "categories.tbm.length")
    print("✅ Changed categories.nodata.length to categories.tbm.length")

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
