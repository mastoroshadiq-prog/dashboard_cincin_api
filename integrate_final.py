"""
Final integration: Add clickable blocks + modals to DASHBOARD_DEMO_FEATURES.html
"""

# Read all components
with open('paparan_section_clickable.html', 'r', encoding='utf-8') as f:
    paparan = f.read()

with open('statistik_section_clickable.html', 'r', encoding='utf-8') as f:
    statistik = f.read()

with open('block_detail_modals.html', 'r', encoding='utf-8') as f:
    modals = f.read()

with open('block_modals_js.txt', 'r', encoding='utf-8') as f:
    modal_js = f.read()

# Read demo file
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("Integrating components...")

# 1. Replace PAPARAN section
old_paparan_marker = '''<div class="space-y-2 max-h-96 overflow-y-auto custom-scrollbar">'''
paparan_idx = demo.find(old_paparan_marker)

if paparan_idx > 0:
    # Find end of this section (next closing div)
    end_idx = demo.find('</div>\n                </div>', paparan_idx) + len('</div>')
    
    # Replace
    new_paparan = f'''{old_paparan_marker}
{paparan}
                    </div'''
    
    demo = demo[:paparan_idx] + new_paparan + demo[end_idx:]
    print("✅ PAPARAN section replaced with clickable version")

# 2. Replace STATISTIK section (find the second occurrence)
statistik_marker = '''<div class="space-y-2 max-h-96 overflow-y-auto custom-scrollbar">'''
first_idx = demo.find(statistik_marker)
second_idx = demo.find(statistik_marker, first_idx + 100)

if second_idx > 0:
    end_idx = demo.find('</div>\n                </div>', second_idx) + len('</div>')
    
    new_statistik = f'''{statistik_marker}
{statistik}
                    </div'''
    
    demo = demo[:second_idx] + new_statistik + demo[end_idx:]
    print("✅ STATISTIK section replaced with clickable version")

# 3. Add modals before closing </body>
body_close = demo.rfind('</body>')
demo = demo[:body_close] + modals + '\n    ' + demo[body_close:]
print("✅ Block detail modals added")

# 4. Add JavaScript before closing </script>
script_close = demo.rfind('</script>')
demo = demo[:script_close] + '\n        // Block Detail Modals\n        ' + modal_js + '\n    ' + demo[script_close:]
print("✅ Modal JavaScript added")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print("\n✅ DASHBOARD_DEMO_FEATURES.html UPDATED!")
print(f"   File size: {len(demo)} chars")
print("\nFEATURES:")
print("   ✅ Clickable blocks in PAPARAN RISK")
print("   ✅ Clickable blocks in STATISTIK BLOK")
print("   ✅ Detail modals for all 8 blocks")
print("   ✅ Full metrics display (Potensi, Realisasi, Gap, SPH, etc.)")
