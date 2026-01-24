
import re
import json

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\block_breakdown_v2.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE OLD JSON INJECTION
# Cari pattern <script>...const BLOCK_BREAKDOWN_DATA_V2 = ...</script>
# Kita hapus semua instance nya.

pattern = r'<script>\s*const BLOCK_BREAKDOWN_DATA_V2 = .*?;\s*console\.log\("BLOCK BREAKDOWN V2 LOADED".*?\);\s*</script>'
html = re.sub(pattern, '', html, flags=re.DOTALL)

# 2. INJECT NEW JSON
with open(json_path, 'r') as f:
    breakdown_data = json.load(f)

json_script = f"""
<script>
    const BLOCK_BREAKDOWN_DATA_V2 = {json.dumps(breakdown_data)};
    console.log("BLOCK BREAKDOWN V2 LOADED", BLOCK_BREAKDOWN_DATA_V2.summary.empty.count + " empty blocks");
</script>
"""
html = html.replace('</body>', json_script + '</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Cleaned old JSON and injected new data.")
