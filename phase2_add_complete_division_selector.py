"""
PHASE 2: Add Complete Division Selector (All 14 Divisions)
Replace limited selector with full estate coverage
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the division selector section
old_selector = '''                <div class="flex gap-3">
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
                        <div class="text-xs opacity-75 mt-1">Mixed</div>
                    </button>
                </div>'''

new_selector = '''                <div class="flex flex-wrap gap-2">
                    <!-- AME Divisions -->
                    <button onclick="filterByDivision('AME01')" id="divBtn_AME01"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-blue-400 transition-all">
                        AME I
                    </button>
                    <button onclick="filterByDivision('AME02')" id="divBtn_AME02"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-blue-600 text-white border-2 border-blue-400 transition-all">
                        AME II ✅
                    </button>
                    <button onclick="filterByDivision('AME03')" id="divBtn_AME03"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-blue-400 transition-all">
                        AME III
                    </button>
                    <button onclick="filterByDivision('AME04')" id="divBtn_AME04"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-blue-400 transition-all">
                        AME IV ✅
                    </button>
                    
                    <div class="w-px h-8 bg-slate-600"></div>
                    
                    <!-- DBE Divisions -->
                    <button onclick="filterByDivision('DBE01')" id="divBtn_DBE01"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-green-400 transition-all">
                        DBE I
                    </button>
                    <button onclick="filterByDivision('DBE02')" id="divBtn_DBE02"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-green-400 transition-all">
                        DBE II
                    </button>
                    <button onclick="filterByDivision('DBE03')" id="divBtn_DBE03"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-green-400 transition-all">
                        DBE III
                    </button>
                    <button onclick="filterByDivision('DBE04')" id="divBtn_DBE04"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-green-400 transition-all">
                        DBE IV
                    </button>
                    <button onclick="filterByDivision('DBE05')" id="divBtn_DBE05"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-green-400 transition-all">
                        DBE V
                    </button>
                    
                    <div class="w-px h-8 bg-slate-600"></div>
                    
                    <!-- OLE Divisions -->
                    <button onclick="filterByDivision('OLE01')" id="divBtn_OLE01"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-purple-400 transition-all">
                        OLE I
                    </button>
                    <button onclick="filterByDivision('OLE02')" id="divBtn_OLE02"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-purple-400 transition-all">
                        OLE II
                    </button>
                    <button onclick="filterByDivision('OLE03')" id="divBtn_OLE03"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-purple-400 transition-all">
                        OLE III
                    </button>
                    <button onclick="filterByDivision('OLE04')" id="divBtn_OLE04"
                        class="px-4 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-purple-400 transition-all">
                        OLE IV
                    </button>
                    
                    <div class="w-px h-8 bg-slate-600"></div>
                    
                    <!-- ALL ESTATE -->
                    <button onclick="filterByDivision('ALL')" id="divBtn_ALL"
                        class="px-6 py-2 rounded-lg font-bold text-xs bg-slate-700 text-slate-300 border border-slate-600 hover:border-emerald-400 transition-all">
                        🌐 ALL ESTATE (644 blocks)
                    </button>
                </div>'''

if old_selector in content:
    content = content.replace(old_selector, new_selector)
    
    with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("="*70)
    print("✅ COMPLETE DIVISION SELECTOR ADDED!")
    print("="*70)
    print("\nAdded buttons for:")
    print("  ✅ AME: AME01, AME02, AME03, AME04 (4 divisions)")
    print("  ✅ DBE: DBE01-05 (5 divisions)")
    print("  ✅ OLE: OLE01-04 (4 divisions)")
    print("  ✅ ALL ESTATE (644 blocks)")
    print("\n🎯 Total: 14 division buttons + ALL option")
    print("\n🌐 REFRESH BROWSER - You can now switch between ALL divisions!")
    print("="*70)
else:
    print("❌ Could not find old selector to replace!")
    print("Searching for alternative pattern...")
