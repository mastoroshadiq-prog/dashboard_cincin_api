"""
IMPLEMENT INTERACTIVE BREAKDOWN + FIX SATUAN (MILIAR)
- Insert breakdown modals
- Update metrics jadi clickable
- Fix satuan: Juta → Miliar (untuk angka >= 1000 Juta)
"""

print("="*80)
print("IMPLEMENTING INTERACTIVE BREAKDOWN WITH CORRECT UNITS")
print("="*80)

# Read HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read breakdown modals component
with open('data/output/breakdown_modals_component.html', 'r', encoding='utf-8') as f:
    modals_html = f.read()

print("\n✅ Files loaded")

# Step 1: Insert modals before </body>
body_close_pos = html_content.rfind('</body>')
if body_close_pos > 0:
    html_updated = (html_content[:body_close_pos] + 
                   '\n    ' + modals_html + '\n' +
                   html_content[body_close_pos:])
    print("✅ Modals inserted before </body>")
else:
    print("⚠️  Could not find </body> tag")
    html_updated = html_content

# Step 2: Update satuan dari Juta ke Miliar untuk angka besar (>= 1000 Juta)
# Current Loss: 1,353 Juta → 1.35 Miliar
# 3-Year: 6,204 Juta → 6.2 Miliar  
# Treatment: 400 Juta → 0.4 Miliar (atau tetap 400 Juta untuk clarity)
# Savings: 4,343 Juta → 4.3 Miliar

print("\n📝 Updating units to Miliar...")

# Find and update Cost of Inaction component
replacements = [
    # Current Loss
    ('Rp 1,353', 'Rp 1.35'),
    ('1,353 Juta', '1.35 Miliar'),
    
    # 3-Year Loss
    ('Rp 6,204', 'Rp 6.2'),
    ('6,204 Juta', '6.2 Miliar'),
    
    # Treatment Cost - Keep as Juta for clarity (400 Juta lebih jelas daripada 0.4 Miliar)
    # No change
    
    # Savings
    ('Rp 4,343', 'Rp 4.3'),
    ('4,343 Juta', '4.3 Miliar'),
    
    # Also update in modals
    ('Total Kerugian Saat Ini:</div>\n                <div class="text-4xl font-black text-white">Rp 1,353 Juta/tahun', 
     'Total Kerugian Saat Ini:</div>\n                <div class="text-4xl font-black text-white">Rp 1.35 Miliar/tahun'),
    
    ('Total Proyeksi 3 Tahun (TANPA Treatment):</div>\n                <div class="text-4xl font-black text-white">Rp 6,204 Juta',
     'Total Proyeksi 3 Tahun (TANPA Treatment):</div>\n                <div class="text-4xl font-black text-white">Rp 6.2 Miliar'),
    
    ('Potensi Penghematan 3 Tahun:</div>\n                <div class="text-4xl font-black text-white">Rp 4,343 Juta',
     'Potensi Penghematan 3 Tahun:</div>\n                <div class="text-4xl font-black text-white">Rp 4.3 Miliar'),
]

for old, new in replacements:
    if old in html_updated:
        html_updated = html_updated.replace(old, new)
        print(f"   ✓ Updated: {old[:40]}...")

# Step 3: Make metrics clickable - Update specific divs
print("\n🖱️  Making metrics clickable...")

# Find and update each metric div to add onclick and hover styling
metrics_updates = [
    # Kerugian Saat Ini
    {
        'find': '<div class="text-3xl font-black text-white">Rp 1.35</div>',
        'replace': '<div class="text-3xl font-black text-white cursor-pointer hover:text-rose-300 transition-all hover:scale-105" onclick="showBreakdown(\'breakdownCurrentLoss\')" title="Klik untuk detail breakdown">Rp 1.35 <span class="text-lg opacity-60">ℹ️</span></div>'
    },
    # Proyeksi 3 Tahun
    {
        'find': '<div class="text-3xl font-black text-white">Rp 6.2</div>',
        'replace': '<div class="text-3xl font-black text-white cursor-pointer hover:text-orange-300 transition-all hover:scale-105" onclick="showBreakdown(\'breakdown3YearLoss\')" title="Klik untuk detail breakdown">Rp 6.2 <span class="text-lg opacity-60">ℹ️</span></div>'
    },
    # Treatment Investment
    {
        'find': '<div class="text-3xl font-black text-white">Rp 400</div>',
        'replace': '<div class="text-3xl font-black text-white cursor-pointer hover:text-emerald-300 transition-all hover:scale-105" onclick="showBreakdown(\'breakdownTreatmentCost\')" title="Klik untuk detail breakdown">Rp 400 <span class="text-lg opacity-60">ℹ️</span></div>'
    },
    # Potential Savings
    {
        'find': '<div class="text-3xl font-black text-white">Rp 4.3</div>',
        'replace': '<div class="text-3xl font-black text-white cursor-pointer hover:text-cyan-300 transition-all hover:scale-105" onclick="showBreakdown(\'breakdownSavings\')" title="Klik untuk detail breakdown">Rp 4.3 <span class="text-lg opacity-60">ℹ️</span></div>'
    },
    # ROI
    {
        'find': '<div class="text-4xl font-black text-yellow-400">986%</div>',
        'replace': '<div class="text-4xl font-black text-yellow-400 cursor-pointer hover:text-yellow-300 transition-all hover:scale-105" onclick="showBreakdown(\'breakdownROI\')" title="Klik untuk detail breakdown">986% <span class="text-xl opacity-60">ℹ️</span></div>'
    },
]

for update in metrics_updates:
    if update['find'] in html_updated:
        html_updated = html_updated.replace(update['find'], update['replace'])
        print(f"   ✓ Made clickable: {update['find'][:40]}...")

# Step 4: Update label units in Cost of Inaction section
label_updates = [
    ('Juta / tahun', 'Miliar / tahun'),
    ('Juta (dengan degradasi)', 'Miliar (dengan degradasi)'),
    ('Juta (dicegah 3 tahun)', 'Miliar (dicegah 3 tahun)'),
]

for old_label, new_label in label_updates:
    if old_label in html_updated:
        html_updated = html_updated.replace(old_label, new_label)
        print(f"   ✓ Updated label: {old_label} → {new_label}")

# Save updated HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html_updated)

print("\n" + "="*80)
print("✅ IMPLEMENTATION COMPLETE!")
print("="*80)
print("\nChanges Applied:")
print("1. ✅ Breakdown modals inserted before </body>")
print("2. ✅ Satuan updated: Juta → Miliar (untuk angka >= 1 Miliar)")
print("   - Kerugian Saat Ini: Rp 1.35 Miliar/tahun")
print("   - Proyeksi 3 Tahun: Rp 6.2 Miliar")
print("   - Treatment: Rp 400 Juta (tetap Juta untuk clarity)")
print("   - Penghematan: Rp 4.3 Miliar")
print("3. ✅ Metrics made clickable with ℹ️ icon")
print("4. ✅ Hover effects added (scale up, color change)")
print("\nReady to test!")
print("Try clicking: Rp 1.35 Miliar → Modal dengan breakdown detail")
print("="*80)
