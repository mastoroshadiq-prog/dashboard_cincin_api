"""
Split-Merge Bias Correction Analysis - Misi 2

Script ini menjalankan analisis dengan dan tanpa Split-Merge untuk
membandingkan hasil dan menunjukkan efek dari koreksi bias umur.

Logika Split-Merge:
1. Identifikasi blok dengan rasio sisipan >20%
2. Untuk blok tersebut, pisahkan pohon berdasarkan tahun tanam
3. Hitung persentil terpisah untuk masing-masing grup umur
4. Bandingkan hasil deteksi sebelum vs sesudah split-merge
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import os
import base64
from io import BytesIO

# Add parent directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
os.chdir(script_dir)

# Import matplotlib with Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.cost_control_loader import load_cost_control_data, get_replant_ratio_dict
from src.ingestion import load_and_clean_data, load_ame_iv_data
from src.clustering import (
    calculate_percentile_rank, 
    calculate_percentile_rank_split_merge,
    run_cincin_api_algorithm,
    classify_trees_with_clustering,
    find_optimal_threshold,
    simulate_thresholds
)
from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS


def generate_split_merge_charts(results: list) -> dict:
    """Generate charts untuk Split-Merge Analysis."""
    charts = {}
    plt.style.use('dark_background')
    
    # Chart 1: Utama vs Sisipan Distribution per Divisi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, result in enumerate(results):
        ax = axes[idx]
        comparison = result['comparison']
        
        if 'utama_count' in comparison.columns and 'sisipan_count' in comparison.columns:
            utama_total = comparison['utama_count'].sum()
            sisipan_total = comparison['sisipan_count'].sum()
            
            bars = ax.bar(['Pokok Utama', 'Sisipan'], [utama_total, sisipan_total],
                         color=['#3498db', '#e74c3c'], edgecolor='white', width=0.6)
            
            ax.text(0, utama_total + 500, f'{utama_total:,}', ha='center', va='bottom', fontsize=12)
            ax.text(1, sisipan_total + 500, f'{sisipan_total:,}', ha='center', va='bottom', fontsize=12)
            
            pct = sisipan_total / (utama_total + sisipan_total) * 100 if (utama_total + sisipan_total) > 0 else 0
            ax.set_title(f"{result['divisi']}\nSisipan: {pct:.1f}%", fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Jumlah Pohon')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('🌳 Distribusi Pohon Pokok vs Sisipan', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    charts['tree_distribution'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Chart 2: Detection Change Before/After Split-Merge
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, result in enumerate(results):
        ax = axes[idx]
        
        # Get blocks with sisipan
        comparison = result['comparison']
        if 'sisipan_count' in comparison.columns:
            blocks_with_sisipan = comparison[comparison['sisipan_count'] > 0].sort_values('diff_pct', ascending=False).head(10)
        else:
            blocks_with_sisipan = comparison.head(10)
        
        if len(blocks_with_sisipan) > 0:
            x = range(len(blocks_with_sisipan))
            width = 0.35
            
            bars1 = ax.bar([i - width/2 for i in x], blocks_with_sisipan['detection_pct_original'], width,
                          label='Tanpa Split', color='#e74c3c', edgecolor='white')
            bars2 = ax.bar([i + width/2 for i in x], blocks_with_sisipan['detection_pct_split'], width,
                          label='Dengan Split', color='#00d26a', edgecolor='white')
            
            ax.set_xticks(x)
            ax.set_xticklabels(blocks_with_sisipan.index, rotation=45, ha='right')
            ax.set_ylabel('Detection Rate (%)')
            ax.set_title(f"{result['divisi'][:10]} - Top 10 Blok dengan Sisipan", fontsize=11, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('📊 Perbandingan Deteksi: Tanpa vs Dengan Split-Merge', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    charts['detection_comparison'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Chart 3: Summary - Total Detection Change
    fig, ax = plt.subplots(figsize=(10, 6))
    
    divisi_names = [r['divisi'][:10] for r in results]
    original_vals = [r['original_total_detected'] for r in results]
    split_vals = [r['split_total_detected'] for r in results]
    
    x = range(len(results))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], original_vals, width, 
                   label='Tanpa Split-Merge', color='#e74c3c', edgecolor='white')
    bars2 = ax.bar([i + width/2 for i in x], split_vals, width, 
                   label='Dengan Split-Merge', color='#00d26a', edgecolor='white')
    
    ax.set_xticks(x)
    ax.set_xticklabels(divisi_names)
    ax.set_ylabel('Total Pohon Terdeteksi')
    ax.set_title('Total Deteksi: Sebelum vs Sesudah Split-Merge', fontsize=14, fontweight='bold', pad=20)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, val in zip(bars1, original_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}', ha='center', va='bottom', fontsize=10)
    for bar, val in zip(bars2, split_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    charts['total_summary'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return charts




def run_comparison_analysis(df: pd.DataFrame, replant_ratios: dict, divisi: str):
    """
    Jalankan analisis perbandingan dengan dan tanpa split-merge.
    
    Args:
        df: DataFrame NDRE
        replant_ratios: Dict rasio sisipan per blok
        divisi: Nama divisi
        
    Returns:
        Dict dengan hasil perbandingan
    """
    print(f"\n{'='*60}")
    print(f"ANALISIS SPLIT-MERGE: {divisi}")
    print('='*60)
    
    # ================================================================
    # ANALISIS 1: TANPA SPLIT-MERGE (Original)
    # ================================================================
    print("\n[1/3] Running original algorithm (without split-merge)...")
    
    df_original = calculate_percentile_rank(df.copy())
    
    # Simulate thresholds
    sim_df = simulate_thresholds(df_original)
    optimal_threshold = find_optimal_threshold(sim_df)
    
    # Classify
    df_classified_original = classify_trees_with_clustering(
        df_original, optimal_threshold
    )
    
    # Get stats per block
    original_stats = df_classified_original.groupby('Blok').apply(
        lambda x: pd.Series({
            'total': len(x),
            'detected': len(x[x['Status_Risiko'].str.contains('MERAH|ORANYE', case=False)]),
            'detection_pct': len(x[x['Status_Risiko'].str.contains('MERAH|ORANYE', case=False)]) / len(x) * 100
        })
    )
    
    # ================================================================
    # ANALISIS 2: DENGAN SPLIT-MERGE (Using 'ket' column)
    # ================================================================
    print("\n[2/3] Running algorithm with split-merge (using 'ket' column)...")
    
    # Check for ket column
    ket_col = None
    for possible_col in ['Keterangan', 'ket', 'Ket', 'KET']:
        if possible_col in df.columns:
            ket_col = possible_col
            break
    
    if ket_col is None:
        print("  ⚠️ No 'ket' column found. Cannot perform split-merge.")
        df_classified_split = df_classified_original.copy()
        df_classified_split['Split_Merge_Applied'] = False
        df_classified_split['Tree_Type'] = 'UNKNOWN'
        did_split_merge = False
    else:
        print(f"  ✓ Found 'ket' column: {ket_col}")
        
        # Show distribution
        ket_dist = df[ket_col].value_counts()
        print(f"  ✓ Tree types: {ket_dist.head(5).to_dict()}")
        
        # Run split-merge
        df_split = calculate_percentile_rank_split_merge(df.copy())
        
        # Show split-merge stats
        if 'Tree_Type' in df_split.columns:
            type_dist = df_split['Tree_Type'].value_counts()
            print(f"  ✓ Classified: {type_dist.to_dict()}")
        
        # Use same threshold for fair comparison
        df_classified_split = classify_trees_with_clustering(
            df_split, optimal_threshold
        )
        did_split_merge = True
    
    # Get stats per block
    split_stats = df_classified_split.groupby('Blok').apply(
        lambda x: pd.Series({
            'total': len(x),
            'detected': len(x[x['Status_Risiko'].str.contains('MERAH|ORANYE', case=False)]),
            'detection_pct': len(x[x['Status_Risiko'].str.contains('MERAH|ORANYE', case=False)]) / len(x) * 100,
            'split_applied': x.get('Split_Merge_Applied', pd.Series([False])).any() if 'Split_Merge_Applied' in x.columns else False,
            'utama_count': len(x[x['Tree_Type'] == 'UTAMA']) if 'Tree_Type' in x.columns else 0,
            'sisipan_count': len(x[x['Tree_Type'] == 'SISIPAN']) if 'Tree_Type' in x.columns else 0
        })
    )
    
    # ================================================================
    # PERBANDINGAN
    # ================================================================
    print("\n[3/3] Generating comparison...")
    
    # Merge stats
    comparison = original_stats.merge(
        split_stats, 
        left_index=True, 
        right_index=True,
        suffixes=('_original', '_split')
    )
    
    comparison['diff_pct'] = comparison['detection_pct_split'] - comparison['detection_pct_original']
    comparison['has_sisipan'] = comparison['sisipan_count'] > 0 if 'sisipan_count' in comparison.columns else False
    
    # Count blocks with sisipan
    blocks_with_sisipan = (comparison['sisipan_count'] > 0).sum() if 'sisipan_count' in comparison.columns else 0
    
    return {
        'divisi': divisi,
        'comparison': comparison,
        'original_total_detected': int(original_stats['detected'].sum()),
        'split_total_detected': int(split_stats['detected'].sum()),
        'optimal_threshold': optimal_threshold,
        'did_split_merge': did_split_merge,
        'blocks_with_sisipan': blocks_with_sisipan,
        'high_replant_blocks': len([b for b, r in replant_ratios.items() if r > 0.20])
    }


def generate_html_report(results: list, output_path: Path):
    """Generate HTML report untuk perbandingan split-merge."""
    
    # Generate charts
    charts = generate_split_merge_charts(results)
    
    html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Merge Bias Correction Report</title>
    <style>
        :root {
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-green: #00d26a;
            --accent-yellow: #ffc107;
            --accent-red: #ff4757;
            --accent-blue: #3498db;
            --accent-purple: #9b59b6;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            padding: 20px;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: rgba(255,255,255,0.8); }
        
        .info-box {
            background: var(--bg-card);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: var(--bg-card);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }
        
        .card h3 { color: var(--text-secondary); font-size: 0.9em; margin-bottom: 10px; }
        .card .value { font-size: 2.2em; font-weight: bold; }
        .card.green .value { color: var(--accent-green); }
        .card.yellow .value { color: var(--accent-yellow); }
        .card.red .value { color: var(--accent-red); }
        .card.blue .value { color: var(--accent-blue); }
        .card.purple .value { color: var(--accent-purple); }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        th {
            background: rgba(255,255,255,0.05);
            font-weight: 600;
            color: var(--text-secondary);
        }
        
        tr:hover { background: rgba(255,255,255,0.05); }
        
        .high-replant { background: rgba(155,89,182,0.2); }
        
        .diff-positive { color: var(--accent-green); }
        .diff-negative { color: var(--accent-red); }
        .diff-neutral { color: var(--text-secondary); }
        
        .divisi-header {
            background: linear-gradient(90deg, #667eea, transparent);
            padding: 15px 20px;
            margin: 30px 0 15px 0;
            border-radius: 10px;
            font-size: 1.3em;
        }
        
        .timestamp {
            text-align: center;
            color: var(--text-secondary);
            margin-top: 30px;
            font-size: 0.9em;
        }
        
        .charts-section {
            margin: 30px 0;
        }
        
        .charts-section h2 {
            color: var(--text-primary);
            margin-bottom: 20px;
            padding-left: 10px;
            border-left: 4px solid #9b59b6;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-card {
            background: var(--bg-card);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .chart-card img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }
        
        .chart-card h4 {
            color: var(--text-secondary);
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔀 Split-Merge Bias Correction Report</h1>
            <p>Misi 2: Pembersihan Bias Umur untuk Blok dengan Sisipan Tinggi</p>
        </div>
        
        <div class="info-box">
            <h3>📋 Logika Split-Merge</h3>
            <ul style="margin-top: 10px; margin-left: 20px;">
                <li>Blok dengan rasio sisipan >20% diidentifikasi</li>
                <li>Untuk blok tersebut, ranking persentil dihitung TERPISAH per kelompok umur</li>
                <li>Hal ini mencegah tanaman muda dianggap sakit hanya karena NDRE berbeda dengan tanaman tua</li>
            </ul>
        </div>
"""
    
    # Add Charts Section
    html += """
        <div class="charts-section">
            <h2>📊 Visualisasi Data</h2>
            <div class="charts-grid">
"""
    
    if 'tree_distribution' in charts:
        html += f"""
                <div class="chart-card">
                    <h4>🌳 Distribusi Pohon Pokok vs Sisipan</h4>
                    <img src="data:image/png;base64,{charts['tree_distribution']}" alt="Tree Distribution">
                </div>
"""
    
    if 'total_summary' in charts:
        html += f"""
                <div class="chart-card">
                    <h4>📈 Total Deteksi: Sebelum vs Sesudah</h4>
                    <img src="data:image/png;base64,{charts['total_summary']}" alt="Total Summary">
                </div>
"""
    
    if 'detection_comparison' in charts:
        html += f"""
                <div class="chart-card" style="grid-column: span 2;">
                    <h4>🔄 Perbandingan Per Blok: Tanpa vs Dengan Split-Merge</h4>
                    <img src="data:image/png;base64,{charts['detection_comparison']}" alt="Detection Comparison">
                </div>
"""
    
    html += """
            </div>
        </div>
"""
    
    for result in results:
        comparison = result['comparison']
        
        # Count blocks affected (use has_sisipan instead of has_high_replant)
        has_sisipan_col = 'has_sisipan' if 'has_sisipan' in comparison.columns else 'has_high_replant'
        if has_sisipan_col in comparison.columns:
            high_replant = comparison[comparison[has_sisipan_col]].copy()
        else:
            high_replant = comparison[comparison['sisipan_count'] > 0].copy() if 'sisipan_count' in comparison.columns else comparison.copy()
        
        html += f"""
        <div class="divisi-header">📍 {result['divisi']}</div>
        
        <div class="summary-cards">
            <div class="card blue">
                <h3>Optimal Threshold</h3>
                <div class="value">{result['optimal_threshold']*100:.0f}%</div>
            </div>
            <div class="card purple">
                <h3>Blok Sisipan >20%</h3>
                <div class="value">{result['high_replant_blocks']}</div>
            </div>
            <div class="card yellow">
                <h3>Deteksi Original</h3>
                <div class="value">{result['original_total_detected']:,}</div>
            </div>
            <div class="card green">
                <h3>Deteksi Split-Merge</h3>
                <div class="value">{result['split_total_detected']:,}</div>
            </div>
        </div>
        
        <h4 style="margin: 20px 0 10px;">Blok dengan Rasio Sisipan Tinggi (>20%)</h4>
        <table>
            <thead>
                <tr>
                    <th>Blok</th>
                    <th>Total Pohon</th>
                    <th>Deteksi Original</th>
                    <th>Deteksi Split-Merge</th>
                    <th>Perubahan</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for blok, row in high_replant.iterrows():
            diff = row['diff_pct']
            if diff > 0:
                diff_class = "diff-positive"
            elif diff < 0:
                diff_class = "diff-negative"
            else:
                diff_class = "diff-neutral"
            
            html += f"""
                <tr class="high-replant">
                    <td><strong>{blok}</strong></td>
                    <td>{int(row['total_original']):,}</td>
                    <td>{row['detection_pct_original']:.1f}%</td>
                    <td>{row['detection_pct_split']:.1f}%</td>
                    <td class="{diff_class}">{diff:+.1f}%</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
