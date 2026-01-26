import json
import datetime
import os
import matplotlib.pyplot as plt
import io
import base64

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
print("Loading Data...")
js_path = 'data/output/blocks_data_embed.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const BLOCKS_DATA = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]
data = json.loads(json_str)

# ---------------------------------------------------------
# 2. CALCULATE AGGREGATES
# ---------------------------------------------------------
total_blocks = len(data)
total_area = sum(d.get('luas_ha', 0) for d in data.values())
total_loss_idr = sum(d.get('loss_value_idr', 0) for d in data.values())
total_mitigation_idr = sum(d.get('mitigation_cost_idr', 0) for d in data.values())
sorted_blocks = sorted(data.values(), key=lambda x: x['rank'])
top_priority = sorted_blocks[:10]

# Status Counts
status_counts = {"INSOLVENCY": 0, "CRYPTIC COLLAPSE": 0, "WARNING": 0, "STABIL": 0}
for d in data.values():
    s = d.get('status_narrative', 'STABIL')
    if s not in status_counts: status_counts[s] = 0
    status_counts[s] += 1

# SPH Anomalies
anomalies = []
for d in data.values():
    sph_ref = d.get('sph', 0)
    sph_drone = d.get('drone_sph_all', 0)
    delta = sph_drone - sph_ref
    if abs(delta) > 15:
        anomalies.append({
            'code': d['block_code'],
            'ref': sph_ref,
            'drone': sph_drone,
            'delta': delta
        })
anomalies = sorted(anomalies, key=lambda x: abs(x['delta']), reverse=True)[:5]

# ---------------------------------------------------------
# 3. GENERATE RECOVERY CHART (Matplotlib)
# ---------------------------------------------------------
def generate_chart_base64():
    # Simulation Data (Aggregated)
    # Scenario A: Do Nothing (Decline continues)
    # Scenario B: Intervention (Dip then Recovery)
    
    years = ['2024 (Saat Ini)', '2025 (+1 Thn)', '2026 (+2 Thn)', '2027 (+3 Thn)']
    
    # Baseline: Current Realization projected downwards
    current_yield = sum(d.get('realisasi_total_ton', 0) for d in data.values())
    
    # Logic: Without action, loss accumulates. 
    # Let's approximate: Y1=100%, Y2=90%, Y3=75%, Y4=60% (Collapse)
    y_do_nothing = [
        current_yield, 
        current_yield * 0.9, 
        current_yield * 0.75, 
        current_yield * 0.60
    ]
    
    # Logic: With Action. Y1=100%, Y2=95% (Treatment shock), Y3=105% (Recovery), Y4=115% (Optimized)
    y_intervention = [
        current_yield,
        current_yield * 0.95,
        current_yield * 1.05,
        current_yield * 1.15
    ]

    plt.figure(figsize=(8, 4), dpi=100)
    
    # Plotting
    plt.plot(years, y_do_nothing, marker='o', color='#ef4444', linewidth=3, label='Tanpa Intervensi (Risk)')
    plt.plot(years, y_intervention, marker='o', color='#10b981', linewidth=3, label='Skenario Intervensi (Target)')
    
    # Filling area
    plt.fill_between(years, y_do_nothing, y_intervention, color='#10b981', alpha=0.1, label='Potential Value Saved')

    # Styling
    plt.title('Proyeksi Yield & Recovery Curve (3 Tahun)', fontsize=12, fontweight='bold', pad=15)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='lower left', fontsize=8)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.ylabel('Total Tonase (Ton)', fontsize=9)
    plt.tight_layout()

    # Save to Base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_str

chart_b64 = generate_chart_base64()


# ---------------------------------------------------------
# 4. GENERATE NARRATIVE (INDONESIAN)
# ---------------------------------------------------------
insolvency_pct = (status_counts.get('INSOLVENCY', 0) + status_counts.get('CRYPTIC COLLAPSE', 0)) / total_blocks * 100
narrative_text = ""

if insolvency_pct > 30:
    narrative_text += f'<span class="font-bold text-red-600">STATUS KRITIS:</span> Sekitar <span class="font-bold bg-white px-1">{int(insolvency_pct)}% dari total area</span> menunjukkan tanda-tanda kegagalan produksi tingkat lanjut (Insolvency). Angka ini jauh melampaui ambang batas risiko standar. '
elif insolvency_pct > 15:
    narrative_text += f'<span class="font-bold text-orange-600">STATUS WASPADA:</span> Kegagalan lokal yang signifikan terdeteksi (<span class="font-bold">{int(insolvency_pct)}% area</span>). Intervensi segera diperlukan untuk mencegah penyebaran. '
else:
    narrative_text += '<span class="font-bold text-emerald-600">STATUS STABIL:</span> Kondisi kebun secara umum sehat, hanya ditemukan isu terisolasi. '

narrative_text += f'Eksposur kerugian finansial dalam 3 tahun ke depan diproyeksikan mencapai <span class="font-bold text-slate-900 border-b-2 border-slate-300">Rp {total_loss_idr/1000000:,.1f} Juta</span> jika tidak dilakukan tindakan. '

