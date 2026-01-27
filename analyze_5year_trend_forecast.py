"""
COMPREHENSIVE 5-YEAR TREND ANALYSIS & FORECASTING
AME02 Production Loss Analysis (2023-2027)

METHODOLOGY:
1. Historical Baseline: 2024-2025 (from Excel)
2. Degradation Model: 2026-2027 (No Treatment Scenario)
3. Backfill Estimate: 2023 (Reverse Modeling)

Author: Cincin API Dashboard
Date: 2026-01-27
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_DIR = Path("poac_sim/data/output/trend_analysis")
OUTPUT_FILE = OUTPUT_DIR / "ame02_5year_trend_forecast.json"

# Division filter
DIVISION_CODE = 'AME02'
DIVISION_NAME = 'AME II'

# Column indices (verified)
DIVISI_COL_IDX = 5

# Historical production columns (discovered)
PROD_COLUMNS = {
    '2024': {'real_idx': 101, 'pot_idx': 110},
    '2025': {'real_idx': 170, 'pot_idx': 173}
}

# Ganoderma & SPH indices
GANO_PCT_IDX = 58
GANO_STADIUM_12_IDX = 55
GANO_STADIUM_34_IDX = 56
GANO_TOTAL_IDX = 57
SPH_COL_IDX = 54

# TBS Price
DEFAULT_TBS_PRICE = 2500  # Rp/KG

# ============================================================================
# DEGRADATION MODEL PARAMETERS
# ============================================================================

DEGRADATION_MODEL = {
    'ganoderma_progression': {
        'annual_severity_increase': 0.15,  # 15% increase in Stadium 3&4
        'yield_impact_per_year': 0.025,    # -2.5% yield loss per year
        'description': 'Ganoderma disease progression without treatment'
    },
    'sph_decline': {
        'annual_mortality_rate': 0.015,    # 1.5% tree mortality per year
        'productivity_impact': 0.012,      # -1.2% yield per year
        'description': 'Natural palm aging and mortality'
    },
    'natural_aging': {
        'annual_decline': 0.008,           # 0.8% base decline
        'description': 'Natural productivity reduction due to aging'
    },
    'combined_rate': None  # Will be calculated
}

# Calculate combined degradation rate
DEGRADATION_MODEL['combined_rate'] = (
    DEGRADATION_MODEL['ganoderma_progression']['yield_impact_per_year'] +
    DEGRADATION_MODEL['sph_decline']['productivity_impact'] +
    DEGRADATION_MODEL['natural_aging']['annual_decline']
)

print("="*80)
print("AME02 - 5-YEAR TREND ANALYSIS & FORECASTING")
print("="*80)

print(f"\n📊 DEGRADATION MODEL (No Treatment Scenario):")
print(f"   Ganoderma Impact:  -{DEGRADATION_MODEL['ganoderma_progression']['yield_impact_per_year']*100:.1f}% per year")
print(f"   SPH Decline:       -{DEGRADATION_MODEL['sph_decline']['productivity_impact']*100:.1f}% per year")
print(f"   Natural Aging:     -{DEGRADATION_MODEL['natural_aging']['annual_decline']*100:.1f}% per year")
print(f"   ─────────────────────────────────────")
print(f"   TOTAL DEGRADATION: -{DEGRADATION_MODEL['combined_rate']*100:.1f}% per year (compounding)")

# ============================================================================
# LOAD DATA
# ============================================================================

print(f"\n[1/6] Loading Excel data...")
df = pd.read_excel(INPUT_FILE)
divisi_col = df.columns[DIVISI_COL_IDX]
ame02_data = df[df[divisi_col] == DIVISION_CODE].copy()

print(f"      Total AME02 blocks: {len(ame02_data)}")

# ============================================================================
# EXTRACT HISTORICAL DATA (2024-2025)
# ============================================================================

print(f"\n[2/6] Extracting historical production (2024-2025)...")

historical = {}

for year, cols in PROD_COLUMNS.items():
    real_col = df.columns[cols['real_idx']]
    pot_col = df.columns[cols['pot_idx']]
    
    ame02_data[f'real_{year}'] = pd.to_numeric(ame02_data[real_col], errors='coerce').fillna(0)
    ame02_data[f'pot_{year}'] = pd.to_numeric(ame02_data[pot_col], errors='coerce').fillna(0)
    ame02_data[f'gap_{year}'] = ame02_data[f'pot_{year}'] - ame02_data[f'real_{year}']
    
    total_real = ame02_data[f'real_{year}'].sum()
    total_pot = ame02_data[f'pot_{year}'].sum()
    total_gap = ame02_data[f'gap_{year}'].sum()
    
    historical[year] = {
        'real_ton': float(total_real),
        'pot_ton': float(total_pot),
        'gap_ton': float(total_gap),
        'gap_kg': float(total_gap * 1000),
        'loss_rp': float(total_gap * 1000 * DEFAULT_TBS_PRICE),
        'loss_million': float(total_gap * 1000 * DEFAULT_TBS_PRICE / 1_000_000),
        'efficiency_pct': float((total_real / total_pot * 100) if total_pot > 0 else 0)
    }
    
    print(f"      {year}: Real={total_real:,.0f} T, Pot={total_pot:,.0f} T, Gap={total_gap:,.0f} T, Eff={historical[year]['efficiency_pct']:.1f}%")

# ============================================================================
# BACKFILL 2023 ESTIMATE
# ============================================================================

print(f"\n[3/6] Backfilling 2023 estimate (reverse modeling)...")

# Use 2024-2025 trend to estimate 2023
# Assumption: degradation started before, use 80% of model rate for backfill
backfill_rate = DEGRADATION_MODEL['combined_rate'] * 0.8  # Conservative estimate

# Reverse calculate from 2024
real_2024 = historical['2024']['real_ton']
pot_2024 = historical['2024']['pot_ton']

# 2023 would have been higher (before degradation)
real_2023_est = real_2024 / (1 - backfill_rate)
pot_2023_est = pot_2024 / (1 - backfill_rate)
gap_2023_est = pot_2023_est - real_2023_est

historical['2023'] = {
    'real_ton': float(real_2023_est),
    'pot_ton': float(pot_2023_est),
    'gap_ton': float(gap_2023_est),
    'gap_kg': float(gap_2023_est * 1000),
    'loss_rp': float(gap_2023_est * 1000 * DEFAULT_TBS_PRICE),
    'loss_million': float(gap_2023_est * 1000 * DEFAULT_TBS_PRICE / 1_000_000),
    'efficiency_pct': float((real_2023_est / pot_2023_est * 100) if pot_2023_est > 0 else 0),
    'is_estimate': True,
    'method': 'Reverse modeling from 2024 using 80% degradation rate'
}

print(f"      2023 (EST): Real={real_2023_est:,.0f} T, Pot={pot_2023_est:,.0f} T, Gap={gap_2023_est:,.0f} T")
print(f"      Note: Estimated using reverse degradation model")

# ============================================================================
# FORECAST 2026-2027 (DEGRADATION MODEL)
# ============================================================================

print(f"\n[4/6] Forecasting 2026-2027 (No Treatment Scenario)...")

forecast = {}

# Start from 2025 actual
base_real = historical['2025']['real_ton']
base_pot = historical['2025']['pot_ton']

for year_offset in [1, 2]:  # 2026, 2027
    year = 2025 + year_offset
    
    # Apply compounding degradation
    degradation_factor = (1 - DEGRADATION_MODEL['combined_rate']) ** year_offset
    
    # Forecast realization (degrades)
    forecast_real = base_real * degradation_factor
    
    # Potensi also degrades slightly (aging palms)
    # But less than realization (assume 30% of degradation rate)
    pot_degradation_factor = (1 - DEGRADATION_MODEL['combined_rate'] * 0.3) ** year_offset
    forecast_pot = base_pot * pot_degradation_factor
    
    forecast_gap = forecast_pot - forecast_real
    
    forecast[str(year)] = {
        'real_ton': float(forecast_real),
        'pot_ton': float(forecast_pot),
        'gap_ton': float(forecast_gap),
        'gap_kg': float(forecast_gap * 1000),
        'loss_rp': float(forecast_gap * 1000 * DEFAULT_TBS_PRICE),
        'loss_million': float(forecast_gap * 1000 * DEFAULT_TBS_PRICE / 1_000_000),
        'efficiency_pct': float((forecast_real / forecast_pot * 100) if forecast_pot > 0 else 0),
        'is_forecast': True,
        'degradation_applied': f"{DEGRADATION_MODEL['combined_rate']*100:.1f}% per year x {year_offset} years",
        'assumptions': 'No treatment, compounding degradation from Ganoderma + SPH decline + aging'
    }
    
    print(f"      {year}: Real={forecast_real:,.0f} T, Pot={forecast_pot:,.0f} T, Gap={forecast_gap:,.0f} T, Eff={forecast[str(year)]['efficiency_pct']:.1f}%")

# ============================================================================
# EXTRACT CURRENT GANODERMA & SPH DATA
# ============================================================================

print(f"\n[5/6] Extracting current Ganoderma & SPH metrics...")

gano_pct_col = df.columns[GANO_PCT_IDX]
gano_stad12_col = df.columns[GANO_STADIUM_12_IDX]
gano_stad34_col = df.columns[GANO_STADIUM_34_IDX]
gano_total_col = df.columns[GANO_TOTAL_IDX]
sph_col = df.columns[SPH_COL_IDX]

ame02_data['gano_pct'] = pd.to_numeric(ame02_data[gano_pct_col], errors='coerce').fillna(0)
ame02_data['gano_stad12'] = pd.to_numeric(ame02_data[gano_stad12_col], errors='coerce').fillna(0)
ame02_data['gano_stad34'] = pd.to_numeric(ame02_data[gano_stad34_col], errors='coerce').fillna(0)
ame02_data['gano_total'] = pd.to_numeric(ame02_data[gano_total_col], errors='coerce').fillna(0)
ame02_data['sph'] = pd.to_numeric(ame02_data[sph_col], errors='coerce').fillna(0)

current_metrics = {
    'ganoderma': {
        'avg_attack_pct': float(ame02_data['gano_pct'].mean() * 100),
        'total_infected_trees': int(ame02_data['gano_total'].sum()),
        'stadium_12_trees': int(ame02_data['gano_stad12'].sum()),
        'stadium_34_trees': int(ame02_data['gano_stad34'].sum()),
        'blocks_infected': int((ame02_data['gano_pct'] > 0).sum()),
        'infection_rate_pct': float((ame02_data['gano_pct'] > 0).sum() / len(ame02_data) * 100)
    },
    'sph': {
        'avg_sph': float(ame02_data['sph'].mean()),
        'min_sph': float(ame02_data['sph'].min()),
        'max_sph': float(ame02_data['sph'].max()),
        'blocks_below_130': int((ame02_data['sph'] < 130).sum()),
        'blocks_within_130_143': int(((ame02_data['sph'] >= 130) & (ame02_data['sph'] <= 143)).sum()),
        'blocks_above_143': int((ame02_data['sph'] > 143).sum())
    }
}

print(f"      Ganoderma: {current_metrics['ganoderma']['avg_attack_pct']:.2f}% attack rate")
print(f"      SPH: {current_metrics['sph']['avg_sph']:.1f} pohon/Ha (avg)")

# ============================================================================
# COMPILE FINAL OUTPUT
# ============================================================================

print(f"\n[6/6] Compiling comprehensive analysis...")

# Combine all years in chronological order
all_years = {**{'2023': historical['2023']}, **{k: historical[k] for k in ['2024', '2025']}, **forecast}

output = {
    'metadata': {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'division': DIVISION_CODE,
        'division_name': DIVISION_NAME,
        'total_blocks': len(ame02_data),
        'tbs_price_per_kg': DEFAULT_TBS_PRICE,
        'analysis_period': '2023-2027 (5 years)',
        'data_sources': {
            '2023': 'Backfill estimate (reverse modeling)',
            '2024-2025': 'Historical data from Excel',
            '2026-2027': 'Forecast (degradation model)'
        }
    },
    'degradation_model': {
        'methodology': 'Compound degradation model for no-treatment scenario',
        'components': DEGRADATION_MODEL,
        'total_annual_rate_pct': round(DEGRADATION_MODEL['combined_rate'] * 100, 2),
        'assumptions': [
            'Ganoderma disease progresses without intervention',
            'Natural SPH decline due to mortality and aging',
            'No replanting or treatment programs',
            'Compounding effect over years'
        ]
    },
    'timeline_data': all_years,
    'current_metrics_2025': current_metrics,
    'trend_analysis': {
        'historical_trend_2023_2025': {
            'real_change_ton': float(historical['2025']['real_ton'] - historical['2023']['real_ton']),
            'real_change_pct': float((historical['2025']['real_ton'] / historical['2023']['real_ton'] - 1) * 100),
            'gap_change_ton': float(historical['2025']['gap_ton'] - historical['2023']['gap_ton']),
            'efficiency_change_pct': float(historical['2025']['efficiency_pct'] - historical['2023']['efficiency_pct'])
        },
        'forecast_trend_2025_2027': {
            'real_change_ton': float(forecast['2027']['real_ton'] - historical['2025']['real_ton']),
            'real_change_pct': float((forecast['2027']['real_ton'] / historical['2025']['real_ton'] - 1) * 100),
            'gap_change_ton': float(forecast['2027']['gap_ton'] - historical['2025']['gap_ton']),
            'additional_loss_million': float(forecast['2027']['loss_million'] - historical['2025']['loss_million'])
        }
    },
    'business_impact': {
        'total_loss_2023_2027_million': float(sum(all_years[y]['loss_million'] for y in all_years)),
        'avg_annual_loss_million': float(sum(all_years[y]['loss_million'] for y in all_years) / len(all_years)),
        'peak_loss_year': max(all_years, key=lambda y: all_years[y]['loss_million']),
        'worst_efficiency_year': min(all_years, key=lambda y: all_years[y]['efficiency_pct'])
    }
}

# Save to JSON
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Analysis complete! Saved to: {OUTPUT_FILE}")

# ============================================================================
# DISPLAY SUMMARY
# ============================================================================

print("\n" + "="*80)
print("5-YEAR TREND SUMMARY (2023-2027)")
print("="*80)

print(f"\n{'Year':<6} {'Type':<10} {'Real (T)':<12} {'Pot (T)':<12} {'Gap (T)':<12} {'Loss (M)':<12} {'Eff %':<8}")
print("-"*80)

for year in ['2023', '2024', '2025', '2026', '2027']:
    data = all_years[year]
    year_type = 'Estimate' if year == '2023' else ('Actual' if year in ['2024', '2025'] else 'Forecast')
    
    print(f"{year:<6} {year_type:<10} {data['real_ton']:<12,.0f} {data['pot_ton']:<12,.0f} "
          f"{data['gap_ton']:<12,.0f} {data['loss_million']:<12,.2f} {data['efficiency_pct']:<8,.1f}")

print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

print(f"\n📈 HISTORICAL TREND (2023-2025):")
print(f"   Real Production Change: {output['trend_analysis']['historical_trend_2023_2025']['real_change_pct']:+.1f}%")
print(f"   Gap Change: {output['trend_analysis']['historical_trend_2023_2025']['gap_change_ton']:+,.0f} Ton")
print(f"   Efficiency Change: {output['trend_analysis']['historical_trend_2023_2025']['efficiency_change_pct']:+.1f} pp")

print(f"\n📉 FORECAST TREND (2025-2027, No Treatment):")
print(f"   Real Production Decline: {output['trend_analysis']['forecast_trend_2025_2027']['real_change_pct']:.1f}%")
print(f"   Gap Increase: {output['trend_analysis']['forecast_trend_2025_2027']['gap_change_ton']:+,.0f} Ton")
print(f"   Additional Loss: Rp {output['trend_analysis']['forecast_trend_2025_2027']['additional_loss_million']:.2f} Million")

print(f"\n💰 BUSINESS IMPACT (5-Year Total):")
print(f"   Total Accumulated Loss: Rp {output['business_impact']['total_loss_2023_2027_million']:.2f} Million")
print(f"   Average Annual Loss: Rp {output['business_impact']['avg_annual_loss_million']:.2f} Million")
print(f"   Peak Loss Year: {output['business_impact']['peak_loss_year']}")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
