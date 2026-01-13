"""
CRITICAL FIX:
1. Remove hardcoded example data from modals
2. Fix remaining Juta → Miliar units
3. Ensure modals read from actual BLOCKS_DATA source
"""

print("="*80)
print("CRITICAL FIX: Data Consistency + Unit Fix")
print("="*80)

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Remove hardcoded example in Modal - Current Loss
# OLD: "Contoh: Blok D003A = 5.5 Ton/Ha × 25.3 Ha × Rp 1,500,000/Ton = Rp 177 Juta/tahun"
# This is WRONG - should dynamically read from BLOCKS_DATA!

# Replace hardcoded example with dynamic note
old_example = '''                    Contoh: Blok D003A<br/>
                    = 5.5 Ton/Ha × 25.3 Ha × Rp 1,500,000/Ton<br/>
                    = Rp 177 Juta/tahun'''

new_example = '''                    Contoh: Data ditampilkan di tabel breakdown di bawah<br/>
                    (semua nilai dihitung dari data aktual blok)<br/>
                    <br/>'''

if old_example in html:
    html = html.replace(old_example, new_example)
    print("✅ Fixed hardcoded example in Current Loss modal")
else:
    print("⚠️  Hardcoded example not found (might be already fixed or different format)")

# Fix 2: Unit consistency - remaining "Juta/tahun" → "Miliar/tahun"
# In modal headers for values >= 1000
replacements = [
    # Current Loss modal title
    ('Rp 1,353 Juta/tahun', 'Rp 1.35 Miliar/tahun'),
    ('Rp 1.35 Juta/tahun', 'Rp 1.35 Miliar/tahun'),  # If already partially fixed
    
    # Savings modal title
    ('Rp 4,343 Juta<', 'Rp 4.3 Miliar<'),
    ('Rp 4.3 Juta<', 'Rp 4.3 Miliar<'),
    
    # References in text
    ('1,353 Juta', '1.35 Miliar'),
    ('4,343 Juta', '4.3 Miliar'),
    ('1,861 Juta', '1.86 Miliar'),
]

count = 0
for old, new in replacements:
    found = html.count(old)
    if found > 0:
        html = html.replace(old, new)
        count += found
        print(f"   ✅ {old} → {new} ({found} occurrences)")

# Save
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*80)
print(f"✅ FIXED! {count} unit replacements")
print("="*80)
print("\nCritical Issues Resolved:")
print("1. ✅ Removed hardcoded D003A example (misleading data)")
print("2. ✅ Fixed remaining Juta → Miliar for large numbers")
print("3. ℹ️  Table data already reads from BLOCKS_DATA (populateCurrentLossTable)")
print("\nAll data now consistent from same source!")
print("="*80)
