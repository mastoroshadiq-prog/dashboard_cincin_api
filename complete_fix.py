"""
COMPLETE FIX SCRIPT - One-shot update untuk Block Trend Modal
Melakukan semua perubahan yang diperlukan dengan aman:
1. Fix script tags
2. Update HISTORICAL_YIELDS
3. Update modal HTML dengan ID baru
4. Update JavaScript function dengan logika tren
"""

import json
import re

print("="*60)
print("COMPLETE BLOCK TREND MODAL FIX")
print("="*60)

# Load historical data
with open('complete_historical_yields.json', 'r') as f:
    historical_data = json.load(f)
print(f"✅ Loaded {len(historical_data)} blocks from historical data")

# Read HTML
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()
original_len = len(content)
print(f"✅ Read HTML file: {original_len} bytes")

# =====================================================
# STEP 1: Fix script tags with src that have inline content
# =====================================================
print("\n[STEP 1] Fixing script tags...")

# Find first script tag with tailwindcss
tailwind_match = re.search(r'<script src="https://cdn\.tailwindcss\.com">\s*[^<]+\s*</script>', content, re.DOTALL)
if tailwind_match:
    content = content.replace(tailwind_match.group(0), '<script src="https://cdn.tailwindcss.com"></script>')
    print("  Fixed tailwindcss script tag")

