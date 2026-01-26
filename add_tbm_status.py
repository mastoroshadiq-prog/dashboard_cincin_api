"""
Add TBM status information to dashboard:
1. Update HISTORICAL_YIELDS with TBM status
2. Add TBM indicator to Block Detail Panel
"""
import json

# Load TBM analysis
with open('tbm_blocks_analysis.json', 'r') as f:
    tbm_data = json.load(f)

tbm_blocks = {item['block']: item for item in tbm_data}
print(f"Loaded {len(tbm_blocks)} TBM block analyses")

# Load and update HISTORICAL_YIELDS
with open('complete_historical_yields.json', 'r') as f:
    hist_yields = json.load(f)

# Add TBM status to each block
for block_code in hist_yields:
    if block_code in tbm_blocks:
        tbm_info = tbm_blocks[block_code]
        hist_yields[block_code]['is_tbm'] = True
        hist_yields[block_code]['tbm_status'] = tbm_info['status']
        hist_yields[block_code]['tbm_reason'] = tbm_info['reason']
        hist_yields[block_code]['tbm_tanam_year'] = tbm_info.get('latest_tanam_year', 0)
        hist_yields[block_code]['tbm_tanam_count'] = tbm_info.get('total_tanam', 0)
    else:
        hist_yields[block_code]['is_tbm'] = False
        hist_yields[block_code]['tbm_status'] = 'TM'  # Tanaman Menghasilkan
        hist_yields[block_code]['tbm_reason'] = ''

# Save updated historical yields
with open('complete_historical_yields.json', 'w') as f:
    json.dump(hist_yields, f, indent=2)
print("Updated complete_historical_yields.json with TBM status")

# Now update the HTML
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HISTORICAL_YIELDS in HTML
start_marker = "const HISTORICAL_YIELDS = {"
start_pos = content.find(start_marker)

if start_pos > 0:
    # Find end
    brace_count = 0
    end_pos = start_pos
    found_first = False
    for i in range(start_pos, min(start_pos + 500000, len(content))):
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
    
    # Build new HISTORICAL_YIELDS
    lines = ["const HISTORICAL_YIELDS = {"]
    for block_code in sorted(hist_yields.keys()):
        block = hist_yields[block_code]
        luas = block.get('luas_ha', 0)
        division = block.get('division', '')
        yields = block.get('yields', {})
        is_tbm = block.get('is_tbm', False)
        tbm_status = block.get('tbm_status', 'TM')
        tbm_reason = block.get('tbm_reason', '').replace('"', '\\"')
        
        lines.append(f'            "{block_code}": {{')
        lines.append(f'                luas_ha: {luas},')
        lines.append(f'                division: "{division}",')
        lines.append(f'                is_tbm: {"true" if is_tbm else "false"},')
        lines.append(f'                tbm_status: "{tbm_status}",')
        lines.append(f'                tbm_reason: "{tbm_reason}",')
        lines.append(f'                yields: {{')
        
        for year in ['2023', '2024', '2025']:
            y = yields.get(year, {})
            real = y.get('real_ton_ha', 0)
            poten = y.get('poten_ton_ha', 0)
            gap = y.get('gap_pct', 0)
            lines.append(f'                    {year}: {{ real_ton_ha: {real}, poten_ton_ha: {poten}, gap_pct: {gap} }},')
        
        lines.append('                }')
        lines.append('            },')
    
    lines.append('        };')
    
    new_hist = '\n'.join(lines)
    content = content[:start_pos] + new_hist + content[end_pos:]
    print("Updated HISTORICAL_YIELDS with TBM status in HTML")

# 2. Add TBM status display to Block Detail Panel HTML
# Find the block detail header and add TBM badge
old_header = '''<h3 class="text-2xl font-black text-white flex items-center gap-2">
                        📊 Detail Blok <span id="detailBlockCode" class="text-cyan-400">-</span>
                    </h3>'''

new_header = '''<h3 class="text-2xl font-black text-white flex items-center gap-2">
                        📊 Detail Blok <span id="detailBlockCode" class="text-cyan-400">-</span>
                        <span id="detailTbmBadge" class="hidden px-3 py-1 text-sm font-bold rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/50">TBM</span>
                    </h3>
                    <p id="detailTbmReason" class="text-amber-300 text-sm hidden"></p>'''

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Added TBM badge to Block Detail Panel header")
else:
    print("Could not find header to update")

# 3. Update showBlockDetail function to display TBM status
# Find where we set detailBlockCode and add TBM display logic
old_show_block = "document.getElementById('detailBlockCode').textContent = blockCode;"

new_show_block = """document.getElementById('detailBlockCode').textContent = blockCode;
                
                // Show TBM status if applicable
                const tbmBadge = document.getElementById('detailTbmBadge');
                const tbmReason = document.getElementById('detailTbmReason');
                if (historical && historical.is_tbm) {
                    tbmBadge.classList.remove('hidden');
                    tbmBadge.textContent = historical.tbm_status || 'TBM';
                    if (tbmReason && historical.tbm_reason) {
                        tbmReason.classList.remove('hidden');
                        tbmReason.textContent = '⚠️ ' + historical.tbm_reason;
                    }
                } else {
                    tbmBadge.classList.add('hidden');
                    if (tbmReason) tbmReason.classList.add('hidden');
                }"""

if old_show_block in content:
    content = content.replace(old_show_block, new_show_block)
    print("Updated showBlockDetail to display TBM status")
else:
    print("Could not find showBlockDetail code to update")

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ HTML updated: {len(content)} bytes")
print("\nTBM blocks will now show amber badge and reason in Block Detail Panel")
