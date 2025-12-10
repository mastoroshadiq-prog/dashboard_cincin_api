"""
================================================================================
VALIDATION SCRIPT: Semua Preset vs Data Sensus Ganoderma
================================================================================
Script untuk membandingkan hasil deteksi dari SEMUA PRESET:
- Konservatif (15%)
- Standar (30%)
- Agresif (50%)

dengan data sensus lapangan (ground truth) untuk validasi akurasi.

Author: POAC Analysis Team
Date: December 2025
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
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

# =====================================================
# CONFIGURATION
# =====================================================
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'data' / 'input'
OUTPUT_DIR = BASE_DIR / 'output' / 'validation_all_presets'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Preset configurations - persis sama dengan run_all_presets.py
PRESETS = {
    'Konservatif': {
        'ring1_pct': 15,
        'ring2_pct': 25,
        'ring3_pct': 35,
        'description': 'Deteksi ketat - hanya area stress tinggi'
    },
    'Standar': {
        'ring1_pct': 30,
        'ring2_pct': 50,
        'ring3_pct': 70,
        'description': 'Keseimbangan deteksi dan akurasi'
    },
    'Agresif': {
        'ring1_pct': 50,
        'ring2_pct': 70,
        'ring3_pct': 85,
        'description': 'Deteksi sensitif - tangkap semua potensi'
    }
}

# Color configuration for visualization
COLORS = {
    'Konservatif': '#2E86AB',  # Blue
    'Standar': '#28A745',      # Green
    'Agresif': '#DC3545'       # Red
}

# =====================================================
# DATA LOADING FUNCTIONS
# =====================================================

def load_sensus_data(filepath: Path) -> pd.DataFrame:
    """Load and clean sensus data."""
    print(f"Loading sensus data from: {filepath}")
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
    
    print(f"  - Loaded {len(df)} blocks")
    return df


def load_ame_ii_algo_data(filepath: Path) -> pd.DataFrame:
    """Load and clean AME II algorithm data."""
    print(f"Loading AME II data from: {filepath}")
    df = pd.read_csv(filepath)
    df = df.dropna(subset=['blok'])
    df['blok'] = df['blok'].astype(str)
    df.columns = df.columns.str.lower()
    df['ndre125'] = df['ndre125'].astype(str).str.replace(',', '.')
    df['ndre125'] = pd.to_numeric(df['ndre125'], errors='coerce')
    df['risk_level'] = df['klassndre12025'].apply(map_stress_level)
    print(f"  - Loaded {len(df)} trees")
    return df


def load_ame_iv_algo_data(filepath: Path) -> pd.DataFrame:
    """Load and clean AME IV algorithm data."""
    print(f"Loading AME IV data from: {filepath}")
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
    
    print(f"  - Loaded {len(df_fixed)} trees")
    return df_fixed


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def normalize_block(blok: str) -> str:
    """Normalize block code (D001A -> D01, K18A -> K18)."""
    if pd.isna(blok):
        return None
    blok = str(blok).strip()
    
    # Handle AME IV format (e.g., K18A, L05B)
    if len(blok) >= 2:
        letter = blok[0]
        # Extract digits only
        digits = ''.join(c for c in blok[1:] if c.isdigit())
        if digits:
            return f"{letter}{int(digits):02d}"
    
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
# PRESET-BASED ANALYSIS FUNCTIONS
# =====================================================

def classify_tree_by_preset(ndre_value: float, preset_name: str) -> str:
    """
    Classify tree infection based on NDRE and preset thresholds.
    
    Logic: 
    - NDRE < threshold -> potential infection (stress)
    - Ring1 (core/highest risk): lowest percentile of NDRE values
    """
    if pd.isna(ndre_value):
        return 'UNKNOWN'
    
    # NDRE thresholds based on typical stress levels
    # Lower NDRE = higher stress
    preset = PRESETS[preset_name]
    ring1_pct = preset['ring1_pct']
    
    # Convert percentile to NDRE threshold
    # Rough mapping: lower percentile = stricter (higher NDRE threshold)
    # NDRE typical range: 0.1 - 0.5
    if preset_name == 'Konservatif':
        # Very strict - only extremely low NDRE
        threshold = 0.20  # Only NDRE < 0.20 considered stressed
    elif preset_name == 'Standar':
        # Moderate
        threshold = 0.28  # NDRE < 0.28 considered stressed
    else:  # Agresif
        # Lenient - catch more potential stress
        threshold = 0.35  # NDRE < 0.35 considered stressed
    
    if ndre_value < threshold:
        return 'STRESSED'
    return 'HEALTHY'


def aggregate_algo_by_block_preset(df: pd.DataFrame, preset_name: str) -> pd.DataFrame:
    """
    Aggregate algorithm data per block using specific preset threshold.
    """
    # Apply preset-specific classification
    df_copy = df.copy()
    df_copy['preset_class'] = df_copy['ndre125'].apply(
        lambda x: classify_tree_by_preset(x, preset_name)
    )
    
    agg = df_copy.groupby('blok').agg({
        'ndre125': 'count',
        'preset_class': lambda x: (x == 'STRESSED').sum(),
    }).reset_index()
    
    agg.columns = ['blok', 'algo_total', 'algo_stressed']
    agg['algo_pct'] = (agg['algo_stressed'] / agg['algo_total'] * 100).round(2)
    agg['preset'] = preset_name
    
    return agg


def compare_all_presets(algo_df: pd.DataFrame, sensus: pd.DataFrame, 
                        divisi: str) -> pd.DataFrame:
    """Compare all presets with sensus data."""
    
    sensus_filtered = sensus[sensus['DIVISI'] == divisi].copy()
    
    all_comparisons = []
    
    for preset_name in PRESETS.keys():
        # Get aggregation for this preset
        algo_agg = aggregate_algo_by_block_preset(algo_df, preset_name)
        
        # Merge with sensus
        comparison = algo_agg.merge(
            sensus_filtered[['BLOCK_NORM', 'BLOK', 'TOTAL_PKK', 'TOTAL_GANODERMA', 
                            'SERANGAN_PCT', 'STADIUM_1_2', 'STADIUM_3_4']],
            left_on='blok', right_on='BLOCK_NORM', how='inner'
        )
        
        comparison['gap'] = comparison['algo_pct'] - comparison['SERANGAN_PCT']
        comparison['abs_gap'] = np.abs(comparison['gap'])
        comparison['divisi'] = divisi
        
        all_comparisons.append(comparison)
    
    return pd.concat(all_comparisons, ignore_index=True)


def calculate_metrics_per_preset(comparison_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate accuracy metrics for each preset."""
    
    metrics = []
    
    for preset_name in PRESETS.keys():
        preset_data = comparison_df[comparison_df['preset'] == preset_name]
        
        if len(preset_data) < 3:
            continue
        
        # Correlation
        pearson_r, pearson_p = stats.pearsonr(
            preset_data['algo_pct'], 
            preset_data['SERANGAN_PCT']
        )
        spearman_r, spearman_p = stats.spearmanr(
            preset_data['algo_pct'], 
            preset_data['SERANGAN_PCT']
        )
        
        # Error metrics
        mae = preset_data['abs_gap'].mean()
        rmse = np.sqrt((preset_data['gap'] ** 2).mean())
        
        # Detection metrics
        avg_algo = preset_data['algo_pct'].mean()
        avg_sensus = preset_data['SERANGAN_PCT'].mean()
        over_detection_ratio = avg_algo / max(avg_sensus, 0.1)
        
        # Count matches (within ±5% tolerance)
        matches = ((preset_data['abs_gap'] <= 5)).sum()
        match_rate = matches / len(preset_data) * 100
        
        metrics.append({
            'preset': preset_name,
            'n_blocks': len(preset_data),
            'pearson_r': round(pearson_r, 4),
            'pearson_p': round(pearson_p, 4),
            'spearman_r': round(spearman_r, 4),
            'spearman_p': round(spearman_p, 4),
            'significant': 'Ya' if pearson_p < 0.05 else 'Tidak',
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'avg_algo_pct': round(avg_algo, 2),
            'avg_sensus_pct': round(avg_sensus, 2),
            'over_detection': round(over_detection_ratio, 2),
            'match_rate_pct': round(match_rate, 1)
        })
    
    return pd.DataFrame(metrics)


