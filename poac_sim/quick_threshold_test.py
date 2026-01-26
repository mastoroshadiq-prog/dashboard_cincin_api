"""Quick threshold comparison test"""
import sys
sys.path.insert(0, 'src')

from pathlib import Path
from src.ingestion import load_and_clean_data
from src.clustering import calculate_percentile_rank, simulate_thresholds, find_optimal_threshold
from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS

df = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
df_ranked = calculate_percentile_rank(df)

print('THRESHOLD SELECTION: EFFICIENCY vs GRADIENT')
print('=' * 60)

for preset_name in ['konservatif', 'standar', 'agresif']:
    preset = CINCIN_API_PRESETS[preset_name]
    final_config = {**CINCIN_API_CONFIG, **preset}
    
    sim_df = simulate_thresholds(
        df_ranked,
        min_threshold=final_config['threshold_min'],
        max_threshold=final_config['threshold_max'],
        step=final_config['threshold_step'],
        min_sick_neighbors=final_config['min_sick_neighbors']
    )
    
    # Compare methods
    thresh_eff = find_optimal_threshold(sim_df, method='efficiency')
    thresh_grad = find_optimal_threshold(sim_df, method='gradient')
    
    range_str = f"{final_config['threshold_min']*100:.0f}%-{final_config['threshold_max']*100:.0f}%"
    print(f"{preset_name.upper()} ({range_str}):")
    print(f"  Efficiency selects: {thresh_eff*100:.0f}%")
    print(f"  Gradient selects:   {thresh_grad*100:.0f}%")
    print()
