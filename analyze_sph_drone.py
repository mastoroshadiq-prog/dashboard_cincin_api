import pandas as pd
import re
import json

# 1. Load Drone Data
print("Loading Drone Data...")
try:
    df_drone = pd.read_csv('data/input/tabelNDREnew.csv')
    # Clean column names (strip spaces if any)
    df_drone.columns = [c.strip() for c in df_drone.columns]
    
    # Group by Block Code ('blok_b' or 'blok'?)
    # Sample row: divisi,blok,blok_b, ...
    # blok_b seems to be "D001A".
    
    # Count Pokok Utama
    drone_utama = df_drone[df_drone['ket'] == 'Pokok Utama'].groupby('blok_b').size()
    
    # Count All (Utama + Tamb)
    drone_all = df_drone.groupby('blok_b').size()
    
    print(f"Loaded {len(drone_all)} blocks from Drone Data.")
except Exception as e:
    print(f"Error loading drone data: {e}")
    exit()

# 2. Load Excel/JS Data (Reference SPH & Area)
# We will parse blocks_data_embed.js as it is cleaner than the raw xlsx
print("Loading Reference Data (JS)...")
blocks_ref = {}
try:
    with open('data/output/blocks_data_embed.js', 'r') as f:
        content = f.read()
        
    # Python regex to find blocks
    # Structure: "BLOCK_CODE": { ... "sph": X, ... "luas_ha": Y ... }
    # This is a bit fragile but should work for the generated file structure.
    
    # Extract entries
    # We will find all blocks first
    # pattern: "([A-Z0-9]+)":\s*\{(.*?)\n\s*\}\,
    
    # Alternative: Use simple searching if regex is too hard on multiline
    # Let's iterate over keys in `drone_all` and look them up in the text
    
    for block in drone_all.index:
        # Find block definition in content
        # Look for "BLOCK": {
        start_idx = content.find(f'"{block}": {{')
        if start_idx == -1:
            continue
            
        # Extract snippet for this block (next 50 lines)
        snippet = content[start_idx:start_idx+1000]
        
        # Regex for SPH
        sph_match = re.search(r'"sph":\s*([\d\.]+)', snippet)
        luas_match = re.search(r'"luas_ha":\s*([\d\.]+)', snippet)
        
        if sph_match and luas_match:
            blocks_ref[block] = {
                'sph_ref': float(sph_match.group(1)),
                'luas_ha': float(luas_match.group(1))
            }

    print(f"Matched {len(blocks_ref)} blocks with Reference Data.")
    
except Exception as e:
    print(f"Error parse JS: {e}")
    exit()

# 3. Compare
results = []
for block, ref in blocks_ref.items():
    area = ref['luas_ha']
    if area <= 0: continue
    
    count_utama = drone_utama.get(block, 0)
    count_all = drone_all.get(block, 0)
    
    sph_drone_utama = round(count_utama / area, 1)
    sph_drone_all = round(count_all / area, 1)
    sph_ref = ref['sph_ref']
    
    diff_utama = sph_drone_utama - sph_ref
    diff_all = sph_drone_all - sph_ref
    
    results.append({
        'Block': block,
        'Area (Ha)': area,
        'Ref SPH': sph_ref,
        'Drone Trees (Utama)': count_utama,
        'Drone SPH (Utama)': sph_drone_utama,
        'Diff Principal': round(diff_utama, 1),
        'Drone Trees (All)': count_all,
        'Drone SPH (All)': sph_drone_all,
        'Diff All': round(diff_all, 1)
    })

# Convert to DataFrame for sorting/display
df_res = pd.DataFrame(results)
# Sort by discrepancy (absolute diff)
df_res['AbsDiff'] = df_res['Diff All'].abs()
df_res = df_res.sort_values('AbsDiff', ascending=False)

print("\n=== TOP 15 SPH DISCREPANCY ANALYSIS (Sorted by Diff) ===")
print(df_res[['Block', 'Area (Ha)', 'Ref SPH', 'Drone SPH (All)', 'Diff All', 'Drone Trees (All)']].head(15).to_string(index=False))

print("\nAverage Diff (All vs Ref):", df_res['Diff All'].mean())
