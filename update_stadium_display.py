"""
Update dashboard with ground truth stadium data:
1. Update BLOCKS_DATA with ground truth attack rate and stadium counts
2. Modify block detail panel to show actual infected tree counts
"""
import json

# Load updated risk data
with open('complete_risk_data.json', 'r') as f:
    risk_data = json.load(f)

print("="*60)
print("UPDATING DASHBOARD WITH GROUND TRUTH DATA")
print("="*60)

# Read HTML
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update BLOCKS_DATA
start_marker = "const BLOCKS_DATA = {"
start_pos = content.find(start_marker)

if start_pos > 0:
    # Find end
    brace_count = 0
    end_pos = start_pos
    found_first = False
    for i in range(start_pos, min(start_pos + 200000, len(content))):
        if content[i] == '{':
            brace_count += 1
            found_first = True
        elif content[i] == '}':
            brace_count -= 1
            if found_first and brace_count == 0:
                end_pos = i + 1
                if end_pos < len(content) and content[end_pos] == ';':
                    end_pos += 1
                break
    
    # Build new BLOCKS_DATA with ground truth
    lines = ["const BLOCKS_DATA = {"]
    for block_code, data in sorted(risk_data.items()):
        line = f'                "{block_code}": {{ '
        line += f'"block_code": "{block_code}", '
        line += f'"attack_rate": {data.get("attack_rate", 0)}, '
        line += f'"sph": {data.get("sph", 0)}, '
        line += f'"stadium_12": {data.get("stadium_12_count", 0)}, '
        line += f'"stadium_34": {data.get("stadium_34_count", 0)}, '
        line += f'"total_infected": {data.get("total_infected", 0)}, '
        line += f'"loss_value_juta": {data.get("loss_value_juta", 0)}, '
        line += f'"gap_pct": {data.get("gap_pct", 0)}, '
        line += f'"luas_ha": {data.get("luas_ha", 0)} '
        line += "},"
        lines.append(line)
    lines.append("            };")
    
    new_blocks_data = '\n'.join(lines)
    content = content[:start_pos] + new_blocks_data + content[end_pos:]
    print("✅ Updated BLOCKS_DATA with ground truth")

# 2. Update block detail panel HTML - change "Stadium" to "Pohon Terinfeksi"
old_stadium_html = '''<div class="bg-black/30 rounded-lg p-3 border border-orange-700/30">
                            <div class="text-xs text-slate-400">Stadium</div>
                            <div class="text-xl font-bold text-orange-400" id="detailStadium">-</div>
                        </div>'''

new_stadium_html = '''<div class="bg-black/30 rounded-lg p-3 border border-orange-700/30">
                            <div class="text-xs text-slate-400">Pohon Terinfeksi</div>
                            <div class="text-lg font-bold text-orange-400" id="detailInfected">-</div>
                            <div class="text-xs text-slate-500" id="detailInfectedBreakdown"></div>
                        </div>'''

if old_stadium_html in content:
    content = content.replace(old_stadium_html, new_stadium_html)
    print("✅ Updated Stadium HTML to show infected tree counts")
else:
    print("⚠️ Could not find Stadium HTML to update")

# 3. Update showBlockDetail JS to populate infected count instead of stadium text
# Find and update the stadium display code
old_stadium_js = "document.getElementById('detailStadium').textContent = stadium;"

new_stadium_js = """// Show infected tree count
                const infectedEl = document.getElementById('detailInfected');
                const breakdownEl = document.getElementById('detailInfectedBreakdown');
                if (riskData && riskData.total_infected > 0) {
                    infectedEl.textContent = riskData.total_infected + ' pohon';
                    if (breakdownEl) {
                        breakdownEl.textContent = 'S1-2: ' + (riskData.stadium_12 || 0) + ' | S3-4: ' + (riskData.stadium_34 || 0);
                    }
                } else {
                    infectedEl.textContent = 'N/A';
                    if (breakdownEl) breakdownEl.textContent = '';
                }"""

if old_stadium_js in content:
    content = content.replace(old_stadium_js, new_stadium_js)
    print("✅ Updated Stadium JS to show infected counts")
else:
    print("⚠️ Could not find Stadium JS to update")

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ File updated: {len(content)} bytes")
print("\nChanges:")
print("  1. Attack rate now uses ground truth from spreadsheet (393 blocks)")
print("  2. 'Stadium' field now shows actual infected tree count")
print("  3. Breakdown shows Stadium 1-2 vs Stadium 3-4 counts")
