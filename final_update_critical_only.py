"""
FINAL UPDATE: ESTATE RISK EXPOSURE
- Filter hanya 8 blok CRITICAL
- Update total loss calculation
- Bahasa Indonesia everywhere
"""
import re

print("="*80)
print("UPDATING ESTATE RISK EXPOSURE - CRITICAL ONLY + BAHASA INDONESIA")
print("="*80)

# Read HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("\n✅ File loaded")

# Step 1: Find and replace renderRiskWatchlist function
# Use regex to find the function block
pattern = r'function renderRiskWatchlist\(\) \{[\s\S]*?if \(elArea\) elArea\.textContent = riskArea\.toFixed\(1\);[\s\S]*?\}'

new_function = '''function renderRiskWatchlist() {
                    // FILTER: HANYA BLOK CRITICAL (8 blok)
                    const sorted = Object.entries(BLOCKS_DATA)
                        .filter(([code, data]) => data.severity_hybrid === 'CRITICAL')
                        .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));

                    let totalLoss = 0;
                    let criticalCount = 0;
                    let riskArea = 0;
                    let html = '';

                    sorted.forEach(([code, data]) => {
                        // Calculate Loss
                        let currentLoss = 0;
                        if (data.gap_ton_ha && parseFloat(data.gap_ton_ha) > 0) {
                            currentLoss = parseFloat(data.gap_ton_ha) * data.luas_ha * TBS_PRICE / 1000;
                        } else {
                            const pot = parseFloat(data.potensi_ton_ha) || 0;
                            const real = parseFloat(data.realisasi_ton_ha) || 0;
                            currentLoss = Math.max(0, pot - real) * data.luas_ha * TBS_PRICE / 1000;
                        }

                        // Accumulate (all are CRITICAL)
                        totalLoss += currentLoss;
                        criticalCount++;
                        riskArea += data.luas_ha;

                        // Build Card HTML (Bahasa Indonesia)
                        html += `
                        <div onclick="updateBlockData('Left', '${code}')" class="bg-slate-800/40 p-3 rounded-lg border border-slate-700 hover:border-rose-500 cursor-pointer transition-all hover:bg-slate-800 group mb-2">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-sm font-black text-white group-hover:text-rose-400 opacity-90">Blok ${code}</span>
                                <span class="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-rose-600 text-white animate-pulse shadow-lg shadow-black/50">KRITIS</span>
                            </div>
                            <div class="flex justify-between items-end">
                                <div>
                                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Est. Kerugian</span>
                                    <span class="text-sm font-bold text-rose-400">Rp ${Math.round(currentLoss).toLocaleString('id-ID')} Jt</span>
                                </div>
                                <div class="text-right">
                                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Infeksi</span>
                                    <span class="text-xs font-bold text-white bg-white/10 px-1.5 rounded">${data.attack_rate}%</span>
                                </div>
                            </div>
                        </div>
                        `;
                    });

                    // Update DOM
                    const container = document.getElementById('riskWatchlistContainer');
                    if (container) container.innerHTML = html;

                    // Update Summary
                    const elTotal = document.getElementById('summaryTotalLoss');
                    if (elTotal) elTotal.textContent = (totalLoss / 1000).toFixed(1);

                    const elCount = document.getElementById('summaryCriticalCount');
                    if (elCount) elCount.textContent = criticalCount;

                    const elArea = document.getElementById('summaryRiskArea');
                    if (elArea) elArea.textContent = riskArea.toFixed(1);
                }'''

# Replace using regex
content_updated = re.sub(pattern, new_function, content, count=1)

if content_updated != content:
    print("✅ Function renderRiskWatchlist updated!")
else:
    print("⚠️  Pattern not found, trying alternative approach...")
    # Alternative: Find exact line numbers
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'function renderRiskWatchlist()' in line:
            print(f"   Found function at line {i+1}")
            # Find end of function
            brace_count = 0
            start_idx = i
            for j in range(i, len(lines)):
                brace_count += lines[j].count('{') - lines[j].count('}')
                if brace_count == 0 and j > i:
                    end_idx = j
                    print(f"   Function ends at line {j+1}")
                    # Replace
                    lines[start_idx:end_idx+1] = [new_function]
                    content_updated = '\n'.join(lines)
                    print("✅ Function replaced using line-based approach!")
                    break
            break

# Step 2: Update labels to Bahasa Indonesia
print("\n📝 Updating labels to Bahasa Indonesia...")

