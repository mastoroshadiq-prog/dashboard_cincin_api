"""
Merge production data into all_blocks_data.json
So dashboard can access REAL yield data
"""
import json

print("🔄 MERGING PRODUCTION DATA INTO all_blocks_data.json")
print("="*70)

# Load both datasets
with open('data/output/all_blocks_data.json') as f:
    blocks_data = json.load(f)

with open('data/output/all_36_blocks_production_data.json') as f:
    production_data = json.load(f)

print(f"✅ Loaded {len(blocks_data)} blocks")
print(f"✅ Loaded {len(production_data)} production records\n")

# Merge
for block_code, prod_info in production_data.items():
    if block_code in blocks_data:
        # Add production fields
        blocks_data[block_code].update({
            'luas_ha': prod_info['luas_ha'],
            'realisasi_ton_ha': prod_info['realisasi_ton_ha'],
            'potensi_ton_ha': prod_info['potensi_ton_ha'],
            'gap_ton_ha': prod_info['gap_ton_ha'],
            'gap_pct': prod_info['gap_pct'],
            'realisasi_total_ton': prod_info['realisasi_ton_total'],
            'potensi_total_ton': prod_info['potensi_ton_total']
        })
        print(f"✅ {block_code}: Added production data")

# Save enhanced version
with open('data/output/all_blocks_data.json', 'w') as f:
    json.dump(blocks_data, f, indent=2)

print(f"\n✅ Updated all_blocks_data.json with production data")
print(f"\nEach block now has:")
print("  • Attack rate, severity, tree counts (original)")
print("  • Luas Ha, Realisasi, Potensi, Gap (NEW!)")
print("\n✅ Ready for dashboard update with REAL data!")
