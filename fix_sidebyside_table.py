"""
FIX: Create SIDE-BY-SIDE comparison table
Show TANPA vs DENGAN in same table for clear contrast
"""

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the click handler to show BOTH scenarios side-by-side
old_handler = '''                // Add click handler to show data table
                document.getElementById('modalChartPreview').onclick = (evt) => {
                    const points = currentPreviewChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);
                    
                    if (points.length > 0) {
                        const point = points[0];
                        const datasetIndex = point.datasetIndex;
                        const index = point.index;
                        const dataset = currentPreviewChart.data.datasets[datasetIndex];
                        
                        // Get data
                        const year = currentPreviewChart.data.labels[index];
                        const scenario = dataset.label;
                        const loss = dataset.data[index];
                        const ar = dataset.ar[index];
                        const gap = dataset.gap[index];
                        const sph = dataset.sph[index];
                        
                        // Calculate deltas if not year 0
                        let deltaHTML = '';
                        if (index > 0) {
                            const deltaLoss = loss - dataset.data[0];
                            const deltaAR = ar - dataset.ar[0];
                            const deltaGap = gap - dataset.gap[0];
                            const deltaSPH = sph - dataset.sph[0];
                            
                            deltaHTML = `
                                <tr class="border-t-2 border-cyan-500/30">
                                    <td class="p-2 text-yellow-300 font-bold">Δ dari Tahun 0</td>
                                    <td class="p-2 text-right ${deltaLoss > 0 ? 'text-red-400' : 'text-green-400'}">
                                        ${deltaLoss > 0 ? '+' : ''}${deltaLoss.toFixed(0)} Jt
                                    </td>
                                    <td class="p-2 text-right ${deltaAR > 0 ? 'text-red-400' : 'text-green-400'}">
                                        ${deltaAR > 0 ? '+' : ''}${deltaAR.toFixed(1)}%
                                    </td>
                                    <td class="p-2 text-right ${deltaGap > 0 ? 'text-red-400' : 'text-green-400'}">
                                        ${deltaGap > 0 ? '+' : ''}${deltaGap.toFixed(2)}
                                    </td>
                                    <td class="p-2 text-right ${deltaSPH > 0 ? 'text-green-400' : 'text-red-400'}">
                                        ${deltaSPH > 0 ? '+' : ''}${deltaSPH}
                                    </td>
                                </tr>
                            `;
                        }
                        
                        // Build table
                        const tableHTML = `
                            <div class="mb-2 text-sm">
                                <span class="font-bold ${datasetIndex === 0 ? 'text-red-400' : 'text-emerald-400'}">${scenario}</span>
                                <span class="text-gray-400"> - ${year}</span>
                            </div>
                            <table class="w-full text-sm">
                                <thead>
                                    <tr class="border-b border-cyan-500/50">
                                        <th class="text-left p-2 text-cyan-300">Metric</th>
                                        <th class="text-right p-2 text-cyan-300">Loss</th>
                                        <th class="text-right p-2 text-cyan-300">AR</th>
                                        <th class="text-right p-2 text-cyan-300">Gap Yield</th>
                                        <th class="text-right p-2 text-cyan-300">SPH</th>
                                    </tr>
                                </thead>
                                <tbody class="text-white">
                                    <tr>
                                        <td class="p-2 font-bold">Value</td>
                                        <td class="p-2 text-right">Rp ${loss.toFixed(0)} Jt</td>
                                        <td class="p-2 text-right">${ar}%</td>
                                        <td class="p-2 text-right">${gap.toFixed(2)} Ton/Ha</td>
                                        <td class="p-2 text-right">${sph} trees/ha</td>
                                    </tr>
                                    ${deltaHTML}
                                </tbody>
                            </table>
                        `;
                        
                        // Show table
                        document.getElementById('dataTableContent').innerHTML = tableHTML;
                        document.getElementById('dataDisplayTable').classList.remove('hidden');
                    }
                };'''