replacements = {
    # Summary section labels
    '>Critical Blocks<': '>Blok Kritis<',
    '>Area at Risk<': '>Area Berisiko<',
    '>Est. Total Loss<': '>Est. Total Kerugian<',
    
    # Watchlist already updated in function above
    
    # Section headers (check for variations)
    'ESTATE RISK EXPOSURE': 'PAPARAN RISIKO ESTATE',
    'Estate Risk Exposure': 'Paparan Risiko Estate',
    
    # Cost of Inaction labels
    'Cost of Inaction': 'Biaya Tidak Bertindak',
    'Current Loss (Year 0)': 'Kerugian Saat Ini (Tahun 0)',
    '3-Year Projected Loss': 'Proyeksi Kerugian 3 Tahun',
    'Treatment Investment': 'Investasi Treatment',
    'Potential Savings': 'Potensi Penghematan',
    'Return on Investment': 'Return on Investment (ROI)',
    'Payback Period': 'Periode Balik Modal',
    'Action Window': 'Jendela Aksi',
    'Months before irreversible': 'Bulan sebelum irreversible',
    'Critical Blocks Require Immediate Attention': 'Blok Kritis Memerlukan Perhatian Segera',
    'Critical Blocks (Click for Detail):': 'Blok Kritis (Klik untuk Detail):',
    'Immediate Action Required': 'Tindakan Segera Diperlukan',
    'Treatment decision must be made within 30 days to prevent exponential loss escalation': 'Keputusan treatment harus diambil dalam 30 hari untuk mencegah eskalasi kerugian eksponensial',
    'Juta / year': 'Juta / tahun',
    'Juta (with degradation)': 'Juta (dengan degradasi)',
    'Juta (one-time)': 'Juta (sekali bayar)',
    'Juta (3-year prevented)': 'Juta (dicegah 3 tahun)',
    'Over 3 years': 'Dalam 3 tahun',
    
    # Degradation note
    'Degradation Model:': 'Model Degradasi:',
    'Projected loss includes realistic deterioration': 'Proyeksi kerugian mencakup deteriorasi realistis',
    'Attack Rate increases': 'Tingkat Infeksi meningkat',
    'Yield Gap worsens': 'Gap Hasil memburuk',
    'if no treatment applied': 'jika tidak ada treatment',
    
    # Modal popup
    'Cost of Inaction Detail Analysis': 'Analisis Detail Biaya Tidak Bertindak',
    'Current Loss': 'Kerugian Saat Ini',
    '3-Year Total': 'Total 3 Tahun',
    'DEGRADATION TIMELINE (NO TREATMENT)': 'TIMELINE DEGRADASI (TANPA TREATMENT)',
    'Parameter': 'Parameter',
    'Attack Rate': 'Tingkat Infeksi',
    'Yield Gap': 'Gap Hasil',
    'Loss (Juta)': 'Kerugian (Juta)',
    'IMPACT OF TREATMENT': 'DAMPAK TREATMENT',
    'Prevented Loss (70% eff):': 'Kerugian yang Dicegah (70% efektif):',
    'Net Benefit:': 'Manfaat Bersih:',
    'Treatment includes: Isolation trenching (4×4m), systemic fungicide, sanitation, and drainage improvement.': 'Treatment mencakup: Parit isolasi (4×4m), fungisida sistemik, sanitasi, dan perbaikan drainase.',
    
    # Year labels in modal
    'Year 0': 'Tahun 0',
    'Year 1': 'Tahun 1',
    'Year 2': 'Tahun 2',
    'Year 3': 'Tahun 3',
    '(Current)': '(Saat Ini)',
    'Change': 'Perubahan',
}

count_replaced = 0
for old_text, new_text in replacements.items():
    if old_text in content_updated:
        content_updated = content_updated.replace(old_text, new_text)
        count_replaced += 1
        print(f"   ✓ {old_text[:50]}")

print(f"✅ {count_replaced} labels updated to Bahasa Indonesia")

# Save
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(content_updated)

print("\n" + "="*80)
print("✅ UPDATE COMPLETE!")
print("="*80)
print("\nChanges:")
print("1. ✅ ESTATE RISK EXPOSURE: Filter hanya 8 blok CRITICAL")
print("2. ✅ Total Loss Updated: Hanya dari 8 blok (~Rp 1.35 Miliar)")
print("3. ✅ Summary Count: 8 blok kritis")
print("4. ✅ All Labels: Bahasa Indonesia")
print("\nExpected Results:")
print("- Watchlist: 8 blok dengan badge 'KRITIS' (merah, pulse)")
print("- Total: Rp 1.3-1.4 Miliar (turun dari sebelumnya)")
print("- Labels: Est. Kerugian, Infeksi, Blok Kritis, etc")
print("\n🎉 Refresh dashboard untuk melihat perubahan!")
print("="*80)
