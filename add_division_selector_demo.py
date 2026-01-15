"""
QUICK DEMO: Add Division Selector to Dashboard
This is a minimal enhancement to show AME II vs AME IV toggle
"""

# Read current dashboard
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert division selector (after Paparan Risk title)
insert_marker = '<h2 class="text-3xl font-black text-white mb-4">🚨 Paparan Risk (Blok Kritis)</h2>'

if insert_marker in content:
    division_selector_html = '''
    
    <!-- DIVISION SELECTOR (NEW - Week 0 Sprint Enhancement) -->
    <div class="mb-6 p-4 bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl border border-blue-500/30">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-sm font-bold text-blue-300 uppercase tracking-wider mb-2">📍 Select Division</h3>
                <p class="text-xs text-slate-400">Showing blocks from:</p>
            </div>
            <div class="flex gap-2">
                <button onclick="filterByDivision('AME_II')" 
                    id="divBtn_AME_II"
                    class="px-4 py-2 rounded-lg font-bold bg-blue-600 text-white border-2 border-blue-400 shadow-lg">
                    AME II ✅ (NDRE)
                </button>
                <button onclick="filterByDivision('AME_IV')" 
                    id="divBtn_AME_IV"
                    class="px-4 py-2 rounded-lg font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">
                    AME IV ✅ (NDRE)
                </button>
                <button onclick="filterByDivision('ALL')" 
                    id="divBtn_ALL"
                    class="px-4 py-2 rounded-lg font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">
                    ALL ESTATE
                </button>
            </div>
        </div>
        <div id="divisionStats" class="mt-3 text-xs text-cyan-400 font-mono">
            Current: AME II - 8 blocks displayed
        </div>
    </div>
    '''
    
    content = content.replace(insert_marker, insert_marker + division_selector_html)
    print("✅ Added division selector UI")
else:
    print("❌ Marker not found")

# Add JavaScript function
js_function = '''
    // Division Filter Function (Week 0 Sprint)
    let currentDivision = 'AME_II';
    
    function filterByDivision(division) {
        currentDivision = division;
        
        // Update button states
        document.getElementById('divBtn_AME_II').className = division === 'AME_II' 
            ? 'px-4 py-2 rounded-lg font-bold bg-blue-600 text-white border-2 border-blue-400 shadow-lg'
            : 'px-4 py-2 rounded-lg font-bold bg-slate-700 text-slate-300 border-2 border-slate-600';
        
        document.getElementById('divBtn_AME_IV').className = division === 'AME_IV'
            ? 'px-4 py-2 rounded-lg font-bold bg-purple-600 text-white border-2 border-purple-400 shadow-lg'
            : 'px-4 py-2 rounded-lg font-bold bg-slate-700 text-slate-300 border-2 border-slate-600';
        
        document.getElementById('divBtn_ALL').className = division === 'ALL'
            ? 'px-4 py-2 rounded-lg font-bold bg-emerald-600 text-white border-2 border-emerald-400 shadow-lg'
            : 'px-4 py-2 rounded-lg font-bold bg-slate-700 text-slate-300 border-2 border-slate-600';
        
        // Update stats display
        let statsText = '';
        if (division === 'AME_II') {
            statsText = 'AME II (TIER 1) - 8 blocks | NDRE Available ✅ | Total Area: ~200 Ha';
        } else if (division === 'AME_IV') {
            statsText = 'AME IV (TIER 1) - 28 blocks | NDRE Available ✅ | Total Area: TBD';
        } else {
            statsText = 'ALL ESTATE - 36+ blocks | Mixed NDRE coverage';
        }
        document.getElementById('divisionStats').innerHTML = `<strong>📊 ${statsText}</strong>`;
        
        // TODO: Actually filter BLOCKS_DATA and re-render
        // For now, just show message
        alert(`Division filter: ${division}\\n\\nNote: Block filtering will be implemented next!\\nCurrently showing AME II blocks.`);
    }
'''

# Insert before closing </script> tag
content = content.replace('</script>', js_function + '\n    </script>')
print("✅ Added filter JavaScript")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
print("✅ DASHBOARD ENHANCED!")
print("="*60)
print("\nWhat was added:")
print("  1. Division selector buttons (AME II, AME IV, ALL)")
print("  2. Visual feedback (active state)")
print("  3. Division stats display")
print("  4. Filter function (placeholder)")
print("\n📂 File: data/output/DASHBOARD_DEMO_FEATURES.html")
print("🌐 Open in browser to see the enhancement!")
print("="*60)
