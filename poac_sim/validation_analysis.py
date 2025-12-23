"""
Validation Analysis: Cincin Api + Z-Score vs Ground Truth
Analyze over-detection and under-detection rates
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, '.')

from src.ingestion import load_and_clean_data
from dashboard_v7_fixed import load_ame_iv_data, analyze_divisi

def load_ground_truth():
    """
    Load ground truth Ganoderma data from data_gabungan.xlsx
    Returns DataFrame with block-level actual infection data
    """
    file_path = Path('data/input/data_gabungan.xlsx')
    df_raw = pd.read_excel(file_path, header=None)
    df = df_raw.iloc[8:].copy().reset_index(drop=True)
    df.columns = [f'col_{i}' for i in range(df.shape[1])]
    
    # col_55: STADIUM 1&2 (early infection)
    # col_56: STADIUM 3&4 (severe infection)
    # col_58: %SERANGAN (total attack %)
    
    ground_truth = df[['col_0', 'col_55', 'col_56', 'col_58']].copy()
    ground_truth.columns = ['Blok', 'Stadium_12', 'Stadium_34', 'Attack_Pct']
    
    ground_truth['Stadium_12'] = pd.to_numeric(ground_truth['Stadium_12'], errors='coerce').fillna(0)
    ground_truth['Stadium_34'] = pd.to_numeric(ground_truth['Stadium_34'], errors='coerce').fillna(0)
    ground_truth['Attack_Pct'] = pd.to_numeric(ground_truth['Attack_Pct'], errors='coerce').fillna(0) * 100
    
    # Calculate total infected trees
    ground_truth['Total_Infected'] = ground_truth['Stadium_12'] + ground_truth['Stadium_34']
    
    return ground_truth


def analyze_detection_gap(divisi_name, df_ndvi, ground_truth, output_dir):
    """
    Analyze gap between algorithm detection and ground truth
    
    Args:
        divisi_name: 'AME II' or 'AME IV'
        df_ndvi: NDVI data with algorithm detection results
        ground_truth: Ground truth infection data
        output_dir: Output directory
    
    Returns:
        dict with analysis results
    """
    
    print(f'\n{"="*70}')
    print(f'VALIDATION ANALYSIS: {divisi_name}')
    print(f'{"="*70}')
    
    # Load productivity data for area info
    from dashboard_v7_fixed import load_productivity_data
    prod_df = load_productivity_data()
    
    # Run algorithm analysis
    print(f'\n[1/4] Running {divisi_name} algorithm detection...')
    results, _ = analyze_divisi(df_ndvi, divisi_name, prod_df, output_dir)
    
    # Analyze EACH preset
    presets = ['konservatif', 'standar', 'agresif']
    all_preset_results = {}
    
    for preset in presets:
        print(f'\n  🔍 Analyzing Preset: {preset.upper()}')
        algo_results = results[preset]['block_stats']
        
        comparison = []
        for _, algo_row in algo_results.iterrows():
            blok = algo_row['Blok']
            
            # Find in ground truth
            gt_match = ground_truth[ground_truth['Blok'] == blok]
            
            if gt_match.empty:
                from dashboard_v7_fixed import convert_gano_to_prod_pattern
                pattern = convert_gano_to_prod_pattern(blok)
                gt_match = ground_truth[ground_truth['Blok'].str.contains(pattern, na=False, regex=False)]
            
            if not gt_match.empty:
                gt_row = gt_match.iloc[0]
                
                algo_stressed = algo_row['MERAH'] + algo_row['ORANYE']
                algo_attack_pct = algo_row['Attack_Pct']
                gt_infected = gt_row['Total_Infected']
                gt_attack_pct = gt_row['Attack_Pct']
                
                comparison.append({
                    'Blok': blok,
                    'Algo_Stressed': algo_stressed,
                    'Algo_Attack_%': algo_attack_pct,
                    'GT_Infected': gt_infected,
                    'GT_Attack_%': gt_attack_pct,
                    'Gap_Trees': algo_stressed - gt_infected,
                    'Gap_%': algo_attack_pct - gt_attack_pct
                })
        
        df_comp = pd.DataFrame(comparison)
        
        if not df_comp.empty:
            over = len(df_comp[df_comp['Gap_Trees'] > 0])
            under = len(df_comp[df_comp['Gap_Trees'] < 0])
            avg_gap = df_comp['Gap_%'].mean()
            mae = df_comp['Gap_%'].abs().mean()
            
            all_preset_results[preset] = {
                'over_pct': (over/len(df_comp)*100),
                'under_pct': (under/len(df_comp)*100),
                'avg_gap': avg_gap,
                'mae': mae
            }
            
            # Save detail for this preset
            df_comp.to_csv(output_dir / f'{divisi_name.lower().replace(" ", "")}_{preset}_validation.csv', index=False)

    return all_preset_results


def main():
    """Main validation analysis."""
    print('='*70)
    print('🔬 ALGORITHM VALIDATION ANALYSIS')
    print('   Cincin Api + Z-Score vs Ground Truth')
    print('='*70)
    
    base_dir = Path(__file__).parent
    output_dir = base_dir / 'data/output/validation_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load ground truth
    print('\n[1/2] Loading ground truth data...')
    ground_truth = load_ground_truth()
    print(f'  ✅ Loaded ground truth for {len(ground_truth)} blocks')
    
    # Load NDVI data
    print('\n[2/2] Loading NDVI data...')
    df_ame2 = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
    print(f'  ✅ AME II: {len(df_ame2)} trees')
    
    df_ame4 = load_ame_iv_data(Path('data/input/AME_IV.csv'))
    print(f'  ✅ AME IV: {len(df_ame4)} trees')
    
    # Run analysis for both divisions
    results_ame2 = analyze_detection_gap('AME II', df_ame2, ground_truth, output_dir)
    results_ame4 = analyze_detection_gap('AME IV', df_ame4, ground_truth, output_dir)
    
    # Overall summary comparison
    print(f'\n{"="*70}')
    print('📋 PRESET COMPARISON SUMMARY')
    print(f'{"="*70}')
    
    for div, results in [('AME II', results_ame2), ('AME IV', results_ame4)]:
        print(f'\n🌐 {div}:')
        print(f'  {"PRESET":<15} | {"OVER %":<10} | {"UNDER %":<10} | {"MAE %":<10} | {"AVG GAP %":<10}')
        print('-'*70)
        for preset in ['konservatif', 'standar', 'agresif']:
            res = results.get(preset, {})
            print(f'  {preset.title():<15} | {res.get("over_pct",0):.1f}%      | {res.get("under_pct",0):.1f}%      | {res.get("mae",0):.2f}%     | {res.get("avg_gap",0):.2f}%')
    
    print(f'\n✅ Validation results saved to: {output_dir}')
    print('='*70)


if __name__ == '__main__':
    main()
