"""
FIX UNIT CONSISTENCY IN MODALS
Update semua satuan Juta → Miliar di breakdown modals (untuk angka >= 1000 Juta)
"""

print("="*80)
print("FIXING UNIT CONSISTENCY IN MODALS")
print("="*80)

# Read dashboard HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("\n📝 Searching and replacing units...")

# All replacements untuk konsistensi Miliar
replacements = [
    # Modal: Current Loss
    ('Rp 1,353 Juta/tahun', 'Rp 1.35 Miliar/tahun'),
    
    # Modal: 3-Year Loss - Title
    ('Rp 6,204 Juta', 'Rp 6.2 Miliar'),
    
    # Modal: 3-Year Loss - Year breakdown
    ('Rp 1,353 Juta<', 'Rp 1.35 Miliar<'),  # In year 0 breakdown
    ('Rp 1,567 Juta<', 'Rp 1.57 Miliar<'),  # Year 1
    ('Rp 1,974 Juta<', 'Rp 1.97 Miliar<'),  # Year 2
    ('Rp 3,133 Juta<', 'Rp 3.13 Miliar<'),  # Year 3
    ('Rp 6,674 Juta<', 'Rp 6.67 Miliar<'),  # Total
    
    # Modal: Savings
    ('Rp 4,343 Juta<', 'Rp 4.3 Miliar<'),
    ('Rp 1,861 Juta', 'Rp 1.86 Miliar'),  # 30% not prevented
    
    # Text references
    ('Year 3 loss (Rp 3.1M)', 'Year 3 loss (Rp 3.1 Miliar)'),
    ('Year 1 (Rp 1.6M)', 'Year 1 (Rp 1.6 Miliar)'),
    ('Angka Rp 4.3 Miliar', 'Angka Rp 4.3 Miliar'),  # Already correct
    
    # Note variations
    ('*Dashboard shows Rp 6,204 (slight calculation variation)', 
     '*Dashboard shows Rp 6.2 Miliar (slight calculation variation)'),
]

count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        count += 1
        print(f"   ✓ {old[:50]}... → {new[:50]}...")
    else:
        print(f"   ⚠️  Not found: {old[:50]}...")

# Save
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*80)
print(f"✅ FIXED! {count} replacements made")
print("="*80)
print("\nNow consistent:")
print("- Dashboard: Rp 6.2 Miliar")
print("- Modal: Rp 6.2 Miliar")
print("\nNo more confusion!")
print("="*80)
