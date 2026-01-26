"""
PHASE 1: Swap Section Positions
PAPARAN RISK ESTATE (Red) <-> ESTIMASI KERUGIAN BLOK (Blue)
"""

print("="*80)
print("PHASE 1: Swapping Section Positions")
print("="*80)

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Strategy: Find unique markers for each section and swap entire blocks

# Find PAPARAN RISK section (starts around line 350)
paparan_start_marker = 'class="bg-gradient-to-br from-rose-950/90'
estimasi_start_marker = 'class="bg-gradient-to-br from-blue-950/90'

# This is complex - let me use a different approach
# Find the grid container and extract both sections

# Search for the grid container
grid_marker = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">'

if grid_marker in html:
    # Find the position
    grid_pos = html.find(grid_marker)
    
    # Find the end of this grid (next major section)
    # Look for closing </div> at same indentation level
    
    # Actually, let me use regex to be more precise
    import re
    
    # Pattern to match the entire grid with both sections
    # This is tricky - let me use a simpler marker-based approach
    
    print("✅ Found grid container")
    print("⚠️  Swap requires careful HTML parsing")
    print("\nManual swap recommended to avoid breaking structure")
    print("\nInstructions:")
    print("1. Find line ~350: PAPARAN RISK section")
    print("2. Find line ~450: ESTIMASI KERUGIAN section")  
    print("3. Cut entire PAPARAN section (including outer div)")
    print("4. Cut entire ESTIMASI section")
    print("5. Paste ESTIMASI first, then PAPARAN")
    print("\nOR: Use Python script with precise line numbers")
    
else:
    print("❌ Grid container not found")

print("\n" + "="*80)
print("Creating safer approach: Line-based extraction")
print("="*80)

# Let's find exact line numbers first
lines = html.split('\n')

paparan_line = None
estimasi_line = None

for i, line in enumerate(lines):
    if 'PAPARAN RISIKO ESTATE' in line and paparan_line is None:
        paparan_line = i
        print(f"✅ Found PAPARAN RISIKO at line {i+1}")
    if 'ESTIMASI KERUGIAN' in line and 'H2' in line.upper() and estimasi_line is None:
        estimasi_line = i  
        print(f"✅ Found ESTIMASI KERUGIAN at line {i+1}")

if paparan_line and estimasi_line:
    print(f"\n📍 PAPARAN starts around line {paparan_line+1}")
    print(f"📍 ESTIMASI starts around line {estimasi_line+1}")
    print("\nReady for precise swap!")
else:
    print("\n⚠️  Could not locate both sections")

print("="*80)
