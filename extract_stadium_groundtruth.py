"""
Extract actual stadium and attack rate data from data_gabungan.xlsx:
- Col 55: Stadium 1&2 count
- Col 56: Stadium 3&4 count
- Col 57: Total infected
- Col 58: %SERANGAN (Attack Rate)
"""
import pandas as pd
import json

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*70)
print("EXTRACTING STADIUM & ATTACK RATE FROM DATA_GABUNGAN.XLSX")
print("="*70)

# Column mappings
BLOCK_COL = 0  # Block code
STADIUM_12_COL = 55  # Stadium 1&2
STADIUM_34_COL = 56  # Stadium 3&4
TOTAL_INFECTED_COL = 57  # Total infected
ATTACK_RATE_COL = 58  # %SERANGAN

# Verify headers
print("\nVerifying column headers at row 4:")
print(f"  Col 55: {df.iloc[4, 55]}")
print(f"  Col 56: {df.iloc[4, 56]}")
print(f"  Col 57: {df.iloc[4, 57]}")
print(f"  Col 58: {df.iloc[4, 58]}")

# Extract data starting from row 10 (data rows)
stadium_data = {}
for row in range(10, len(df)):
    block_code = df.iloc[row, BLOCK_COL]
    if pd.isna(block_code):
        continue
    block_code = str(block_code).strip()
    if len(block_code) < 3:
        continue
    
    # Get stadium counts
    s12 = df.iloc[row, STADIUM_12_COL]
    s34 = df.iloc[row, STADIUM_34_COL]
    total_infected = df.iloc[row, TOTAL_INFECTED_COL]
    attack_rate = df.iloc[row, ATTACK_RATE_COL]
    
    # Convert to numbers
    s12 = int(s12) if pd.notna(s12) and str(s12).replace('.','').replace('-','').isdigit() else 0
    s34 = int(s34) if pd.notna(s34) and str(s34).replace('.','').replace('-','').isdigit() else 0
    total_infected = int(total_infected) if pd.notna(total_infected) and str(total_infected).replace('.','').replace('-','').isdigit() else 0
    
    # Attack rate - handle percentage
    if pd.notna(attack_rate):
        try:
            ar = float(attack_rate)
            # If it's already a percentage (0-100), use as is
            # If it's a decimal (0-1), multiply by 100
            if ar > 0 and ar < 1:
                ar = ar * 100
            attack_rate = round(ar, 2)
        except:
            attack_rate = 0
    else:
        attack_rate = 0
    
    stadium_data[block_code] = {
        'stadium_12': s12,
        'stadium_34': s34,
        'total_infected': total_infected,
        'attack_rate_ground_truth': attack_rate
    }

print(f"\nExtracted stadium data for {len(stadium_data)} blocks")

# Show samples
print("\nSamples:")
sample_blocks = ['D001A', 'E007A', 'F004A', 'A001A', 'D005A']
for block in sample_blocks:
    if block in stadium_data:
        d = stadium_data[block]
        print(f"  {block}: S12={d['stadium_12']}, S34={d['stadium_34']}, Total={d['total_infected']}, AR={d['attack_rate_ground_truth']}%")
    else:
        print(f"  {block}: NOT FOUND")

# Check how many have non-zero data
non_zero = sum(1 for d in stadium_data.values() if d['total_infected'] > 0 or d['attack_rate_ground_truth'] > 0)
print(f"\nBlocks with stadium/attack data: {non_zero}")

# Save to JSON
with open('stadium_groundtruth.json', 'w') as f:
    json.dump(stadium_data, f, indent=2)
print("\nSaved to stadium_groundtruth.json")

# Now let's update complete_risk_data.json with this ground truth
print("\n" + "="*70)
print("UPDATING RISK DATA WITH GROUND TRUTH")
print("="*70)

with open('complete_risk_data.json', 'r') as f:
    risk_data = json.load(f)

updated = 0
for block_code, risk in risk_data.items():
    if block_code in stadium_data:
        gt = stadium_data[block_code]
        # Update with ground truth if available
        if gt['attack_rate_ground_truth'] > 0:
            risk['attack_rate'] = gt['attack_rate_ground_truth']
            risk['attack_rate_source'] = 'ground_truth'
            updated += 1
        
        # Always add stadium counts
        risk['stadium_12_count'] = gt['stadium_12']
        risk['stadium_34_count'] = gt['stadium_34']
        risk['total_infected'] = gt['total_infected']

print(f"Updated attack rate for {updated} blocks with ground truth")

# Save updated risk data
with open('complete_risk_data.json', 'w') as f:
    json.dump(risk_data, f, indent=2)
print("Saved updated complete_risk_data.json")

# Show summary of attack rate sources
from_gt = sum(1 for r in risk_data.values() if r.get('attack_rate_source') == 'ground_truth')
from_ndre = sum(1 for r in risk_data.values() if r.get('attack_rate_source') != 'ground_truth' and r.get('attack_rate', 0) > 0)
no_ar = sum(1 for r in risk_data.values() if r.get('attack_rate', 0) == 0)

print(f"\nAttack Rate Source Summary:")
print(f"  Ground Truth (spreadsheet): {from_gt} blocks")
print(f"  NDRE Estimation: {from_ndre} blocks")
print(f"  No Data: {no_ar} blocks")
