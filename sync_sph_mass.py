import pandas as pd
import json

# 1. Load Excel Data
print("Loading Excel Data...")
excel_path = 'poac_sim/data/input/data_gabungan.xlsx'

# Read Header Row 5 to get columns
df = pd.read_excel(excel_path, header=5)
# Ensure columns are stripped of spaces
df.columns = [str(c).strip() for c in df.columns]

# Rename columns for clarity (mapping based on observed structure)
# Col 0: Block Code (Unnamed: 0)
# Col 13: SD 2025 Area (Unnamed: 13 / SD 2025)
# Col 21-29 : Year checks
# However, precise column indices from previous exploration:
# Col 0: Block
# Col 13: Area (SD 2025)
# Cols 16, 17, 18, 19, 20, 21, 22, 23, 24 -> 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016
# Wait, based on previous `print(row.iloc[16:25])` for D001A (Index 81): 
# 16: Unnamed: 16 (0)
# 17: Unnamed: 17 (1.56996) -> This looks like Area addition?
# 18: Unnamed: 18 (0)
# 19: Unnamed: 19 (27.36996) -> Total Area?
# 20: 2008 (0)
# 21: 2009 (641)
# 22: 2010 (1765)
# 23: 2011 (0)
# 24: 2012 (1027) ...
# Let's look at the output of Step 2164 again.
# Unnamed: 16 (0)
# Unnamed: 17 (1.56996)
# Unnamed: 18 (0)
# Unnamed: 19 (27.36996)
# 2008 (0) <- Index 20
# 2009 (641) <- Index 21
# ...
# The user said D001A total is 3484.
# My previous sum `641 + 1765 + 1027 + 51 = 3484`.
# So columns are: 2009 (21), 2010 (22), 2012 (24), 2013 (25??)
# Let's just sum ALL columns from Index 20 (Year 2008) up to Index 31 (Year 2019) to be safe.
# Actually, let's just use the column names (years) to be safer if possible, but indices are more reliable given 'Unnamed' mess.

# Target Columns for Tree Count Summation: Indices 20 to 31 (inclusive)
# 20: 2008
# ...
# 31: 2019

target_tree_indices = list(range(20, 32)) 

# Target Column for Area: Index 13 (SD 2025)

# 2. Load Existing JS Data
js_path = 'data/output/blocks_data_embed.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const BLOCKS_DATA = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]
data = json.loads(json_str)

print(f"Loaded JS Data for {len(data)} blocks.")

updated_count = 0
for block_code, block_data in data.items():
    # Find row in DF
    # Use str() conversion to ensure matching
    row = df[df.iloc[:, 0].astype(str) == block_code]
    
    if not row.empty:
        r = row.iloc[0]
        
        # Calculate Total Trees
        # Force numeric conversion, coerce errors to 0
        trees_series = pd.to_numeric(r.iloc[target_tree_indices], errors='coerce').fillna(0)
        total_trees = trees_series.sum()
        
        # Get Area
        area = pd.to_numeric(r.iloc[13], errors='coerce')
        if pd.isna(area) or area == 0:
            area = block_data.get('luas_ha', 25) # Fallback
            
        # Calculate SPH
        sph = round(total_trees / area, 2) if area > 0 else 0
        
        # Update Data
        # We update 'total_pohon' and 'sph'
        # We also need to preserve the Drone Data we just added
        
        old_sph = block_data.get('sph', 0)
        block_data['sph'] = sph
        block_data['total_pohon'] = int(total_trees)
        block_data['luas_ha'] = float(area) # Ensure area is also synced
        
        # Recalculate 'hijau' (Healthy trees) to match new total
        # Hijau = Total - (Merah + Kuning + Oranye)
        invalid_trees = (block_data.get('merah', 0) + 
                         block_data.get('oranye', 0) + 
                         block_data.get('kuning', 0))
        block_data['hijau'] = int(total_trees) - invalid_trees
        
        print(f"Updated {block_code}: SPH {old_sph} -> {sph}, Trees -> {int(total_trees)}")
        updated_count += 1
    else:
        print(f"Warning: Block {block_code} not found in Excel.")

# 3. Save Back
new_content = f"const BLOCKS_DATA = {json.dumps(data, indent=2)};"
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully synced {updated_count} blocks.")
