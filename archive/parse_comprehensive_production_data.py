"""
Parse production data and combine with attack rates
Display comprehensive table: Attack Rate, Potensi, Realisasi, Gap
"""
import pandas as pd
import json

print("🔍 PARSING PRODUCTION DATA FOR ALL 36 AME II BLOCKS")
print("="*70)

# Load attack rate data
with open('data/output/all_blocks_data.json', 'r') as f:
    blocks_data = json.load(f)

print(f"✅ Loaded {len(blocks_data)} blocks with attack rates")

# Manual data from static dashboard (F008A and D001A)
production_data = {}

# From dashboard HTML, these are the known values
known_blocks = {
    'F008A': {'potensi': 19.52, 'realisasi': 21.22},
    'D001A': {'potensi': 22.13, 'realisasi': 17.42}
}

print(f"✅ Have production data for {len(known_blocks)} blocks from dashboard")

# Try to load from Realisasi vs Potensi file
try:
    df_prod = pd.read_excel('data/input/Realisasi vs Potensi PT SR.xlsx')
    print(f"✅ Loaded production file: {df_prod.shape}")
    
    # The file has complex structure, need to find where data starts
    # Look for row with "BLOK" or block codes
    for i in range(30):
        row_values = df_prod.iloc[i].astype(str).tolist()
        # Check if row contains block-like patterns
        if any('008A' in str(v) or '001A' in str(v) for v in row_values):
            print(f"\n✅ Found blocks data around row {i}")
            print(f"Row {i}: {row_values[:10]}")
            break
            
except Exception as e:
    print(f"⚠️  Could not parse Excel: {e}")

# ALTERNATIVE: Use the data from dashboard HTML as ground truth
# Then estimate for other blocks based on attack rate correlation

print("\n" + "="*70)
print("📊 CREATING COMPREHENSIVE TABLE")
print("="*70)

# Build comprehensive table
results = []

for block_code, block_data in sorted(blocks_data.items(), key=lambda x: x[1]['rank']):
    row = {
        'Rank': block_data['rank'],
        'Block': block_code,
        'Attack_Rate': block_data['attack_rate'],
        'Total_Pohon': block_data['total_pohon'],
        'Merah': block_data['merah'],
        'Oranye': block_data['oranye'],
        'SPH': block_data['sph'],
        'TT': block_data['tt'],
        'Age': block_data['age']
    }
    
    # Add production data if known
    if block_code in known_blocks:
        row['Potensi_Ton_Ha'] = known_blocks[block_code]['potensi']
        row['Realisasi_Ton_Ha'] = known_blocks[block_code]['realisasi']
        row['Gap_Ton_Ha'] = round(known_blocks[block_code]['realisasi'] - known_blocks[block_code]['potensi'], 2)
        row['Gap_Pct'] = round((row['Gap_Ton_Ha'] / known_blocks[block_code]['potensi']) * 100, 1)
    else:
        # Estimate based on correlation if not known
        # For now, mark as N/A
        row['Potensi_Ton_Ha'] = 'N/A'
        row['Realisasi_Ton_Ha'] = 'N/A'
        row['Gap_Ton_Ha'] = 'N/A'
        row['Gap_Pct'] = 'N/A'
    
    results.append(row)

# Create DataFrame
df_results = pd.DataFrame(results)

print("\n" + "="*70)
print("📋 COMPREHENSIVE BLOCK DATA TABLE")
print("="*70)
print()
print(df_results.to_string(index=False))

# Save to CSV
output_file = 'data/output/blocks_comprehensive_with_production.csv'
df_results.to_csv(output_file, index=False)
print(f"\n✅ Saved to: {output_file}")

# Show summary statistics
print("\n" + "="*70)
print("📊 SUMMARY STATISTICS")
print("="*70)

print(f"\nTotal blocks: {len(df_results)}")
print(f"Blocks with production data: {df_results['Potensi_Ton_Ha'].apply(lambda x: x != 'N/A').sum()}")
print(f"Blocks without production data: {df_results['Potensi_Ton_Ha'].apply(lambda x: x == 'N/A').sum()}")

# For blocks with data, show correlation
known_df = df_results[df_results['Gap_Pct'] != 'N/A']
if len(known_df) > 0:
    print(f"\n📈 BLOCKS WITH PRODUCTION DATA:")
    for _, row in known_df.iterrows():
        print(f"\n{row['Block']} (Rank #{row['Rank']}):")
        print(f"  Attack Rate: {row['Attack_Rate']}%")
        print(f"  Potensi: {row['Potensi_Ton_Ha']} ton/ha")
        print(f"  Realisasi: {row['Realisasi_Ton_Ha']} ton/ha")
        print(f"  Gap: {row['Gap_Pct']:+}% ({row['Gap_Ton_Ha']:+} ton/ha)")
        
        # Calculate what loss would be
        if row['Gap_Ton_Ha'] < 0:
            ha = (row['Total_Pohon'] * 64) / 10000
            loss = abs(row['Gap_Ton_Ha']) * ha * 1500  # ton * Rp 1500/kg
            print(f"  → Actual Loss: Rp {loss/1e6:.1f} MILAR/tahun")

print("\n" + "="*70)
print("⚠️  NOTE: Only 2 blocks have production data from dashboard")
print("Need to parse Realisasi vs Potensi Excel for remaining 34 blocks")
print("="*70)
