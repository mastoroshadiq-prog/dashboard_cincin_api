import json
import pandas as pd

# Load existing all_blocks_data.json
all_blocks_file = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\all_blocks_data.json'
with open(all_blocks_file, 'r') as f:
    all_blocks = json.load(f)

print(f"Existing blocks in all_blocks_data.json: {len(all_blocks)}")

# Load TBM blocks data
with open('tbm_blocks_data.json', 'r') as f:
    tbm_data = json.load(f)

print(f"TBM blocks found in Excel: {tbm_data['total_tbm_blocks']}")

# Create TBM block entries with required fields
tbm_blocks_to_add = {}

for tbm in tbm_data['all_blocks']:
    block_code = tbm['block_code']
    
    # Create a minimal block entry for TBM
    #Since these are TBM blocks (not producing yet), we set production values to 0
    tbm_blocks_to_add[block_code] = {
        "block_code": block_code,
        "tahun_tanam": tbm['tahun_tanam'],
        "estate": tbm['estate'],
        "division": tbm['division'],
        
        # TBM blocks don't have production data yet
        "total_pohon": 0,
        "merah": 0,
        "oranye": 0,
        "kuning": 0,
        "hijau": 0,
        "attack_rate": 0,
        "sph": 0,
        "tt": tbm['tahun_tanam'],
        "age": 2026 - tbm['tahun_tanam'],  # Calculate age
        "sisip": None,
        "has_map": False,
        "map_filename": None,
        "luas_ha": 0,  # We could extract this from Excel if needed
        "realisasi_ton_ha": 0,  # TBM = no production
        "potensi_ton_ha": 0,    # Could be estimated based on age
        "gap_ton_ha": 0,
        "gap_pct": 0,
        "realisasi_total_ton": 0,
        "potensi_total_ton": 0,
        
        # Yield history - all zeros for TBM
        "yield_history": {
            "2021": 0,
            "2022": 0,
            "2023": 0,
            "2024": 0,
            "2025": 0
        },
        
        # TBM status
        "consecutive_drop": False,
        "drop_type": None,
        "status_narrative": "TBM",
        "status_desc": f"TANAMAN BELUM MENGHASILKAN (TBM): Ditanam tahun {tbm['tahun_tanam']}, umur {2026 - tbm['tahun_tanam']} tahun",
        "severity": "TBM",
        "vanishing_phase": None,
        "rank": 999,  # Low priority for mature block analysis
        "is_tbm": True  # NEW FLAG to identify TBM blocks
    }

print(f"\nCreating {len(tbm_blocks_to_add)} TBM block entries...")

# Merge TBM blocks into all_blocks
updated_all_blocks = {**all_blocks, **tbm_blocks_to_add}

print(f"Total blocks after adding TBM: {len(updated_all_blocks)}")

# Save updated data
output_file = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\all_blocks_data_with_tbm.json'
with open(output_file, 'w') as f:
    json.dump(updated_all_blocks, f, indent=2)

print(f"\n✅ Updated data saved to: all_blocks_data_with_tbm.json")

# Also save just TBM blocks as separate file for reference
tbm_only_file = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\tbm_blocks_only.json'
with open(tbm_only_file, 'w') as f:
    json.dump(tbm_blocks_to_add, f, indent=2)

print(f"✅ TBM-only data saved to: tbm_blocks_only.json")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Original blocks: {len(all_blocks)}")
print(f"TBM blocks added: {len(tbm_blocks_to_add)}")
print(f"Total blocks: {len(updated_all_blocks)}")
print("\nTBM Blocks by Division:")
for div, blocks in tbm_data['by_division'].items():
    print(f"  {div}: {len(blocks)} blocks")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("1. Replace all_blocks_data.json with all_blocks_data_with_tbm.json")
print("2. OR update dashboard to load from all_blocks_data_with_tbm.json")
print("3. TBM blocks will now appear in the dashboard with tahun_tanam field")
print("="*80)
