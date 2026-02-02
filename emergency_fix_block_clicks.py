"""
Emergency Fix: Add onclick handlers directly to existing block items
Search for block item HTML generation and add onclick attribute
"""

import re

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"📖 Total lines: {len(lines)}")

# Search for lines that might be rendering block items
# Pattern: HTML for block items that show block code and percentage

print("\n🔍 Searching for block item rendering...")

found_count = 0
for i, line in enumerate(lines):
    # Look for patterns that might be block item HTML
    if ('block_code' in line.lower() or 'blockcode' in line.lower()) and ('innerHTML' in line or '+=' in line):
        print(f"   Line {i+1}: {line[:80].strip()}")
        found_count += 1
        if found_count >= 5:
            break

if found_count == 0:
    print("   ❌ No obvious block rendering code found in simple search")
    print("\n   Let's add a generic onclick updater function instead...")

# Strategy: Add a function that updates ALL block items after they're rendered
# This function will run after the modal opens and add onclick handlers

onclick_updater = '''
        /**
         * Add onclick handlers to all block items in production trend modal
         * Called after blocks are rendered in modal
         */
        function addBlockClickHandlers() {
            console.log('[BLOCK DRILL-DOWN] Adding click handlers to block items...');
            
            // Find all block containers
            const containers = [
                'decliningBlocksList',
                'stableBlocksList', 
                'increasingBlocksList',
                'emptyBlocksList',
                'tbmBlocksList'
            ];
            
            let totalHandlers = 0;
            
            containers.forEach(containerId => {
                const container = document.getElementById(containerId);
                if (!container) return;
                
                // Find all block items (divs that might contain block codes)
                const items = container.querySelectorAll('div[class*="bg-"]');
                
                items.forEach(item => {
                    // Try to find block code in text content
                    const text = item.textContent || '';
                    const blockCodeMatch = text.match(/([A-Z]\\d{3,4}[A-Z]?)/);
                    
                    if (blockCodeMatch) {
                        const blockCode = blockCodeMatch[1];
                        
                        // Add onclick if not already present
                        if (!item.onclick) {
                            item.style.cursor = 'pointer';
                            item.onclick = function(e) {
                                e.stopPropagation();
                                const divisionCode = window.currentDivision || 'AME02';
                                openBlockDetail(blockCode, divisionCode);
                            };
                            
                            // Add hover effect
                            item.classList.add('hover:scale-105', 'transition-transform');
                            
                            totalHandlers++;
                        }
                    }
                });
            });
            
            console.log(`[BLOCK DRILL-DOWN] Added ${totalHandlers} click handlers`);
        }
        
        // Also modify the modal open function to call this
        const originalOpenBlockModal = window.openBlockBreakdownModal;
        if (originalOpenBlockModal) {
            window.openBlockBreakdownModal = function(divisionCode) {
                originalOpenBlockModal(divisionCode);
                
                // Wait for blocks to render, then add handlers
                setTimeout(() => {
                    addBlockClickHandlers();
                }, 500);
            };
        }
'''

# Find where to insert this - look for other block-related functions
insert_pos = -1
for i, line in enumerate(lines):
    if 'function openBlockDetail' in line:
        insert_pos = i
        break

if insert_pos > 0:
    lines.insert(insert_pos, onclick_updater + '\n')
    print(f"\n✅ Inserted onclick updater function at line {insert_pos}")
else:
    # Insert before </script>
    for i in range(len(lines)-1, -1, -1):
        if '</script>' in lines[i]:
            lines.insert(i, onclick_updater + '\n')
            print(f"\n✅ Inserted onclick updater function before </script> at line {i}")
            break

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ EMERGENCY FIX APPLIED!")
print(f"   Added: addBlockClickHandlers() function")
print(f"   This will automatically add onclick to ALL block items")
print(f"   Runs 500ms after modal opens to ensure blocks are rendered")
print(f"\n🔧 How it works:")
print(f"   1. Modal opens → blocks render")
print(f"   2. After 500ms → addBlockClickHandlers() runs")
print(f"   3. Searches for all divs with block codes (D010A, F004A, etc)")
print(f"   4. Adds onclick handler: openBlockDetail(blockCode, division)")
print(f"   5. User clicks block → Detail modal opens!")
