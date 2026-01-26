"""
UPDATE ESTATE RISK EXPOSURE WATCHLIST
- Tampilkan hanya 8 blok CRITICAL (konsisten dengan Cost of Inaction)
- Update total loss calculation
- Ubah semua ke Bahasa Indonesia
"""

print("="*80)
print("UPDATING ESTATE RISK EXPOSURE - FILTER 8 CRITICAL BLOCKS")
print("="*80)

# Read HTML
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# NEW renderRiskWatchlist function (CRITICAL only + Bahasa Indonesia)
new_function = '''                function renderRiskWatchlist() {
                    // Sort by Risk Score (highest first)  
                    const sorted = Object.entries(BLOCKS_DATA)
                        .filter(([code, data]) => data.severity_hybrid === 'CRITICAL') // HANYA CRITICAL
                        .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));

                    let totalLoss = 0;
                    let criticalCount = 0;
                    let riskArea = 0;
                    let html = '';

                    sorted.forEach(([code, data]) => {
                        // Calculate Loss
                        let currentLoss = 0;
                        if (data.gap_ton_ha && parseFloat(data.gap_ton_ha) > 0) {
                            currentLoss = parseFloat(data.gap_ton_ha) * data.luas_ha * TBS_PRICE / 1000; // Juta
                        } else {
                            const pot = parseFloat(data.potensi_ton_ha) || 0;
                            const real = parseFloat(data.realisasi_ton_ha) || 0;
                            currentLoss = Math.max(0, pot - real) * data.luas_ha * TBS_PRICE / 1000;
                        }

                        // Accumulate Stats (CRITICAL only)
                        totalLoss += currentLoss;
                        criticalCount++;
                        riskArea += data.luas_ha;

                        // Color (All CRITICAL = red)
                        let badgeColor = 'bg-rose-600 text-white animate-pulse';

                        // Build Card HTML (Bahasa Indonesia)
                        html += `
                        <div onclick="updateBlockData('Left', '${code}')" class="bg-slate-800/40 p-3 rounded-lg border border-slate-700 hover:border-rose-500 cursor-pointer transition-all hover:bg-slate-800 group mb-2">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-sm font-black text-white group-hover:text-rose-400 opacity-90">Blok ${code}</span>
                                <span class="text-[9px] font-black uppercase px-2 py-0.5 rounded ${badgeColor} shadow-lg shadow-black/50">KRITIS</span>
                            </div>
                            <div class="flex justify-between items-end">
                                <div>
                                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Estimasi Kerugian</span>
                                    <span class="text-sm font-bold text-rose-400">Rp ${Math.round(currentLoss).toLocaleString('id-ID')} Jt</span>
                                </div>
                                <div class="text-right">
                                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Tingkat Infeksi</span>
                                    <span class="text-xs font-bold text-white bg-white/10 px-1.5 rounded">${data.attack_rate}%</span>
                                </div>
                            </div>
                        </div>
                        `;
                    });

                    // Update DOM
                    const container = document.getElementById('riskWatchlistContainer');
                    if (container) container.innerHTML = html;

                    // Update Summary (Bahasa Indonesia)
                    const elTotal = document.getElementById('summaryTotalLoss');
                    if (elTotal) elTotal.textContent = (totalLoss / 1000).toFixed(1); // Miliar

                    const elCount = document.getElementById('summaryCriticalCount');
                    if (elCount) elCount.textContent = criticalCount;

                    const elArea = document.getElementById('summaryRiskArea');
                    if (elArea) elArea.textContent = riskArea.toFixed(1);
                }'''

# Find and replace old function
old_func_start = "function renderRiskWatchlist() {"
old_func_end = "if (elArea) elArea.textContent = riskArea.toFixed(1);"

