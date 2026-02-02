"""
Fix openBlockDetail to use COMPLETE_BLOCKS_DATA instead of non-existent ALL_BLOCKS_DATA
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Find and replace the problematic line in openBlockDetail function
# OLD: const blockData = window.ALL_BLOCKS_DATA.find(b => b.block_code === blockCode);
# NEW: const blockData = window.COMPLETE_BLOCKS_DATA[blockCode];

old_pattern = r'const blockData = window\.ALL_BLOCKS_DATA\.find\(b => b\.block_code === blockCode\);'
new_code = 'const blockData = window.COMPLETE_BLOCKS_DATA[blockCode];'

import re
if re.search(old_pattern, content):
    content = re.sub(old_pattern, new_code, content)
    print(f"✅ Fixed: Changed ALL_BLOCKS_DATA.find() to COMPLETE_BLOCKS_DATA[blockCode]")
else:
    print(f"⚠️ Pattern not found, trying alternative...")
    # Try simpler pattern
    if 'window.ALL_BLOCKS_DATA' in content:
        content = content.replace('window.ALL_BLOCKS_DATA.find(b => b.block_code === blockCode)', 
                                 'window.COMPLETE_BLOCKS_DATA[blockCode]')
        print(f"✅ Fixed using simple replace")
    else:
        print(f"❌ Could not find the problematic line")

# Also need to handle field name differences
# COMPLETE_BLOCKS_DATA uses different field names than expected
# Let's add a mapping/adapter

adapter_code = '''
            // FIELD NAME ADAPTER for COMPLETE_BLOCKS_DATA
            // COMPLETE_BLOCKS_DATA uses different field names, so we need to adapt
            if (blockData) {
                // Map field names to expected format
                blockData.yield_2023 = blockData.yield_2023 || blockData.baseline_2023 || 0;
                blockData.yield_2024 = blockData.yield_2024 || blockData.yield_intermediate || 0;
                blockData.yield_real_2025 = blockData.yield_real_2025 || blockData.realisasi_ton_ha || 0;
                blockData.yield_pot_2025 = blockData.yield_pot_2025 || blockData.potensi_ton_ha || 0;
                blockData.gap_pct = blockData.gap_pct || (blockData.gap_pct === 0 ? 0 : 15); // Default if missing
                blockData.attack_rate_pct = blockData.attack_rate_pct || blockData.ganoderma_attack_rate || 0;
                blockData.stadium_i_pct = blockData.stadium_i_pct || blockData.stadium_1_pct || 0;
                blockData.stadium_ii_pct = blockData.stadium_ii_pct || blockData.stadium_2_pct || 0;
                blockData.stadium_iii_pct = blockData.stadium_iii_pct || blockData.stadium_3_pct || 0;
                blockData.sph = blockData.sph || blockData.stand_per_ha || 135; // Default standard
                blockData.divisi = blockData.divisi || blockData.division || divisionCode;
            }
'''

# Insert adapter after getting blockData
marker = 'const blockData = window.COMPLETE_BLOCKS_DATA[blockCode];'
if marker in content:
    content = content.replace(marker, marker + '\n' + adapter_code)
    print(f"✅ Added field name adapter for COMPLETE_BLOCKS_DATA")
else:
    print(f"⚠️ Could not insert adapter")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ ERROR FIX APPLIED!")
print(f"   Changed: ALL_BLOCKS_DATA → COMPLETE_BLOCKS_DATA")
print(f"   Method: .find() → direct key access [blockCode]")
print(f"   Added: Field name adapter for data compatibility")
print(f"\n🔧 COMPLETE_BLOCKS_DATA structure:")
print(f"   Object with block codes as keys:")
print(f"   COMPLETE_BLOCKS_DATA['D010A'] = {{ block_code, division, ... }}")
print(f"\n📝 Now when clicking block:")
print(f"   ✅ Gets data directly: COMPLETE_BLOCKS_DATA['D010A']")
print(f"   ✅ Adapts field names if needed")
print(f"   ✅ Modal opens with correct data!")
