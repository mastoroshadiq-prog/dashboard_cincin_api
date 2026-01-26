"""
================================================================================
VALIDATION SCRIPT: Metode Adaptif vs Data Sensus Ganoderma
================================================================================
Membandingkan hasil 3 metode adaptif dengan data sensus lapangan.

Metode yang divalidasi:
1. Age-Based Preset Selection
2. Ensemble Scoring + Age Weight
3. Ensemble Scoring Pure

Output:
- Korelasi Pearson & Spearman
- Match rate (toleransi ±5%)
- Error metrics (MAE, RMSE)
- Perbandingan visual
================================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Import dari modul lokal
from src.ingestion import load_and_clean_data, load_ame_iv_data, validate_data_integrity
from src.clustering import run_cincin_api_algorithm
from src.adaptive_detection import (
    run_all_adaptive_methods, 
    AGE_BASED_CONFIG, 
    ENSEMBLE_CONFIG,
    PRESET_NAMES
)
from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS

# Paths
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'data' / 'input'
OUTPUT_DIR = BASE_DIR / 'data' / 'output' / 'validation_adaptive'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color scheme for methods
METHOD_COLORS = {
    'age_based': '#9b59b6',      # Purple
    'ensemble_age': '#e67e22',   # Orange
    'ensemble_pure': '#1abc9c',  # Teal
    'konservatif': '#3498db',    # Blue
    'standar': '#27ae60',        # Green
    'agresif': '#e74c3c',        # Red
}

METHOD_NAMES = {
    'age_based': 'Age-Based Selection',
    'ensemble_age': 'Ensemble + Age Weight',
    'ensemble_pure': 'Ensemble Pure (Voting)',
    'konservatif': 'Konservatif',
    'standar': 'Standar',
    'agresif': 'Agresif',
}

# =============================================================================
# DATA LOADING
# =============================================================================

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


def normalize_block(blok: str) -> str:
    """Normalize block code (D001A -> D01)."""
    if pd.isna(blok):
        return None
    blok = str(blok).strip()
    
    if len(blok) >= 2:
        letter = blok[0]
        digits = ''.join(c for c in blok[1:] if c.isdigit())
        if digits:
            return f"{letter}{int(digits):02d}"
    
    return blok


# =============================================================================
# AGGREGATE RESULTS BY BLOCK
# =============================================================================

def aggregate_preset_results(all_results: dict, preset_name: str) -> pd.DataFrame:
    """Aggregate preset results by block."""
    df = all_results[preset_name]['df']
    
    # Count detected trees per block
    detected = df[df['Status_Risiko'].isin([
        'MERAH (KLUSTER AKTIF)', 
        'ORANYE (CINCIN API)', 
        'KUNING (SUSPECT TERISOLASI)'
    ])].groupby('Blok').size()
    
    total = df.groupby('Blok').size()
    
    result = pd.DataFrame({
        'Blok': total.index,
        'total_trees': total.values,
        'detected_trees': detected.reindex(total.index).fillna(0).astype(int).values
    })
    result['detected_pct'] = (result['detected_trees'] / result['total_trees'] * 100).round(2)
    result['method'] = preset_name
    result['BLOCK_NORM'] = result['Blok'].apply(normalize_block)
    
    return result


def aggregate_adaptive_results(adaptive_results: dict, method_name: str) -> pd.DataFrame:
    """Aggregate adaptive method results by block."""
    df = adaptive_results[method_name]['df']
    
    if method_name in ['ensemble_age', 'ensemble_pure']:
        # For ensemble methods, use confidence level
        high_conf = df[df['Confidence_Level'] == 'HIGH'].groupby('Blok').size()
        medium_conf = df[df['Confidence_Level'] == 'MEDIUM'].groupby('Blok').size()
        low_conf = df[df['Confidence_Level'] == 'LOW'].groupby('Blok').size()
        total = df.groupby('Blok').size()
        
        # Count detected as any non-NONE
        detected = df[df['Confidence_Level'] != 'NONE'].groupby('Blok').size()
        
        result = pd.DataFrame({
            'Blok': total.index,
            'total_trees': total.values,
            'detected_trees': detected.reindex(total.index).fillna(0).astype(int).values,
            'high_conf': high_conf.reindex(total.index).fillna(0).astype(int).values,
            'medium_conf': medium_conf.reindex(total.index).fillna(0).astype(int).values,
            'low_conf': low_conf.reindex(total.index).fillna(0).astype(int).values,
        })
    else:
        # For age-based, use Status_Risiko
        detected = df[df['Status_Risiko'].isin([
            'MERAH (KLUSTER AKTIF)', 
            'ORANYE (CINCIN API)', 
            'KUNING (SUSPECT TERISOLASI)'
        ])].groupby('Blok').size()
        
        total = df.groupby('Blok').size()
        
        result = pd.DataFrame({
            'Blok': total.index,
            'total_trees': total.values,
            'detected_trees': detected.reindex(total.index).fillna(0).astype(int).values,
        })
    
    result['detected_pct'] = (result['detected_trees'] / result['total_trees'] * 100).round(2)
    result['method'] = method_name
    result['BLOCK_NORM'] = result['Blok'].apply(normalize_block)
    
    return result


# =============================================================================
# METRICS CALCULATION
# =============================================================================

def calculate_metrics(comparison_df: pd.DataFrame, method_name: str) -> dict:
    """Calculate validation metrics for a method."""
    data = comparison_df[comparison_df['method'] == method_name].copy()
    
    if len(data) < 3:
        return None
    
    # Correlation
    try:
        pearson_r, pearson_p = stats.pearsonr(data['detected_pct'], data['SERANGAN_PCT'])
        spearman_r, spearman_p = stats.spearmanr(data['detected_pct'], data['SERANGAN_PCT'])
    except:
        pearson_r = pearson_p = spearman_r = spearman_p = np.nan
    
    # Error metrics
    data['gap'] = data['detected_pct'] - data['SERANGAN_PCT']
    data['abs_gap'] = data['gap'].abs()
    
    mae = data['abs_gap'].mean()
    rmse = np.sqrt((data['gap'] ** 2).mean())
    
    # Detection metrics
    avg_algo = data['detected_pct'].mean()
    avg_sensus = data['SERANGAN_PCT'].mean()
    over_detection = avg_algo / max(avg_sensus, 0.1)
    
    # Match rate (within ±5%)
    matches = (data['abs_gap'] <= 5).sum()
    match_rate = matches / len(data) * 100
    
    # Close matches (within ±2%)
    close_matches = (data['abs_gap'] <= 2).sum()
    close_match_rate = close_matches / len(data) * 100
    
    return {
        'method': method_name,
        'method_display': METHOD_NAMES.get(method_name, method_name),
        'n_blocks': len(data),
        'pearson_r': round(pearson_r, 4),
        'pearson_p': round(pearson_p, 4),
        'spearman_r': round(spearman_r, 4),
        'spearman_p': round(spearman_p, 4),
        'significant': 'Ya' if pearson_p < 0.05 else 'Tidak',
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'avg_algo_pct': round(avg_algo, 2),
        'avg_sensus_pct': round(avg_sensus, 2),
        'over_detection': round(over_detection, 2),
        'match_rate_5pct': round(match_rate, 1),
        'match_rate_2pct': round(close_match_rate, 1),
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_validation_charts(comparison_df: pd.DataFrame, metrics_df: pd.DataFrame, 
                            divisi: str, output_dir: Path):
    """Create validation visualization charts."""
    print(f"\n📊 Creating validation charts for {divisi}...")
    
    methods = comparison_df['method'].unique()
    
    # 1. Correlation Scatter Plot
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, method in enumerate(methods):
        if idx >= 6:
            break
        ax = axes[idx]
        data = comparison_df[comparison_df['method'] == method]
        
        color = METHOD_COLORS.get(method, '#333333')
        ax.scatter(data['SERANGAN_PCT'], data['detected_pct'], 
                  c=color, alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
        
        # Regression line
        if len(data) >= 3:
            z = np.polyfit(data['SERANGAN_PCT'], data['detected_pct'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(0, data['SERANGAN_PCT'].max() * 1.1, 100)
            ax.plot(x_line, p(x_line), '--', color=color, alpha=0.8, linewidth=2)
        
        # Perfect line
        max_val = max(data['SERANGAN_PCT'].max(), data['detected_pct'].max()) * 1.1
        ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Perfect Match')
        
        # Get metrics
        metric = metrics_df[metrics_df['method'] == method].iloc[0] if len(metrics_df[metrics_df['method'] == method]) > 0 else None
        
        title = METHOD_NAMES.get(method, method)
        if metric is not None:
            ax.set_title(f"{title}\nr={metric['pearson_r']:.3f}, p={metric['pearson_p']:.4f}", 
                        fontsize=11, fontweight='bold')
        else:
            ax.set_title(title, fontsize=11, fontweight='bold')
        
        ax.set_xlabel('Sensus Serangan (%)')
        ax.set_ylabel('Deteksi Algoritma (%)')
        ax.grid(True, alpha=0.3)
    
    # Hide unused axes
    for idx in range(len(methods), 6):
        axes[idx].set_visible(False)
    
    plt.suptitle(f'Korelasi Deteksi vs Sensus - {divisi}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(output_dir / f'correlation_scatter_{divisi.replace(" ", "_")}.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✅ Saved: correlation_scatter_{divisi.replace(' ', '_')}.png")
    
    # 2. Metrics Comparison Bar Chart
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    metrics_plot = metrics_df.copy()
    x = np.arange(len(metrics_plot))
    colors = [METHOD_COLORS.get(m, '#333') for m in metrics_plot['method']]
    
    # Pearson R
    ax = axes[0, 0]
    bars = ax.bar(x, metrics_plot['pearson_r'], color=colors, alpha=0.8)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_ylabel('Pearson r')
    ax.set_title('Korelasi dengan Data Sensus', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_NAMES.get(m, m) for m in metrics_plot['method']], rotation=45, ha='right')
    for bar, val in zip(bars, metrics_plot['pearson_r']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    
    # MAE
    ax = axes[0, 1]
    bars = ax.bar(x, metrics_plot['mae'], color=colors, alpha=0.8)
    ax.set_ylabel('MAE (%)')
    ax.set_title('Mean Absolute Error (lebih rendah = lebih baik)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_NAMES.get(m, m) for m in metrics_plot['method']], rotation=45, ha='right')
    for bar, val in zip(bars, metrics_plot['mae']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    
    # Match Rate
    ax = axes[1, 0]
    bars = ax.bar(x, metrics_plot['match_rate_5pct'], color=colors, alpha=0.8)
    ax.set_ylabel('Match Rate (%)')
    ax.set_title('Blok dengan Gap ≤5% (lebih tinggi = lebih baik)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_NAMES.get(m, m) for m in metrics_plot['method']], rotation=45, ha='right')
    for bar, val in zip(bars, metrics_plot['match_rate_5pct']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{val:.0f}%', ha='center', va='bottom', fontsize=9)
    
    # Over Detection Ratio
    ax = axes[1, 1]
    bars = ax.bar(x, metrics_plot['over_detection'], color=colors, alpha=0.8)
    ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.7, label='Ideal (1.0)')
    ax.set_ylabel('Ratio')
    ax.set_title('Over-Detection Ratio (1.0 = sempurna)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_NAMES.get(m, m) for m in metrics_plot['method']], rotation=45, ha='right')
    ax.legend()
    for bar, val in zip(bars, metrics_plot['over_detection']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{val:.2f}x', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle(f'Perbandingan Metrik Validasi - {divisi}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(output_dir / f'metrics_comparison_{divisi.replace(" ", "_")}.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✅ Saved: metrics_comparison_{divisi.replace(' ', '_')}.png")


def create_summary_report(all_metrics: dict, output_dir: Path):
    """Generate summary markdown and HTML reports."""
    
    # Generate HTML Report
    html_path = create_html_report(all_metrics, output_dir)
    
    # Generate Markdown Report (existing code)
    report = []
    report.append("# 📊 Validasi Metode Adaptif vs Data Sensus Ganoderma\n")
    report.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    
    report.append("## Ringkasan Eksekutif\n\n")
    
    for divisi, metrics_df in all_metrics.items():
        report.append(f"### {divisi}\n\n")
        
        # Best method by correlation
        best_corr = metrics_df.loc[metrics_df['pearson_r'].idxmax()]
        report.append(f"- **Korelasi Tertinggi:** {best_corr['method_display']} (r={best_corr['pearson_r']:.3f})\n")
        
        # Best method by MAE
        best_mae = metrics_df.loc[metrics_df['mae'].idxmin()]
        report.append(f"- **Error Terendah:** {best_mae['method_display']} (MAE={best_mae['mae']:.2f}%)\n")
        
        # Best method by match rate
        best_match = metrics_df.loc[metrics_df['match_rate_5pct'].idxmax()]
        report.append(f"- **Match Rate Tertinggi:** {best_match['method_display']} ({best_match['match_rate_5pct']:.0f}%)\n")
        
        # Closest to 1.0 over-detection
        metrics_df['od_distance'] = (metrics_df['over_detection'] - 1.0).abs()
        best_od = metrics_df.loc[metrics_df['od_distance'].idxmin()]
        report.append(f"- **Paling Akurat:** {best_od['method_display']} (Rasio={best_od['over_detection']:.2f}x)\n\n")
        
        # Full table
        report.append("#### Tabel Metrik Lengkap\n\n")
        report.append("| Metode | r | p-value | Signifikan | MAE | Match Rate | Over-Det |\n")
        report.append("|--------|---|---------|------------|-----|------------|----------|\n")
        
        for _, row in metrics_df.iterrows():
            report.append(f"| {row['method_display']} | {row['pearson_r']:.3f} | {row['pearson_p']:.4f} | "
                         f"{row['significant']} | {row['mae']:.1f}% | {row['match_rate_5pct']:.0f}% | "
                         f"{row['over_detection']:.2f}x |\n")
        
        report.append("\n")
    
    report.append("## Interpretasi\n\n")
    report.append("- **Pearson r:** Korelasi linear (-1 sampai +1). Nilai positif tinggi = deteksi sejalan dengan sensus.\n")
    report.append("- **p-value:** Signifikansi statistik. <0.05 = signifikan.\n")
    report.append("- **MAE:** Mean Absolute Error. Rata-rata selisih absolut.\n")
    report.append("- **Match Rate:** Persentase blok dengan gap ≤5%.\n")
    report.append("- **Over-Detection:** Rasio deteksi/sensus. 1.0 = sempurna, >1 = over-detect, <1 = under-detect.\n")
    
    report_path = output_dir / 'validation_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.writelines(report)
    
    print(f"\n📄 Report saved: {report_path}")
    print(f"📄 HTML Report saved: {html_path}")
    return report_path


def create_html_report(all_metrics: dict, output_dir: Path) -> Path:
    """Generate beautiful HTML validation report."""
    
    timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
    
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔬 Validasi Metode Adaptif - POAC v3.3</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e8e8e8;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            padding: 30px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        header p {{
            color: #aaa;
        }}
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #f39c12;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(243, 156, 18, 0.3);
        }}
        .section h3 {{
            color: #3498db;
            margin: 20px 0 15px 0;
        }}
        .highlights {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}
        .highlight-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
        }}
        .highlight-card .label {{
            font-size: 0.85em;
            color: #888;
            margin-bottom: 5px;
        }}
        .highlight-card .value {{
            font-size: 1.3em;
            font-weight: bold;
            color: #27ae60;
        }}
        .highlight-card .method {{
            font-size: 0.9em;
            color: #aaa;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{
            background: rgba(52, 152, 219, 0.3);
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        .method-name {{
            text-align: left;
            font-weight: 500;
        }}
        .good {{ color: #27ae60; font-weight: bold; }}
        .medium {{ color: #f39c12; font-weight: bold; }}
        .bad {{ color: #e74c3c; font-weight: bold; }}
        .preset {{ 
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .preset.konservatif {{ background: rgba(52, 152, 219, 0.3); }}
        .preset.standar {{ background: rgba(39, 174, 96, 0.3); }}
        .preset.agresif {{ background: rgba(231, 76, 60, 0.3); }}
        .preset.adaptive {{ background: rgba(155, 89, 182, 0.3); }}
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}
        .viz-item {{
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            overflow: hidden;
        }}
        .viz-item img {{
            width: 100%;
            height: auto;
        }}
        .interpretation {{
            background: rgba(52, 152, 219, 0.1);
            border-left: 4px solid #3498db;
            padding: 15px 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .interpretation h4 {{
            margin-bottom: 10px;
            color: #3498db;
        }}
        .interpretation ul {{
            padding-left: 20px;
        }}
        .interpretation li {{
            margin: 8px 0;
            color: #ccc;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: bold;
        }}
        .badge.yes {{ background: #27ae60; color: white; }}
        .badge.no {{ background: #7f8c8d; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔬 Validasi Metode Adaptif</h1>
            <p>POAC v3.3 - Perbandingan Hasil Algoritma dengan Data Sensus Lapangan</p>
            <p style="margin-top: 10px; color: #666;">Generated: {timestamp}</p>
        </header>
'''
    
    for divisi, metrics_df in all_metrics.items():
        # Calculate best methods
        best_corr = metrics_df.loc[metrics_df['pearson_r'].idxmax()]
        best_mae = metrics_df.loc[metrics_df['mae'].idxmin()]
        best_match = metrics_df.loc[metrics_df['match_rate_5pct'].idxmax()]
        metrics_df['od_distance'] = (metrics_df['over_detection'] - 1.0).abs()
        best_od = metrics_df.loc[metrics_df['od_distance'].idxmin()]
        
        html += f'''
        <div class="section">
            <h2>📍 {divisi}</h2>
            
            <div class="highlights">
                <div class="highlight-card">
                    <div class="label">Korelasi Tertinggi</div>
                    <div class="value">r = {best_corr['pearson_r']:.3f}</div>
                    <div class="method">{best_corr['method_display']}</div>
                </div>
                <div class="highlight-card">
                    <div class="label">Error Terendah</div>
                    <div class="value">MAE = {best_mae['mae']:.1f}%</div>
                    <div class="method">{best_mae['method_display']}</div>
                </div>
                <div class="highlight-card">
                    <div class="label">Match Rate Tertinggi</div>
                    <div class="value">{best_match['match_rate_5pct']:.0f}%</div>
                    <div class="method">{best_match['method_display']}</div>
                </div>
                <div class="highlight-card">
                    <div class="label">Paling Akurat</div>
                    <div class="value">{best_od['over_detection']:.2f}x</div>
                    <div class="method">{best_od['method_display']}</div>
                </div>
            </div>
            
            <h3>📊 Tabel Metrik Lengkap</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metode</th>
                        <th>Korelasi (r)</th>
                        <th>p-value</th>
                        <th>Signifikan?</th>
                        <th>MAE</th>
                        <th>Match Rate</th>
                        <th>Over-Detection</th>
                        <th>Avg Deteksi</th>
                        <th>Avg Sensus</th>
                    </tr>
                </thead>
                <tbody>
'''
        
        for _, row in metrics_df.iterrows():
            # Determine color classes
            r_class = 'good' if row['pearson_r'] > 0.3 else ('medium' if row['pearson_r'] > 0 else 'bad')
            mae_class = 'good' if row['mae'] < 10 else ('medium' if row['mae'] < 20 else 'bad')
            match_class = 'good' if row['match_rate_5pct'] > 50 else ('medium' if row['match_rate_5pct'] > 30 else 'bad')
            od_class = 'good' if 0.5 <= row['over_detection'] <= 2 else 'bad'
            sig_badge = 'yes' if row['significant'] == 'Ya' else 'no'
            
            # Determine method type for styling
            method_type = 'adaptive' if row['method'] in ['age_based', 'ensemble_age', 'ensemble_pure'] else row['method']
            
            html += f'''
                    <tr>
                        <td class="method-name"><span class="preset {method_type}">{row['method_display']}</span></td>
                        <td class="{r_class}">{row['pearson_r']:.3f}</td>
                        <td>{row['pearson_p']:.4f}</td>
                        <td><span class="badge {sig_badge}">{row['significant']}</span></td>
                        <td class="{mae_class}">{row['mae']:.1f}%</td>
                        <td class="{match_class}">{row['match_rate_5pct']:.0f}%</td>
                        <td class="{od_class}">{row['over_detection']:.2f}x</td>
                        <td>{row['avg_algo_pct']:.1f}%</td>
                        <td>{row['avg_sensus_pct']:.1f}%</td>
                    </tr>
'''
        
        html += f'''
                </tbody>
            </table>
            
            <h3>📈 Visualisasi</h3>
            <div class="viz-grid">
                <div class="viz-item">
                    <img src="correlation_scatter_{divisi.replace(' ', '_')}.png" alt="Correlation Scatter">
                </div>
                <div class="viz-item">
                    <img src="metrics_comparison_{divisi.replace(' ', '_')}.png" alt="Metrics Comparison">
                </div>
            </div>
        </div>
'''
    
    html += '''
        <div class="section">
            <h2>📖 Interpretasi Hasil</h2>
            <div class="interpretation">
                <h4>Panduan Membaca Metrik:</h4>
                <ul>
                    <li><strong>Pearson r:</strong> Korelasi linear antara deteksi dan sensus (-1 hingga +1). Nilai positif tinggi menunjukkan deteksi sejalan dengan data sensus.</li>
                    <li><strong>p-value:</strong> Signifikansi statistik. Nilai < 0.05 berarti korelasi signifikan secara statistik.</li>
                    <li><strong>MAE (Mean Absolute Error):</strong> Rata-rata selisih absolut. Semakin rendah semakin baik.</li>
                    <li><strong>Match Rate:</strong> Persentase blok dengan selisih ≤ 5%. Semakin tinggi semakin baik.</li>
                    <li><strong>Over-Detection:</strong> Rasio rata-rata deteksi terhadap sensus. 1.0 = sempurna, > 1 = over-detect, < 1 = under-detect.</li>
                </ul>
            </div>
            
            <div class="interpretation" style="border-left-color: #9b59b6; background: rgba(155, 89, 182, 0.1); margin-top: 15px;">
                <h4 style="color: #9b59b6;">Metode Adaptif:</h4>
                <ul>
                    <li><strong>Age-Based Selection:</strong> Memilih preset berdasarkan umur blok. Efektif jika pola serangan berkorelasi dengan umur.</li>
                    <li><strong>Ensemble + Age Weight:</strong> Kombinasi 3 preset dengan bobot sesuai umur. Memberikan fleksibilitas tinggi.</li>
                    <li><strong>Ensemble Pure:</strong> Voting murni tanpa faktor umur. Mengukur konsensus antara preset.</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    html_path = output_dir / 'validation_report.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html_path



# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_validation_for_divisi(divisi_name: str, df_ndre: pd.DataFrame, 
                              sensus_df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """Run full validation for a single divisi."""
    print(f"\n{'='*60}")
    print(f"🔄 VALIDASI: {divisi_name}")
    print('='*60)
    
    # Filter sensus for this divisi
    divisi_code = 'AME002' if 'II' in divisi_name else 'AME004'
    sensus = sensus_df[sensus_df['DIVISI'] == divisi_code].copy()
    print(f"  Sensus blocks: {len(sensus)}")
    
    # Run all presets
    print(f"\n📍 Running preset analysis...")
    all_results = {}
    for preset_name in PRESET_NAMES:
        preset_config = CINCIN_API_PRESETS.get(preset_name, {})
        final_config = {**CINCIN_API_CONFIG, **preset_config}
        
        df_classified, metadata = run_cincin_api_algorithm(
            df_ndre.copy(),
            auto_tune=True,
            manual_threshold=None,
            config_override=final_config
        )
        
        all_results[preset_name] = {
            'df': df_classified,
            'metadata': metadata
        }
        print(f"  ✅ {preset_name}: {metadata['merah_count']} MERAH")
    
    # Run adaptive methods
    print(f"\n📍 Running adaptive methods...")
    adaptive_results = run_all_adaptive_methods(all_results, df_ndre)
    
    # Aggregate results by block
    print(f"\n📍 Aggregating results by block...")
    all_aggregated = []
    
    # Presets
    for preset_name in PRESET_NAMES:
        agg = aggregate_preset_results(all_results, preset_name)
        all_aggregated.append(agg)
    
    # Adaptive methods
    for method_name in ['age_based', 'ensemble_age', 'ensemble_pure']:
        agg = aggregate_adaptive_results(adaptive_results, method_name)
        all_aggregated.append(agg)
    
    agg_df = pd.concat(all_aggregated, ignore_index=True)
    
    # Merge with sensus
    comparison_df = agg_df.merge(
        sensus[['BLOCK_NORM', 'SERANGAN_PCT', 'TOTAL_GANODERMA', 'TT']],
        on='BLOCK_NORM',
        how='inner'
    )
    print(f"  Matched blocks: {len(comparison_df['BLOCK_NORM'].unique())}")
    
    # Calculate metrics
    print(f"\n📍 Calculating metrics...")
    all_metrics = []
    for method in comparison_df['method'].unique():
        metrics = calculate_metrics(comparison_df, method)
        if metrics:
            all_metrics.append(metrics)
    
    metrics_df = pd.DataFrame(all_metrics)
    
    # Print summary
    print(f"\n📊 HASIL VALIDASI {divisi_name}:")
    print("-" * 80)
    print(f"{'Metode':<25} {'r':>8} {'p-val':>10} {'MAE':>8} {'Match%':>8} {'Over-Det':>10}")
    print("-" * 80)
    for _, row in metrics_df.iterrows():
        print(f"{row['method_display']:<25} {row['pearson_r']:>8.3f} {row['pearson_p']:>10.4f} "
              f"{row['mae']:>8.1f} {row['match_rate_5pct']:>7.0f}% {row['over_detection']:>9.2f}x")
    print("-" * 80)
    
    # Create visualizations
    create_validation_charts(comparison_df, metrics_df, divisi_name, output_dir)
    
    # Save data
    comparison_df.to_csv(output_dir / f'comparison_{divisi_name.replace(" ", "_")}.csv', index=False)
    metrics_df.to_csv(output_dir / f'metrics_{divisi_name.replace(" ", "_")}.csv', index=False)
    
    return metrics_df


def main():
    """Main validation execution."""
    print("\n" + "="*70)
    print("🔬 POAC v3.3 - VALIDASI METODE ADAPTIF")
    print("Membandingkan hasil deteksi dengan data sensus lapangan")
    print("="*70)
    
    # Load sensus data
    sensus_path = INPUT_DIR / 'ame_2_4_hasil_sensus.csv'
    sensus_df = load_sensus_data(sensus_path)
    
    all_metrics = {}
    
    # Validate AME II
    print("\n" + "="*70)
    print("📂 LOADING AME II DATA")
    print("-"*40)
    df_ame_ii = load_and_clean_data(INPUT_DIR / 'tabelNDREnew.csv')
    print(f"  Loaded: {len(df_ame_ii):,} trees")
    metrics_ii = run_validation_for_divisi("AME II", df_ame_ii, sensus_df, OUTPUT_DIR)
    all_metrics['AME II'] = metrics_ii
    
    # Validate AME IV
    print("\n" + "="*70)
    print("📂 LOADING AME IV DATA")
    print("-"*40)
    df_ame_iv = load_ame_iv_data(INPUT_DIR / 'AME_IV.csv')
    print(f"  Loaded: {len(df_ame_iv):,} trees")
    metrics_iv = run_validation_for_divisi("AME IV", df_ame_iv, sensus_df, OUTPUT_DIR)
    all_metrics['AME IV'] = metrics_iv
    
    # Generate summary report
    create_summary_report(all_metrics, OUTPUT_DIR)
    
    print("\n" + "="*70)
    print("✅ VALIDASI SELESAI!")
    print(f"📁 Hasil tersimpan di: {OUTPUT_DIR}")
    print("="*70)


if __name__ == '__main__':
    main()
