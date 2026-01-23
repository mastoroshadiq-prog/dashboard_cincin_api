
import json
import re
import os

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\risk_metrics_real.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    risk_data = json.load(f)

# 1. HAPUS SEMUA DEKLARASI RISK_METRICS_DATA LAMA
# Pattern: const RISK_METRICS_DATA = \{.*?\}; (dotall)
# Kita gunakan regex flags re.DOTALL
# Hati-hati jangan hapus terlalu banyak.
# Karena json dump bisa mengandung semicolon, kita cari pattern yang aman.
# Kita asumsikan deklarasi dimulai dengan "const RISK_METRICS_DATA =" dan diakhiri dengan semicolon di level root.
# Guna amannya: kita replace variabel dengan komentar kosong.
# Tapi regex sulit.

# Pendekatan string:
# Kita tahu text injection kita sebelumnya dimulai dengan "const RISK_METRICS_DATA = {"
# Kita cari semua kemunculan string ini dan hapus sampai... akhir block? Sulit.

# Kita pakai data yang kita inject tadi sebagai 'search query' untuk menghapusnya? Tidak, karena dinamis.

# SOLUSI: Inject variabel baru dengan nama BEDA: `RISK_METRICS_DATA_REV`
# Lalu update referensi di kode JS.
# Ini menjamin yang lama tidak terpakai.

new_var_name = "RISK_METRICS_DATA_FINAL"
new_data_script = f"<script>\nconst {new_var_name} = {json.dumps(risk_data)};\nconsole.log('RISK METRICS FINAL LOADED', {new_var_name}['A012C']);\n</script>\n"

# Inject di akhir body
if f"const {new_var_name}" not in html_content:
    html_content = html_content.replace('</body>', new_data_script + '</body>')
    print("Injected New Data Variable: " + new_var_name)

# Update Logic JS untuk menggunakan variable baru
# Cari: if (typeof RISK_METRICS_DATA !== 'undefined'
# Ganti dengan: if (typeof RISK_METRICS_DATA_FINAL !== 'undefined'

html_content = html_content.replace('RISK_METRICS_DATA', new_var_name)
print("Updated JS references to new variable.")

# Masalah: Replacement di atas juga mengganti string deklarasi `const RISK_METRICS_DATA =` menjadi `const RISK_METRICS_DATA_FINAL =`.
# Jadi variabel lama jadi bernama baru (dan isinya lama/salah).
# Variabel baru yang kita inject di bawah juga bernama baru.
# Jadi ada DUA variabel bernama sama -> Syntax Error / Conflict.

# KOREKSI:
# Jangan rename variabel di text replace global.
# Kita cari logic JS *pengambilannya* saja.
# Logic JS di `showBlockDetail`:
# `if (typeof RISK_METRICS_DATA !== 'undefined' && RISK_METRICS_DATA[blockCode])`

old_logic_snippet = "typeof RISK_METRICS_DATA !=="
new_logic_snippet = f"typeof {new_var_name} !=="

if old_logic_snippet in html_content:
    html_content = html_content.replace("RISK_METRICS_DATA", new_var_name)
    # Ini masih berisiko me-rename deklarasi lama.
    
    # Solusi Lebih Cerdas:
    # Biarkan deklarasi lama (RISK_METRICS_DATA).
    # Kita inject variabel baru (RISK_METRICS_DATA_FINAL).
    # Kita ubah logic JS untuk memprioritaskan FINAL.
    
    # Tapi replace global "RISK_METRICS_DATA" -> "RISK_METRICS_DATA_FINAL" akan me-rename deklarasi lama juga.
    # Jadi deklarasi lama jadi "const RISK_METRICS_DATA_FINAL = ...old data...".
    # Dan deklarasi baru di bawah jadi "const RISK_METRICS_DATA_FINAL = ...new data...".
    # Hasilnya: Syntax Error (Identifier '...' has already been declared).
    
    pass 

# STRATEGI HAPUS YANG LAMA (Manual Search)
# Kita cari "const RISK_METRICS_DATA = "
# Jika ketemu, kita comment out baris itu?
# Atau ganti nama variabel lama jadi "RISK_METRICS_DATA_DEPRECATED".
# Ini aman!

html_content = html_content.replace("const RISK_METRICS_DATA =", "const RISK_METRICS_DATA_DEPRECATED =")
print("Renamed old variable to DEPRECATED.")

# Sekarang variable RISK_METRICS_DATA sudah tidak ada (yang ada _DEPRECATED).
# Kita inject variabel baru dengan nama ASLI `RISK_METRICS_DATA`.
# Jadi logic JS tidak perlu diubah! (tetap pakai RISK_METRICS_DATA).

final_data_script = f"\n<script>\nconst RISK_METRICS_DATA = {json.dumps(risk_data)};\nconsole.log('RISK METRICS RELOADED', RISK_METRICS_DATA['A012C']);\n</script>\n"

html_content = html_content.replace('</body>', final_data_script + '</body>')
print("Injected Fresh RISK_METRICS_DATA variable.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Patch Complete.")