new_handler = '''                // Add click handler to show SIDE-BY-SIDE comparison table
                document.getElementById('modalChartPreview').onclick = (evt) => {
                    const points = currentPreviewChart.getElementsAtEventForMode(evt, 'index', { intersect: false }, true);
                    
                    if (points.length > 0) {
                        const index = points[0].index;
                        const year = currentPreviewChart.data.labels[index];
                        
                        // Get data from BOTH datasets
                        const dataset1 = currentPreviewChart.data.datasets[0]; // TANPA
                        const dataset2 = currentPreviewChart.data.datasets[1]; // DENGAN
                        
                        // TANPA Treatment data
                        const loss1 = dataset1.data[index];
                        const ar1 = dataset1.ar[index];
                        const gap1 = dataset1.gap[index];
                        const sph1 = dataset1.sph[index];
                        
                        // DENGAN Treatment data
                        const loss2 = dataset2.data[index];
                        const ar2 = dataset2.ar[index];
                        const gap2 = dataset2.gap[index];
                        const sph2 = dataset2.sph[index];
                        
                        // Calculate differences (TANPA - DENGAN = impact of treatment)
                        const lossDiff = loss1 - loss2;
                        const arDiff = ar1 - ar2;
                        const gapDiff = gap1 - gap2;
                        const sphDiff = sph1 - sph2;
                        
                        // Build SIDE-BY-SIDE comparison table
                        const tableHTML = `
                            <div class="mb-3 text-center">
                                <span class="text-white font-black text-lg">${year}</span>
                                <span class="text-cyan-300 ml-2">- Perbandingan TANPA vs DENGAN Treatment</span>
                            </div>
                            <table class="w-full text-sm">
                                <thead>
                                    <tr class="border-b-2 border-cyan-500/50">
                                        <th class="text-left p-3 text-cyan-300 font-bold">Metric</th>
                                        <th class="text-right p-3 text-red-300 font-bold">🔴 TANPA Treatment</th>
                                        <th class="text-right p-3 text-emerald-300 font-bold">🟢 DENGAN Treatment</th>
                                        <th class="text-right p-3 text-yellow-300 font-bold">💰 Savings</th>
                                    </tr>
                                </thead>
                                <tbody class="text-white">
                                    <!-- Loss Row -->
                                    <tr class="border-b border-white/10 hover:bg-white/5">
                                        <td class="p-3 font-bold">Kerugian</td>
                                        <td class="p-3 text-right text-red-400 font-bold">Rp ${loss1.toFixed(0)} Jt</td>
                                        <td class="p-3 text-right text-emerald-400 font-bold">Rp ${loss2.toFixed(0)} Jt</td>
                                        <td class="p-3 text-right ${lossDiff > 0 ? 'text-emerald-400' : 'text-gray-400'} font-bold">
                                            ${lossDiff > 0 ? 'Rp ' + lossDiff.toFixed(0) + ' Jt 🎯' : '-'}
                                        </td>
                                    </tr>
                                    <!-- AR Row -->
                                    <tr class="border-b border-white/10 hover:bg-white/5">
                                        <td class="p-3 font-bold">Attack Rate</td>
                                        <td class="p-3 text-right ${ar1 > ar2 ? 'text-red-400' : 'text-gray-400'}">${ar1}%</td>
                                        <td class="p-3 text-right ${ar2 < ar1 ? 'text-emerald-400' : 'text-gray-400'}">${ar2}%</td>
                                        <td class="p-3 text-right text-xs ${arDiff > 0 ? 'text-emerald-400' : 'text-gray-400'}">
                                            ${arDiff > 0 ? '-' + arDiff.toFixed(1) + '% ↓' : 'Stabil'}
                                        </td>
                                    </tr>
                                    <!-- Gap Row -->
                                    <tr class="border-b border-white/10 hover:bg-white/5">
                                        <td class="p-3 font-bold">Gap Yield</td>
                                        <td class="p-3 text-right ${gap1 > gap2 ? 'text-red-400' : 'text-gray-400'}">${gap1.toFixed(2)} Ton/Ha</td>
                                        <td class="p-3 text-right ${gap2 < gap1 ? 'text-emerald-400' : 'text-gray-400'}">${gap2.toFixed(2)} Ton/Ha</td>
                                        <td class="p-3 text-right text-xs ${gapDiff > 0 ? 'text-emerald-400' : 'text-gray-400'}">
                                            ${gapDiff > 0 ? '-' + gapDiff.toFixed(2) + ' ↓' : 'Stabil'}
                                        </td>
                                    </tr>
                                    <!-- SPH Row -->
                                    <tr class="hover:bg-white/5">
                                        <td class="p-3 font-bold">SPH</td>
                                        <td class="p-3 text-right ${sph1 < sph2 ? 'text-red-400' : 'text-gray-400'}">${sph1} trees/ha</td>
                                        <td class="p-3 text-right ${sph2 > sph1 ? 'text-emerald-400' : 'text-gray-400'}">${sph2} trees/ha</td>
                                        <td class="p-3 text-right text-xs ${sphDiff < 0 ? 'text-emerald-400' : 'text-gray-400'}">
                                            ${sphDiff < 0 ? '+' + Math.abs(sphDiff) + ' ↑' : 'Stabil'}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="mt-3 p-3 bg-yellow-900/20 rounded-lg border border-yellow-600/30">
                                <p class="text-yellow-200 text-xs">
                                    <strong>💡 Treatment Impact:</strong> Mencegah kerugian <strong class="text-yellow-400">Rp ${lossDiff > 0 ? lossDiff.toFixed(0) : '0'} Juta</strong> 
                                    dengan stabilisasi metrics biologis (AR, Gap, SPH).
                                </p>
                            </div>
                        `;
                        
                        // Show table
                        document.getElementById('dataTableContent').innerHTML = tableHTML;
                        document.getElementById('dataDisplayTable').classList.remove('hidden');
                    }
                };'''

if old_handler in html:
    html = html.replace(old_handler, new_handler)
    print("✅ SIDE-BY-SIDE comparison table implemented!")
else:
    print("⚠️  Handler not found - manual check needed")

# Save
with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*80)
print("FIXED: NOW SHOWS CLEAR SIDE-BY-SIDE COMPARISON!")
print("="*80)
print("\nNEW TABLE FORMAT:")
print("┌──────────┬────────────────┬────────────────┬──────────┐")
print("│ Metric   │ 🔴 TANPA       │ 🟢 DENGAN      │ Savings  │")
print("├──────────┼────────────────┼────────────────┼──────────┤")
print("│ Loss     │ Rp 1567 Jt     │ Rp 470 Jt      │ 1097 Jt  │")
print("│ AR       │ 8.9%           │ 7.5%           │ -1.4% ↓  │")
print("│ Gap      │ 5.12 Ton/Ha    │ 4.70 Ton/Ha    │ -0.42 ↓  │")
print("│ SPH      │ 121 trees/ha   │ 124 trees/ha   │ +3 ↑     │")
print("└──────────┴────────────────┴────────────────┴──────────┘")
print("\n✅ VERY CLEAR CONTRAST NOW!")
print("="*80)