# Find script tag with chart.js
chartjs_match = re.search(r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js">\s*[^<]+\s*</script>', content, re.DOTALL)
if chartjs_match:
    content = content.replace(chartjs_match.group(0), '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>')
    print("  Fixed chart.js script tag")

# =====================================================
# STEP 2: Update HISTORICAL_YIELDS
# =====================================================
print("\n[STEP 2] Updating HISTORICAL_YIELDS...")

# Find HISTORICAL_YIELDS block
start_marker = "const HISTORICAL_YIELDS = {"
start_pos = content.find(start_marker)

if start_pos == -1:
    print("  ERROR: HISTORICAL_YIELDS not found!")
else:
    # Find closing brace by counting
    brace_count = 0
    end_pos = start_pos
    found_first = False
    for i in range(start_pos, min(start_pos + 200000, len(content))):
        if content[i] == '{':
            brace_count += 1
            found_first = True
        elif content[i] == '}':
            brace_count -= 1
            if found_first and brace_count == 0:
                end_pos = i + 1
                if end_pos < len(content) and content[end_pos] == ';':
                    end_pos += 1
                break
    
    # Build clean HISTORICAL_YIELDS
    new_yields = "const HISTORICAL_YIELDS = {\n"
    for block_code in sorted(historical_data.keys()):
        block = historical_data[block_code]
        luas = block.get('luas_ha', 0)
        division = block.get('division', '')
        yields = block.get('yields', {})
        
        new_yields += f'            "{block_code}": {{\n'
        new_yields += f'                luas_ha: {luas},\n'
        new_yields += f'                division: "{division}",\n'
        new_yields += f'                yields: {{\n'
        
        for year in ['2023', '2024', '2025']:
            y = yields.get(year, {})
            real = y.get('real_ton_ha', 0)
            poten = y.get('poten_ton_ha', 0)
            gap = y.get('gap_pct', 0)
            new_yields += f'                    {year}: {{ real_ton_ha: {real}, poten_ton_ha: {poten}, gap_pct: {gap} }},\n'
        
        new_yields += '                }\n'
        new_yields += '            },\n'
    
    new_yields += "        };"
    
    content = content[:start_pos] + new_yields + content[end_pos:]
    print(f"  Updated HISTORICAL_YIELDS with {len(historical_data)} blocks")

# =====================================================
# STEP 3: Update Modal HTML
# =====================================================
print("\n[STEP 3] Updating modal HTML elements...")

# Update header
content = content.replace('BLOCK CATEGORIZATION', 'TREN PRODUKSI PER BLOK')
print("  Updated modal title")

# Update category card 1: CRITICAL -> DECLINING
content = content.replace(
    '<div class="text-4xl mb-2">🔴</div>\n                            <div class="text-red-200 text-xs font-bold uppercase mb-2">CRITICAL</div>',
    '<div class="text-4xl mb-2">📉</div>\n                            <div class="text-red-200 text-xs font-bold uppercase mb-2">TREN PENURUNAN</div>'
)
content = content.replace('id="categoryCount_critical"', 'id="categoryCount_declining"')
content = content.replace('Stadium 4 • AR ≥ 30%', 'Produksi turun > 5%')
print("  Updated CRITICAL -> DECLINING")

# Update category card 2: HIGH -> STABLE  
content = content.replace(
    '<div class="text-4xl mb-2">🟠</div>\n                            <div class="text-orange-200 text-xs font-bold uppercase mb-2">HIGH</div>',
    '<div class="text-4xl mb-2">➡️</div>\n                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">TREN STABIL</div>'
)
content = content.replace('id="categoryCount_high"', 'id="categoryCount_stable"')
content = content.replace('Stadium 3 • AR 15-30%', 'Perubahan -5% s/d +5%')
print("  Updated HIGH -> STABLE")

# Update category card 3: MEDIUM -> INCREASING
content = content.replace(
    '<div class="text-4xl mb-2">🟡</div>\n                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">MEDIUM</div>',
    '<div class="text-4xl mb-2">📈</div>\n                            <div class="text-green-200 text-xs font-bold uppercase mb-2">TREN KENAIKAN</div>'
)
content = content.replace('id="categoryCount_medium"', 'id="categoryCount_increasing"')
content = content.replace('Stadium 2 • AR 5-15%', 'Produksi naik > 5%')
print("  Updated MEDIUM -> INCREASING")

# Update category card 4: LOW -> NO DATA
content = content.replace(
    '<div class="text-4xl mb-2">🟢</div>\n                            <div class="text-green-200 text-xs font-bold uppercase mb-2">LOW</div>',
    '<div class="text-4xl mb-2">❓</div>\n                            <div class="text-slate-200 text-xs font-bold uppercase mb-2">NO DATA</div>'
)
content = content.replace('id="categoryCount_low"', 'id="categoryCount_nodata"')
content = content.replace('Stadium 1 • AR < 5%', 'Tidak ada data historis')
print("  Updated LOW -> NO DATA")

# Update analysis section IDs and labels
content = content.replace('Multi-Factor Analysis Summary', 'Analisis Blok dengan Tren Penurunan')
content = content.replace('📈 Analisis Blok dengan Tren Penurunan', '📉 Analisis Blok dengan Tren Penurunan')
content = content.replace('id="avgAR_critical"', 'id="avgChange_declining"')
content = content.replace('id="avgSPH_critical"', 'id="avgProd2023_declining"')
content = content.replace('id="avgGap_critical"', 'id="avgProd2025_declining"')
content = content.replace('id="totalAreaRisk"', 'id="totalArea_declining"')
content = content.replace('Avg Attack Rate (Critical)', 'Rata-rata Perubahan')
content = content.replace('Avg SPH Decline (Critical)', 'Avg Produksi 2023')
content = content.replace('Avg Yield Gap (Critical)', 'Avg Produksi 2025')
content = content.replace('Total Area at Risk', 'Total Luas Terdampak')
print("  Updated analysis section IDs")

# Update distribution chart title
content = content.replace('Category Distribution', 'Distribusi Tren Produksi (2023-2025)')
print("  Updated chart title")

# =====================================================
# STEP 4: Update JavaScript functions
# =====================================================
print("\n[STEP 4] Updating JavaScript functions...")

# Find and replace the categorization logic
old_js_block = '''// Categorize blocks by stadium
                const categories = {
                    critical: [], // Stadium 4
                    high: [],     // Stadium 3
                    medium: [],   // Stadium 2
                    low: []       // Stadium 1
                };

                mergedBlocks.forEach(block => {
                    const attackRate = parseFloat(block.attack_rate) || 0;
                    const gapPct = Math.abs(parseFloat(block.gap_pct) || 0);

                    // Stadium classification (inline logic)
                    if (attackRate >= 30 || gapPct >= 40) {
                        categories.critical.push(block);
                    } else if (attackRate >= 15 || gapPct >= 20) {
                        categories.high.push(block);
                    } else if (attackRate >= 5 || gapPct >= 10) {
                        categories.medium.push(block);
                    } else {
                        categories.low.push(block);
                    }
                });

                console.log('[BREAKDOWN] Categories:', {
                    critical: categories.critical.length,
                    high: categories.high.length,
                    medium: categories.medium.length,
                    low: categories.low.length
                });'''

new_js_block = '''// Categorize blocks by PRODUCTION TREND (2023-2025)
                const categories = {
                    declining: [],   // Produksi turun > 5%
                    stable: [],      // Perubahan -5% s/d +5%
                    increasing: [],  // Produksi naik > 5%
                    nodata: []       // Tidak ada data historis
                };

                mergedBlocks.forEach(block => {
                    const blockCode = block.block_code;
                    const historical = typeof HISTORICAL_YIELDS !== 'undefined' ? HISTORICAL_YIELDS[blockCode] : null;
                    
                    if (!historical || !historical.yields) {
                        categories.nodata.push({...block, prodChangePct: 0, prod2023: 0, prod2025: 0});
                        return;
                    }
                    
                    const y2023 = historical.yields[2023] || historical.yields['2023'] || {};
                    const y2025 = historical.yields[2025] || historical.yields['2025'] || {};
                    const prod2023 = y2023.real_ton_ha || 0;
                    const prod2025 = y2025.real_ton_ha || 0;
                    
                    if (prod2023 === 0 && prod2025 === 0) {
                        categories.nodata.push({...block, prodChangePct: 0, prod2023: 0, prod2025: 0});
                        return;
                    }
                    
                    const changePct = prod2023 > 0 ? ((prod2025 - prod2023) / prod2023) * 100 : 0;
                    const enrichedBlock = {...block, prodChangePct: changePct, prod2023, prod2025};
                    
                    if (changePct < -5) {
                        categories.declining.push(enrichedBlock);
                    } else if (changePct > 5) {
                        categories.increasing.push(enrichedBlock);
                    } else {
                        categories.stable.push(enrichedBlock);
                    }
                });

                // Sort by change percentage
                categories.declining.sort((a, b) => a.prodChangePct - b.prodChangePct);
                categories.increasing.sort((a, b) => b.prodChangePct - a.prodChangePct);

                console.log('[BREAKDOWN] Production Trend Categories:', {
                    declining: categories.declining.length,
                    stable: categories.stable.length,
                    increasing: categories.increasing.length,
                    nodata: categories.nodata.length
                });'''

if old_js_block in content:
    content = content.replace(old_js_block, new_js_block)
    print("  ✅ Updated categorization logic")
else:
    print("  ⚠️ Could not find old categorization block")

# Update category counts
content = content.replace(
    "document.getElementById('categoryCount_critical').textContent = categories.critical.length;",
    "document.getElementById('categoryCount_declining').textContent = categories.declining.length;"
)
content = content.replace(
    "document.getElementById('categoryCount_high').textContent = categories.high.length;",
    "document.getElementById('categoryCount_stable').textContent = categories.stable.length;"
)
content = content.replace(
    "document.getElementById('categoryCount_medium').textContent = categories.medium.length;",
    "document.getElementById('categoryCount_increasing').textContent = categories.increasing.length;"
)
content = content.replace(
    "document.getElementById('categoryCount_low').textContent = categories.low.length;",
    "document.getElementById('categoryCount_nodata').textContent = categories.nodata.length;"
)
print("  Updated category count updates")

# Update multi-factor analysis section
old_analysis = '''// Calculate multi-factor analysis for CRITICAL + HIGH blocks (Stadium 3+)
                // This matches Division Overview "Critical Blocks" count
                const stadium3Plus = [...categories.critical, ...categories.high];

                console.log('[BREAKDOWN] Stadium 3+ blocks:', stadium3Plus.length);
                if (stadium3Plus.length > 0) {
                    console.log('[BREAKDOWN] Sample block fields:', stadium3Plus[0]);
                    console.log('[BREAKDOWN] ALL KEYS:', Object.keys(stadium3Plus[0]));
                }

                if (stadium3Plus.length > 0) {
                    const avgAR = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.attack_rate) || 0), 0) / stadium3Plus.length;
                    const avgSPH = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.sph) || 0), 0) / stadium3Plus.length;
                    const avgGap = stadium3Plus.reduce((sum, b) => sum + Math.abs(parseFloat(b.gap_pct) || 0), 0) / stadium3Plus.length;
                    const totalArea = stadium3Plus.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

                    console.log('[BREAKDOWN] Calculated avgAR:', avgAR);
                    console.log('[BREAKDOWN] Calculated avgSPH:', avgSPH);
                    console.log('[BREAKDOWN] Calculated avgGap:', avgGap);

                    document.getElementById('avgAR_critical').textContent = avgAR.toFixed(1) + '%';
                    document.getElementById('avgSPH_critical').textContent = Math.round(avgSPH);
                    document.getElementById('avgGap_critical').textContent = avgGap.toFixed(1) + '%';
                    document.getElementById('totalAreaRisk').textContent = totalArea.toFixed(1) + ' Ha';
                } else {
                    document.getElementById('avgAR_critical').textContent = '0%';
                    document.getElementById('avgSPH_critical').textContent = '0';
                    document.getElementById('avgGap_critical').textContent = '0%';
                    document.getElementById('totalAreaRisk').textContent = '0 Ha';
                }'''

new_analysis = '''// Calculate stats for DECLINING BLOCKS
                const decliningBlocks = categories.declining;

                console.log('[BREAKDOWN] Declining blocks:', decliningBlocks.length);

                if (decliningBlocks.length > 0) {
                    const avgChange = decliningBlocks.reduce((sum, b) => sum + (b.prodChangePct || 0), 0) / decliningBlocks.length;
                    const avgProd2023 = decliningBlocks.reduce((sum, b) => sum + (b.prod2023 || 0), 0) / decliningBlocks.length;
                    const avgProd2025 = decliningBlocks.reduce((sum, b) => sum + (b.prod2025 || 0), 0) / decliningBlocks.length;
                    const totalArea = decliningBlocks.reduce((sum, b) => sum + (parseFloat(b.luas_ha) || 0), 0);

                    document.getElementById('avgChange_declining').textContent = avgChange.toFixed(1) + '%';
                    document.getElementById('avgProd2023_declining').textContent = avgProd2023.toFixed(1) + ' T/Ha';
                    document.getElementById('avgProd2025_declining').textContent = avgProd2025.toFixed(1) + ' T/Ha';
                    document.getElementById('totalArea_declining').textContent = totalArea.toFixed(1) + ' Ha';
                    
                    // Populate declining block list
                    const decliningList = document.getElementById('decliningBlocksList');
                    if (decliningList) {
                        let html = decliningBlocks.slice(0, 10).map(b => 
                            '<div class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 border border-transparent hover:border-red-500/50">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                            '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');
                        if (decliningBlocks.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (decliningBlocks.length - 10) + ' blok lainnya...</div>';
                        decliningList.innerHTML = html;
                    }
                } else {
                    document.getElementById('avgChange_declining').textContent = '0%';
                    document.getElementById('avgProd2023_declining').textContent = '0 T/Ha';
                    document.getElementById('avgProd2025_declining').textContent = '0 T/Ha';
                    document.getElementById('totalArea_declining').textContent = '0 Ha';
                }
                
                // Populate increasing block list
                const increasingBlocks = categories.increasing;
                const increasingList = document.getElementById('increasingBlocksList');
                if (increasingList && increasingBlocks.length > 0) {
                    let html = increasingBlocks.slice(0, 10).map(b => 
                        '<div class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 border border-transparent hover:border-green-500/50">' +
                        '<span class="text-white font-medium">' + b.block_code + '</span>' +
                        '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                        '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                        '</div>'
                    ).join('');
                    if (increasingBlocks.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (increasingBlocks.length - 10) + ' blok lainnya...</div>';
                    increasingList.innerHTML = html;
                } else if (increasingList) {
                    increasingList.innerHTML = '<div class="text-slate-500 text-center py-4">Tidak ada data</div>';
                }'''

if old_analysis in content:
    content = content.replace(old_analysis, new_analysis)
    print("  ✅ Updated analysis calculations")
else:
    print("  ⚠️ Could not find old analysis block")

# Update chart data
content = content.replace(
    "labels: ['🔴 Critical', '🟠 High', '🟡 Medium', '🟢 Low']",
    "labels: ['📉 Penurunan', '➡️ Stabil', '📈 Kenaikan', '❓ No Data']"
)
content = content.replace(
    """data: [
                            categories.critical.length,
                            categories.high.length,
                            categories.medium.length,
                            categories.low.length
                        ]""",
    """data: [
                            categories.declining.length,
                            categories.stable.length,
                            categories.increasing.length,
                            categories.nodata.length
                        ]"""
)
print("  Updated chart data")

# =====================================================
# STEP 5: Add block lists HTML if not present
# =====================================================
print("\n[STEP 5] Adding block lists HTML...")

if 'id="decliningBlocksList"' not in content:
    # Find the Distribution section and insert before it
    dist_marker = '<h3 class="text-xl font-bold text-white mb-4">📊 Distribusi Tren Produksi'
    dist_pos = content.find(dist_marker)
    
    if dist_pos > 0:
        # Find the div opening before distribution
        div_start = content.rfind('<div class="bg-black/20 rounded-xl p-6 border border-slate-700">', 0, dist_pos)
        
        block_lists_html = '''<!-- Two Column Layout: Block Lists -->
                        <div class="grid grid-cols-2 gap-4 mb-6">
                            <!-- DECLINING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                                <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                                    📉 Blok dengan Penurunan Produksi
                                </h3>
                                <div id="decliningBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                    <div class="text-slate-500 text-center py-4">Loading...</div>
                                </div>
                            </div>

                            <!-- INCREASING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-green-700/30">
                                <h3 class="text-lg font-bold text-green-400 mb-3 flex items-center gap-2">
                                    📈 Blok dengan Kenaikan Produksi
                                </h3>
                                <div id="increasingBlocksList" class="max-h-64 overflow-y-auto custom-scrollbar">
                                    <div class="text-slate-500 text-center py-4">Loading...</div>
                                </div>
                            </div>
                        </div>

                        '''
        
        if div_start > 0:
            content = content[:div_start] + block_lists_html + content[div_start:]
            print("  ✅ Added block lists HTML")
        else:
            print("  ⚠️ Could not find insertion point")
else:
    print("  Block lists already exist")

# =====================================================
# FINAL: Write file
# =====================================================
print("\n" + "="*60)
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ COMPLETE! File saved: {len(content)} bytes")
print(f"   Original: {original_len} bytes")
print(f"   Change: {len(content) - original_len:+d} bytes")
