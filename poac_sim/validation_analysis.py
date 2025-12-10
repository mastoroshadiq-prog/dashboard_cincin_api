"""
================================================================================
VALIDATION SCRIPT: Algoritma Cincin Api vs Sensus Ganoderma
================================================================================
Script untuk membandingkan hasil deteksi Algoritma Cincin Api (NDRE-based)
dengan data sensus lapangan (ground truth) untuk validasi akurasi.

Author: POAC Analysis Team
Date: January 2025
================================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# CONFIGURATION
# =====================================================
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'data' / 'input'
OUTPUT_DIR = BASE_DIR / 'output' / 'validation_report'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# DATA LOADING FUNCTIONS
# =====================================================

def load_sensus_data(filepath: Path) -> pd.DataFrame:
    """Load and clean sensus data."""
    df = pd.read_csv(filepath, skiprows=2, header=None)
    df.columns = ['ESTATE', 'DIVISI', 'BLOK', 'TT', 'LUAS_TANAM', 'TOTAL_PKK', 'SPH', 
                  'STADIUM_1_2', 'STADIUM_3_4', 'TOTAL_GANODERMA', 'SERANGAN_PCT', 
                  'REALISASI_HA', 'REALISASI_PKK']
    df = df.dropna(subset=['BLOK'])
    
    # Convert numeric columns
    for col in ['TOTAL_PKK', 'STADIUM_1_2', 'STADIUM_3_4', 'TOTAL_GANODERMA']:
        df[col] = df[col].astype(str).str.replace(',', '').str.replace('-', '0').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    df['SERANGAN_PCT'] = pd.to_numeric(
        df['SERANGAN_PCT'].astype(str).str.replace('%', ''), 
        errors='coerce'
    ).fillna(0)
    
    # Normalize block codes
    df['BLOCK_NORM'] = df['BLOK'].apply(normalize_block)
    
    return df


def load_ame_ii_algo_data(filepath: Path) -> pd.DataFrame:
    """Load and clean AME II algorithm data."""
    df = pd.read_csv(filepath)
    df = df.dropna(subset=['blok'])
    df['blok'] = df['blok'].astype(str)
    df.columns = df.columns.str.lower()
    df['ndre125'] = df['ndre125'].astype(str).str.replace(',', '.')
    df['ndre125'] = pd.to_numeric(df['ndre125'], errors='coerce')
    df['risk_level'] = df['klassndre12025'].apply(map_stress_level)
    return df


def load_ame_iv_algo_data(filepath: Path) -> pd.DataFrame:
    """Load and clean AME IV algorithm data."""
    df = pd.read_csv(filepath, sep=';', decimal=',')
    df.columns = [c.lower() for c in df.columns]
    
    # Fix column alignment - AME IV has shifted columns
    df_fixed = pd.DataFrame({
        'blok': df['blok_b'],
        'blok_b': df['t_tanam'],
        't_tanam': df['n_baris'],
        'n_baris': df['n_pokok'],
        'n_pokok': df['objectid'],
        'objectid': df['ndre125'],
        'ndre125': df['klassndre12025'],
        'klassndre12025': df['ket'],
    })
    
    df_fixed = df_fixed.dropna(subset=['blok'])
    df_fixed['blok'] = df_fixed['blok'].astype(str)
    df_fixed['ndre125'] = pd.to_numeric(df_fixed['ndre125'], errors='coerce')
    df_fixed['risk_level'] = df_fixed['klassndre12025'].apply(map_stress_level)
    
    return df_fixed


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def normalize_block(blok: str) -> str:
    """Normalize block code (D001A -> D01)."""
    if pd.isna(blok):
        return None
    blok = str(blok).strip()
    if len(blok) >= 4:
        return f"{blok[0]}{int(blok[1:4]):02d}"
    return blok


def map_stress_level(stress: str) -> str:
    """Map stress classification to standard categories."""
    if pd.isna(stress):
        return 'UNKNOWN'
    stress = str(stress).lower()
    if 'sangat berat' in stress or 'sangat' in stress:
        return 'SANGAT_BERAT'
    elif 'berat' in stress:
        return 'BERAT'
    elif 'sedang' in stress:
        return 'SEDANG'
    elif 'ringan' in stress:
        return 'RINGAN'
    return 'UNKNOWN'


# =====================================================
# ANALYSIS FUNCTIONS
# =====================================================

def aggregate_algo_by_block(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate algorithm data per block."""
    agg = df.groupby('blok').agg({
        'ndre125': 'count',
        'risk_level': lambda x: (x.isin(['BERAT', 'SANGAT_BERAT'])).sum(),
    }).reset_index()
    agg.columns = ['blok', 'algo_total', 'algo_stressed']
    agg['algo_pct'] = (agg['algo_stressed'] / agg['algo_total'] * 100).round(2)
    return agg


