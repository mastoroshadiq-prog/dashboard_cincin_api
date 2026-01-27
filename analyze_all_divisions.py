"""
COMPREHENSIVE LOSS ANALYSIS - ALL DIVISIONS
Extends AME02 analysis to: AME01, AME03, AME04, OLE01, OLE02

Output: JSON file per division
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_DIR = Path("poac_sim/data/output/divisions")

# Fixed column indices
DIVISI_COL_IDX = 5
BLOK_COL_IDX = 8
GANO_STADIUM_12_IDX = 55
GANO_STADIUM_34_IDX = 56
GANO_TOTAL_IDX = 57
GANO_PCT_IDX = 58

# 2025 Production columns
REAL_TON_2025_IDX = 170
POT_TON_2025_IDX = 173
GAP_TON_2025_IDX = 176

# SPH column
SPH_COL_IDX = 54
SPH_STANDARD_MIN = 130
SPH_STANDARD_MAX = 143

DEFAULT_TBS_PRICE = 2500

DIVISIONS = ['AME01', 'AME02', 'AME03', 'AME04', 'OLE01', 'OLE02']
DIVISION_NAMES = {
    'AME01': 'AME I',
    'AME02': 'AME II',
    'AME03': 'AME III',
    'AME04': 'AME IV',
    'OLE01': 'OLE I',
    'OLE02': 'OLE II'
}

def format_currency(value):
    """Format Rupiah"""
    if value >= 1_000_000_000:
        return f"Rp {value/1_000_000_000:.2f} Miliar"
    elif value >= 1_000_000:
        return f"Rp {value/1_000_000:.2f} Juta"
    else:
        return f"Rp {value:,.0f}"

def analyze_division(df, division_code, tbs_price=DEFAULT_TBS_PRICE):
    """
    Analyze single division
    """
    print(f"\n{'='*80}")
    print(f"ANALYZING: {DIVISION_NAMES.get(division_code, division_code)}")
    print(f"{'='*80}")
    
    # Filter division
    divisi_col = df.columns[DIVISI_COL_IDX]
    division_data = df[df[divisi_col] == division_code].copy()
    
    if len(division_data) == 0:
        print(f"[SKIP] No data found for {division_code}")
        return None
    
    print(f"[OK] Blocks found: {len(division_data)}")
    
    # Extract columns
    real_col = df.columns[REAL_TON_2025_IDX]
    pot_col = df.columns[POT_TON_2025_IDX]
    gano_pct_col = df.columns[GANO_PCT_IDX]
    gano_stad_12_col = df.columns[GANO_STADIUM_12_IDX]
    gano_stad_34_col = df.columns[GANO_STADIUM_34_IDX]
    gano_total_col = df.columns[GANO_TOTAL_IDX]
    sph_col = df.columns[SPH_COL_IDX]
    
    # Convert to numeric
    division_data['real_ton_2025'] = pd.to_numeric(division_data[real_col], errors='coerce').fillna(0)
    division_data['pot_ton_2025'] = pd.to_numeric(division_data[pot_col], errors='coerce').fillna(0)
    division_data['gap_final'] = division_data['pot_ton_2025'] - division_data['real_ton_2025']
    division_data['gap_kg'] = division_data['gap_final'] * 1000
    division_data['loss_rp'] = division_data['gap_kg'] * tbs_price
    
    # Ganoderma
    division_data['gano_pct'] = pd.to_numeric(division_data[gano_pct_col], errors='coerce').fillna(0)
    division_data['gano_stad_12'] = pd.to_numeric(division_data[gano_stad_12_col], errors='coerce').fillna(0)
    division_data['gano_stad_34'] = pd.to_numeric(division_data[gano_stad_34_col], errors='coerce').fillna(0)
    division_data['gano_total'] = pd.to_numeric(division_data[gano_total_col], errors='coerce').fillna(0)
    
    # SPH
    division_data['sph'] = pd.to_numeric(division_data[sph_col], errors='coerce').fillna(0)
    
    # Aggregate
    total_real_ton = division_data['real_ton_2025'].sum()
    total_pot_ton = division_data['pot_ton_2025'].sum()
    total_gap_ton = division_data['gap_final'].sum()
    total_gap_kg = total_gap_ton * 1000
    total_loss_rp = division_data['loss_rp'].sum()
    
    avg_attack_rate = division_data['gano_pct'].mean() * 100
    blocks_with_gano = (division_data['gano_pct'] > 0).sum()
    total_gano_stad_12 = division_data['gano_stad_12'].sum()
    total_gano_stad_34 = division_data['gano_stad_34'].sum()
    total_gano_all = division_data['gano_total'].sum()
    
    avg_sph = division_data['sph'].mean()
    min_sph = division_data['sph'].min()
    max_sph = division_data['sph'].max()
    blocks_below_standard = (division_data['sph'] < SPH_STANDARD_MIN).sum()
    blocks_within_standard = ((division_data['sph'] >= SPH_STANDARD_MIN) & (division_data['sph'] <= SPH_STANDARD_MAX)).sum()
    blocks_above_standard = (division_data['sph'] > SPH_STANDARD_MAX).sum()
    
    # Build result
    results = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'division': division_code,
        'division_name': DIVISION_NAMES.get(division_code, division_code),
        'total_blocks': len(division_data),
        'tbs_price_per_kg': tbs_price,
        'metrics': {
            'production': {
                'total_real_ton': float(total_real_ton),
                'total_pot_ton': float(total_pot_ton),
                'avg_real_per_block_ton': float(total_real_ton / len(division_data)),
                'avg_pot_per_block_ton': float(total_pot_ton / len(division_data)),
                'yield_efficiency_pct': float((total_real_ton / total_pot_ton * 100) if total_pot_ton > 0 else 0)
            },
            'gap_yield': {
                'total_gap_ton': float(total_gap_ton),
                'total_gap_kg': float(total_gap_kg),
                'avg_gap_per_block_ton': float(total_gap_ton / len(division_data)),
                'avg_gap_per_block_kg': float(total_gap_kg / len(division_data))
            },
            'financial_loss': {
                'tbs_price_rp_per_kg': tbs_price,
                'total_loss_rp': float(total_loss_rp),
                'total_loss_juta': float(total_loss_rp / 1_000_000),
                'total_loss_miliar': float(total_loss_rp / 1_000_000_000),
                'avg_loss_per_block_rp': float(total_loss_rp / len(division_data))
            },
            'ganoderma': {
                'avg_attack_rate_pct': float(avg_attack_rate),
                'blocks_with_ganoderma': int(blocks_with_gano),
                'blocks_clean': int(len(division_data) - blocks_with_gano),
                'infection_rate_pct': float((blocks_with_gano / len(division_data) * 100)),
                'total_trees_stadium_12': int(total_gano_stad_12),
                'total_trees_stadium_34': int(total_gano_stad_34),
                'total_trees_infected': int(total_gano_all),
                'severity_ratio_34_vs_12': float(total_gano_stad_34 / total_gano_stad_12) if total_gano_stad_12 > 0 else 0
            },
            'sph': {
                'avg_sph': float(avg_sph),
                'min_sph': float(min_sph),
                'max_sph': float(max_sph),
                'standard_range': f"{SPH_STANDARD_MIN}-{SPH_STANDARD_MAX}",
                'blocks_below_standard': int(blocks_below_standard),
                'blocks_within_standard': int(blocks_within_standard),
                'blocks_above_standard': int(blocks_above_standard),
                'status': 'Below Standard' if avg_sph < SPH_STANDARD_MIN else ('Above Standard' if avg_sph > SPH_STANDARD_MAX else 'Within Standard')
            }
        }
    }
    
    # Display summary
    print(f"\n✅ SUMMARY:")
    print(f"   Blocks: {len(division_data)}")
    print(f"   Real: {total_real_ton:,.2f} Ton | Pot: {total_pot_ton:,.2f} Ton")
    print(f"   Gap: {total_gap_ton:,.2f} Ton | Efficiency: {(total_real_ton/total_pot_ton*100) if total_pot_ton > 0 else 0:.2f}%")
    print(f"   Loss: {format_currency(total_loss_rp)}")
    print(f"   Gano: {avg_attack_rate:.2f}% | SPH: {avg_sph:.1f} ({results['metrics']['sph']['status']})")
    
    return results

def main():
    """
    Analyze all divisions
    """
    print("="*80)
    print("COMPREHENSIVE LOSS ANALYSIS - ALL DIVISIONS")
    print("="*80)
    
    # Load Excel
    print(f"\n[1/3] Loading Excel...")
    df = pd.read_excel(INPUT_FILE)
    print(f"      Total rows: {len(df)}, Columns: {len(df.columns)}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Analyze each division
    print(f"\n[2/3] Analyzing divisions...")
    all_results = {}
    
    for division in DIVISIONS:
        result = analyze_division(df, division)
        if result:
            all_results[division] = result
            
            # Save individual JSON
            output_file = OUTPUT_DIR / f"{division.lower()}_analysis.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"      [SAVED] {output_file}")
    
    # Save combined JSON
    print(f"\n[3/3] Saving combined results...")
    combined_file = OUTPUT_DIR / "all_divisions_analysis.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"      [SAVED] {combined_file}")
    
    # Summary table
    print(f"\n{'='*80}")
    print("COMPARATIVE SUMMARY")
    print(f"{'='*80}")
    print(f"{'Division':<12} {'Blocks':>8} {'Gap (Ton)':>12} {'Loss (Miliar)':>15} {'Gano %':>8} {'SPH':>8}")
    print("-"*80)
    
    for div_code, result in all_results.items():
        metrics = result['metrics']
        print(f"{result['division_name']:<12} "
              f"{result['total_blocks']:>8} "
              f"{metrics['gap_yield']['total_gap_ton']:>12,.0f} "
              f"{metrics['financial_loss']['total_loss_miliar']:>15,.2f} "
              f"{metrics['ganoderma']['avg_attack_rate_pct']:>8,.2f} "
              f"{metrics['sph']['avg_sph']:>8,.1f}")
    
    print("="*80)
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"📊 Total divisions analyzed: {len(all_results)}")

if __name__ == "__main__":
    main()
