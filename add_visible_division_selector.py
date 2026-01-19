"""
Add VISIBLE Division Selector UI to Dashboard
Insert after the main dashboard header
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find insertion point - after the main container div opens
# Look for the dashboard grid or main content area
insert_marker = '<div class="grid grid-cols-12 gap-6">'

if insert_marker in content:
    division_selector_html = '''
    <!-- ============================================ -->
    <!-- DIVISION SELECTOR (Week 0 Sprint Enhancement) -->
    <!-- ============================================ -->
    <div class="col-span-12 mb-4">
        <div class="bg-gradient-to-r from-blue-900/40 to-purple-900/40 rounded-2xl border-2 border-cyan-500/50 p-6 shadow-2xl">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h2 class="text-2xl font-black text-cyan-400 mb-1">🌍 ESTATE DIVISION SELECTOR</h2>
                    <p class="text-sm text-slate-300">Toggle between divisions to view their blocks</p>
                </div>
                <div class="flex gap-3">
                    <button onclick="filterByDivision('AME_II')" 
                        id="divBtn_AME_II"
                        class="px-6 py-3 rounded-xl font-bold text-sm bg-blue-600 text-white border-2 border-blue-400 shadow-lg hover:shadow-blue-500/50 transition-all transform hover:scale-105">
                        📍 AME II
                        <div class="text-xs opacity-75 mt-1">NDRE ✅</div>
                    </button>
                    <button onclick="filterByDivision('AME_IV')" 
                        id="divBtn_AME_IV"
                        class="px-6 py-3 rounded-xl font-bold text-sm bg-slate-700 text-slate-300 border-2 border-slate-600 hover:shadow-purple-500/50 transition-all transform hover:scale-105">
                        📍 AME IV
                        <div class="text-xs opacity-75 mt-1">NDRE ✅</div>
                    </button>
                    <button onclick="filterByDivision('ALL')" 
                        id="divBtn_ALL"
                        class="px-6 py-3 rounded-xl font-bold text-sm bg-slate-700 text-slate-300 border-2 border-slate-600 hover:shadow-emerald-500/50 transition-all transform hover:scale-105">
                        🌐 ALL ESTATE
                        <div class="text-xs opacity-75 mt-1">Mixed Coverage</div>
                    </button>
                </div>
            </div>
            
            <!-- Division Stats Display -->
            <div id="divisionStats" class="mt-4 p-4 bg-black/30 rounded-xl border border-cyan-500/30">
                <div class="flex items-center gap-3">
                    <div class="text-4xl">📊</div>
                    <div>
                        <div class="text-sm text-cyan-300 font-bold">Currently Viewing:</div>
                        <div class="text-lg text-white font-black">AME II (TIER 1) - 8 blocks | NDRE Available ✅ | Area: ~200 Ha</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    '''
    
    content = content.replace(insert_marker, division_selector_html + '\n    ' + insert_marker)
    
    # Save
    with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("="*60)
    print("✅ DIVISION SELECTOR ADDED!")
    print("="*60)
    print("\nWhat you'll see:")
    print("  🔵 AME II button (active/blue)")
    print("  🟣 AME IV button (inactive/gray)")
    print("  🟢 ALL ESTATE button (inactive/gray)")
    print("  📊 Division stats panel showing current selection")
    print("\nLocation: Top of dashboard, before block grid")
    print("\n🌐 REFRESH YOUR BROWSER NOW!")
    print("="*60)
else:
    print("❌ Marker not found! Trying alternative insertion point...")
    
    # Try alternative marker
    alt_marker = '<div class="container mx-auto px-4 py-6">'
    if alt_marker in content:
        content = content.replace(alt_marker, alt_marker + division_selector_html)
        with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Added via alternative marker!")
    else:
        print("❌ Could not find insertion point!")
        print("Available markers:")
        import re
        grids = re.findall(r'<div class="[^"]*grid[^"]*">', content)
        for g in grids[:5]:
            print(f"  {g}")
