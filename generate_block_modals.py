"""
Create interactive block detail cards based on Image 2 structure
Each block when clicked shows detailed breakdown modal
"""

import json

# Load blocks data
with open('critical_blocks_data.json', 'r') as f:
    blocks = json.load(f)

# Load full data for additional metrics
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    all_blocks = json.load(f)

# Build complete block data with all metrics
complete_blocks = {}
for code in blocks.keys():
    if code in all_blocks:
        data = all_blocks[code]
        complete_blocks[code] = {
            'code': code,
            'loss_juta': round(data.get('loss_value_juta', 0), 2),
            'potensi': data.get('potensi_ton_ha', 0),
            'realisasi': data.get('realisasi_ton_ha', 0),
            'gap_volume': data.get('gap_ton_ha', 0),
            'gap_persen': data.get('gap_pct', 0),
            'luas_ha': data.get('luas_ha', 0),
            'tahun': data.get('tt', 0),
            'sph': data.get('sph', 0),
            'ar': data.get('attack_rate', 0),
            'census_rate': data.get('census_rate_pct', 0),
            'total_loss': round(data.get('loss_value_juta', 0), 2)
        }

# Generate modal HTML for each block
modals_html = ""

for code, data in complete_blocks.items():
    # Determine status
    status = "STABIL ✓" if abs(data['gap_persen']) < 10 else "DEGRADASI ⚠️"
    status_class = "bg-green-600" if "STABIL" in status else "bg-orange-600"
    
    modal_html = f'''
    <!-- Modal for Block {code} -->
    <div id="modal{code}" class="hidden fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-gradient-to-br from-indigo-900 to-purple-900 rounded-3xl border-2 border-indigo-400 max-w-2xl w-full p-8 relative">
            <!-- Close button -->
            <button onclick="closeBlockModal('{code}')" 
                class="absolute top-4 right-4 text-white hover:text-rose-300 text-3xl font-bold">×</button>
            
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
                <div>
                    <p class="text-indigo-300 text-sm uppercase">Estimasi Kerugian (Blok A)</p>
                </div>
                <div class="text-right">
                    <p class="text-6xl font-black text-white">{code}</p>
                </div>
            </div>
            
            <!-- Large Loss Value -->
            <div class="mb-6">
                <p class="text-red-400 text-5xl font-black">Rp <span class="text-7xl">{int(data['loss_juta'])}</span> Juta</p>
            </div>
            
            <!-- Metrics Grid -->
            <div class="grid grid-cols-2 gap-6 bg-indigo-950/50 p-6 rounded-2xl mb-6">
                <!-- Potensi & Gap Volume -->
                <div>
                    <p class="text-indigo-300 text-xs uppercase mb-1">Potensi Est</p>
                    <p class="text-white text-3xl font-black">{data['potensi']:.2f} <span class="text-lg">Ton/Ha</span></p>
                </div>
                <div class="text-right">
                    <p class="text-indigo-300 text-xs uppercase mb-1">Gap (Volume)</p>
                    <p class="text-red-400 text-3xl font-black">{abs(data['gap_volume']):.2f}</p>
                </div>
                
                <!-- Realisasi & Gap Persen -->
                <div>
                    <p class="text-indigo-300 text-xs uppercase mb-1">Realisasi ACT</p>
                    <p class="text-white text-3xl font-black">{data['realisasi']:.2f} <span class="text-lg">Ton/Ha</span></p>
                </div>
                <div class="text-right">
                    <p class="text-indigo-300 text-xs uppercase mb-1">Gap (Persen)</p>
                    <p class="text-green-400 text-3xl font-black">{abs(data['gap_persen']):.0f}%</p>
                </div>
            </div>
            
            <!-- Additional Info Grid -->
            <div class="grid grid-cols-2 gap-4 mb-6">
                <div>
                    <p class="text-slate-400 text-sm uppercase">Luas Area</p>
                    <p class="text-white text-2xl font-bold">{data['luas_ha']:.1f} <span class="text-base">Ha</span></p>
                </div>
                <div class="text-right">
                    <p class="text-slate-400 text-sm uppercase">Tahun Tanam</p>
                    <p class="text-white text-2xl font-bold">{data['tahun']}</p>
                </div>
                
                <div>
                    <p class="text-slate-400 text-sm uppercase">Kerapatan (SPH)</p>
                    <p class="text-white text-2xl font-bold">{data['sph']}</p>
                </div>
                <div class="text-right">
                    <p class="text-slate-400 text-sm uppercase">Tingkat Infeksi (NDRE vs Sensus)</p>
                    <p class="text-white text-base font-bold">
                        <span class="text-red-400">{data['ar']:.1f}%</span> vs <span class="text-orange-400">{data['census_rate']:.2f}%</span>
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="flex items-center justify-between pt-4 border-t border-white/20">
                <div>
                    <p class="text-slate-400 text-xs uppercase mb-1">Total</p>
                    <p class="text-emerald-400 text-2xl font-black">Rp {data['total_loss']:.2f} Juta</p>
                </div>
                <div class="flex items-center gap-2">
                    <p class="text-slate-400 text-xs uppercase">Status Indikasi</p>
                    <div class="{status_class} px-4 py-2 rounded-lg">
                        <p class="text-white font-bold text-sm">{status}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
'''
    modals_html += modal_html

# Save modals
with open('block_detail_modals.html', 'w', encoding='utf-8') as f:
    f.write(modals_html)

# Generate clickable list JavaScript
js_onclick = "const openBlockModal = (code) => { document.getElementById('modal' + code).classList.remove('hidden'); };\n"
js_onclick += "const closeBlockModal = (code) => { document.getElementById('modal' + code).classList.add('hidden'); };\n"

with open('block_modals_js.txt', 'w', encoding='utf-8') as f:
    f.write(js_onclick)

print("✅ Block detail modals generated!")
print(f"   Created modals for {len(complete_blocks)} blocks")
print("   Files: block_detail_modals.html, block_modals_js.txt")
