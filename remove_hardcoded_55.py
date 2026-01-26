"""
FINAL FIX - Direct string replacement in dashboard HTML
Remove hardcoded D003A example with wrong Gap (5.5 instead of 4.66)
"""

print("="*80)
print("FINAL FIX: Remove hardcoded 5.5 Ton/Ha from dashboard")
print("="*80)

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Exact search for the problematic lines
if "= 5.5 Ton/Ha" in html:
    print("✅ Found '5.5 Ton/Ha' - fixing now...")
    
    # Replace the entire example block
    old_text = """                            Contoh: Blok D003A<br />
                            = 5.5 Ton/Ha × 25.3 Ha × Rp 1,500,000/Ton<br />
                            = Rp 177 Juta/tahun"""
    
    new_text = """                            <em class="text-gray-400">(Lihat tabel breakdown di bawah untuk data actual per blok)</em><br />
                            <br />"""
    
    html = html.replace(old_text, new_text)
    
    with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ FIXED! Hardcoded example removed")
    print("   OLD: Contoh Blok D003A = 5.5 Ton/Ha...")
    print("   NEW: (Lihat tabel breakdown...)")
    
else:
    print("⚠️  '5.5 Ton/Ha' not found - might be already fixed or different format")
    
    # Try alternative search
    if "D003A" in html and "5.5" in html:
        print("   WARNING: Both 'D003A' and '5.5' exist separately")
        print("   Manual inspection needed")
    else:
        print("   Looks clean!")

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

# Verify it's gone
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

if "5.5 Ton/Ha" in html:
    print("❌ STILL EXISTS! Need manual fix")
else:
    print("✅ CONFIRMED: '5.5 Ton/Ha' REMOVED from dashboard")

print("="*80)
print("\nNEXT: Hard refresh browser (Ctrl+Shift+R) to see changes")
print("="*80)
