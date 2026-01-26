"""
POAC v3.4 Recalibration Test
============================
Test Scenario A (Intersection, min_votes=2) and Scenario B (Union, min_votes=1)
with widened ranges per consultant guideline.
"""
import sys
sys.path.insert(0, 'src')

import pandas as pd
from pathlib import Path
from datetime import datetime
from src.ingestion import load_and_clean_data
from src.clustering import (
    calculate_percentile_rank,
    simulate_thresholds,
    find_optimal_threshold,
    classify_trees_with_clustering,
    apply_consensus_voting
)
from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS

# Constants
GT_TOTAL_GANO = 5969  # Ground Truth AME II
TARGET_LOW = 4500     # -25% from GT
TARGET_HIGH = 8000    # +35% from GT

# Output
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_dir = Path(f'data/output/v34_recalibration_{timestamp}')
output_dir.mkdir(parents=True, exist_ok=True)

def run_all_presets_gradient(df):
    """Run all 3 presets with gradient method."""
    results = {}
    
    for preset_name in ['konservatif', 'standar', 'agresif']:
        preset_config = CINCIN_API_PRESETS.get(preset_name, {})
        final_config = {**CINCIN_API_CONFIG, **preset_config}
        
        print(f'\n  {preset_name.upper()}:')
        print(f'    Range: {final_config["threshold_min"]*100:.0f}% - {final_config["threshold_max"]*100:.0f}%')
        
        df_ranked = calculate_percentile_rank(df.copy())
        
        sim_df = simulate_thresholds(
            df_ranked,
            min_threshold=final_config['threshold_min'],
            max_threshold=final_config['threshold_max'],
            step=final_config['threshold_step'],
            min_sick_neighbors=final_config['min_sick_neighbors']
        )
        
        optimal_threshold = find_optimal_threshold(sim_df, method='gradient')
        print(f'    Kneedle Threshold: {optimal_threshold*100:.0f}%')
        
        df_classified = classify_trees_with_clustering(
            df_ranked,
            optimal_threshold,
            final_config['min_sick_neighbors']
        )
        
        merah = len(df_classified[df_classified['Status_Risiko'].str.contains('MERAH', na=False)])
        print(f'    MERAH: {merah:,}')
        
        results[preset_name] = df_classified
    
    return results

def main():
    print('=' * 70)
    print('POAC v3.4 RECALIBRATION TEST')
    print('=' * 70)
    
    print('\n[CONFIG v3.4 - WIDENED RANGES]')
    for preset in ['konservatif', 'standar', 'agresif']:
        p = CINCIN_API_PRESETS[preset]
        print(f'  {preset}: {p["threshold_min"]*100:.0f}% - {p["threshold_max"]*100:.0f}%')
    
    # Load data
    print('\n[1/4] Loading AME II data...')
    df = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
    print(f'  Total: {len(df):,} pohon')
    print(f'  Ground Truth: {GT_TOTAL_GANO:,} GANO')
    
    # Run all presets
    print('\n[2/4] Running presets with GRADIENT (Kneedle)...')
    results = run_all_presets_gradient(df.copy())
    
    # Scenario A: Intersection (min_votes=2)
    print('\n[3/4] Scenario A: Intersection (min_votes=2)...')
    df_scenario_a = apply_consensus_voting(results, min_votes=2)
    approved_a = len(df_scenario_a[df_scenario_a['consensus_status'] == 'APPROVED'])
    
    # Scenario B: Union (min_votes=1)
    print('\n[4/4] Scenario B: Union (min_votes=1)...')
    df_scenario_b = apply_consensus_voting(results, min_votes=1)
    approved_b = len(df_scenario_b[df_scenario_b['consensus_status'] == 'APPROVED'])
    
    # Results
    print('\n' + '=' * 70)
    print('RESULTS COMPARISON')
    print('=' * 70)
    
    print('\n📊 GROUND TRUTH:')
    print(f'  TOTAL_GANO: {GT_TOTAL_GANO:,}')
    print(f'  Target Range: {TARGET_LOW:,} - {TARGET_HIGH:,}')
    
    print('\n📈 SCENARIO COMPARISON:')
    print('-' * 70)
    print(f'{"Scenario":<25} {"Config Range":<15} {"Voting":<15} {"Result":<10} {"vs GT":<10} {"Status":<10}')
    print('-' * 70)
    
    # v3.3 (old)
    v33_pct = (1022 - GT_TOTAL_GANO) / GT_TOTAL_GANO * 100
    print(f'{"v3.3 (Old)":<25} {"Capped (30%)":<15} {"min_votes=2":<15} {"1,022":<10} {f"{v33_pct:+.0f}%":<10} {"❌ UNDER":<10}')
    
    # v3.4 Scenario A
    pct_a = (approved_a - GT_TOTAL_GANO) / GT_TOTAL_GANO * 100
    status_a = "✅ OK" if TARGET_LOW <= approved_a <= TARGET_HIGH else ("❌ UNDER" if approved_a < TARGET_LOW else "⚠️ OVER")
    print(f'{"v3.4 A (Wide+Intersect)":<25} {"Wide (60%)":<15} {"min_votes=2":<15} {f"{approved_a:,}":<10} {f"{pct_a:+.0f}%":<10} {status_a:<10}')
    
    # v3.4 Scenario B
    pct_b = (approved_b - GT_TOTAL_GANO) / GT_TOTAL_GANO * 100
    status_b = "✅ OK" if TARGET_LOW <= approved_b <= TARGET_HIGH else ("❌ UNDER" if approved_b < TARGET_LOW else "⚠️ OVER")
    print(f'{"v3.4 B (Wide+Union)":<25} {"Wide (60%)":<15} {"min_votes=1":<15} {f"{approved_b:,}":<10} {f"{pct_b:+.0f}%":<10} {status_b:<10}')
    
    print('-' * 70)
    
    # Recommendation
    print('\n💡 RECOMMENDATION:')
    if TARGET_LOW <= approved_a <= TARGET_HIGH:
        print(f'  USE Scenario A (min_votes=2): {approved_a:,} - Within target range!')
    elif TARGET_LOW <= approved_b <= TARGET_HIGH:
        print(f'  USE Scenario B (min_votes=1): {approved_b:,} - Within target range!')
    elif approved_a < TARGET_LOW and approved_b >= TARGET_LOW:
        print(f'  USE Scenario B (min_votes=1): {approved_b:,} - Better than A')
    else:
        print('  NEED FURTHER ADJUSTMENT - Both scenarios outside target range')
    
    # Save results
    df_scenario_a.to_csv(output_dir / 'scenario_a_results.csv', index=False)
    df_scenario_b.to_csv(output_dir / 'scenario_b_results.csv', index=False)
    
    print(f'\nResults saved to: {output_dir}')
    
    return approved_a, approved_b

if __name__ == '__main__':
    main()
