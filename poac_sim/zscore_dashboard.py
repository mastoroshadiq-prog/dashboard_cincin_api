"""
Z-Score v2.0 Visual Dashboard with Ground Truth Comparison
===========================================================
Creates visual charts comparing Z-Score detection vs Ground Truth.
"""
import sys
sys.path.insert(0, 'src')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.ingestion import load_and_clean_data
from src.zscore_detection import run_zscore_detection, run_zscore_comparison
from src.clustering import run_cincin_api_algorithm

# Ground Truth data (AME II)
GT_DATA = {
    'Total_Pohon': 95055,
    'Stadium_12': 4733,
    'Stadium_34': 1236,
    'Total_Gano': 5969
}

# Target range
TARGET_LOW = 4500
TARGET_HIGH = 8000

# Output
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_dir = Path(f'data/output/zscore_dashboard_{timestamp}')
output_dir.mkdir(parents=True, exist_ok=True)

def create_comparison_bar_chart(results_dict, output_path):
    """Create bar chart comparing methods vs Ground Truth."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    methods = list(results_dict.keys())
    values = list(results_dict.values())
    colors = []
    
    for v in values:
        if TARGET_LOW <= v <= TARGET_HIGH:
            colors.append('#2ecc71')  # Green - within range
        elif v < TARGET_LOW:
            colors.append('#e74c3c')  # Red - under
        else:
            colors.append('#f39c12')  # Orange - over
    
    bars = ax.bar(methods, values, color=colors, edgecolor='white', linewidth=2)
    
    # Ground Truth line
    ax.axhline(y=GT_DATA['Total_Gano'], color='#3498db', linestyle='--', linewidth=3, label=f"Ground Truth ({GT_DATA['Total_Gano']:,})")
    
    # Target range
    ax.axhspan(TARGET_LOW, TARGET_HIGH, alpha=0.2, color='green', label=f'Target Range ({TARGET_LOW:,}-{TARGET_HIGH:,})')
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        pct = (val - GT_DATA['Total_Gano']) / GT_DATA['Total_Gano'] * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
                f'{val:,}\n({pct:+.0f}%)', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Method', fontsize=12)
    ax.set_ylabel('Deteksi Pohon', fontsize=12)
    ax.set_title('PERBANDINGAN METODE DETEKSI vs GROUND TRUTH\nZ-Score v2.0 vs Ranking/Elbow', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.set_ylim(0, max(values) * 1.2)
    
    # Rotate x labels
    plt.xticks(rotation=15, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {output_path}')

def create_threshold_sensitivity_chart(comparison_df, output_path):
    """Create line chart showing Z-Score threshold sensitivity."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    thresholds = comparison_df['Threshold'].values
    merah = comparison_df['MERAH'].values
    kuning = comparison_df['KUNING'].values
    total = comparison_df['Total_Deteksi'].values
    
    ax.plot(thresholds, total, 'o-', color='#e74c3c', linewidth=3, markersize=12, label='Total Deteksi')
    ax.plot(thresholds, merah, 's-', color='#c0392b', linewidth=2, markersize=8, label='MERAH (Kluster)')
    ax.plot(thresholds, kuning, 'd-', color='#f39c12', linewidth=2, markersize=8, label='KUNING (Indikasi)')
    
    # Ground Truth line
    ax.axhline(y=GT_DATA['Total_Gano'], color='#3498db', linestyle='--', linewidth=2, label='Ground Truth')
    
    # Target range
    ax.axhspan(TARGET_LOW, TARGET_HIGH, alpha=0.2, color='green', label='Target Range')
    
    ax.set_xlabel('Z-Score Threshold', fontsize=12)
    ax.set_ylabel('Jumlah Pohon', fontsize=12)
    ax.set_title('SENSITIVITAS THRESHOLD Z-SCORE\nPengaruh Threshold terhadap Jumlah Deteksi', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.invert_xaxis()  # More negative = more sensitive
    
    # Add annotations
    for i, (t, v) in enumerate(zip(thresholds, total)):
        label = ['Agresif', 'Seimbang', 'Konservatif'][i]
        ax.annotate(label, (t, v), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {output_path}')

def create_method_comparison_table(results_dict, output_path):
    """Create styled comparison table as image."""
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')
    
    # Prepare data
    data = []
    for method, value in results_dict.items():
        pct = (value - GT_DATA['Total_Gano']) / GT_DATA['Total_Gano'] * 100
        status = '✅ OK' if TARGET_LOW <= value <= TARGET_HIGH else ('❌ UNDER' if value < TARGET_LOW else '⚠️ OVER')
        data.append([method, f'{value:,}', f'{pct:+.1f}%', status])
    
    # Add GT row
    data.insert(0, ['Ground Truth (Sensus)', f'{GT_DATA["Total_Gano"]:,}', '0%', '📊 BASELINE'])
    
    table = ax.table(
        cellText=data,
        colLabels=['Metode', 'Deteksi', 'vs GT', 'Status'],
        loc='center',
        cellLoc='center',
        colWidths=[0.35, 0.2, 0.15, 0.15]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)
    
    # Header styling
    for j in range(4):
        table[(0, j)].set_facecolor('#34495e')
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    # Row colors
    for i in range(1, len(data) + 1):
        for j in range(4):
            if i == 1:  # GT row
                table[(i, j)].set_facecolor('#e8f6f3')
            elif 'OK' in data[i-1][3]:
                table[(i, j)].set_facecolor('#d5f5e3')
            elif 'UNDER' in data[i-1][3]:
                table[(i, j)].set_facecolor('#fadbd8')
            else:
                table[(i, j)].set_facecolor('#fdebd0')
    
    ax.set_title('TABEL PERBANDINGAN METODE DETEKSI GANODERMA\nZ-Score v2.0 Spatial Filter', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {output_path}')

def create_zero_block_analysis_chart(df_zscore, output_path):
    """Visualize blocks with zero detection (healthy blocks)."""
    # Count detections per block
    block_deteksi = df_zscore.groupby('Blok')['Status_ZScore'].apply(
        lambda x: (x != 'HIJAU (SEHAT)').sum()
    )
    
    zero_blocks = block_deteksi[block_deteksi == 0]
    nonzero_blocks = block_deteksi[block_deteksi > 0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart
    sizes = [len(zero_blocks), len(nonzero_blocks)]
    labels = [f'Blok Sehat\n(0 deteksi)\n{len(zero_blocks)} blok', 
              f'Blok Ada Deteksi\n{len(nonzero_blocks)} blok']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0)
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 11})
    ax1.set_title('PROPORSI BLOK SEHAT vs ADA DETEKSI\nZ-Score v2.0', fontsize=12, fontweight='bold')
    
    # Histogram of detection count per block
    ax2.hist(block_deteksi.values, bins=30, color='#3498db', edgecolor='white', alpha=0.8)
    ax2.axvline(x=0, color='#2ecc71', linestyle='--', linewidth=2, label='Blok Sehat')
    ax2.set_xlabel('Jumlah Deteksi per Blok')
    ax2.set_ylabel('Jumlah Blok')
    ax2.set_title('DISTRIBUSI DETEKSI PER BLOK', fontsize=12, fontweight='bold')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {output_path}')

def main():
    print('=' * 70)
    print('Z-SCORE v2.0 DASHBOARD - GROUND TRUTH COMPARISON')
    print('=' * 70)
    
    # Load data
    print('\n[1/5] Loading data...')
    df = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
    print(f'  Total: {len(df):,} pohon')
    
    # Run old method
    print('\n[2/5] Running OLD method (Ranking + Elbow v3.5)...')
    df_old, meta_old = run_cincin_api_algorithm(df.copy(), auto_tune=True)
    old_merah = len(df_old[df_old['Status_Risiko'].str.contains('MERAH', na=False)])
    
    # Run Z-Score methods
    print('\n[3/5] Running Z-Score v2.0...')
    comparison = run_zscore_comparison(df.copy())
    
    # Get detailed results for -1.5 threshold
    df_zscore, meta_zscore = run_zscore_detection(df.copy(), z_threshold=-1.5)
    
    # Prepare results dictionary
    results_dict = {
        'Ranking+Elbow v3.5': old_merah,
        'Z-Score Agresif (-1.0)': comparison[comparison['Threshold'] == -1.0]['Total_Deteksi'].values[0],
        'Z-Score Seimbang (-1.5)': comparison[comparison['Threshold'] == -1.5]['Total_Deteksi'].values[0],
        'Z-Score Konservatif (-2.0)': comparison[comparison['Threshold'] == -2.0]['Total_Deteksi'].values[0]
    }
    
    # Create visualizations
    print('\n[4/5] Creating visualizations...')
    
    # 1. Bar chart comparison
    create_comparison_bar_chart(results_dict, output_dir / 'comparison_bar_chart.png')
    
    # 2. Threshold sensitivity
    create_threshold_sensitivity_chart(comparison, output_dir / 'threshold_sensitivity.png')
    
    # 3. Comparison table
    create_method_comparison_table(results_dict, output_dir / 'comparison_table.png')
    
    # 4. Zero block analysis
    create_zero_block_analysis_chart(df_zscore, output_dir / 'zero_block_analysis.png')
    
    # Save data
    print('\n[5/5] Saving results...')
    df_zscore.to_csv(output_dir / 'zscore_results.csv', index=False)
    comparison.to_csv(output_dir / 'threshold_comparison.csv', index=False)
    
    # Summary report
    summary = pd.DataFrame([{
        'Timestamp': timestamp,
        'Ground_Truth': GT_DATA['Total_Gano'],
        'Target_Low': TARGET_LOW,
        'Target_High': TARGET_HIGH,
        **results_dict
    }])
    summary.to_csv(output_dir / 'summary.csv', index=False)
    
    print('\n' + '=' * 70)
    print('RESULTS SUMMARY')
    print('=' * 70)
    print(f"\nGround Truth: {GT_DATA['Total_Gano']:,}")
    print(f"Target Range: {TARGET_LOW:,} - {TARGET_HIGH:,}")
    print()
    for method, value in results_dict.items():
        pct = (value - GT_DATA['Total_Gano']) / GT_DATA['Total_Gano'] * 100
        status = '✅' if TARGET_LOW <= value <= TARGET_HIGH else ('❌' if value < TARGET_LOW else '⚠️')
        print(f"  {status} {method}: {value:,} ({pct:+.0f}%)")
    
    print(f'\nOutput saved to: {output_dir}')
    
    return results_dict, df_zscore

if __name__ == '__main__':
    results, df = main()
