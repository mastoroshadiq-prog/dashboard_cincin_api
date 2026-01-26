"""
Script lengkap untuk:
1. Fix script tag errors 
2. Update HISTORICAL_YIELDS dengan format yang benar
3. Update modal HTML untuk tren produksi
"""

import json
import re

print("=== Loading data ===")
with open('complete_historical_yields.json', 'r') as f:
    complete_data = json.load(f)
print(f"Loaded {len(complete_data)} blocks")

print("\n=== Reading HTML ===")
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()
print(f"Original size: {len(content)} bytes")

# STEP 1: Fix script tags with src that have inline content
print("\n=== Fixing script tags ===")
# Pattern to find <script src="...">...inline content...</script>
pattern = r'<script src="([^"]+)">\s*([^<]+)\s*</script>'
matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} script tags with src and inline content")

for m in reversed(matches):  # Reverse to not mess up positions
    src = m.group(1)
    # Replace with clean script tag
    clean_tag = f'<script src="{src}"></script>'
    content = content[:m.start()] + clean_tag + content[m.end():]
    print(f"Fixed: {src[:50]}...")

# STEP 2: Update HISTORICAL_YIELDS
print("\n=== Updating HISTORICAL_YIELDS ===")
start_marker = "const HISTORICAL_YIELDS = {"
start_pos = content.find(start_marker)

if start_pos == -1:
    print("ERROR: HISTORICAL_YIELDS not found!")
    exit(1)

# Find end by counting braces  
brace_count = 0
end_pos = start_pos
found_first = False
for i in range(start_pos, min(start_pos + 100000, len(content))):
    if content[i] == '{':
        brace_count += 1
        found_first = True
    elif content[i] == '}':
        brace_count -= 1
        if found_first and brace_count == 0:
            end_pos = i + 1
            # Include semicolon
            if end_pos < len(content) and content[end_pos] == ';':
                end_pos += 1
            break

print(f"HISTORICAL_YIELDS: {start_pos} to {end_pos}")

# Build new HISTORICAL_YIELDS with clean format
lines = ["const HISTORICAL_YIELDS = {"]

for block_code, block_data in sorted(complete_data.items()):
    luas = block_data.get('luas_ha', 0)
    division = block_data.get('division', '')
    yields = block_data.get('yields', {})
    
    lines.append(f'    "{block_code}": {{')
    lines.append(f'        luas_ha: {luas},')
    lines.append(f'        division: "{division}",')
    lines.append(f'        yields: {{')
    
    for year in ['2023', '2024', '2025']:
        y = yields.get(year, {})
        real = y.get('real_ton_ha', 0)
        poten = y.get('poten_ton_ha', 0)
        gap = y.get('gap_pct', 0)
        lines.append(f'            {year}: {{ real_ton_ha: {real}, poten_ton_ha: {poten}, gap_pct: {gap} }},')
    
    lines.append('        }')
    lines.append('    },')

lines.append('};')

new_historical = '\n            '.join(lines)
content = content[:start_pos] + new_historical + content[end_pos:]
print(f"HISTORICAL_YIELDS updated with {len(complete_data)} blocks")

# STEP 3: Update Modal HTML - change Block Categorization to Production Trend
print("\n=== Updating modal HTML ===")

old_header = 'BLOCK CATEGORIZATION'
new_header = 'TREN PRODUKSI PER BLOK'

if old_header in content:
    content = content.replace(old_header, new_header)
    print(f"Updated header: {old_header} -> {new_header}")
else:
    print(f"Header '{old_header}' not found (might already be updated)")

# Find and update the modal category cards
# Old: CRITICAL, HIGH, MEDIUM, LOW cards
# New: DECLINING, STABLE, INCREASING, NO DATA cards

old_critical = '''<div class="text-4xl mb-2">🔴</div>
                            <div class="text-red-200 text-xs font-bold uppercase mb-2">CRITICAL</div>
                            <div class="text-5xl font-black text-red-400 mb-2" id="categoryCount_critical">0</div>
                            <div class="text-xs text-red-300/70">Stadium 4 • AR ≥ 30%</div>'''

