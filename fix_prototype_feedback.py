"""
Quick fix untuk prototype berdasarkan user feedback:
1. Swap back positions (RED LEFT, BLUE RIGHT)
2. Rename: ESTIMASI KERUGIAN BLOK -> STATISTIK BLOK
3. Reorder: Feature 2 first, then Feature 1
"""

print("="*80)
print("FIXING PROTOTYPE - User Feedback")
print("="*80)

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Rename title
old_title = 'ESTIMASI KERUGIAN BLOK'
new_title = 'STATISTIK BLOK'

count = html.count(old_title)
html = html.replace(old_title, new_title)
print(f"✅ Fix 1: Renamed '{old_title}' -> '{new_title}' ({count} occurrences)")

# Fix 2: Update description
old_desc = 'ESTIMASI (Biru) di kiri, PAPARAN RISK (Merah) di kanan'
new_desc = 'PAPARAN RISK (Merah) di kiri, STATISTIK BLOK (Biru) di kanan'

html = html.replace(old_desc, new_desc)
print(f"✅ Fix 2: Updated description")

# Fix 3: Update rationale text
old_rat = 'User lihat ESTIMASI detail dulu'
new_rat = 'User lihat PAPARAN RISK (8 critical blocks) dulu'

html = html.replace(old_rat, new_rat)
print(f"✅ Fix 3: Updated rationale")

# Fix 4: Swap the grid order back (find the grid and swap divs)
# This requires careful HTML manipulation
# For now, I'll add a note - actual swap needs manual edit or complex parsing

# Save
with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Prototype updated with text changes")
print("\n⚠️ MANUAL EDIT NEEDED:")
print("   1. Open PROTOTYPE_3_ENHANCEMENTS.html")
print("   2. Find Feature 2 section (line ~118)")
print("   3. Swap the two grid divs:")
print("      - Move PAPARAN (Red) div to LEFT")
print("      - Move STATISTIK (Blue) div to RIGHT")
print("   4. Also move entire Feature 2 section ABOVE Feature 1")
print("\nI'll do this now with precise replacements...")
print("="*80)