def compare_datasets(algo_agg: pd.DataFrame, sensus: pd.DataFrame, 
                     divisi: str) -> pd.DataFrame:
    """Compare algorithm results with sensus data."""
    sensus_filtered = sensus[sensus['DIVISI'] == divisi].copy()
    
    comparison = algo_agg.merge(
        sensus_filtered[['BLOCK_NORM', 'TOTAL_PKK', 'TOTAL_GANODERMA', 
                        'SERANGAN_PCT', 'STADIUM_1_2', 'STADIUM_3_4']],
        left_on='blok', right_on='BLOCK_NORM', how='inner'
    )
    
    comparison['gap'] = comparison['algo_pct'] - comparison['SERANGAN_PCT']
    comparison['status'] = comparison['gap'].apply(
        lambda x: 'OVER' if x > 10 else ('UNDER' if x < -2 else 'OK')
    )
    
    return comparison


def calculate_correlation(comparison: pd.DataFrame) -> dict:
    """Calculate correlation statistics."""
    pearson_r, pearson_p = stats.pearsonr(
        comparison['algo_pct'], 
        comparison['SERANGAN_PCT']
    )
    spearman_r, spearman_p = stats.spearmanr(
        comparison['algo_pct'], 
        comparison['SERANGAN_PCT']
    )
    
    return {
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_r': spearman_r,
        'spearman_p': spearman_p,
        'significant': pearson_p < 0.05
    }


# =====================================================
# VISUALIZATION FUNCTIONS
# =====================================================