new_declining = '''<div class="text-4xl mb-2">📉</div>
                            <div class="text-red-200 text-xs font-bold uppercase mb-2">TREN PENURUNAN</div>
                            <div class="text-5xl font-black text-red-400 mb-2" id="categoryCount_declining">0</div>
                            <div class="text-xs text-red-300/70">Produksi turun > 5%</div>'''

if old_critical in content:
    content = content.replace(old_critical, new_declining)
    print("Updated CRITICAL -> TREN PENURUNAN card")

old_high = '''<div class="text-4xl mb-2">🟠</div>
                            <div class="text-orange-200 text-xs font-bold uppercase mb-2">HIGH</div>
                            <div class="text-5xl font-black text-orange-400 mb-2" id="categoryCount_high">0</div>
                            <div class="text-xs text-orange-300/70">Stadium 3 • AR 15-30%</div>'''

new_stable = '''<div class="text-4xl mb-2">➡️</div>
                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">TREN STABIL</div>
                            <div class="text-5xl font-black text-yellow-400 mb-2" id="categoryCount_stable">0</div>
                            <div class="text-xs text-yellow-300/70">Perubahan -5% s/d +5%</div>'''

if old_high in content:
    content = content.replace(old_high, new_stable)
    print("Updated HIGH -> TREN STABIL card")

old_medium = '''<div class="text-4xl mb-2">🟡</div>
                            <div class="text-yellow-200 text-xs font-bold uppercase mb-2">MEDIUM</div>
                            <div class="text-5xl font-black text-yellow-400 mb-2" id="categoryCount_medium">0</div>
                            <div class="text-xs text-yellow-300/70">Stadium 2 • AR 5-15%</div>'''

new_increasing = '''<div class="text-4xl mb-2">📈</div>
                            <div class="text-green-200 text-xs font-bold uppercase mb-2">TREN KENAIKAN</div>
                            <div class="text-5xl font-black text-green-400 mb-2" id="categoryCount_increasing">0</div>
                            <div class="text-xs text-green-300/70">Produksi naik > 5%</div>'''

if old_medium in content:
    content = content.replace(old_medium, new_increasing)
    print("Updated MEDIUM -> TREN KENAIKAN card")

old_low = '''<div class="text-4xl mb-2">🟢</div>
                            <div class="text-green-200 text-xs font-bold uppercase mb-2">LOW</div>
                            <div class="text-5xl font-black text-green-400 mb-2" id="categoryCount_low">0</div>
                            <div class="text-xs text-green-300/70">Stadium 1 • AR < 5%</div>'''

new_nodata = '''<div class="text-4xl mb-2">❓</div>
                            <div class="text-slate-200 text-xs font-bold uppercase mb-2">NO DATA</div>
                            <div class="text-5xl font-black text-slate-400 mb-2" id="categoryCount_nodata">0</div>
                            <div class="text-xs text-slate-300/70">Tidak ada data historis</div>'''

if old_low in content:
    content = content.replace(old_low, new_nodata)
    print("Updated LOW -> NO DATA card")

# Update Multi-Factor Analysis section title
old_analysis_title = 'Multi-Factor Analysis Summary'
new_analysis_title = 'Analisis Blok dengan Tren Penurunan'

if old_analysis_title in content:
    content = content.replace(old_analysis_title, new_analysis_title)
    print(f"Updated: {old_analysis_title} -> {new_analysis_title}")

# Update Distribution Chart title
old_dist = 'Category Distribution'
new_dist = 'Distribusi Tren Produksi (2023-2025)'

if old_dist in content:
    content = content.replace(old_dist, new_dist)
    print(f"Updated: {old_dist} -> {new_dist}")

# Write back
print("\n=== Writing file ===")
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ File saved: {len(content)} bytes")
