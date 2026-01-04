"""
Create comprehensive table combining attack rates and production data
"""
import json
import pandas as pd

print("📊 CREATING COMPREHENSIVE TABLE")
print("="*70)

# Load attack rate data
with open('data/output/all_blocks_data.json') as f:
    attack_data = json.load(f)

# Load production data
with open('data/output/all_36_blocks_production_data.json') as f:
    production_data = json.load(f)

print(f"✅ Loaded {len(attack_data)} blocks with attack data")
print(f"✅ Loaded {len(production_data)} blocks with production data\n")

# Combine data
comprehensive = []

for block_code in sorted(attack_data.keys(), key=lambda x: attack_data[x]['rank']):
    attack = attack_data[block_code]
    prod = production_data.get(block_code, {})
    
    row = {
        'Rank': attack['rank'],
        'Block': block_code,
        'Attack_Rate_%': attack['attack_rate'],
        'Severity': attack['severity'],
        'Merah': attack['merah'],
        'Oranye': attack['oranye'],
        'Kuning': attack['kuning'],
        'Total_Infected': attack['merah'] + attack['oranye'],
        'Total_Pohon': attack['total_pohon'],
        'SPH': attack['sph'],
        'TT': attack['tt'],
        'Age': attack['age'],
        'Luas_Ha': prod.get('luas_ha', 0),
        'Realisasi_Ton_Ha': prod.get('realisasi_ton_ha', 0),
        'Potensi_Ton_Ha': prod.get('potensi_ton_ha', 0),
        'Gap_Ton_Ha': prod.get('gap_ton_ha', 0),
        'Gap_%': prod.get('gap_pct', 0),
        'Realisasi_Total_Ton': prod.get('realisasi_ton_total', 0),
        'Potensi_Total_Ton': prod.get('potensi_ton_total', 0)
    }
    
    comprehensive.append(row)

# Create DataFrame
df = pd.DataFrame(comprehensive)

# Save to CSV
output_csv = 'data/output/comprehensive_attack_production_36_blocks.csv'
df.to_csv(output_csv, index=False)
print(f"✅ Saved to: {output_csv}\n")

# Display table
print("="*70)
print("📋 COMPREHENSIVE TABLE - ALL 36 AME II BLOCKS")
print("="*70)
print()
print(df.to_string(index=False))

# Summary statistics
print("\n" + "="*70)
print("📈 KEY INSIGHTS")
print("="*70)

# Correlation between attack rate and gap
print("\n1. ATTACK RATE vs YIELD GAP CORRELATION:")
print("-" * 70)

high_attack = df[df['Attack_Rate_%'] >= 10]
medium_attack = df[(df['Attack_Rate_%'] >= 5) & (df['Attack_Rate_%'] < 10)]
low_attack = df[df['Attack_Rate_%'] < 5]

print(f"\nHigh Attack (≥10%): {len(high_attack)} blocks")
print(f"  Average Gap: {high_attack['Gap_%'].mean():.1f}%")
print(f"  Negative gaps: {len(high_attack[high_attack['Gap_%'] < 0])}")
print(f"  Positive gaps: {len(high_attack[high_attack['Gap_%'] > 0])}")

print(f"\nMedium Attack (5-10%): {len(medium_attack)} blocks")
print(f"  Average Gap: {medium_attack['Gap_%'].mean():.1f}%")

print(f"\nLow Attack (<5%): {len(low_attack)} blocks")
print(f"  Average Gap: {low_attack['Gap_%'].mean():.1f}%")

print("\n2. SYMPTOM LAG EVIDENCE:")
print("-" * 70)
symptom_lag = df[(df['Attack_Rate_%'] >= 10) & (df['Gap_%'] > 0)]
print(f"Blocks with high attack (≥10%) BUT positive gap: {len(symptom_lag)}")
print("These blocks likely experiencing SYMPTOM LAG:")
for _, row in symptom_lag.iterrows():
    print(f"  • {row['Block']}: {row['Attack_Rate_%']}% attack, {row['Gap_%']:+.1f}% gap")

print("\n3. ACTUAL IMPACT EVIDENCE:")
print("-" * 70)
actual_impact = df[(df['Attack_Rate_%'] >= 10) & (df['Gap_%'] < -10)]
print(f"Blocks with high attack AND significant deficit: {len(actual_impact)}")
print("These blocks showing REAL Ganoderma impact:")
for _, row in actual_impact.iterrows():
    print(f"  • {row['Block']}: {row['Attack_Rate_%']}% attack, {row['Gap_%']:.1f}% gap")

print("\n" + "="*70)
print("✅ COMPREHENSIVE DATA READY FOR DASHBOARD UPDATE!")
print("="*70)
