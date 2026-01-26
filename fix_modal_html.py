"""
Update modal HTML to add the declining analysis elements
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and update the Multi-Factor Analysis section to show declining stats
# Look for the existing avgAR_critical and replace the whole section

old_analysis_section = '''<h3 class="text-xl font-bold text-white mb-4">📈 Analisis Blok dengan Tren Penurunan</h3>
                            <div class="grid grid-cols-2 gap-4">
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg Attack Rate (Critical)</div>
                                    <div class="text-2xl font-bold text-red-400" id="avgAR_critical">0%</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg SPH Decline (Critical)</div>
                                    <div class="text-2xl font-bold text-orange-400" id="avgSPH_critical">0</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Avg Yield Gap (Critical)</div>
                                    <div class="text-2xl font-bold text-yellow-400" id="avgGap_critical">0%</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4">
                                    <div class="text-xs text-slate-400 mb-1">Total Area at Risk</div>
                                    <div class="text-2xl font-bold text-cyan-400" id="totalAreaRisk">0 Ha</div>
                                </div>
                            </div>'''

new_analysis_section = '''<h3 class="text-xl font-bold text-white mb-4">📉 Analisis Blok dengan Tren Penurunan</h3>
                            <div class="grid grid-cols-4 gap-4">
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center">
                                    <div class="text-xs text-slate-400 mb-1">Rata-rata Perubahan</div>
                                    <div class="text-2xl font-bold text-red-400" id="avgChange_declining">0%</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center">
                                    <div class="text-xs text-slate-400 mb-1">Avg Produksi 2023</div>
                                    <div class="text-2xl font-bold text-cyan-400" id="avgProd2023_declining">0 T/Ha</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center">
                                    <div class="text-xs text-slate-400 mb-1">Avg Produksi 2025</div>
                                    <div class="text-2xl font-bold text-cyan-400" id="avgProd2025_declining">0 T/Ha</div>
                                </div>
                                <div class="bg-slate-800/50 rounded-lg p-4 text-center">
                                    <div class="text-xs text-slate-400 mb-1">Total Luas Terdampak</div>
                                    <div class="text-2xl font-bold text-orange-400" id="totalArea_declining">0 Ha</div>
                                </div>
                            </div>'''

if old_analysis_section in content:
    content = content.replace(old_analysis_section, new_analysis_section)
    print("✅ Updated analysis section with new IDs")
else:
    print("⚠️ Old analysis section not found exactly")
    
    # Try to find by avgAR_critical and replace individual elements
    replacements = [
        ('id="avgAR_critical"', 'id="avgChange_declining"'),
        ('id="avgSPH_critical"', 'id="avgProd2023_declining"'),
        ('id="avgGap_critical"', 'id="avgProd2025_declining"'),
        ('id="totalAreaRisk"', 'id="totalArea_declining"'),
        ('Avg Attack Rate (Critical)', 'Rata-rata Perubahan'),
        ('Avg SPH Decline (Critical)', 'Avg Produksi 2023'),
        ('Avg Yield Gap (Critical)', 'Avg Produksi 2025'),
        ('Total Area at Risk', 'Total Luas Terdampak'),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Replaced: {old[:30]} -> {new[:30]}")

# Also need to add decliningBlocksList and increasingBlocksList if not exist
if 'id="decliningBlocksList"' not in content:
    # Find where to insert - after the analysis section and before distribution chart
    insert_marker = 'Distribusi Tren Produksi'
    insert_pos = content.find(insert_marker)
    
    if insert_pos > 0:
        # Go back to find the div start
        block_lists_html = '''
                        <!-- Two Column Layout: Block Lists -->
                        <div class="grid grid-cols-2 gap-4 mb-6">
                            <!-- DECLINING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                                <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                    📉 Blok dengan Penurunan Produksi
                                    <span class="text-xs text-slate-400 font-normal">(klik untuk detail)</span>
                                </h3>
                                <div id="decliningBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                    <div class="text-slate-500 text-center py-4">Loading...</div>
                                </div>
                            </div>

                            <!-- INCREASING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-green-700/30">
                                <h3 class="text-lg font-bold text-green-400 mb-3 flex items-center gap-2">
                                    📈 Blok dengan Kenaikan Produksi
                                    <span class="text-xs text-slate-400 font-normal">(klik untuk detail)</span>
                                </h3>
                                <div id="increasingBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                    <div class="text-slate-500 text-center py-4">Loading...</div>
                                </div>
                            </div>
                        </div>

                        <!-- '''
        
        # Find the start of Distribution section div
        div_start = content.rfind('<div class="bg-black/20 rounded-xl p-6 border border-slate-700">', 0, insert_pos)
        if div_start > 0:
            content = content[:div_start] + block_lists_html + content[div_start:]
            print("✅ Added block lists HTML before distribution chart")
        else:
            print("⚠️ Could not find insertion point for block lists")
else:
    print("✅ decliningBlocksList already exists")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
