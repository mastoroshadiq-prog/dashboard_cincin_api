"""
Fix Block Detail Panel:
1. Add Yield 2024 display
2. Fix risk metrics to handle missing data better
3. Use data from multiple sources
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Yield 2024 HTML element
# Find the Yield 2023 div and add 2024 after it
old_yield_section = '''<div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2023</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2023">- T/Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2025</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2025">- T/Ha</div>
                        </div>'''

new_yield_section = '''<div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2023</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2023">- T/Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2024</div>
                            <div class="text-xl font-bold text-blue-400" id="detailYield2024">- T/Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2025</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2025">- T/Ha</div>
                        </div>'''

if old_yield_section in content:
    content = content.replace(old_yield_section, new_yield_section)
    print("✅ Added Yield 2024 HTML element")
else:
    print("⚠️ Could not find yield section to update")

# 2. Update showBlockDetail function to include 2024 and better data handling
old_js_function = '''function showBlockDetail(blockCode) {
                console.log('[BLOCK DETAIL] Opening for:', blockCode);
                
                // Get panel elements
                const panel = document.getElementById('blockDetailPanel');
                if (!panel) {
                    console.error('Block detail panel not found');
                    return;
                }
                
                // Set block code
                document.getElementById('detailBlockCode').textContent = blockCode;
                
                // Get historical data
                const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                
                // Get risk data from BLOCKS_DATA
                const riskData = typeof BLOCKS_DATA !== 'undefined' ? BLOCKS_DATA[blockCode] : null;
                
                // Calculate metrics
                let luas = 0, yield2023 = 0, yield2024 = 0, yield2025 = 0;
                let poten2023 = 0, poten2024 = 0, poten2025 = 0;
                let gap2025 = 0;
                
                if (historical) {
                    luas = historical.luas_ha || 0;
                    const y23 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y24 = historical.yields[2024] || historical.yields['2024'] || {};
                    const y25 = historical.yields[2025] || historical.yields['2025'] || {};
                    
                    yield2023 = y23.real_ton_ha || 0;
                    yield2024 = y24.real_ton_ha || 0;
                    yield2025 = y25.real_ton_ha || 0;
                    
                    poten2023 = y23.poten_ton_ha || 0;
                    poten2024 = y24.poten_ton_ha || 0;
                    poten2025 = y25.poten_ton_ha || 0;
                    
                    gap2025 = y25.gap_pct || 0;
                }
                
                const changePct = yield2023 > 0 ? ((yield2025 - yield2023) / yield2023) * 100 : 0;
                
                // Get risk metrics
                let attackRate = 0, stadium = '-', sph = 0, lossValue = 0;
                if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                    
                    // Determine stadium
                    if (attackRate >= 30) stadium = 'Stadium 4 (Kritis)';
                    else if (attackRate >= 15) stadium = 'Stadium 3 (Tinggi)';
                    else if (attackRate >= 5) stadium = 'Stadium 2 (Sedang)';
                    else stadium = 'Stadium 1 (Rendah)';
                }
                
                // Update UI
                document.getElementById('detailLuas').textContent = luas.toFixed(1) + ' Ha';
                document.getElementById('detailYield2023').textContent = yield2023.toFixed(1) + ' T/Ha';
                document.getElementById('detailYield2025').textContent = yield2025.toFixed(1) + ' T/Ha';
                
                const changeEl = document.getElementById('detailChange');
                changeEl.textContent = (changePct >= 0 ? '+' : '') + changePct.toFixed(1) + '%';
                changeEl.className = 'text-xl font-bold ' + (changePct >= 0 ? 'text-green-400' : 'text-red-400');
                
                document.getElementById('detailAttackRate').textContent = attackRate.toFixed(1) + ' %';
                document.getElementById('detailStadium').textContent = stadium;
                document.getElementById('detailSPH').textContent = Math.round(sph);
                document.getElementById('detailLoss').textContent = 'Rp ' + lossValue.toFixed(1) + ' Juta';
                
                document.getElementById('detailPotential').textContent = poten2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailActual').textContent = yield2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailGap').textContent = gap2025.toFixed(1) + '%';
                
                // Render chart
                renderBlockDetailChart(blockCode, yield2023, yield2024, yield2025, poten2023, poten2024, poten2025);
                
                // Show panel
                panel.classList.remove('hidden');
            }'''

new_js_function = '''function showBlockDetail(blockCode) {
                console.log('[BLOCK DETAIL] Opening for:', blockCode);
                
                // Get panel elements
                const panel = document.getElementById('blockDetailPanel');
                if (!panel) {
                    console.error('Block detail panel not found');
                    return;
                }
                
                // Set block code
                document.getElementById('detailBlockCode').textContent = blockCode;
                
                // Get historical data
                const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                
                // Get risk data from BLOCKS_DATA
                const riskData = typeof BLOCKS_DATA !== 'undefined' ? BLOCKS_DATA[blockCode] : null;
                
                // Get complete block data
                const completeData = typeof COMPLETE_BLOCKS_DATA !== 'undefined' ? COMPLETE_BLOCKS_DATA[blockCode] : null;
                
                // Calculate metrics
                let luas = 0, yield2023 = 0, yield2024 = 0, yield2025 = 0;
                let poten2023 = 0, poten2024 = 0, poten2025 = 0;
                let gap2025 = 0;
                
                if (historical) {
                    luas = historical.luas_ha || 0;
                    const y23 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y24 = historical.yields[2024] || historical.yields['2024'] || {};
                    const y25 = historical.yields[2025] || historical.yields['2025'] || {};
                    
                    yield2023 = y23.real_ton_ha || 0;
                    yield2024 = y24.real_ton_ha || 0;
                    yield2025 = y25.real_ton_ha || 0;
                    
                    poten2023 = y23.poten_ton_ha || 0;
                    poten2024 = y24.poten_ton_ha || 0;
                    poten2025 = y25.poten_ton_ha || 0;
                    
                    gap2025 = y25.gap_pct || 0;
                }
                
                const changePct = yield2023 > 0 ? ((yield2025 - yield2023) / yield2023) * 100 : 0;
                
                // Get risk metrics - try multiple sources
                let attackRate = 0, stadium = '-', sph = 0, lossValue = 0;
                
                // First try BLOCKS_DATA
                if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                }
                
                // If no risk data, try COMPLETE_BLOCKS_DATA
                if (attackRate === 0 && completeData) {
                    attackRate = parseFloat(completeData.attack_rate) || parseFloat(completeData.ar_pct) || 0;
                    sph = parseFloat(completeData.sph) || parseFloat(completeData.stands_per_ha) || 0;
                    lossValue = parseFloat(completeData.loss_value_juta) || parseFloat(completeData.loss_juta) || 0;
                }
                
                // Calculate estimated loss if no direct value (using gap and area)
                if (lossValue === 0 && gap2025 !== 0 && luas > 0) {
                    // Estimate: gap_ton_ha * luas * price_per_ton (assume Rp 1.5 juta/ton)
                    const gapTonHa = Math.abs(gap2025 * poten2025 / 100);
                    lossValue = gapTonHa * luas * 1.5; // Rp juta
                }
                
                // Determine stadium based on attack rate
                if (attackRate >= 30) stadium = 'Stadium 4 (Kritis)';
                else if (attackRate >= 15) stadium = 'Stadium 3 (Tinggi)';
                else if (attackRate >= 5) stadium = 'Stadium 2 (Sedang)';
                else if (attackRate > 0) stadium = 'Stadium 1 (Rendah)';
                else stadium = 'Data tidak tersedia';
                
                // Update UI
                document.getElementById('detailLuas').textContent = luas.toFixed(1) + ' Ha';
                document.getElementById('detailYield2023').textContent = yield2023.toFixed(1) + ' T/Ha';
                
                // Update Yield 2024 if element exists
                const yield2024El = document.getElementById('detailYield2024');
                if (yield2024El) yield2024El.textContent = yield2024.toFixed(1) + ' T/Ha';
                
                document.getElementById('detailYield2025').textContent = yield2025.toFixed(1) + ' T/Ha';
                
                const changeEl = document.getElementById('detailChange');
                changeEl.textContent = (changePct >= 0 ? '+' : '') + changePct.toFixed(1) + '%';
                changeEl.className = 'text-xl font-bold ' + (changePct >= 0 ? 'text-green-400' : 'text-red-400');
                
                // Update risk metrics with fallback styling
                const arEl = document.getElementById('detailAttackRate');
                if (attackRate > 0) {
                    arEl.textContent = attackRate.toFixed(1) + ' %';
                    arEl.className = 'text-xl font-bold text-red-400';
                } else {
                    arEl.textContent = 'N/A';
                    arEl.className = 'text-xl font-bold text-slate-500';
                }
                
                document.getElementById('detailStadium').textContent = stadium;
                
                const sphEl = document.getElementById('detailSPH');
                if (sph > 0) {
                    sphEl.textContent = Math.round(sph);
                    sphEl.className = 'text-xl font-bold text-yellow-400';
                } else {
                    sphEl.textContent = 'N/A';
                    sphEl.className = 'text-xl font-bold text-slate-500';
                }
                
                const lossEl = document.getElementById('detailLoss');
                if (lossValue > 0) {
                    lossEl.textContent = 'Rp ' + lossValue.toFixed(1) + ' Juta';
                    lossEl.className = 'text-xl font-bold text-rose-400';
                } else {
                    lossEl.textContent = 'N/A';
                    lossEl.className = 'text-xl font-bold text-slate-500';
                }
                
                document.getElementById('detailPotential').textContent = poten2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailActual').textContent = yield2025.toFixed(1) + ' T/Ha';
                document.getElementById('detailGap').textContent = gap2025.toFixed(1) + '%';
                
                // Render chart with all 3 years
                renderBlockDetailChart(blockCode, yield2023, yield2024, yield2025, poten2023, poten2024, poten2025);
                
                // Show panel
                panel.classList.remove('hidden');
            }'''

if old_js_function in content:
    content = content.replace(old_js_function, new_js_function)
    print("✅ Updated showBlockDetail function")
else:
    print("⚠️ Could not find old showBlockDetail function")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
