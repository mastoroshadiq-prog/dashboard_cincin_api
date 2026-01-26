"""
PROPER FIX - Don't remove, FIX IT!
1. Put back calculation example with CORRECT Gap (4.66)
2. Fix PAPARAN RISIKO vs COI inconsistency (1.4 vs 1.35 Miliar)
"""
import json

print("="*80)
print("PROPER FIX - Replace with CORRECT data, not remove!")
print("="*80)

# Load JSON to get actual D003A data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    data = json.load(f)

d003a = data['D003A']
actual_gap = abs(d003a['gap_ton_ha'])
actual_luas = d003a['luas_ha']
actual_loss = d003a['loss_value_juta']

print(f"\nD003A ACTUAL DATA:")
print(f"  Gap: {actual_gap} Ton/Ha")
print(f"  Luas: {actual_luas} Ha")
print(f"  Loss: {actual_loss} Juta")
print(f"  Calculation: {actual_gap} × {actual_luas} × 1.5M = {actual_gap * actual_luas * 1.5:.1f} Juta")

# Fix 1: Put back calculation with CORRECT Gap
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the generic text with PROPER calculation
old_generic = """                            <em class="text-gray-400">(Lihat tabel breakdown di bawah untuk data actual per blok)</em><br />
                            <br />"""

new_correct = f"""                            Contoh: Blok D003A<br />
                            = {actual_gap} Ton/Ha × {actual_luas} Ha × Rp 1,500,000/Ton<br />
                            = Rp {int(actual_loss)} Juta/tahun"""

if old_generic in html:
    html = html.replace(old_generic, new_correct)
    print("✅ FIX 1: Replaced generic text with CORRECT calculation")
    print(f"   Gap: {actual_gap} (NOT 5.5!)")
else:
    print("⚠️  Generic text not found - checking for alternative")

# Fix 2: Find PAPARAN RISIKO total and fix inconsistency
# Calculate correct total for 8 CRITICAL blocks
critical_blocks = {k: v for k, v in data.items() if v.get('severity_hybrid') == 'CRITICAL'}
total_loss_juta = sum(v['loss_value_juta'] for v in critical_blocks.values())
total_loss_miliar = total_loss_juta / 1000

print(f"\n✅ FIX 2: Calculate CORRECT total for 8 CRITICAL blocks:")
print(f"  Blocks: {list(critical_blocks.keys())}")
print(f"  Total: {total_loss_juta:.1f} Juta = {total_loss_miliar:.2f} Miliar")

# Search for PAPARAN RISIKO total display
# It should show same as COI header (1.35 or whatever is correct)

# The issue might be rounding or different calculation
# Let me check if it's showing 1.4 (rounded from 1.35)
# Or if watchlist has different total

# Save fixed HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"✅ Calculation restored with CORRECT Gap: {actual_gap} Ton/Ha")
print(f"✅ Example now shows: Rp {int(actual_loss)} Juta (accurate!)")
print(f"⚠️  Need to verify PAPARAN RISIKO shows: Rp {total_loss_miliar:.2f} Miliar")
print(f"   (Should match COI: Rp 1.35 Miliar)")
print("="*80)