if top_priority:
    top = top_priority[0]
    narrative_text += f'Prioritas utama adalah <span class="font-bold text-indigo-700">Blok {top["block_code"]}</span> ({top["status_narrative"]}), yang memerlukan mobilisasi sumber daya segera. '

if len(anomalies) > 0:
    top_anom = [a for a in anomalies if abs(a['delta']) > 20]
    if top_anom:
        narrative_text += f' <span class="italic text-slate-500 block mt-2 border-t border-indigo-200 pt-2">Catatan: Ditemukan diskrepanasi data signifikan pada {len(top_anom)} blok (contoh: {top_anom[0]["code"]}), disarankan audit sensus ulang sebelum treatment kimia.</span>'


# ---------------------------------------------------------
# 5. GENERATE HTML
# ---------------------------------------------------------
today_str = datetime.datetime.now().strftime("%d %B %Y")
currency = lambda x: f"Rp {x/1000000:,.1f} Jt"

html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Ringkasan Eksekutif - Cincin API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        body {{ font-family: 'Inter', sans-serif; -webkit-print-color-adjust: exact; }}
        @media print {{
            @page {{ size: A4 landscape; margin: 0.5cm; }}
            .no-print {{ display: none; }}
            body {{ background-color: white; padding: 0 !important; max-width: 100% !important; box-shadow: none !important; }}
        }}
    </style>
</head>
<body class="bg-slate-100 text-slate-800 p-8 pt-6 max-w-[290mm] mx-auto min-h-screen bg-white shadow-2xl origin-top scale-[0.95]">

    <!-- HEADER -->
    <div class="flex justify-between items-end border-b-4 border-indigo-900 pb-4 mb-6">
        <div>
            <h1 class="text-4xl font-black text-indigo-900 tracking-tighter uppercase mb-1">Ringkasan Eksekutif</h1>
            <p class="text-slate-500 font-bold tracking-widest text-sm uppercase">Cincin Api Early Warning System • V8 Hybrid Engine</p>
        </div>
        <div class="text-right">
            <div class="text-xs font-bold text-slate-400 uppercase">Tanggal Laporan</div>
            <div class="text-lg font-black text-slate-800">{today_str}</div>
        </div>
    </div>

    <!-- STRATEGIC COMMENTARY -->
    <div class="bg-indigo-50 border-l-4 border-indigo-600 p-4 mb-6 rounded-r-xl shadow-sm">
        <h2 class="text-xs font-black text-indigo-800 uppercase tracking-widest mb-2 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            Komentar Strategis
        </h2>
        <p class="text-slate-700 leading-relaxed text-sm">
            {narrative_text}
        </p>
    </div>

    <!-- KPI CARDS -->
    <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="col-span-1 p-3 bg-white border border-slate-200 rounded-xl shadow-sm">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Luas Area</div>
            <div class="text-2xl font-black text-slate-900">{total_area:,.1f} <span class="text-xs text-slate-400">Ha</span></div>
            <div class="text-[10px] font-bold text-slate-500 mt-1">{total_blocks} Blok Dianalisis</div>
        </div>
        <div class="col-span-1 p-3 bg-red-50 border border-red-100 rounded-xl shadow-sm">
            <div class="text-[10px] font-black text-red-400 uppercase tracking-widest mb-1">Potensi Loss (3 Thn)</div>
            <div class="text-2xl font-black text-red-900">{currency(total_loss_idr)}</div>
            <div class="text-[10px] font-bold text-red-600 mt-1">Tanpa Tindakan</div>
        </div>
        <div class="col-span-1 p-3 bg-emerald-50 border border-emerald-100 rounded-xl shadow-sm">
            <div class="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Estimasi Biaya Mitigasi</div>
            <div class="text-2xl font-black text-emerald-900">{currency(total_mitigation_idr)}</div>
            <div class="text-[10px] font-bold text-emerald-600 mt-1">Capex Dibutuhkan</div>
        </div>
        <div class="col-span-1 p-3 bg-indigo-50 border border-indigo-100 rounded-xl shadow-sm">
            <div class="text-[10px] font-black text-indigo-400 uppercase tracking-widest mb-1">Rasio Kritis</div>
            <div class="text-2xl font-black text-indigo-900">{round((status_counts['INSOLVENCY'] + status_counts['CRYPTIC COLLAPSE'])/total_blocks * 100)}%</div>
            <div class="text-[10px] font-bold text-indigo-500 mt-1">dari Total Blok</div>
        </div>
    </div>

    <!-- MAIN GRID 3 COLUMNS -->
    <div class="grid grid-cols-3 gap-6 mb-4 h-full">
        
        <!-- COL 1: PRIORITY TABLE (Wider) -->
        <div class="col-span-2 flex flex-col h-full">
            <div class="mb-2 flex justify-between items-center">
                <h3 class="font-black text-slate-800 uppercase tracking-tight text-sm">🚨 Target Prioritas (Top 10)</h3>
            </div>
            <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm flex-grow">
                <table class="w-full text-xs text-left">
                    <thead class="bg-slate-800 text-white uppercase font-black">
                        <tr>
                            <th class="p-2 py-3">Rank</th>
                            <th class="p-2 py-3">Blok</th>
                            <th class="p-2 py-3">Status</th>
                            <th class="p-2 py-3">Attack Rate</th>
                            <th class="p-2 py-3 text-center">Rencana Tindakan</th>
                            <th class="p-2 py-3 text-right">Risk Value</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
