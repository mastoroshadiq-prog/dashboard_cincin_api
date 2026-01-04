import re

file_path = r'd:\PythonProjects\simulasi_poac\data\output\dashboard_cincin_api_INTERACTIVE_FULL.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the pattern to replace (the updates array section)
pattern = re.compile(r'// Potensi Kerugian Skala Makro - GROUND TRUTH DATA.*?card3GapText\', \`\$\{Math\.abs\(data\.gap_pct\)\}\%\`\]\s+\];', re.DOTALL)

replacement = """// Potensi Kerugian Skala Makro - GROUND TRUTH DATA
                ['potensiHeaderBlock', blockCode],
                ['prodPotensi', `${data.potensi_ton_ha} TON/HA`],
                ['prodRealisasi', `${data.realisasi_ton_ha} TON/HA`],
                ['prodGapAbs', `${Math.abs(data.gap_ton_ha).toFixed(2)} TON/HA`],
                ['prodGapPct', `(${data.gap_pct > 0 ? '+' : ''}${data.gap_pct}%)`],
                
                // LOSS CALCULATION (Actual Financial Gap):
                ['lossValue', data.gap_ton_ha < 0 ? `Rp ${(Math.abs(data.gap_ton_ha) * data.luas_ha * 1500 / 1000000).toFixed(1)}` : 'Rp 0.0'],

                // MITIGATION COST - REFINED PARIT ISOLASI:
                ['mitigationValue', `Rp ${((Math.sqrt(data.merah + data.oranye) * 8 * 4 * 35000) / 1000000).toFixed(2)}`],

                // Snapshot Table Updates (Dynamic Row 1)
                ['tableId1', blockCode],
                ['tablePot1', data.potensi_ton_ha],
                ['tableReal1', data.realisasi_ton_ha],
                ['tableGapAbs1', Math.abs(data.gap_ton_ha).toFixed(2)],
                ['tableGapPct1', `(${data.gap_pct > 0 ? '+' : ''}${data.gap_pct}%)`],
                ['tableAttack1', `${data.attack_rate}%`],
                ['tableInti1', data.merah],
                ['tableRing1', data.oranye],
                ['tableLoss1', data.gap_ton_ha < 0 ? `Rp ${(Math.abs(data.gap_ton_ha) * data.luas_ha * 1500 / 1000000).toFixed(1)} JUTA` : 'Rp 0 JUTA'],

                // Kartu Bukti Ilmiah - COMPREHENSIVE
                ['card1TTFull', `TT ${data.tt || 2008} (Usia ${data.age || 18} Tahun)`],
                ['card2AttackNarrative', `${blockCode} ${data.attack_rate}%`],
                ['card2SymptomLagText', data.gap_pct > 0 ? `Produksi masih surplus (${data.gap_pct}%) meskipun serangan aktif (SYMPTOM LAG).` : `Produksi menurun (${data.gap_pct}%) akibat kerusakan sistem perakaran.`],
                ['card3GapText', `${Math.abs(data.gap_pct)}%`]
            ];"""

new_content = pattern.sub(replacement, content)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Successfully updated the updates array logic.")
else:
    print("❌ Failed to find the pattern.")
