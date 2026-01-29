"""
Phase 1: Insert sections into main dashboard
Careful line-by-line approach
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Define sections to extract with exact line numbers (1-indexed)
# Visual Analysis: lines 18697-18773
visual_start = 18697 - 1  # Convert to 0-indexed
visual_end = 18773
visual_section = lines[visual_start:visual_end]

print(f"✅ Extracted Visual Analysis: {len(visual_section)} lines")

# Loss Analysis: lines 18776-18985
loss_start = 18776 - 1
loss_end = 18985
loss_section = lines[loss_start:loss_end]

print(f"✅ Extracted Loss Analysis: {len(loss_section)} lines")

# 5-Year Trend: lines 18987-19086
trend_start = 18987 - 1
trend_end = 19086
trend_section = lines[trend_start:trend_end]

print(f"✅ Extracted 5-Year Trend: {len(trend_section)} lines")

# Create wrapper sections for main dashboard
new_sections = []

# Add Visual Analysis with header
new_sections.append('\n')
new_sections.append('            <!-- ================================================ -->\n')
new_sections.append('            <!-- PRODUCTION TREND OVERVIEW (Moved from Popup) -->\n')
new_sections.append('            <!-- ================================================ -->\n')
new_sections.append('            <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-6 border-2 border-cyan-500/30 shadow-2xl">\n')
new_sections.append('                <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">\n')
new_sections.append('                    <span class="text-3xl">📊</span>\n')
new_sections.append('                    PRODUCTION TREND OVERVIEW - AME II\n')
new_sections.append('                </h2>\n')
new_sections.extend(visual_section)
new_sections.append('            </div>\n')
new_sections.append('\n')

# Add Loss Analysis (already has its own wrapper)
new_sections.append('            <!-- ================================================ -->\n')
new_sections.append('            <!-- LOSS ANALYSIS DASHBOARD (Moved from Popup) -->\n')
new_sections.append('            <!-- ================================================ -->\n')
new_sections.extend(loss_section)
new_sections.append('\n')

# Add 5-Year Trend (already has its own wrapper)
new_sections.append('            <!-- ================================================ -->\n')
new_sections.append('            <!-- 5-YEAR TREND ANALYSIS (Moved from Popup) -->\n')
new_sections.append('            <!-- ================================================ -->\n')
new_sections.extend(trend_section)
new_sections.append('\n')

print(f"✅ Created new sections: {len(new_sections)} lines")

# Insert after line 466 (0-indexed = 466)
insertion_point = 466

# Split the file
before_insertion = lines[:insertion_point]
after_insertion = lines[insertion_point:]

# Combine
new_content = before_insertion + new_sections + after_insertion

print(f"✅ New total lines: {len(new_content)}")
print(f"   Added: {len(new_sections)} lines")
print(f"   Expected: {len(lines) + len(new_sections)}")

# Write to new file
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print(f"\n✅ PHASE 1 STEP 1 COMPLETE!")
print(f"   Inserted 3 sections into main dashboard at line 467")
print(f"   Visual Analysis: {len(visual_section)} lines")
print(f"   Loss Analysis: {len(loss_section)} lines")
print(f"   5-Year Trend: {len(trend_section)} lines")
print(f"\n⚠️ NOTE: Popup still contains these sections (will remove in Phase 2)")
