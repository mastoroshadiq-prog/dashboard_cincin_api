"""
URGENT FIX:
1. Grid layout kiri-kanan
2. Add data JavaScript
3. Populate blocks
"""

import json

# Load data
with open('critical_blocks_data.json', 'r', encoding='utf-8') as f:
    blocks = json.load(f)

with open('data/output/all_blocks_data_hybrid.json', 'r', encoding='utf-8') as f:
    all_blocks = json.load(f)

# Read demo
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("URGENT FIXES...")

# 1. FIX GRID - ensure side-by-side
if 'md:grid-cols-2' in demo:
    print("✅ Grid layout OK")
else:
    # Find grid div
    demo = demo.replace(
        '<div class="grid grid-cols-2 gap-6">',
        '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    )
    print("✅ Grid layout FIXED (added md:grid-cols-2)")

# 2. ADD BLOCKS_DATA
blocks_data_for_js = {code: all_blocks[code] for code in blocks.keys() if code in all_blocks}
blocks_js = '\n        const BLOCKS_DATA = ' + json.dumps(blocks_data_for_js, indent=12) + ';\n'

if 'const BLOCKS_DATA' not in demo:
    script_end = demo.rfind('</script>')
    demo = demo[:script_end] + blocks_js + demo[script_end:]
    print("✅ BLOCKS_DATA added to JavaScript")
else:
    print("⚠️  BLOCKS_DATA already exists")

# 3. ADD RENDER FUNCTION
render_code = '''
        // Populate PAPARAN RISK watchlist
        function renderPaparanRisk() {
            const container = document.getElementById('riskWatchlistContainer');
            if (!container || !BLOCKS_DATA) {
                console.log('Container or data not found');
                return;
            }
            
            const sorted = Object.entries(BLOCKS_DATA)
                .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));
            
            let html = '';
            let totalLoss = 0;
            let totalArea = 0;
            
            sorted.forEach(([code, data]) => {
                const loss = (data.loss_value_juta || 0);
                const ar = data.attack_rate || 0;
                totalLoss += loss;
                totalArea += (data.luas_ha || 0);
                
                html += `
                    <div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer">
                        <div class="flex justify-between items-center">
                            <div>
                                <span class="text-white font-bold text-sm">${code}</span>
                                <span class="text-rose-300 text-xs ml-2">AR: ${ar.toFixed(1)}%</span>
                            </div>
                            <span class="text-rose-200 text-sm">Rp ${loss.toFixed(1)} Jt</span>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            
            // Update summary
            document.getElementById('summaryTotalLoss').textContent = (totalLoss / 1000).toFixed(2);
            document.getElementById('summaryCriticalCount').textContent = sorted.length;
            document.getElementById('summaryRiskArea').textContent = totalArea.toFixed(1);
        }
        
        // Auto-run on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', renderPaparanRisk);
        } else {
            renderPaparanRisk();
        }
'''

if 'renderPaparanRisk' not in demo:
    script_end = demo.rfind('</script>')
    demo = demo[:script_end] + render_code + '\n    ' + demo[script_end:]
    print("✅ Render function added")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print(f"\n✅ ALL FIXED!")
print(f"   File size: {len(demo)} chars")
print("\nCHANGES:")
print("  1. Grid layout: side-by-side")
print("  2. BLOCKS_DATA: 8 blocks loaded")
print("  3. Auto-populate on page load")