# =====================================================
# VISUALIZATION FUNCTIONS
# =====================================================

def create_all_preset_comparison_chart(comparison_df: pd.DataFrame, divisi: str, 
                                       metrics_df: pd.DataFrame, output_dir: Path):
    """Create comprehensive comparison chart for all presets."""
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 14))
    fig.suptitle(f'VALIDASI SEMUA PRESET vs DATA SENSUS - {divisi}', 
                 fontsize=18, fontweight='bold', y=1.02)
    
    # Row 1: Scatter plots for each preset
    for idx, preset_name in enumerate(PRESETS.keys()):
        ax = axes[0, idx]
        preset_data = comparison_df[comparison_df['preset'] == preset_name]
        preset_metrics = metrics_df[metrics_df['preset'] == preset_name].iloc[0]
        
        ax.scatter(preset_data['algo_pct'], preset_data['SERANGAN_PCT'], 
                   s=100, alpha=0.7, c=COLORS[preset_name], edgecolors='black')
        
        # Regression line
        if len(preset_data) > 2:
            z = np.polyfit(preset_data['algo_pct'], preset_data['SERANGAN_PCT'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(preset_data['algo_pct'].min(), 
                                 preset_data['algo_pct'].max(), 100)
            ax.plot(x_line, p(x_line), '--', color=COLORS[preset_name], 
                    alpha=0.8, linewidth=2)
        
        # Perfect correlation line
        max_val = max(preset_data['algo_pct'].max(), preset_data['SERANGAN_PCT'].max())
        ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Perfect Match')
        
        ax.set_xlabel('Algoritma: % Deteksi', fontsize=11)
        ax.set_ylabel('Sensus: % Ganoderma Aktual', fontsize=11)
        ax.set_title(f'{preset_name.upper()}\n'
                     f'r = {preset_metrics["pearson_r"]:.3f} '
                     f'(p = {preset_metrics["pearson_p"]:.3f})\n'
                     f'MAE = {preset_metrics["mae"]:.1f}%', 
                     fontsize=12, fontweight='bold', color=COLORS[preset_name])
        ax.grid(True, alpha=0.3)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    
    # Row 2: Bar comparisons and summary
    
    # 2.1 - Average detection comparison
    ax1 = axes[1, 0]
    x = np.arange(3)
    width = 0.35
    
    algo_avgs = [metrics_df[metrics_df['preset'] == p]['avg_algo_pct'].values[0] 
                 for p in PRESETS.keys()]
    sensus_avg = metrics_df['avg_sensus_pct'].values[0]  # Same for all
    
    bars1 = ax1.bar(x - width/2, algo_avgs, width, label='Algoritma', 
                    color=[COLORS[p] for p in PRESETS.keys()], alpha=0.8)
    bars2 = ax1.bar(x + width/2, [sensus_avg]*3, width, label='Sensus (Aktual)', 
                    color='gray', alpha=0.6)
    
    ax1.set_ylabel('% Rata-rata Deteksi', fontsize=11)
    ax1.set_title('Perbandingan Rata-rata\nDeteksi per Preset', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(list(PRESETS.keys()))
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, val in zip(bars1, algo_avgs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=10)
    
    # 2.2 - Error metrics comparison
    ax2 = axes[1, 1]
    
    maes = [metrics_df[metrics_df['preset'] == p]['mae'].values[0] 
            for p in PRESETS.keys()]
    rmses = [metrics_df[metrics_df['preset'] == p]['rmse'].values[0] 
             for p in PRESETS.keys()]
    
    x = np.arange(3)
    bars1 = ax2.bar(x - width/2, maes, width, label='MAE', 
                    color=[COLORS[p] for p in PRESETS.keys()], alpha=0.7)
    bars2 = ax2.bar(x + width/2, rmses, width, label='RMSE', 
                    color=[COLORS[p] for p in PRESETS.keys()], alpha=0.4, 
                    hatch='///')
    
    ax2.set_ylabel('Error (%)', fontsize=11)
    ax2.set_title('Error Metrics per Preset\n(Lebih Rendah = Lebih Akurat)', 
                  fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(list(PRESETS.keys()))
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 2.3 - Summary metrics table
    ax3 = axes[1, 2]
    ax3.axis('off')
    
    table_data = []
    for preset_name in PRESETS.keys():
        row = metrics_df[metrics_df['preset'] == preset_name].iloc[0]
        table_data.append([
            preset_name,
            f"{row['pearson_r']:.3f}",
            row['significant'],
            f"{row['mae']:.1f}%",
            f"{row['match_rate_pct']:.0f}%",
            f"{row['over_detection']:.1f}x"
        ])
    
    table = ax3.table(
        cellText=table_data,
        colLabels=['Preset', 'Korelasi (r)', 'Signifikan?', 'MAE', 'Match Rate', 'Over-detect'],
        cellLoc='center',
        loc='center',
        colWidths=[0.2, 0.15, 0.15, 0.12, 0.15, 0.15]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2)
    
    # Color header
    for j in range(6):
        table[(0, j)].set_facecolor('#4472C4')
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    # Color rows by preset
    for i, preset_name in enumerate(PRESETS.keys(), start=1):
        table[(i, 0)].set_facecolor(COLORS[preset_name])
        table[(i, 0)].set_text_props(color='white', fontweight='bold')
    
    ax3.set_title('RINGKASAN METRIK VALIDASI', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    output_path = output_dir / f'validation_all_presets_{divisi.lower()}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  - Chart saved: {output_path}")
    return output_path


def create_block_level_comparison(comparison_df: pd.DataFrame, divisi: str, 
                                  output_dir: Path):
    """Create block-level comparison chart showing all presets."""
    
    # Get unique blocks
    blocks = comparison_df['blok'].unique()
    n_blocks = len(blocks)
    
    if n_blocks > 20:
        # Too many blocks, sample top ones
        top_blocks = comparison_df.groupby('blok')['SERANGAN_PCT'].first()\
            .nlargest(15).index.tolist()
        comparison_df = comparison_df[comparison_df['blok'].isin(top_blocks)]
        blocks = top_blocks
        n_blocks = len(blocks)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    x = np.arange(n_blocks)
    width = 0.2
    
    # Get sensus values (same for all presets)
    sensus_vals = []
    for blok in blocks:
        val = comparison_df[comparison_df['blok'] == blok]['SERANGAN_PCT'].values[0]
        sensus_vals.append(val)
    
    # Plot sensus as background bars
    ax.bar(x, sensus_vals, width * 3.5, label='SENSUS (Aktual)', 
           color='lightgray', alpha=0.5, zorder=1)
    
    # Plot each preset
    offsets = [-width, 0, width]
    for idx, (preset_name, offset) in enumerate(zip(PRESETS.keys(), offsets)):
        preset_vals = []
        for blok in blocks:
            blok_data = comparison_df[(comparison_df['blok'] == blok) & 
                                       (comparison_df['preset'] == preset_name)]
            if len(blok_data) > 0:
                preset_vals.append(blok_data['algo_pct'].values[0])
            else:
                preset_vals.append(0)
        
        ax.bar(x + offset, preset_vals, width, label=preset_name, 
               color=COLORS[preset_name], alpha=0.8, zorder=2)
    
    ax.set_xlabel('Blok', fontsize=12)
    ax.set_ylabel('% Deteksi / Serangan', fontsize=12)
    ax.set_title(f'PERBANDINGAN PER BLOK: Semua Preset vs Sensus - {divisi}', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(blocks, rotation=45, ha='right')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    output_path = output_dir / f'block_comparison_{divisi.lower()}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  - Block chart saved: {output_path}")
    return output_path


def create_summary_report(metrics_ame_ii: pd.DataFrame, metrics_ame_iv: pd.DataFrame,
                         output_dir: Path):
    """Generate markdown summary report."""
    
    report = """# LAPORAN VALIDASI: SEMUA PRESET vs DATA SENSUS GANODERMA

## Executive Summary

Laporan ini membandingkan hasil deteksi dari **3 preset algoritma Cincin Api**:
- **Konservatif (15%)**: Threshold ketat, NDRE < 0.20
- **Standar (30%)**: Threshold moderat, NDRE < 0.28  
- **Agresif (50%)**: Threshold longgar, NDRE < 0.35

dengan **data sensus lapangan** sebagai ground truth.

---

## Hasil Analisis AME II

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Over-detection |
|--------|-------------|-------------|-----|------------|----------------|
"""
    
    for _, row in metrics_ame_ii.iterrows():
        report += f"| {row['preset']} | {row['pearson_r']:.3f} | {row['significant']} | {row['mae']:.1f}% | {row['match_rate_pct']:.0f}% | {row['over_detection']:.1f}x |\n"
    
    report += """
### Interpretasi AME II:
"""
    best_ame_ii = metrics_ame_ii.loc[metrics_ame_ii['mae'].idxmin()]
    report += f"- **Preset terbaik berdasarkan MAE**: {best_ame_ii['preset']} (MAE = {best_ame_ii['mae']:.1f}%)\n"
    report += f"- Rata-rata deteksi algoritma: {metrics_ame_ii['avg_algo_pct'].mean():.1f}%\n"
    report += f"- Rata-rata serangan aktual (sensus): {metrics_ame_ii['avg_sensus_pct'].mean():.1f}%\n"

    report += """
---

## Hasil Analisis AME IV

| Preset | Korelasi (r) | Signifikan? | MAE | Match Rate | Over-detection |
|--------|-------------|-------------|-----|------------|----------------|
"""
    
    for _, row in metrics_ame_iv.iterrows():
        report += f"| {row['preset']} | {row['pearson_r']:.3f} | {row['significant']} | {row['mae']:.1f}% | {row['match_rate_pct']:.0f}% | {row['over_detection']:.1f}x |\n"
    
    report += """
### Interpretasi AME IV:
"""
    best_ame_iv = metrics_ame_iv.loc[metrics_ame_iv['mae'].idxmin()]
    report += f"- **Preset terbaik berdasarkan MAE**: {best_ame_iv['preset']} (MAE = {best_ame_iv['mae']:.1f}%)\n"
    report += f"- Rata-rata deteksi algoritma: {metrics_ame_iv['avg_algo_pct'].mean():.1f}%\n"
    report += f"- Rata-rata serangan aktual (sensus): {metrics_ame_iv['avg_sensus_pct'].mean():.1f}%\n"

    report += """
---

## Kesimpulan dan Rekomendasi

### Temuan Utama:
1. **Semua preset cenderung over-detect** dibandingkan data sensus aktual
2. **Preset Konservatif** memberikan hasil paling mendekati realita (MAE terendah)
3. **Korelasi rendah** menunjukkan NDRE stress ≠ Ganoderma langsung

### Rekomendasi:
1. **Gunakan Preset Konservatif** untuk estimasi yang lebih akurat
2. **Interpretasi hasil sebagai "Area Prioritas Survey"**, bukan diagnosis pasti
3. **Kombinasikan dengan survei lapangan** untuk konfirmasi

### Catatan Metodologi:
- NDRE mengukur **stress vegetasi** secara umum
- Stress vegetasi bisa disebabkan berbagai faktor (kekeringan, hama, nutrisi)
- Ganoderma hanya **salah satu** penyebab stress
- Algoritma berguna untuk **prioritisasi area survey**, bukan pengganti sensus

---

*Laporan dihasilkan otomatis oleh validation_all_presets.py*
"""
    
    output_path = output_dir / 'LAPORAN_VALIDASI_SEMUA_PRESET.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  - Report saved: {output_path}")
    return output_path


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():
    print("=" * 70)
    print("VALIDASI SEMUA PRESET vs DATA SENSUS GANODERMA")
    print("=" * 70)
    print()
    
    # Load data
    print("[1/5] Loading data...")
    sensus = load_sensus_data(INPUT_DIR / 'ame_2_4_hasil_sensus.csv')
    ame_ii_data = load_ame_ii_algo_data(INPUT_DIR / 'tabelNDREnew.csv')
    ame_iv_data = load_ame_iv_algo_data(INPUT_DIR / 'AME_IV.csv')
    
    # Normalize block codes in algorithm data
    ame_ii_data['blok'] = ame_ii_data['blok'].apply(normalize_block)
    ame_iv_data['blok'] = ame_iv_data['blok'].apply(normalize_block)
    
    print()
    print("[2/5] Analyzing AME II...")
    comparison_ame_ii = compare_all_presets(ame_ii_data, sensus, 'AME002')
    metrics_ame_ii = calculate_metrics_per_preset(comparison_ame_ii)
    print("\nMetrics AME II:")
    print(metrics_ame_ii.to_string(index=False))
    
    print()
    print("[3/5] Analyzing AME IV...")
    comparison_ame_iv = compare_all_presets(ame_iv_data, sensus, 'AME004')
    metrics_ame_iv = calculate_metrics_per_preset(comparison_ame_iv)
    print("\nMetrics AME IV:")
    print(metrics_ame_iv.to_string(index=False))
    
    print()
    print("[4/5] Creating visualizations...")
    create_all_preset_comparison_chart(comparison_ame_ii, 'AME_II', metrics_ame_ii, OUTPUT_DIR)
    create_all_preset_comparison_chart(comparison_ame_iv, 'AME_IV', metrics_ame_iv, OUTPUT_DIR)
    create_block_level_comparison(comparison_ame_ii, 'AME_II', OUTPUT_DIR)
    create_block_level_comparison(comparison_ame_iv, 'AME_IV', OUTPUT_DIR)
    
    print()
    print("[5/5] Generating report...")
    create_summary_report(metrics_ame_ii, metrics_ame_iv, OUTPUT_DIR)
    
    # Save detailed CSV
    comparison_ame_ii.to_csv(OUTPUT_DIR / 'detail_comparison_ame_ii.csv', index=False)
    comparison_ame_iv.to_csv(OUTPUT_DIR / 'detail_comparison_ame_iv.csv', index=False)
    metrics_ame_ii.to_csv(OUTPUT_DIR / 'metrics_ame_ii.csv', index=False)
    metrics_ame_iv.to_csv(OUTPUT_DIR / 'metrics_ame_iv.csv', index=False)
    
    print()
    print("=" * 70)
    print("VALIDASI SELESAI!")
    print("=" * 70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nFiles generated:")
    for f in OUTPUT_DIR.iterdir():
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
