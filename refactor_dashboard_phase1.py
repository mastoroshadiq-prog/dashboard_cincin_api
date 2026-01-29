"""
Dashboard Refactoring Script - Phase 1
Move sections from popup to main dashboard for better UX
"""

import re

# Read the HTML file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
output_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 Reading HTML file...")
print(f"   File size: {len(content):,} characters")

# Find insertion point in main dashboard (after historical trends section, line ~466)
insertion_marker = '<div class="max-w-7xl mx-auto space-y-8">'
if insertion_marker not in content:
    print("❌ ERROR: Insertion marker not found!")
    exit(1)

print(f"✅ Found insertion point")

# Extract Visual Analysis section (5 category cards) from popup
# This is between lines ~18698 and ~18773
visual_analysis_pattern = r'(<!-- Category Cards Grid - 5 COLUMNS -->.*?</div>\s*<!-- TBM \(NEW CARD\) -->.*?</div>\s*</div>)'
visual_match = re.search(visual_analysis_pattern, content, re.DOTALL)

if not visual_match:
    print("❌ ERROR: Visual Analysis section not found!")
    exit(1)

visual_analysis_section = visual_match.group(1)
print(f"✅ Extracted Visual Analysis section ({len(visual_analysis_section)} chars)")

# Extract Loss Analysis section from popup
# This is between lines ~18776 and ~18985
loss_analysis_pattern = r'(<!-- AME II LOSS ANALYSIS SECTION -->.*?<!-- 5-YEAR TREND ANALYSIS)'
loss_match = re.search(loss_analysis_pattern, content, re.DOTALL)

if not loss_match:
    print("❌ ERROR: Loss Analysis section not found!")
    exit(1)

loss_analysis_section = loss_match.group(1).replace('<!-- 5-YEAR TREND ANALYSIS', '')
print(f"✅ Extracted Loss Analysis section ({len(loss_analysis_section)} chars)")

# Extract 5-Year Trend Analysis section from popup
# This is between lines ~18987 and ~19086
trend_5year_pattern = r'(<!-- 5-YEAR TREND ANALYSIS \(2023-2027\) -->.*?</div>\s*<!-- Search Box -->)'
trend_match = re.search(trend_5year_pattern, content, re.DOTALL)

if not trend_match:
    print("❌ ERROR: 5-Year Trend Analysis section not found!")
    exit(1)

trend_5year_section = trend_match.group(1).replace('<!-- Search Box -->', '')
print(f"✅ Extracted 5-Year Trend Analysis section ({len(trend_5year_section)} chars)")

# Create new main dashboard sections
new_main_sections = f'''
        <!-- ============================================ -->
        <!-- PRODUCTION TREND OVERVIEW (Moved from Popup) -->
        <!-- ============================================ -->
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-6 border-2 border-cyan-500/30 shadow-2xl">
            <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                <span class="text-3xl">📊</span>
                PRODUCTION TREND OVERVIEW - AME II
            </h2>
            {visual_analysis_section}
        </div>

        {loss_analysis_section}

        {trend_5year_section}
'''

# Insert new sections into main dashboard
parts = content.split(insertion_marker, 1)
if len(parts) != 2:
    print("❌ ERROR: Could not split content at insertion point!")
    exit(1)

new_content = parts[0] + insertion_marker + new_main_sections + parts[1]

print(f"✅ Inserted sections into main dashboard")

# Now remove these sections from the popup
# We'll keep the popup header, search box, and block lists only

# Remove Visual Analysis from popup
new_content = re.sub(
    r'<!-- Category Cards Grid - 5 COLUMNS -->.*?</div>\s*<!-- ======================================== -->',
    '<!-- Visual Analysis moved to main dashboard -->\n\n                    <!-- ======================================== -->',
    new_content,
    flags=re.DOTALL
)

print(f"✅ Removed Visual Analysis from popup")

# Remove Loss Analysis from popup  
new_content = re.sub(
    r'<!-- AME II LOSS ANALYSIS SECTION -->.*?<!-- 5-YEAR TREND ANALYSIS',
    '<!-- Loss Analysis moved to main dashboard -->\n\n                    <!-- 5-YEAR TREND ANALYSIS',
    new_content,
    flags=re.DOTALL
)

print(f"✅ Removed Loss Analysis from popup")

# Remove 5-Year Trend from popup
new_content = re.sub(
    r'<!-- 5-YEAR TREND ANALYSIS \(2023-2027\) -->.*?<!-- Search Box -->',
    '<!-- 5-Year Trend moved to main dashboard -->\n\n                    <!-- Search Box -->',
    new_content,
    flags=re.DOTALL
)

print(f"✅ Removed 5-Year Trend from popup")

# Write the new content
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ PHASE 1 COMPLETE!")
print(f"   Output file: {output_file}")
print(f"   New file size: {len(new_content):,} characters")
print(f"\n📊 Summary:")
print(f"   ✓ Moved Visual Analysis (5 cards) to main dashboard")
print(f"   ✓ Moved Loss Analysis to main dashboard")
print(f"   ✓ Moved 5-Year Trend Analysis to main dashboard")
print(f"   ✓ Simplified popup to show only block lists")
