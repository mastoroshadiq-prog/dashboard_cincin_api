"""
Analyze correlation between Attack Rate and Yield Gap
Does Ganoderma CAUSE the production loss?
"""
import pandas as pd
import json

print("🔍 ANALYZING: Attack Rate vs Yield Gap Correlation")
print("="*70)

# Load blocks data with attack rates
with open('data/output/all_blocks_data.json', 'r') as f:
    blocks_data = json.load(f)

print(f"✅ Loaded {len(blocks_data)} blocks data")

# Try to load production data
try:
    # Realisasi vs Potensi has complex format
    df = pd.read_excel('data/input/Realisasi vs Potensi PT SR.xlsx')
    print(f"✅ Loaded production data: {df.shape}")
    
    # Try to find where actual data starts (skip header rows)
    # Look for numeric data
    for i in range(20):
        if pd.notna(df.iloc[i, 0]) and isinstance(df.iloc[i, 0], (int, float)):
            start_row = i
            break
    
    print(f"Data starts at row {start_row}")
    
    # Find column headers (usually row before data)
    header_row = start_row - 1
    print(f"\nChecking row {header_row} for headers:")
    print(df.iloc[header_row].head(20))
    
except Exception as e:
    print(f"❌ Error loading production data: {e}")

print("\n" + "="*70)
print("Checking data_baru.csv instead...")

try:
    df_baru = pd.read_csv('data/input/data_baru.csv')
    print(f"✅ Loaded data_baru.csv: {df_baru.shape}")
    print(f"Columns: {df_baru.columns.tolist()}")
    
    # Check if it has block codes
    if 'BLOK' in df_baru.columns or 'Blok' in df_baru.columns:
        block_col = 'BLOK' if 'BLOK' in df_baru.columns else 'Blok'
        print(f"\n✅ Found block column: {block_col}")
        print(f"Sample blocks: {df_baru[block_col].head(10).tolist()}")
        
        # Filter for AME II blocks (starting with D, E, F)
        ame2_blocks = df_baru[df_baru[block_col].str.match(r'^[DEF]\d{3}A$', na=False)]
        print(f"\n✅ Found {len(ame2_blocks)} AME II blocks")
        
        if len(ame2_blocks) > 0:
            print(f"\nColumns available:")
            for col in ame2_blocks.columns:
                print(f"  - {col}")
                
except Exception as e:
    print(f"❌ Error: {e}")
