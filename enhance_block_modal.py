"""
Enhance Block Trend Modal:
1. Add stable blocks list section
2. Show all blocks instead of limiting to 10
3. Add search functionality
"""

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*60)
print("ENHANCING BLOCK TREND MODAL")
print("="*60)

# 1. Find the block lists section and add stable blocks
# Look for the current two-column grid (declining + increasing)
old_block_lists = '''<!-- Two Column Layout: Block Lists -->
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
                        </div>'''

new_block_lists = '''<!-- Search Box -->
                        <div class="mb-4">
                            <div class="relative">
                                <input type="text" id="blockSearchInput" placeholder="🔍 Cari blok (contoh: D001A, E002A...)" 
                                    class="w-full bg-slate-800/50 border border-slate-600 rounded-xl px-4 py-3 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none"
                                    onkeyup="filterBlockLists(this.value)">
                                <div class="absolute right-3 top-3 text-slate-400 text-sm" id="searchResultCount"></div>
                            </div>
                        </div>

                        <!-- Three Column Layout: Block Lists -->
                        <div class="grid grid-cols-3 gap-4 mb-6">
                            <!-- DECLINING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-red-700/30">
                                <h3 class="text-md font-bold text-red-400 mb-3 flex items-center gap-2">
                                    📉 Penurunan <span id="decliningCount" class="text-xs bg-red-500/20 px-2 py-1 rounded-full">0</span>
                                </h3>
                                <div id="decliningBlocksList" class="max-h-80 overflow-y-auto custom-scrollbar space-y-1">
                                    <div class="text-slate-500 text-center py-4 text-sm">Loading...</div>
                                </div>
                            </div>

                            <!-- STABLE BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-yellow-700/30">
                                <h3 class="text-md font-bold text-yellow-400 mb-3 flex items-center gap-2">
                                    ➡️ Stabil <span id="stableCount" class="text-xs bg-yellow-500/20 px-2 py-1 rounded-full">0</span>
                                </h3>
                                <div id="stableBlocksList" class="max-h-80 overflow-y-auto custom-scrollbar space-y-1">
                                    <div class="text-slate-500 text-center py-4 text-sm">Loading...</div>
                                </div>
                            </div>

                            <!-- INCREASING BLOCKS LIST -->
                            <div class="bg-black/20 rounded-xl p-4 border border-green-700/30">
                                <h3 class="text-md font-bold text-green-400 mb-3 flex items-center gap-2">
                                    📈 Kenaikan <span id="increasingCount" class="text-xs bg-green-500/20 px-2 py-1 rounded-full">0</span>
                                </h3>
                                <div id="increasingBlocksList" class="max-h-80 overflow-y-auto custom-scrollbar space-y-1">
                                    <div class="text-slate-500 text-center py-4 text-sm">Loading...</div>
                                </div>
                            </div>
                        </div>'''

if old_block_lists in content:
    content = content.replace(old_block_lists, new_block_lists)
    print("✅ Updated block lists HTML (3 columns + search)")
else:
    print("⚠️ Could not find old block lists HTML")

# 2. Update JavaScript to show ALL blocks and add stable list
# Find the block list population code and update it

# Update declining blocks rendering (remove limit of 10)
old_declining_js = '''let html = decliningBlocks.slice(0, 10).map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 cursor-pointer border border-transparent hover:border-red-500/50 hover:bg-red-900/40 transition-all">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                            '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                            '</div>'
                        ).join('');
                        if (decliningBlocks.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (decliningBlocks.length - 10) + ' blok lainnya...</div>';
                        decliningList.innerHTML = html;'''

new_declining_js = '''let html = decliningBlocks.map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" data-block="' + b.block_code.toLowerCase() + '" class="block-item flex justify-between items-center py-2 px-2 bg-red-900/20 rounded cursor-pointer border border-transparent hover:border-red-500/50 hover:bg-red-900/40 transition-all text-sm">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
                            '</div>'
                        ).join('');
                        decliningList.innerHTML = html || '<div class="text-slate-500 text-center py-4 text-xs">Tidak ada</div>';
                        document.getElementById('decliningCount').textContent = decliningBlocks.length;'''

if old_declining_js in content:
    content = content.replace(old_declining_js, new_declining_js)
    print("✅ Updated declining blocks JS (show all, compact)")
