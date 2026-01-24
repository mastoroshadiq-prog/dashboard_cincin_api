
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\tbm_stats_real.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    tbm_data = json.load(f)

# Buat blok script baru
new_script = f"\n<script>\nconst TBM_REAL_STATS = {json.dumps(tbm_data)};\nconsole.log('TBM STATS RELOADED', Object.keys(TBM_REAL_STATS).length);\n</script>\n"

# Cari dan hapus deklarasi lama jika ada (regex atau string)
# Karena TBM_STATS sebelumnya mungkin diinject, kita replace variable name lama menjadi deprecated.
html_content = html_content.replace('const TBM_REAL_STATS =', 'const TBM_REAL_STATS_DEPRECATED =')

# Inject variable baru di akhir body
html_content = html_content.replace('</body>', new_script + '</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Patched TBM_REAL_STATS in HTML.")