start_pos = html_content.find(old_func_start)
if start_pos > 0:
    # Find the closing brace of function
    end_marker_pos = html_content.find(old_func_end, start_pos)
    if end_marker_pos > 0:
        # Find next closing brace after the marker
        closing_brace = html_content.find("\n                }", end_marker_pos)
        if closing_brace > 0:
            # Replace
            html_updated = (html_content[:start_pos] + 
                           new_function + 
                           html_content[closing_brace + len("\n                }"):])
            
            # Also update text labels to Bahasa Indonesia
            replacements = {
                # Summary section
                '"Critical Blocks"': '"Blok Kritis"',
                '"Area at Risk"': '"Area Berisiko"',
                '"Est. Total Loss"': '"Est. Total Kerugian"',
                
                # Cost of Inaction section  
                '"Current Loss (Year 0)"': '"Kerugian Saat Ini (Tahun 0)"',
                '"3-Year Projected Loss"': '"Proyeksi Kerugian 3 Tahun"',
                '"Treatment Investment"': '"Investasi Treatment"',
                '"Potential Savings"': '"Potensi Penghematan"',
                '"Return on Investment"': '"Return on Investment (ROI)"',
                '"Payback Period"': '"Periode Balik Modal"',
                '"Action Window"': '"Jendela Aksi"',
                '"Months before irreversible"': '"Bulan sebelum irreversible"',
                '"Cost of Inaction"': '"Biaya Tidak Bertindak"',
                '"Critical Blocks Require Immediate Attention"': '"Blok Kritis Memerlukan Perhatian Segera"',
                '"Critical Blocks (Click for Detail):"': '"Blok Kritis (Klik untuk Detail):"',
                '"Immediate Action Required"': '"Tindakan Segera Diperlukan"',
                '"Treatment decision must be made within 30 days to prevent exponential loss escalation"': '"Keputusan treatment harus diambil dalam 30 hari untuk mencegah eskalasi kerugian eksponensial"',
                
                # Degradation note
                '"Degradation Model:"': '"Model Degradasi:"',
                '"Projected loss includes realistic deterioration"': '"Proyeksi kerugian mencakup deteriorasi realistis"',
                '"Attack Rate increases"': '"Tingkat Infeksi meningkat"',
                '"Yield Gap worsens"': '"Gap Hasil memburuk"',
                '"if no treatment applied"': '"jika tidak ada treatment"',
                
                # Modal
                '"Cost of Inaction Detail Analysis"': '"Analisis Detail Biaya Tidak Bertindak"',
                '"Current Loss"': '"Kerugian Saat Ini"',
                '"3-Year Total"': '"Total 3 Tahun"',
                '"Treatment"': '"Treatment"',
                '"DEGRADATION TIMELINE (NO TREATMENT)"': '"TIMELINE DEGRADASI (TANPA TREATMENT)"',
                '"Year 0<br/><span class=\\"text-xs text-gray-400\\">(Current)</span>"': '"Tahun 0<br/><span class=\\"text-xs text-gray-400\\">(Saat Ini)</span>"',
                '"Year 1"': '"Tahun 1"',
                '"Year 2"': '"Tahun 2"',
                '"Year 3"': '"Tahun 3"',
                '"Change"': '"Perubahan"',
                '"Parameter"': '"Parameter"',
                '"Attack Rate"': '"Tingkat Infeksi"',
                '"Yield Gap"': '"Gap Hasil"',
                '"SPH (trees/ha)"': '"SPH (pohon/ha)"',
                '"Loss (Juta)"': '"Kerugian (Juta)"',
                '"IMPACT OF TREATMENT"': '"DAMPAK TREATMENT"',
                '"Prevented Loss (70% eff):"': '"Kerugian yang Dicegah (70% efektif):"',
                '"Net Benefit:"': '"Manfaat Bersih:"',
                '"Treatment includes: Isolation trenching (4×4m), systemic fungicide, sanitation, and drainage improvement."': '"Treatment mencakup: Parit isolasi (4×4m), fungisida sistemik, sanitasi, dan perbaikan drainase."',
            }
            
            for old_text, new_text in replacements.items():
                html_updated = html_updated.replace(old_text, new_text)
            
            # Save
            with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
                f.write(html_updated)
            
            print("\n✅ Function UPDATED!")
            print("✅ Filter: HANYA 8 blok CRITICAL")
            print("✅ Labels: Ubah ke Bahasa Indonesia")
            print("\nChanges:")
            print("- Watchlist: Show only CRITICAL blocks (8 blocks)")
            print("- Total Loss: Calculated from 8 CRITICAL blocks only")
            print("- Summary Count: 8 (instead of ~14)")
            print("- Labels: Bahasa Indonesia")
        else:
            print("❌ Could not find closing brace")
    else:
        print("❌ Could not find end marker")
else:
    print("❌ Could not find function start")

print("\n" + "="*80)
print("DONE! Refresh dashboard to see:")
print("- ESTATE RISK EXPOSURE: 8 blok CRITICAL (konsisten)")
print("- Total loss: Hanya dari 8 blok")
print("- Semua label: Bahasa Indonesia")
print("="*80)
