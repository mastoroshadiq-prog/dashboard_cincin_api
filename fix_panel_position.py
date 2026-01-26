"""
Fix Block Detail Panel - move it to body level (outside modal) 
and fix z-index issues
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the current panel HTML from inside the modal
panel_start_marker = '<!-- BLOCK DETAIL PANEL (Hidden by default) -->'
panel_start = content.find(panel_start_marker)

if panel_start > 0:
    # Find the closing div of this panel (need to count divs)
    search_start = panel_start
    div_count = 0
    panel_end = -1
    
    i = search_start
    while i < len(content):
        if content[i:i+4] == '<div':
            div_count += 1
        elif content[i:i+6] == '</div>':
            div_count -= 1
            if div_count == 0:
                panel_end = i + 6
                break
        i += 1
    
    if panel_end > 0:
        # Extract the panel HTML
        panel_html = content[panel_start:panel_end]
        print(f"Found panel HTML: {len(panel_html)} chars")
        
        # Remove it from current position
        content = content[:panel_start] + content[panel_end:]
        print("✅ Removed panel from inside modal")
        
        # Insert it right before </body>
        body_end = content.rfind('</body>')
        if body_end > 0:
            # Update z-index to be higher
            panel_html = panel_html.replace('z-[60]', 'z-[100]')
            content = content[:body_end] + '\n    ' + panel_html + '\n' + content[body_end:]
            print("✅ Moved panel to body level with z-[100]")
else:
    print("⚠️ Panel not found - adding fresh")
    
    # Add brand new panel before </body>
    panel_html = '''
    <!-- BLOCK DETAIL PANEL (Outside modal for proper z-index) -->
    <div id="blockDetailPanel" class="hidden fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4">
        <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border-2 border-cyan-500/30 shadow-2xl">
            <!-- Header -->
            <div class="bg-gradient-to-r from-cyan-900 to-blue-900 p-4 rounded-t-2xl flex justify-between items-center border-b border-cyan-500/30">
                <div>
                    <h3 class="text-2xl font-black text-white flex items-center gap-2">
                        📊 Detail Blok <span id="detailBlockCode" class="text-cyan-400">-</span>
                    </h3>
                    <p class="text-slate-300 text-sm">Analisis tren produksi dan risiko</p>
                </div>
                <button onclick="closeBlockDetail()" class="text-3xl text-slate-400 hover:text-white transition-colors">&times;</button>
            </div>
            
            <!-- Content -->
            <div class="p-6 space-y-6">
                <!-- Trend Chart -->
                <div class="bg-black/30 rounded-xl p-4 border border-cyan-700/30">
                    <h4 class="text-lg font-bold text-cyan-400 mb-3">📈 Tren Produksi 2023-2025</h4>
                    <div class="h-64">
                        <canvas id="blockDetailChart"></canvas>
                    </div>
                </div>
                
                <!-- Metrics Grid -->
                <div class="grid grid-cols-2 gap-4">
                    <!-- Left Column: Production Metrics -->
                    <div class="space-y-3">
                        <h4 class="text-md font-bold text-white flex items-center gap-2">🌾 Metrik Produksi</h4>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Luas Area</div>
                            <div class="text-xl font-bold text-white" id="detailLuas">- Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2023</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2023">- T/Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2025</div>
                            <div class="text-xl font-bold text-cyan-400" id="detailYield2025">- T/Ha</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Perubahan Produksi</div>
                            <div class="text-xl font-bold" id="detailChange">-%</div>
                        </div>
                    </div>
                    
                    <!-- Right Column: Risk Metrics -->
                    <div class="space-y-3">
                        <h4 class="text-md font-bold text-white flex items-center gap-2">⚠️ Metrik Risiko</h4>
                        <div class="bg-black/30 rounded-lg p-3 border border-red-700/30">
                            <div class="text-xs text-slate-400">Attack Rate</div>
                            <div class="text-xl font-bold text-red-400" id="detailAttackRate">- %</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-orange-700/30">
                            <div class="text-xs text-slate-400">Stadium</div>
                            <div class="text-xl font-bold text-orange-400" id="detailStadium">-</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-yellow-700/30">
                            <div class="text-xs text-slate-400">SPH (Stands/Ha)</div>
                            <div class="text-xl font-bold text-yellow-400" id="detailSPH">-</div>
                        </div>
                        <div class="bg-black/30 rounded-lg p-3 border border-rose-700/30">
                            <div class="text-xs text-slate-400">Estimasi Kerugian</div>
                            <div class="text-xl font-bold text-rose-400" id="detailLoss">Rp - Juta</div>
                        </div>
                    </div>
                </div>
                
                <!-- Yield Gap Analysis -->
                <div class="bg-gradient-to-r from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-600">
                    <h4 class="text-md font-bold text-white mb-3">📉 Analisis Gap Yield</h4>
                    <div class="grid grid-cols-3 gap-4 text-center">
                        <div>
                            <div class="text-xs text-slate-400">Potensi</div>
                            <div class="text-lg font-bold text-green-400" id="detailPotential">- T/Ha</div>
                        </div>
                        <div>
                            <div class="text-xs text-slate-400">Realisasi</div>
                            <div class="text-lg font-bold text-blue-400" id="detailActual">- T/Ha</div>
                        </div>
                        <div>
                            <div class="text-xs text-slate-400">Gap</div>
                            <div class="text-lg font-bold text-red-400" id="detailGap">- %</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
'''
    body_end = content.rfind('</body>')
    if body_end > 0:
        content = content[:body_end] + panel_html + '\n' + content[body_end:]
        print("✅ Added new panel before body end")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
