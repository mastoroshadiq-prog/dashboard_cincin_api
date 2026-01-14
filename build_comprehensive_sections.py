"""
Build COMPREHENSIVE dashboard with FULL content:
- ALL 8 critical blocks in PAPARAN RISK
- ALL 8 blocks in STATISTIK BLOK
- ALL modal charts (Current Loss, 3-Year, Treatment, Savings, ROI)
"""

import json

# Load blocks data
with open('critical_blocks_data.json', 'r') as f:
    blocks = json.load(f)

# Calculate total
total_loss = sum(b['loss_juta'] for b in blocks.values())
total_loss_miliar = total_loss / 1000

print("Building COMPREHENSIVE dashboard...")
print(f"8 Blocks loaded, Total Loss: Rp {total_loss_miliar:.2f} Miliar")

# Build HTML sections
# This will be integrated into DASHBOARD_DEMO_FEATURES.html

# Generate PAPARAN RISK section (8 blocks watchlist)
paparan_html = ""
for code, data in sorted(blocks.items(), key=lambda x: x[1]['risk_score'], reverse=True):
   paparan_html += f'''
                        <div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>
                                    <span class="text-rose-300 text-xs ml-2">AR: {data['ar']}%</span>
                                </div>
                                <span class="text-rose-200">Rp {data['loss_juta']:.1f} Jt</span>
                            </div>
                        </div>
'''

# Generate STATISTIK BLOK section (8 blocks detail)
statistik_html = ""
for code, data in sorted(blocks.items(), key=lambda x: x[1]['loss_juta'], reverse=True):
    statistik_html += f'''
                        <div class="bg-blue-900/40 p-3 rounded-xl border border-blue-500/30 hover:border-blue-400 transition-all cursor-pointer">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>
                                    <span class="text-blue-300 text-xs ml-2">Gap: {data['gap']:.2f} T/Ha</span>
                                </div>
                                <span class="text-blue-200">Rp {data['loss_juta']:.1f} Jt</span>
                            </div>
                        </div>
'''

# Save sections
with open('paparan_section.html', 'w', encoding='utf-8') as f:
    f.write(paparan_html)

with open('statistik_section.html', 'w', encoding='utf-8') as f:
    f.write(statistik_html)

# Generate JavaScript data
js_blocks = f"const BLOCKS_DATA = {json.dumps(blocks, indent=8)};"

with open('blocks_data_js.txt', 'w', encoding='utf-8') as f:
    f.write(js_blocks)

print("\n✅ Sections generated:")
print("   - paparan_section.html (PAPARAN RISK watchlist)")
print("   - statistik_section.html (STATISTIK BLOK details)")
print("   - blocks_data_js.txt (JavaScript data object)")
print("\nReady to integrate into comprehensive dashboard!")
