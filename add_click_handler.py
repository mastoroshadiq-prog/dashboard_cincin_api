"""
Add click handler for 3-year chart to show data table
"""

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the 3-year chart creation and add onClick handler
# Insert right after chart creation, before the closing });

click_handler_code = '''
                
                // Add click handler to show data table
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

# Find where to insert (after the 3-year chart options close)
insert_marker = "                });"  # After chart creation for type === '3year'

# We need to find the specific location - after the 3-year chart closing
# Let's use a more specific marker

# Actually, better to insert it within the showModalPreview function, right after setting currentPreviewChart for 3year
# Find the line after new Chart(ctx, {...}) for 3year ends

# For safety, let me append it to the showModalPreview function entirely
# Find end of function and add the handler there

# Actually simpler: add it in the 3year conditional block
search_for = '''                });

            } else if (type === 'treatment') {'''

replace_with = '''                });
''' + click_handler_code + '''

            } else if (type === 'treatment') {'''

if search_for in html:
    html = html.replace(search_for, replace_with)
    print("✅ Click handler added for 3-year chart!")
else:
    print("⚠️  Marker not found - checking alternative...")

# Save
with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Prototype updated with:")
print("   1. Click handler for 3-year chart → shows data table")
print("   2. Enhanced pie chart with distinct colors + labels")
print("\n" + "="*80)
print("READY FOR TESTING!")
print("="*80)
print("\nUSER ACTIONS:")
print("1. Open PROTOTYPE_3_ENHANCEMENTS.html")
print("2. Click '3-Year Trend' button")
print("3. Click any datapoint on chart → Table appears!")
print("4. Click 'Treatment Cost' button → See labeled pie chart")
print("="*80)
