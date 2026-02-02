"""
Part 2: Add click handlers to block items in the production trend modal
Update the block rendering to call openBlockDetail() when clicked
"""

import re

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# We need to find where block items are generated
# They are likely rendered dynamically in JavaScript
# Let's add a pattern to find and update block item rendering

# Pattern 1: Find block rendering in forEach loops or similar
# Look for patterns like: innerHTML += `<div class="...block...">${blockCode}</div>`

print("\n🔍 Searching for block rendering code...")

# Since we don't know the exact pattern, let's add a generic function
# that can be called to render a clickable block item

clickable_block_renderer = '''
        /**
         * Render clickable block item for production trend modal
         * @param {object} block - Block data object
         * @param {string} category - Category: declining, stable, increasing, etc
         * @returns {string} HTML string for block item
         */
        function renderClickableBlockItem(block, category) {
            const blockCode = block.block_code || block.code_block || 'UNKNOWN';
            const divisionCode = block.divisi || block.division || 'AME02';
            
            // Calculate trend percentage
            const yield2023 = block.yield_2023 || 0;
            const yield2025 = block.yield_real_2025 || 0;
            const trendPct = yield2023 > 0 ? ((yield2025 - yield2023) / yield2023 * 100) : 0;
            
            // Color based on category
            const colors = {
                declining: { bg: 'bg-red-900/20', border: 'border-red-500/30', text: 'text-red-400', hover: 'hover:bg-red-900/40' },
                stable: { bg: 'bg-orange-900/20', border: 'border-orange-500/30', text: 'text-orange-400', hover: 'hover:bg-orange-900/40' },
                increasing: { bg: 'bg-green-900/20', border: 'border-green-500/30', text: 'text-green-400', hover: 'hover:bg-green-900/40' },
                empty: { bg: 'bg-gray-900/20', border: 'border-gray-500/30', text: 'text-gray-400', hover: 'hover:bg-gray-900/40' },
                tbm: { bg: 'bg-yellow-900/20', border: 'border-yellow-500/30', text: 'text-yellow-400', hover: 'hover:bg-yellow-900/40' }
            };
            
            const color = colors[category] || colors.stable;
            
            return `
                <div class="${color.bg} ${color.border} ${color.hover} rounded-lg p-3 mb-2 border cursor-pointer transition-all hover:scale-105 hover:shadow-lg"
                     onclick="openBlockDetail('${blockCode}', '${divisionCode}')">
                    <div class="flex items-center justify-between">
                        <div class="font-bold ${color.text} text-sm">${blockCode}</div>
                        <div class="font-black ${color.text} text-lg">${trendPct >= 0 ? '+' : ''}${trendPct.toFixed(1)}%</div>
                    </div>
                    <div class="text-xs text-slate-400 mt-1">
                        ${yield2023.toFixed(1)} → ${yield2025.toFixed(1)} T/Ha
                    </div>
                </div>
            `;
        }
'''

# Insert this function into the JavaScript section
script_tag = content.rfind('<script>')
if script_tag != -1:
    # Find position after <script> opening tag
    insert_pos = content.find('\n', script_tag) + 1
    content = content[:insert_pos] + clickable_block_renderer + '\n' + content[insert_pos:]
    print(f"✅ Added renderClickableBlockItem() function")
else:
    print(f"⚠️ Could not find <script> tag")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ CLICK HANDLER FUNCTION ADDED!")
print(f"   Function: renderClickableBlockItem(block, category)")
print(f"   Returns: HTML for clickable block item")
print(f"   Click action: openBlockDetail(blockCode, divisionCode)")
print(f"\n📝 Note: You may need to manually update existing block rendering")
print(f"   to use this new function instead of generating HTML directly")
