"""
Integrate complete_risk_data.json into the dashboard HTML
Replace/update BLOCKS_DATA with complete risk data
"""

import json

print("="*60)
print("INTEGRATING COMPLETE RISK DATA INTO DASHBOARD")
print("="*60)

# Load complete risk data
with open('complete_risk_data.json', 'r') as f:
    risk_data = json.load(f)
print(f"Loaded {len(risk_data)} blocks from complete_risk_data.json")

# Read HTML
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()
print(f"Read HTML: {len(content)} bytes")

# Find BLOCKS_DATA and replace it
start_marker = "const BLOCKS_DATA = {"
start_pos = content.find(start_marker)

if start_pos == -1:
    print("ERROR: BLOCKS_DATA not found!")
else:
    # Find end by counting braces
    brace_count = 0
    end_pos = start_pos
    found_first = False
    for i in range(start_pos, min(start_pos + 50000, len(content))):
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
    
    # Build new BLOCKS_DATA
    lines = ["const BLOCKS_DATA = {"]
    for block_code, data in sorted(risk_data.items()):
        # Format each block as single line
        line = f'                "{block_code}": {{ '
        line += f'"block_code": "{block_code}", '
        line += f'"attack_rate": {data["attack_rate"]}, '
        line += f'"sph": {data["sph"]}, '
        line += f'"stadium": {data["stadium"]}, '
        line += f'"loss_value_juta": {data["loss_value_juta"]}, '
        line += f'"gap_pct": {data["gap_pct"]}, '
        line += f'"luas_ha": {data["luas_ha"]}, '
        line += f'"stress_class": "{data.get("stress_class", "")}" '
        line += "},"
        lines.append(line)
    lines.append("            };")
    
    new_blocks_data = '\n'.join(lines)
    content = content[:start_pos] + new_blocks_data + content[end_pos:]
    print(f"Updated BLOCKS_DATA with {len(risk_data)} blocks")

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Saved HTML: {len(content)} bytes")
print("\n" + "="*60)
print("COMPLETE!")
print("="*60)
