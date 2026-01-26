import sys
sys.path.insert(0, '.')
from dashboard_v7_fixed import load_productivity_data, convert_prod_to_gano_pattern
from src.ingestion import load_and_clean_data
from pathlib import Path
import pandas as pd

# Load data
df_gano = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
prod_df = load_productivity_data()

print('=== POV 2 Filter Analysis ===')
print(f'Total productivity blocks: {len(prod_df)}')

# Filter 1: Age 3-25 years
productive_df = prod_df[(prod_df['Umur_Tahun'] >= 3) & (prod_df['Umur_Tahun'] <= 25)]
print(f'After age filter (3-25y): {len(productive_df)}')

if productive_df.empty:
    print('❌ NO DATA after age filter!')
else:
    # Get lowest yield blocks
    low_yield = productive_df.nsmallest(20, 'Yield_TonHa')
    print(f'\nTop 20 lowest yield blocks (age 3-25):')
    
    # Check attack % for each
    from dashboard_v7_fixed import analyze_divisi
    results, _ = analyze_divisi(df_gano, 'AME II', prod_df, Path('data/output/temp'))
    block_stats = results['standar']['block_stats']
    
    matched_count = 0
    for idx, row in low_yield.head(20).iterrows():
        gano_pattern = convert_prod_to_gano_pattern(row['Blok_Prod'])
        blok_match = block_stats[block_stats['Blok'].str.contains(gano_pattern, na=False, regex=False)]
        attack = blok_match['Attack_Pct'].mean() if not blok_match.empty else 0
        
        meets_criteria = "✅" if attack >= 5 else "❌"
        print(f'{meets_criteria} {row["Blok_Prod"]:10s} | Umur: {row["Umur_Tahun"]:2.0f}y | Yield: {row["Yield_TonHa"]:5.2f} | Attack: {attack:5.1f}%')
        
        if attack >= 5:
            matched_count += 1
    
    print(f'\n📊 Summary:')
    print(f'Blocks with age 3-25y: {len(productive_df)}')
    print(f'Top 20 lowest yield: {len(low_yield)}')
    print(f'Blocks meeting attack >5%: {matched_count}')
    
    if matched_count == 0:
        print('\n⚠️ ISSUE: No blocks with attack >5%')
        print('Recommendation: Lower attack threshold to 3% or 2%')
        
        # Check with lower threshold
        print('\n=== Testing with attack >3% ===')
        count_3pct = 0
        for idx, row in low_yield.head(20).iterrows():
            gano_pattern = convert_prod_to_gano_pattern(row['Blok_Prod'])
            blok_match = block_stats[block_stats['Blok'].str.contains(gano_pattern, na=False, regex=False)]
            attack = blok_match['Attack_Pct'].mean() if not blok_match.empty else 0
            if attack >= 3:
                count_3pct += 1
                print(f'✅ {row["Blok_Prod"]:10s} | Attack: {attack:.1f}%')
        
        print(f'\nWith 3% threshold: {count_3pct} blocks would show')