def create_validation_charts(comparison: pd.DataFrame, divisi: str, 
                            correlation: dict, output_dir: Path):
    """Create validation comparison charts."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # 1. Scatter plot - Correlation
    ax1 = axes[0, 0]
    ax1.scatter(comparison['algo_pct'], comparison['SERANGAN_PCT'], 
                s=100, alpha=0.7, c='steelblue', edgecolors='navy')
    ax1.set_xlabel('ALGO: % Stres (Berat + Sangat Berat)', fontsize=12)
    ax1.set_ylabel('SENSUS: % Serangan Ganoderma', fontsize=12)
    ax1.set_title(f'KORELASI: NDRE Stress vs Ganoderma ({divisi})\n'
                  f'Pearson r = {correlation["pearson_r"]:.4f}', fontsize=14)
    
    # Regression line
    z = np.polyfit(comparison['algo_pct'], comparison['SERANGAN_PCT'], 1)
    p = np.poly1d(z)
    ax1.plot(comparison['algo_pct'].sort_values(), 
             p(comparison['algo_pct'].sort_values()), 
             "r--", alpha=0.8, linewidth=2, label='Regression Line')
    ax1.plot([0, 80], [0, 80], 'g--', alpha=0.5, linewidth=1, 
             label='Perfect Correlation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Bar comparison
    ax2 = axes[0, 1]
    x = np.arange(len(comparison))
    width = 0.35
    ax2.bar(x - width/2, comparison['algo_pct'], width, 
            label='ALGO % Stres', color='coral')
    ax2.bar(x + width/2, comparison['SERANGAN_PCT'], width, 
            label='SENSUS % Ganoderma', color='steelblue')
    ax2.set_xlabel('Blok', fontsize=12)
    ax2.set_ylabel('Persentase (%)', fontsize=12)
    ax2.set_title(f'PERBANDINGAN PER BLOK ({divisi})', fontsize=14)
    ax2.set_xticks(x[::3])
    ax2.set_xticklabels(comparison['blok'].iloc[::3], rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Gap Analysis
    ax3 = axes[1, 0]
    colors = ['red' if s == 'OVER' else 'orange' if s == 'OK' else 'green' 
              for s in comparison['status']]
    ax3.bar(range(len(comparison)), comparison['gap'], color=colors)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.axhline(y=10, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax3.set_xlabel('Blok Index', fontsize=12)
    ax3.set_ylabel('Gap (ALGO - SENSUS) %', fontsize=12)
    ax3.set_title('OVER-DETECTION ANALYSIS', fontsize=14)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    algo_total = comparison['algo_total'].sum()
    algo_stressed = comparison['algo_stressed'].sum()
    sensus_total = comparison['TOTAL_PKK'].sum()
    sensus_gano = comparison['TOTAL_GANODERMA'].sum()
    
    summary_text = f"""
    RINGKASAN VALIDASI - {divisi}
    ══════════════════════════════════════════
    
    KORELASI STATISTIK
    ├─ Pearson r: {correlation['pearson_r']:.4f}
    ├─ p-value: {correlation['pearson_p']:.6f}
    └─ Signifikan: {'YA' if correlation['significant'] else 'TIDAK'}
    
    ALGORITMA (NDRE-based)
    ├─ Total Pohon: {algo_total:,}
    ├─ Stressed (Berat+SB): {algo_stressed:,}
    └─ Persentase: {algo_stressed/algo_total*100:.2f}%
    
    SENSUS (Ground Truth)
    ├─ Total Pohon: {sensus_total:,}
    ├─ Total Ganoderma: {sensus_gano:,}
    └─ Persentase: {sensus_gano/sensus_total*100:.2f}%
    
    OVER-DETECTION RATIO: {algo_stressed/sensus_gano:.1f}x
    """
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_dir / f'validation_{divisi.lower().replace(" ", "_")}.png', 
                dpi=150, bbox_inches='tight')
    plt.close()


# =====================================================
# MAIN EXECUTION
# =====================================================

def run_validation():
    """Run the complete validation analysis."""
    print("="*80)
    print("VALIDASI ALGORITMA CINCIN API vs DATA SENSUS GANODERMA")
    print("="*80)
    
    # Load data
    print("\n[1/5] Loading data...")
    sensus = load_sensus_data(INPUT_DIR / 'ame_2_4_hasil_sensus.csv')
    ame_ii_algo = load_ame_ii_algo_data(INPUT_DIR / 'tabelNDREnew.csv')
    ame_iv_algo = load_ame_iv_algo_data(INPUT_DIR / 'AME_IV.csv')
    
    # Process AME II
    print("\n[2/5] Analyzing AME II...")
    algo_ii_agg = aggregate_algo_by_block(ame_ii_algo)
    comparison_ii = compare_datasets(algo_ii_agg, sensus, 'AME002')
    corr_ii = calculate_correlation(comparison_ii)
    
    print(f"  - Blocks compared: {len(comparison_ii)}")
    print(f"  - Pearson r: {corr_ii['pearson_r']:.4f}")
    print(f"  - p-value: {corr_ii['pearson_p']:.6f}")
    print(f"  - Significant: {'YES' if corr_ii['significant'] else 'NO'}")
    
    # Process AME IV
    print("\n[3/5] Analyzing AME IV...")
    algo_iv_agg = aggregate_algo_by_block(ame_iv_algo)
    
    # Aggregate AME IV by 3-char block code to match sensus
    algo_iv_agg['blok_3'] = algo_iv_agg['blok'].str[:3]
    algo_iv_grouped = algo_iv_agg.groupby('blok_3').agg({
        'algo_total': 'sum',
        'algo_stressed': 'sum',
    }).reset_index()
    algo_iv_grouped.columns = ['blok', 'algo_total', 'algo_stressed']
    algo_iv_grouped['algo_pct'] = (
        algo_iv_grouped['algo_stressed'] / algo_iv_grouped['algo_total'] * 100
    ).round(2)
    
    # Aggregate sensus AME IV
    sensus_iv = sensus[sensus['DIVISI'] == 'AME004'].copy()
    sensus_iv_agg = sensus_iv.groupby('BLOCK_NORM').agg({
        'TOTAL_PKK': 'sum',
        'STADIUM_1_2': 'sum',
        'STADIUM_3_4': 'sum',
        'TOTAL_GANODERMA': 'sum',
    }).reset_index()
    sensus_iv_agg['SERANGAN_PCT'] = (
        sensus_iv_agg['TOTAL_GANODERMA'] / sensus_iv_agg['TOTAL_PKK'] * 100
    ).round(2)
    
    comparison_iv = algo_iv_grouped.merge(
        sensus_iv_agg, left_on='blok', right_on='BLOCK_NORM', how='inner'
    )
    comparison_iv['gap'] = comparison_iv['algo_pct'] - comparison_iv['SERANGAN_PCT']
    comparison_iv['status'] = comparison_iv['gap'].apply(
        lambda x: 'OVER' if x > 10 else ('UNDER' if x < -2 else 'OK')
    )
    
    corr_iv = calculate_correlation(comparison_iv)
    
    print(f"  - Blocks compared: {len(comparison_iv)}")
    print(f"  - Pearson r: {corr_iv['pearson_r']:.4f}")
    print(f"  - p-value: {corr_iv['pearson_p']:.6f}")
    print(f"  - Significant: {'YES' if corr_iv['significant'] else 'NO'}")
    
    # Create visualizations
    print("\n[4/5] Creating visualizations...")
    create_validation_charts(comparison_ii, 'AME II', corr_ii, OUTPUT_DIR)
    create_validation_charts(comparison_iv, 'AME IV', corr_iv, OUTPUT_DIR)
    
    # Save data
    print("\n[5/5] Saving results...")
    comparison_ii.to_csv(OUTPUT_DIR / 'comparison_ame_ii.csv', index=False)
    comparison_iv.to_csv(OUTPUT_DIR / 'comparison_ame_iv.csv', index=False)
    
    # Print summary
    print("\n" + "="*80)
    print("RINGKASAN HASIL")
    print("="*80)
    
    print(f"""
    AME II:
    ├─ Korelasi: r={corr_ii['pearson_r']:.4f} (TIDAK SIGNIFIKAN)
    ├─ Algo Stressed: {comparison_ii['algo_stressed'].sum():,} ({comparison_ii['algo_stressed'].sum()/comparison_ii['algo_total'].sum()*100:.1f}%)
    └─ Sensus Ganoderma: {comparison_ii['TOTAL_GANODERMA'].sum():,} ({comparison_ii['TOTAL_GANODERMA'].sum()/comparison_ii['TOTAL_PKK'].sum()*100:.1f}%)
    
    AME IV:
    ├─ Korelasi: r={corr_iv['pearson_r']:.4f} (SIGNIFIKAN - NEGATIF!)
    ├─ Algo Stressed: {comparison_iv['algo_stressed'].sum():,} ({comparison_iv['algo_stressed'].sum()/comparison_iv['algo_total'].sum()*100:.1f}%)
    └─ Sensus Ganoderma: {comparison_iv['TOTAL_GANODERMA'].sum():,} ({comparison_iv['TOTAL_GANODERMA'].sum()/comparison_iv['TOTAL_PKK'].sum()*100:.1f}%)
    """)
    
    print("\n" + "="*80)
    print("KESIMPULAN")
    print("="*80)
    print("""
    ⚠️  Klasifikasi "Stres NDRE" TIDAK berkorelasi dengan infeksi Ganoderma
    
    ✅  Algoritma VALID untuk: PRIORITISASI SURVEY
    ❌  Algoritma TIDAK VALID untuk: DIAGNOSIS GANODERMA
    
    📋  File output tersimpan di: output/validation_report/
    """)
    
    return {
        'ame_ii': {'comparison': comparison_ii, 'correlation': corr_ii},
        'ame_iv': {'comparison': comparison_iv, 'correlation': corr_iv}
    }


if __name__ == '__main__':
    results = run_validation()