"""

count = 0
for b in top_priority:
    if count >= 8: break # Limit to 8 rows to fit page better
    count += 1
    rank = count
    
    color = "text-slate-600"
    if b['status_narrative'] == 'INSOLVENCY': color = "text-red-600 font-bold bg-red-50"
    elif b['status_narrative'] == 'CRYPTIC COLLAPSE': color = "text-red-500 font-bold"
    
    # INDONESIAN ACTIONS
    action = "MONITORING"
    action_color = "text-slate-500"
    
    sph_ref = b.get('sph', 0)
    sph_drone = b.get('drone_sph_all', 0)
    delta = abs(sph_drone - sph_ref)
    
    if delta > 20:
        action = "🔍 AUDIT SENSUS"
        action_color = "text-indigo-600 font-bold bg-indigo-50 border border-indigo-100 rounded px-2 py-1"
    elif b['status_narrative'] == 'INSOLVENCY':
        action = "🚜 REPLANTING/SALVAGE"
        action_color = "text-red-700 font-bold bg-red-100 border border-red-200 rounded px-2 py-1"
    elif b['status_narrative'] == 'CRYPTIC COLLAPSE':
        action = "💉 FUNGISIDA + ISOLASI"
        action_color = "text-orange-700 font-bold bg-orange-100 border border-orange-200 rounded px-2 py-1"
    elif b['attack_rate'] > 5:
        action = "🛡️ TRENCHING ISOLASI"
        action_color = "text-yellow-700 font-bold bg-yellow-100 border border-yellow-200 rounded px-2 py-1"
    
    status_ind = b['status_narrative']
    if status_ind == 'INSOLVENCY': status_ind = 'KEBANGKRUTAN'
    elif status_ind == 'CRYPTIC COLLAPSE': status_ind = 'KRITIS TERSEMBUNYI'
    
    html_content += f"""
                        <tr class="hover:bg-slate-50">
                            <td class="p-2 text-center text-slate-400 font-bold">{rank}</td>
                            <td class="p-2 font-black">{b['block_code']}</td>
                            <td class="p-2 text-[10px] {color}">{status_ind}</td>
                            <td class="p-2 font-mono text-slate-500">{b['attack_rate']}%</td>
                            <td class="p-2 text-center"><span class="{action_color} text-[9px] uppercase tracking-wide">{action}</span></td>
                            <td class="p-2 text-right font-mono font-bold text-red-600">{currency(b['loss_value_idr'])}</td>
                        </tr>
    """

html_content += """
                    </tbody>
                </table>
            </div>
        </div>

        <!-- COL 2: CHARTS & INSIGHTS -->
        <div class="col-span-1 flex flex-col gap-6">
            
            <!-- RECOVERY CHART -->
            <div class="bg-white border border-slate-200 rounded-xl p-2 shadow-sm">
                <img src="data:image/png;base64,""" + chart_b64 + """" class="w-full h-auto rounded" alt="Recovery Chart">
            </div>

            <!-- ANOMALY TABLE -->
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 flex-grow">
                <h3 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-3">Anomali Data (Top 5)</h3>
                <div class="space-y-2">
"""

for a in anomalies:
    sign = "+" if a['delta'] > 0 else ""
    color = "text-emerald-600" if a['delta'] > 0 else "text-red-500"
    html_content += f"""
                    <div class="flex justify-between items-center text-xs border-b border-slate-200 pb-1 last:border-0 last:pb-0">
                        <div>
                            <span class="font-bold block">{a['code']}</span>
                            <span class="text-[9px] text-slate-400">Ref: {a['ref']}</span>
                        </div>
                        <div class="text-right">
                            <span class="font-black font-mono {color} ml-1 text-sm">{sign}{round(a['delta'],1)}</span>
                            <span class="text-[9px] text-slate-400 block">Delta</span>
                        </div>
                    </div>
    """

html_content += """
                </div>
            </div>

        </div>
    </div>
    
    <!-- FOOTER -->
    <div class="bg-slate-900 text-white rounded-xl p-4 flex justify-between items-center mt-auto">
        <div class="text-xs text-slate-400">
            Dicetak otomatis oleh Sistem Cincin API • Rahasia & Terbatas
        </div>
        <div class="text-xs font-bold text-white">
            Halaman 1 dari 1
        </div>
    </div>

</body>
</html>
"""

# ---------------------------------------------------------
# 6. WRITE FILE
# ---------------------------------------------------------
output_path = 'data/output/executive_summary.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Laporan Bahasa Indonesia generated at: {output_path}")
