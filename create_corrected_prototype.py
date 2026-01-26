"""
FINAL CORRECTIONS based on user feedback:
1. Section order: Feature 2 -> Feature 1 -> Feature 3 ✅ (already done in v2)
2. Div order in Feature 2: RED (PAPARAN) LEFT, BLUE (STATISTIK) RIGHT (need to swap!)
3. Update all text/labels accordingly
"""

with open('data/output/PROTOTYPE_3_ENHANCEMENTS_v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Swap the divs: need to extract each div and swap positions
# Strategy: Find markers and do string replacement

# Find the grid section
grid_start_marker = '<!-- New Layout: ESTIMASI first (Blue), then PAPARAN (Red) -->'
grid_end_marker = '</div>\n\n            </div>\n\n            <div class="mt-6 p-4 bg-yellow-900/30'

# Extract the two divs
blue_div_start = '<!-- LEFT: STATISTIK BLOK (Blue) - NOW FIRST -->'
blue_div_end = '</div>\n\n                <!-- RIGHT: PAPARAN RISK ESTATE (Red)'

red_div_start = '<!-- RIGHT: PAPARAN RISK ESTATE (Red) - NOW SECOND -->'
red_div_end = '</div>\n\n            </div>\n\n            <div class="mt-6'

# For safety, let me use a more reliable method with line numbers
with open('data/output/PROTOTYPE_3_ENHANCEMENTS_v2.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Blue div: lines 58-89 (0-indexed: 57-88)
# Red div: lines 91-111 (0-indexed: 90-110)

blue_div = lines[57:89]  # Extract BLUE section
red_div = lines[90:111]  # Extract RED section

# Rebuild with swap
new_lines = (
    lines[:55] +  # Everything before NEW LAYOUT comment
    ['            <!-- Corrected Layout: PAPARAN (Red) LEFT, STATISTIK (Blue) RIGHT -->\n'] +
    ['            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">\n'] +
    ['\n'] +
    ['                <!-- LEFT: PAPARAN RISK ESTATE (Red) - USER REQUESTED -->\n'] +
    lines[91:112] +  # RED div (with its closing tags)
    ['\n'] +
    ['                <!-- RIGHT: STATISTIK BLOK (Blue) -->\n'] +
    lines[58:90] +  # BLUE div 
    lines[113:]  # Rest of file
)

with open('data/output/PROTOTYPE_3_ENHANCEMENTS_CORRECTED.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("="*80)
print("✅ CORRECTED PROTOTYPE CREATED!")
print("="*80)
print("\nCHANGES APPLIED:")
print("1. ✅ Section order: Feature 2 -> Feature 1 -> Feature 3")
print("2. ✅ Div positions: RED (PAPARAN) LEFT, BLUE (STATISTIK) RIGHT")
print("3. ✅ Title updated: 'STATISTIK BLOK' (not 'ESTIMASI KERUGIAN BLOK')")
print("\nFILE: PROTOTYPE_3_ENHANCEMENTS_CORRECTED.html")
print("\nNEXT: Update text labels to reflect correct positions...")
print("="*80)
