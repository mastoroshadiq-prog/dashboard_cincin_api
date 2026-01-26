
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\risk_metrics_real.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    risk_data = json.load(f)

# 1. INJECT DATA VARIABLE
# We inject it right after TBM_REAL_STATS or TBM_STATS_DATA
risk_data_script = f"\n            const RISK_METRICS_DATA = {json.dumps(risk_data)};\n"

if 'const RISK_METRICS_DATA' not in html_content:
    if 'const TBM_REAL_STATS' in html_content:
        html_content = html_content.replace('const TBM_REAL_STATS', risk_data_script + 'const TBM_REAL_STATS')
    elif 'const HISTORICAL_YIELDS' in html_content:
        html_content = html_content.replace('const HISTORICAL_YIELDS', risk_data_script + 'const HISTORICAL_YIELDS')
    print("Risk Data Injected.")


# 2. UPDATE DATA FETCH LOGIC IN JS
# Cari bagian: // First try BLOCKS_DATA
# Kita akan menyisipkan logic baru SEBELUM itu.

target_fetch_logic = """
                // First try BLOCKS_DATA
                if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                }
"""
new_fetch_logic = """
                // PRIORITY: Try Real Risk Metrics Data
                if (typeof RISK_METRICS_DATA !== 'undefined' && RISK_METRICS_DATA[blockCode]) {
                    const rd = RISK_METRICS_DATA[blockCode];
                    attackRate = (rd.attack_rate !== undefined) ? rd.attack_rate : 0;
                    sph = (rd.sph !== undefined) ? rd.sph : 0;
                    // Pass infected data via riskData object if possible, or store temporarily
                    if (!riskData) riskData = {};
                    riskData.total_infected = rd.total_infected;
                }
                // Fallback: First try BLOCKS_DATA
                else if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                }
"""

# Lakukan replace string manual karena select string mungkin susah dengan whitespace
if 'RISK_METRICS_DATA[blockCode]' not in html_content:
    # Kita cari string unik di baris sebelumnya
    anchor = "// Get risk metrics - try multiple sources"
    if anchor in html_content:
        # Regex replacement untuk safe insertion
        # Kita replace logic BLOCKS_DATA lama dengan logic Baru + Lama
        # Tapi regex harus hati-hati. Mending replace logic lama dengan yang baru (yang mengandung fallback)
        
        # Cari pola yang pas
        pattern = r'// First try BLOCKS_DATA\s+if \(riskData\) \{[^}]+\}'
        
        # Cek apakah regex ketemu
        match = re.search(pattern, html_content)
        if match:
             html_content = html_content.replace(match.group(0), new_fetch_logic.strip())
             print("Fetch Logic Updated via Regex.")
        else:
            # Coba string replace sederhana jika format indentasi pas
            # Ambil potongan dari file view sebelumnya (Baris 19545-19550)
            old_block = """                // First try BLOCKS_DATA
                if (riskData) {
                    attackRate = parseFloat(riskData.attack_rate) || 0;
                    sph = parseFloat(riskData.sph) || 0;
                    lossValue = parseFloat(riskData.loss_value_juta) || 0;
                }"""
            
            if old_block in html_content:
                html_content = html_content.replace(old_block, new_fetch_logic)
                print("Fetch Logic Updated via String Replace.")
            else:
                print("WARNING: Could not match fetch logic block exactly.")

# 3. UPDATE DISPLAY LOGIC (Allow 0 values)
# attackRate > 0 -> attackRate >= 0 (tapi hati2 kalau emang N/A)
# Kita logic: Jika Data Ada (ditemukan di JSON), tampilkan meski 0. Jika tidak ada, baru N/A.
# Tapi untuk simplifikasi: Jika RISK_METRICS_DATA[blockCode] exist, berarti datanya valid (walau 0).

# Kita update logic display attackRate
display_logic_ar_old = """                const arEl = document.getElementById('detailAttackRate');
                if (attackRate > 0) {
                    arEl.textContent = attackRate.toFixed(1) + ' %';
                    arEl.className = 'text-xl font-bold text-red-400';
                } else {
                    arEl.textContent = 'N/A';
                    arEl.className = 'text-xl font-bold text-slate-500';
                }"""

display_logic_ar_new = """                const arEl = document.getElementById('detailAttackRate');
                // Check if we have real data source
                const hasRiskSource = (typeof RISK_METRICS_DATA !== 'undefined' && RISK_METRICS_DATA[blockCode]);
                
                if (attackRate > 0) {
                    arEl.textContent = attackRate.toFixed(1) + ' %';
                    arEl.className = 'text-xl font-bold text-red-400';
                } else if (hasRiskSource && attackRate === 0) {
                    arEl.textContent = '0.0 % (Sehat)';
                    arEl.className = 'text-xl font-bold text-green-400';
                } else {
                    arEl.textContent = 'N/A';
                    arEl.className = 'text-xl font-bold text-slate-500';
                }"""

if display_logic_ar_old in html_content:
    html_content = html_content.replace(display_logic_ar_old, display_logic_ar_new)
    print("AR Display Logic Updated.")
    
# Update logic display SPH
# Sama kasusnya, izinkan 0 atau tampilkan jika source ada
# Tapi SPH 143.33 harusnya tembus > 0.
# Kita update juga biar konsisten

display_logic_sph_old = """                const sphEl = document.getElementById('detailSPH');
                if (sph > 0) {
                    sphEl.textContent = Math.round(sph);
                    sphEl.className = 'text-xl font-bold text-yellow-400';
                } else {
                    sphEl.textContent = 'N/A';
                    sphEl.className = 'text-xl font-bold text-slate-500';
                }"""

display_logic_sph_new = """                const sphEl = document.getElementById('detailSPH');
                if (sph > 0) {
                    sphEl.textContent = Math.round(sph);
                    sphEl.className = 'text-xl font-bold text-yellow-400';
                } else if (hasRiskSource) {
                     sphEl.textContent = Math.round(sph); // Show even if 0
                     sphEl.className = 'text-xl font-bold text-slate-300';
                } else {
                    sphEl.textContent = 'N/A';
                    sphEl.className = 'text-xl font-bold text-slate-500';
                }"""

if display_logic_sph_old in html_content:
    html_content = html_content.replace(display_logic_sph_old, display_logic_sph_new)
    print("SPH Display Logic Updated.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML Risk Metrics Deep Fix Complete.")
