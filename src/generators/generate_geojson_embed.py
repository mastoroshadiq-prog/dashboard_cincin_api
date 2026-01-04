import json
import os
from pathlib import Path

print("="*80)
print("🚀 CONSOLIDATING GEOJSON MAPS INTO JS EMBED (OFFLINE SUPPORT)")
print("="*80)

input_dir = Path('data/output/geojson')
output_file = Path('data/output/geojson_data_embed.js')

if not input_dir.exists():
    print(f"❌ Input directory not found: {input_dir}")
    exit(1)

# Initialize container
all_geojson = {}
total_files = 0
total_size = 0

# Scan and merge
for file_path in input_dir.glob('*.json'):
    block_code = file_path.stem  # e.g. "F008A"
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        all_geojson[block_code] = data
        
        # Calculate size
        total_size += file_path.stat().st_size
        total_files += 1
        
    if total_files % 5 == 0:
        print(f"  Processed {total_files} maps...")

print(f"\n✅ Merged {total_files} GeoJSON maps")
print(f"📦 Total Data Size: {total_size / 1024 / 1024:.2f} MB")

# Minimize JSON to save space (removes whitespace)
print("⚙️  Minimizing and writing to JS file...")
json_str = json.dumps(all_geojson, separators=(',', ':'))

# Wrap in JS variable
js_content = f"const GEOJSON_DATA = {json_str};\nconsole.log('✅ GEOJSON_DATA Loaded:', Object.keys(GEOJSON_DATA).length, 'maps');"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ Saved to: {output_file}")
print("🎯 You can now load this script in HTML to bypass CORS issues!")