"""
    
    html += f"""
        <p class="timestamp">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            POAC v3.3 - Algoritma Cincin Api - Split-Merge Analysis
        </p>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\nHTML report saved to: {output_path}")


def main():
    """Main function untuk menjalankan Split-Merge Analysis."""
    print("\n" + "="*70)
    print("SPLIT-MERGE BIAS CORRECTION - MISI 2")
    print("Pembersihan Bias Umur untuk Blok dengan Sisipan Tinggi")
    print("="*70)
    
    # Setup paths
    base_path = Path(__file__).parent
    data_path = base_path / "data" / "input"
    output_path = base_path / "data" / "output" / "split_merge_analysis"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load cost control data (untuk rasio sisipan)
    print("\n[1/4] Loading cost control data...")
    df_cost = load_cost_control_data(data_path / "data_baru.csv")
    
    # Get replant ratios
    df_ame002 = df_cost[df_cost['DIVISI'] == 'AME002']
    df_ame004 = df_cost[df_cost['DIVISI'] == 'AME004']
    
    replant_ame002 = get_replant_ratio_dict(df_ame002)
    replant_ame004 = get_replant_ratio_dict(df_ame004)
    
    high_replant_002 = len([b for b, r in replant_ame002.items() if r > 0.20])
    high_replant_004 = len([b for b, r in replant_ame004.items() if r > 0.20])
    
    print(f"  - AME002: {len(replant_ame002)} blok, {high_replant_002} dengan sisipan >20%")
    print(f"  - AME004: {len(replant_ame004)} blok, {high_replant_004} dengan sisipan >20%")
    
    # Load NDRE data
    print("\n[2/4] Loading NDRE data...")
    df_ndre_ame2 = load_and_clean_data(data_path / "tabelNDREnew.csv")
    df_ndre_ame4 = load_ame_iv_data(data_path / "AME_IV.csv")
    
    print(f"  - AME II: {len(df_ndre_ame2):,} pohon")
    print(f"  - AME IV: {len(df_ndre_ame4):,} pohon")
    
    # Run comparison analysis
    print("\n[3/4] Running comparison analysis...")
    
    results = []
    
    result_ame2 = run_comparison_analysis(df_ndre_ame2, replant_ame002, "AME002 (AME II)")
    results.append(result_ame2)
    
    result_ame4 = run_comparison_analysis(df_ndre_ame4, replant_ame004, "AME004 (AME IV)")
    results.append(result_ame4)
    
    # Generate reports
    print("\n[4/4] Generating reports...")
    
    # Save comparison CSVs
    for result in results:
        csv_path = output_path / f"comparison_{result['divisi'].replace(' ', '_').replace('(', '').replace(')', '')}.csv"
        result['comparison'].to_csv(csv_path)
        print(f"  - CSV saved: {csv_path}")
    
    # Generate HTML
    html_path = output_path / "split_merge_report.html"
    generate_html_report(results, html_path)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for result in results:
        print(f"\n{result['divisi']}:")
        print(f"  - Blok dengan sisipan >20%: {result['high_replant_blocks']}")
        print(f"  - Deteksi tanpa split-merge: {result['original_total_detected']:,}")
        print(f"  - Deteksi dengan split-merge: {result['split_total_detected']:,}")
        diff = result['split_total_detected'] - result['original_total_detected']
        print(f"  - Perubahan: {diff:+,} pohon")
    
    print(f"\n✅ Reports saved to: {output_path}")
    print("="*70)


if __name__ == "__main__":
    main()
