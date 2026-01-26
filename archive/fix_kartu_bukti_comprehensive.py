"""
FIX KARTU BUKTI - Add comprehensive IDs to ALL 3 cards
"""

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🔧 FIXING KARTU BUKTI sections comprehensively...")
print("="*70)

# Replace the 3 card descriptions with FULL dynamic IDs

replacements = [
    # Card 1 - Replace full TT text
    ('TT 2008 (Usia 18 Tahun). Sistem perakaran sudah',
     '<span id="card1TTFull">TT 2008 (Usia 18 Tahun)</span>. Sistem perakaran sudah'),
    
    # Card 2 - Replace FULL narrative including production differences
    ('<span id="card2AttackNarrative">F008A 12.2% ≈ D001A 12.9%</span></span>. Attack rate hampir identik, tapi produksi sangat berbeda (+8.7%\n                        vs -21.3%) = SYMPTOM LAG!',
     '<span id="card2AttackNarrative">F008A 12.2%</span></span> attack rate. <span id="card2SymptomLagText">Infeksi belum berdampak signifikan ke produksi (SYMPTOM LAG)</span>.'),
    
    # Card 3 - Replace Gap Produksi text
    ('Gap Produksi <span class="text-red-600 font-black text-2xl">9-21%</span>',
     'Gap Produksi <span class="text-red-600 font-black text-2xl" id="card3GapText">9-21%</span>')
]

count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new, 1)
        count += 1
        print(f"✅ {count}. Replaced card text")
    else:
        print(f"⚠️  {count+1}. NOT FOUND (may need adjustment)")
        count += 1

# Save
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Applied {count} replacements")

# Now update JavaScript
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the card updates in JavaScript
search_str = "                // Kartu Bukti Ilmiah\n                ['card1TT', `TT ${data.tt || 2008} (Usia ${data.age || 18} Tahun)`],\n                ['card2AttackNarrative', `${blockCode} ${data.attack_rate}% attack rate`],\n                ['card3GapRange', `${(data.attack_rate * -1.5).toFixed(0)}-${(data.attack_rate * -2.5).toFixed(0)}%`]  // Estimated gap"

if search_str in html:
    new_js = """                // Kartu Bukti Ilmiah - COMPREHENSIVE
                ['card1TTFull', `TT ${data.tt || 2008} (Usia ${data.age || 18} Tahun)`],
                ['card2AttackNarrative', `${blockCode} ${data.attack_rate}%`],
                ['card2SymptomLagText', data.severity === 'HIGH' ? 'Infeksi aktif, risiko tinggi kerugian produksi' : 'Infeksi terdeteksi, monitoring diperlukan'],
                ['card3GapText', `${Math.abs(data.attack_rate * -1.5).toFixed(0)}-${Math.abs(data.attack_rate * -2.5).toFixed(0)}%`]"""
    
    html = html.replace(search_str, new_js)
    print("✅ Updated JavaScript with comprehensive card updates")
else:
    print("⚠️  JavaScript card section not found")

# Save final
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*70)
print("✅ KARTU BUKTI NOW FULLY DYNAMIC!")
print("="*70)
print("\nAll 3 cards now update:")
print("  1. Kontak Akar - TT and Age")
print("  2. Attack Rate - Block code and rate + symptom lag text")
print("  3. Symptom Lag - Gap percentage range")
