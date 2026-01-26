import sys
sys.path.insert(0, '.')
from dashboard_v7_fixed import load_productivity_data
import pandas as pd

# Load productivity data
prod_df = load_productivity_data()

print('=== POV 2 Filter Step-by-Step Analysis ===\n')
print(f'Step 1: Total productivity blocks loaded: {len(prod_df)}')

# Check age distribution
print(f'\n=== Age Distribution ===')
print(prod_df['Umur_Tahun'].describe())
print(f'\nBlocks by age category:')
print(f'  TBM (<3y):        {len(prod_df[prod_df["Umur_Tahun"] < 3])}')
print(f'  Productive (3-25y): {len(prod_df[(prod_df["Umur_Tahun"] >= 3) & (prod_df["Umur_Tahun"] <= 25)])}')
print(f'  Old (>25y):       {len(prod_df[prod_df["Umur_Tahun"] > 25])}')

# Filter 1: Age 3-25 years
productive_df = prod_df[(prod_df['Umur_Tahun'] >= 3) & (prod_df['Umur_Tahun'] <= 25)]
print(f'\nStep 2: After age filter (3-25y): {len(productive_df)} blocks')

if productive_df.empty:
    print('\n❌ ISSUE: No blocks after age filter!')
    print('All blocks are either <3y (TBM) or >25y (old)')
else:
    # Get lowest yield blocks
    low_yield = productive_df.nsmallest(20, 'Yield_TonHa')
    print(f'\nStep 3: Top 20 lowest yield blocks:')
    print(low_yield[['Blok_Prod', 'Umur_Tahun', 'Yield_TonHa', 'Produksi_Ton', 'Luas_Ha']].to_string())
    
    print(f'\n📊 These {len(low_yield)} blocks would be checked for Ganoderma attack')
    print('If none show in POV 2, it means attack % < 5% for all of them.')
    print('\n💡 Recommendation: Lower attack threshold from 5% to 2-3%')