else:
    print("⚠️ Could not find old declining JS")

# Update increasing blocks rendering (remove limit of 10)
old_increasing_js = '''let html = increasingBlocks.slice(0, 10).map(b => 
                        '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" class="flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 cursor-pointer border border-transparent hover:border-green-500/50 hover:bg-green-900/40 transition-all">' +
                        '<span class="text-white font-medium">' + b.block_code + '</span>' +
                        '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                        '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
                        '</div>'
                    ).join('');
                    if (increasingBlocks.length > 10) html += '<div class="text-slate-400 text-sm text-center mt-2">+' + (increasingBlocks.length - 10) + ' blok lainnya...</div>';
                    increasingList.innerHTML = html;'''

new_increasing_js = '''let html = increasingBlocks.map(b => 
                        '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" data-block="' + b.block_code.toLowerCase() + '" class="block-item flex justify-between items-center py-2 px-2 bg-green-900/20 rounded cursor-pointer border border-transparent hover:border-green-500/50 hover:bg-green-900/40 transition-all text-sm">' +
                        '<span class="text-white font-medium">' + b.block_code + '</span>' +
                        '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
                        '</div>'
                    ).join('');
                    increasingList.innerHTML = html || '<div class="text-slate-500 text-center py-4 text-xs">Tidak ada</div>';
                    document.getElementById('increasingCount').textContent = increasingBlocks.length;
                    
                    // Also populate stable blocks list
                    const stableBlocks = categories.stable || [];
                    const stableList = document.getElementById('stableBlocksList');
                    if (stableList) {
                        let stableHtml = stableBlocks.map(b => 
                            '<div onclick="showBlockDetail(\\'' + b.block_code + '\\')" data-block="' + b.block_code.toLowerCase() + '" class="block-item flex justify-between items-center py-2 px-2 bg-yellow-900/20 rounded cursor-pointer border border-transparent hover:border-yellow-500/50 hover:bg-yellow-900/40 transition-all text-sm">' +
                            '<span class="text-white font-medium">' + b.block_code + '</span>' +
                            '<span class="text-yellow-400 font-bold">' + (b.prodChangePct >= 0 ? '+' : '') + b.prodChangePct.toFixed(1) + '%</span>' +
                            '</div>'
                        ).join('');
                        stableList.innerHTML = stableHtml || '<div class="text-slate-500 text-center py-4 text-xs">Tidak ada</div>';
                        document.getElementById('stableCount').textContent = stableBlocks.length;
                    }'''

if old_increasing_js in content:
    content = content.replace(old_increasing_js, new_increasing_js)
    print("✅ Updated increasing blocks JS + added stable list")
else:
    print("⚠️ Could not find old increasing JS")

# 3. Add search filter function
search_function = '''
            // Filter block lists by search query
            function filterBlockLists(query) {
                query = query.toLowerCase().trim();
                const allBlocks = document.querySelectorAll('.block-item');
                let visibleCount = 0;
                
                allBlocks.forEach(block => {
                    const blockCode = block.getAttribute('data-block') || '';
                    if (query === '' || blockCode.includes(query)) {
                        block.style.display = '';
                        visibleCount++;
                    } else {
                        block.style.display = 'none';
                    }
                });
                
                const resultEl = document.getElementById('searchResultCount');
                if (resultEl) {
                    if (query) {
                        resultEl.textContent = visibleCount + ' blok ditemukan';
                    } else {
                        resultEl.textContent = '';
                    }
                }
            }

'''

# Insert before showBlockDetail function
insert_marker = 'function showBlockDetail(blockCode)'
insert_pos = content.find(insert_marker)
if insert_pos > 0:
    # Find the function declaration with proper indentation
    line_start = content.rfind('\n', 0, insert_pos) + 1
    indent = content[line_start:insert_pos]
    
    # Check if filter function already exists
    if 'function filterBlockLists' not in content:
        content = content[:line_start] + search_function + content[line_start:]
        print("✅ Added search filter function")
    else:
        print("✅ Search filter function already exists")

# Write back
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
print("\nEnhancements:")
print("  1. 3-column layout: Penurunan | Stabil | Kenaikan")
print("  2. Show all blocks (no limit)")
print("  3. Search box to filter blocks")
