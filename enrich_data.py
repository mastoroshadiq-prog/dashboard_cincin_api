import pandas as pd
import json
import re

# 1. Load CSV Data
print("Loading Drone Data...")
try:
    df = pd.read_csv('data/input/tabelNDREnew.csv')
    df.columns = [c.strip() for c in df.columns]
    
    # Calculate Counts
    # Group by 'blok_b' (Block Code)
    grp = df.groupby('blok_b')
    
    # Count All
    count_all = grp.size()
    
    # Count Main (ket == 'Pokok Utama')
    count_main = df[df['ket'] == 'Pokok Utama'].groupby('blok_b').size()
    
    print(f"Processed {len(count_all)} blocks.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# 2. Load Existing JS Data
js_path = 'data/output/blocks_data_embed.js'
try:
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON part
    # Removing "const BLOCKS_DATA = " and trailing ";"
    json_str = content.replace('const BLOCKS_DATA = ', '').strip()
    if json_str.endswith(';'):
        json_str = json_str[:-1]
    
    data = json.loads(json_str)
    print(f"Loaded JS Data for {len(data)} blocks.")
    
except Exception as e:
    print(f"Error parsing JS: {e}")
    exit()

# 3. Enrich Data
updated_count = 0
for block_code, block_data in data.items():
    area = block_data.get('luas_ha', 0)
    
    # Get Drone Counts (Default to 0 if not found)
    c_all = int(count_all.get(block_code, 0))
    c_main = int(count_main.get(block_code, 0))
    
    # Calculate SPH
    sph_drone_all = round(c_all / area, 1) if area > 0 else 0
    sph_drone_main = round(c_main / area, 1) if area > 0 else 0
    
    # Inject into data
    block_data['drone_tree_all'] = c_all
    block_data['drone_tree_main'] = c_main
    block_data['drone_sph_all'] = sph_drone_all
    block_data['drone_sph_main'] = sph_drone_main
    
    updated_count += 1

print(f"Enriched {updated_count} blocks.")

# 4. Save Back
new_content = f"const BLOCKS_DATA = {json.dumps(data, indent=2)};"
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated blocks_data_embed.js")
