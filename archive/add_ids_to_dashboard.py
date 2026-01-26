"""
Quick script to add IDs to dashboard for interactivity
Focuses on key dynamic elements
"""
import re

print("Adding IDs to dashboard...")

# Read file
with open('data/output/dashboard_cincin_api_FINAL_CORRECTED.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define replacements (old_text, new_text_with_ID)
replacements = [
    # F008A section - Transform to generic dynamic section
    ('>2009 (17 Tahun)<', ' id="blockTT">2009 (17 Tahun)<'),
    ('>127 Pokok/Ha<', ' id="blockSPH">127 Pokok/Ha<'),
    ('>3,745 <span', ' id="blockTotalPohon">3,745 <span'),
    ('>142 <span class="text-xs uppercase">PKK<', ' id="blockSisip">142 <span class="text-xs uppercase">PKK<'),
    
    # Distribution stats (reuse for all blocks)
    ('>90 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockMerahCount">90 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
    ('>369 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockOranyeCount">369 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
    ('>141 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockKuningCount">141 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
    
    # Hide D001A section (we'll use F008A section as the dynamic one)
    ('<!-- SECTION DETAIL BLOK D001A -->', '<!-- SECTION DETAIL BLOK D001A (HIDDEN - Using F008A as dynamic) -->\n        <div style="display:none;">'),
]

# Apply replacements
for old, new in replacements:
    if old in html:
        html = html.replace(old, new, 1)  # Replace first occurrence only
        print(f"✅ Replaced: {old[:50]}...")
    else:
        print(f"⚠️  Not found: {old[:50]}...")

# Close the hidden D001A div (find end of D001A section)
# Add closing div before F008A PROYEKSI section
html = html.replace(
    '<!-- SECTION PETA KLUSTER CINCIN API -->',
    '</div>\n        <!-- SECTION PETA KLUSTER CINCIN API -->',
    1
)

# Save
with open('data/output/dashboard_cincin_api_FINAL_CORRECTED.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ IDs added successfully!")
print("Updated elements:")
print("  - blockTT, blockSPH, blockTotalPohon, blockSisip")
print("  - blockMerahCount, blockOranyeCount, blockKuningCount")
print("  - D001A section hidden (using F008A as dynamic template)")
