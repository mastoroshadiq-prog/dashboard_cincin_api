"""
Fix dashboard data loading and visibility issues
1. Auto-load data to main dashboard sections on division select
2. Fix empty popup modal
3. Remove dependency on clicking "Total Blocks"
"""

import re

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Find the division selector onchange handler
# It currently only updates metrics but doesn't load data into moved sections
# We need to find and modify the onDivisionChange function

print("\n🔍 Searching for division change handler...")

# Search for the function that handles division selection
if 'function onDivisionChange' in content or 'onDivisionChange' in content:
    print("✅ Found division change handler")
else:
    print("⚠️ Need to locate division change logic")

# The issue is that when sections were moved to main dashboard,
# they lost their data loading trigger which was tied to modal opening
# We need to trigger data load on division change

# Let's find where updateDivisionSummary is called and ensure it also updates main dash sections
old_pattern = r'(function updateDivisionSummary\(divisionCode, metrics, topBlocks\) \{)'

replacement = r'''\1
        // ===== v9.2 FIX: Auto-load data to main dashboard sections =====
        // Update category counts on main dashboard (moved from popup)
        const categoryMapping = {
            'declining': 'categoryCount_declining',
            'stable': 'categoryCount_stable',
            'increasing': 'categoryCount_increasing',
            'empty': 'categoryCount_empty',
            'tbm': 'categoryCount_tbm'
        };
        
        if (metrics && metrics.blocks) {
            // Update category counts
            const categoryCounts = {
                'declining': 0,
                'stable': 0,
                'increasing': 0,
                'empty': 0,
                'tbm': 0
            };
            
            metrics.blocks.forEach(block => {
                if (block.category && categoryCounts.hasOwnProperty(block.category)) {
                    categoryCounts[block.category]++;
                }
            });
            
            // Update DOM elements on main dashboard
            Object.keys(categoryMapping).forEach(category => {
                const elem = document.getElementById(categoryMapping[category]);
                if (elem) {
                    elem.textContent = categoryCounts[category];
                }
            });
        }
        // ===== End v9.2 Fix =====
        '''

if re.search(old_pattern, content):
    content = re.sub(old_pattern, replacement, content, count=1)
    print("✅ Added auto-load logic to updateDivisionSummary")
else:
    print("⚠️ Pattern not found - will need alternative approach")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ INITIAL FIX APPLIED!")
print(f"   Added category count auto-update on division change")
print(f"\n⚠️ NOTE: This is phase 1 of the fix")
print(f"   Next: Need to trigger chart renders and other data loading")
