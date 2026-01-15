import pandas as pd
import json

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# F blocks that are missing
f_blocks = ['F002A', 'F004A']

# Production columns (from previous investigation)
production_cols = {
    2023: 152,
    2024: 161,  
    2025: 170,
}

print("="*80)
print("EXTRACTING F002A and F004A DATA")
print("="*80)

for block in f_blocks:
    block_rows = df[df[0] == block]
    
    if len(block_rows) == 0:
        print(f"\nNOT FOUND: {block}")
        continue
    
    row_idx = block_rows.index[0]
    luas_ha = df.iloc[row_idx, 11]
    
    print(f"\n{block} (Row {row_idx}, Luas: {luas_ha} Ha):")
    
    for year, col in production_cols.items():
        real_ton_total = df.iloc[row_idx, col]
        poten_ton_total = df.iloc[row_idx, col + 3]  # Potensi is 3 columns after Real
        
        if pd.notna(real_ton_total) and pd.notna(luas_ha):
            real_ton_ha = round(float(real_ton_total) / float(luas_ha), 2)
            poten_ton_ha = round(float(poten_ton_total) / float(luas_ha), 2) if pd.notna(poten_ton_total) else 0
            gap_ton_ha = round(poten_ton_ha - real_ton_ha, 2)
            gap_pct = round((gap_ton_ha / poten_ton_ha) * 100, 1) if poten_ton_ha > 0 else 0
            
            print(f"  {year}: Real={real_ton_ha} Ton/Ha, Poten={poten_ton_ha} Ton/Ha, Gap={gap_ton_ha} ({gap_pct}%)")

print("\n" + "="*80)
