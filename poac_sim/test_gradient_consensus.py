"""
Test Script: Gradient Elbow + Consensus Voting
Validates the new implementation per consultant guidelines.
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

# Output
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_dir = Path(f'data/output/gradient_test_{timestamp}')
output_dir.mkdir(parents=True, exist_ok=True)

def run_preset_with_gradient(df, preset_name):
    """Run single preset with new gradient method."""
    preset_config = CINCIN_API_PRESETS.get(preset_name, {})
    final_config = {**CINCIN_API_CONFIG, **preset_config}
    
    print(f'\n  {preset_name.upper()}:')
    print(f'    Range: {final_config["threshold_min"]*100:.0f}% - {final_config["threshold_max"]*100:.0f}%')
    
    # Calculate percentile
    df_ranked = calculate_percentile_rank(df.copy())
    
    # Simulate thresholds
    sim_df = simulate_thresholds(
        df_ranked,
        min_threshold=final_config['threshold_min'],
        max_threshold=final_config['threshold_max'],
        step=final_config['threshold_step'],
        min_sick_neighbors=final_config['min_sick_neighbors']
    )
    
    print(f'    Simulation points: {len(sim_df)}')
    
    # Find optimal using GRADIENT (Kneedle)
    optimal_threshold = find_optimal_threshold(
        sim_df, 
        method='gradient'
    )
    
    print(f'    Knee Point Threshold: {optimal_threshold*100:.0f}%')
    
    # Classify
    df_classified = classify_trees_with_clustering(
        df_ranked,
        optimal_threshold,
        final_config['min_sick_neighbors']
    )
    
    # Count
    merah = len(df_classified[df_classified['Status_Risiko'].str.contains('MERAH', na=False)])
    print(f'    MERAH: {merah:,}')
    
    return df_classified, optimal_threshold, merah

def main():
    print('=' * 70)
    print('TEST: GRADIENT ELBOW + CONSENSUS VOTING')
    print('=' * 70)
    print(f'\nConfig: elbow_method = {CINCIN_API_CONFIG["elbow_method"]}')
    print(f'Config: use_consensus = {CINCIN_API_CONFIG["use_consensus"]}')
    print(f'Config: min_votes = {CINCIN_API_CONFIG["min_votes"]}')
    
    # Load data
    print('\n[1/3] Loading data...')
    df = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
    print(f'  Total: {len(df):,} pohon')
    
    # Run all presets with gradient
    print('\n[2/3] Running presets with GRADIENT method...')
    results = {}
    presets = ['konservatif', 'standar', 'agresif']
    
    for preset in presets:
        df_classified, threshold, merah = run_preset_with_gradient(df.copy(), preset)
        results[preset] = df_classified
    
    # Apply Consensus Voting
    print('\n[3/3] Applying Consensus Voting...')
    df_consensus = apply_consensus_voting(results, min_votes=2)
    
    # Final counts
    approved = len(df_consensus[df_consensus['consensus_status'] == 'APPROVED'])
    
    print('\n' + '=' * 70)
    print('RESULTS SUMMARY')
    print('=' * 70)
    
    print('\n📊 DETEKSI PER PRESET (GRADIENT):')
    for preset in presets:
        merah = len(results[preset][results[preset]['Status_Risiko'].str.contains('MERAH', na=False)])
        print(f'  {preset.title()}: {merah:,} MERAH')
    
    print(f'\n🗳️ CONSENSUS VOTING (min_votes=2):')
    print(f'  APPROVED: {approved:,} pohon')
    
    # Vote distribution
    print('\n📈 VOTE DISTRIBUTION:')
    for v in [3, 2, 1, 0]:
        count = len(df_consensus[df_consensus['vote_count'] == v])
        pct = count / len(df_consensus) * 100
        label = 'HIGH' if v == 3 else ('MEDIUM' if v == 2 else ('LOW' if v == 1 else 'NONE'))
        print(f'  {v} votes: {count:>8,} ({pct:5.1f}%) - {label}')
    
    # Save results
    df_consensus.to_csv(output_dir / 'consensus_results.csv', index=False)
    print(f'\nResults saved to: {output_dir}')
    
    return results, df_consensus

if __name__ == '__main__':
    main()
