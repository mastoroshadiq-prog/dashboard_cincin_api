"""
Early Detection Report - Misi 1: Ground Truth Check

Script ini membandingkan hasil deteksi algoritma Cincin Api dengan data sensus
untuk mengkategorikan setiap blok:

- MATCH: Algoritma ≈ Sensus (selisih ≤2%)
- EARLY_DETECT: Algoritma > Sensus + 2% → TEMUAN EMAS! (Infeksi baru yang lolos sensus manual)
- UNDER_DETECT: Algoritma < Sensus - 2% → Perlu kalibrasi atau pohon sudah dibongkar

Output:
- early_detection_report.csv: Detail per blok
- early_detection_report.html: Laporan visual dengan highlight temuan emas
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

# Import matplotlib with Agg backend for non-interactive use
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.cost_control_loader import (
    load_cost_control_data, get_census_data_dict, normalize_block,
    load_ground_truth_excel, get_ground_truth_census_dict, get_ground_truth_book_dict
)
from src.ingestion import load_and_clean_data, load_ame_iv_data
from src.clustering import run_cincin_api_algorithm
from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS


def generate_charts(df_all: pd.DataFrame, output_dir: Path) -> dict:
    """
    Generate charts untuk Early Detection Report.
    Hanya menampilkan chart per divisi dengan superimpose style yang jelas.
    
    Returns:
        Dict dengan base64 encoded images
    """
    charts = {}
    
    # Style settings
    plt.style.use('dark_background')
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.weight'] = 'normal'
    
    # Filter out NO_ALGO_DATA for meaningful analysis
    df_valid = df_all[df_all['category'] != 'NO_ALGO_DATA'].copy()
    
    # Color scheme: Sensus = Green, Algoritma = Red
    COLOR_SENSUS = '#2ecc71'     # Emerald Green
    COLOR_ALGORITMA = '#e74c3c'  # Coral Red
    
    # Generate separate chart for each divisi (more detail, clearer)
    divisi_list = df_valid['divisi'].unique()
    
    for divisi in divisi_list:
        df_div = df_valid[df_valid['divisi'] == divisi].sort_values('diff_pct', ascending=False).head(20)
        
        if len(df_div) == 0:
            continue
        
        # Larger figure for single divisi - more detail
        fig, ax = plt.subplots(figsize=(16, 12))
        
        x = np.arange(len(df_div))
        width = 0.8  # Lebar bar untuk superimpose
        
        # Sensus di belakang (hijau, lebih lebar, transparan)
        bars_sensus = ax.bar(x, df_div['census_pct'], width, 
                            label='🟢 Sensus (Data Lapangan)', color=COLOR_SENSUS, alpha=0.5, 
                            edgecolor='white', linewidth=2)
        
        # Algoritma di depan (merah, lebih tipis, solid)
        bars_algo = ax.bar(x, df_div['algorithm_pct'], width * 0.5, 
                          label='🔴 Algoritma (Deteksi NDRE)', color=COLOR_ALGORITMA, alpha=0.95,
                          edgecolor='white', linewidth=2)
        
        ax.set_xticks(x)
        ax.set_xticklabels(df_div['blok'], rotation=45, ha='right', fontsize=12, fontweight='bold')
        ax.set_ylabel('Persentase Deteksi (%)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Blok', fontsize=13)
        ax.set_title(f'📊 {divisi}\nPerbandingan Deteksi: Algoritma vs Sensus (Top 20 Blok)', 
                    fontsize=18, fontweight='bold', pad=25)
        ax.legend(loc='upper right', fontsize=13, framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Double label di atas bar: Algoritma dan Sensus
        for i, (bar_a, bar_s, (_, row)) in enumerate(zip(bars_algo, bars_sensus, df_div.iterrows())):
            algo_h = bar_a.get_height()
            sens_h = bar_s.get_height()
            max_h = max(algo_h, sens_h)
            diff = algo_h - sens_h
            
            # Label Algoritma (merah) - di atas
            ax.text(bar_a.get_x() + width/2, max_h + 2, 
                   f'{algo_h:.1f}%', fontsize=10, color=COLOR_ALGORITMA, fontweight='bold',
                   ha='center', va='bottom')
            # Label Sensus (hijau) - di bawah label algoritma
            ax.text(bar_a.get_x() + width/2, max_h + 6, 
                   f'{sens_h:.1f}%', fontsize=10, color=COLOR_SENSUS, fontweight='bold',
                   ha='center', va='bottom')
            # Selisih (jika positif)
            if diff > 0:
                ax.text(bar_a.get_x() + width/2, max_h + 10, 
                       f'+{diff:.1f}%', fontsize=9, color='#f39c12', fontweight='bold',
                       ha='center', va='bottom', style='italic')
        
        # Y-axis max dengan ruang untuk label
        max_y = max(df_div['algorithm_pct'].max(), df_div['census_pct'].max()) + 18
        ax.set_ylim(0, max_y)
        
        # Legend box di pojok kiri
        info_text = f"Total Blok Ditampilkan: {len(df_div)}\n"
        info_text += f"Blok dengan Algo > Sensus: {len(df_div[df_div['diff_pct'] > 0])}\n"
        avg_diff = df_div['diff_pct'].mean()
        info_text += f"Rata-rata Selisih: +{avg_diff:.1f}%"
        
        props = dict(boxstyle='round,pad=0.5', facecolor='#2c3e50', alpha=0.9, edgecolor='white')
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=11, 
               verticalalignment='top', bbox=props, color='white')
        
        # Subtitle
        fig.text(0.5, 0.01, 
                '🔴 Bar Merah = Deteksi Algoritma | 🟢 Bar Hijau = Data Sensus | 🟡 Angka Kuning = Selisih',
                fontsize=13, ha='center', color='#bdc3c7')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='#1a1a2e')
        buf.seek(0)
        
        # Store with divisi key
        chart_key = f'divisi_{divisi.replace(" ", "_").lower()}'
        charts[chart_key] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    return charts


def calculate_algorithm_detection_rate(df_classified: pd.DataFrame) -> dict:
    """
    Hitung persentase pohon terdeteksi per blok.
    
    Args:
        df_classified: DataFrame hasil klasifikasi algoritma
        
    Returns:
        Dict[blok_normalized, detection_pct]
    """
    # Tentukan kolom blok (bisa Blok atau blok)
    blok_col = 'Blok' if 'Blok' in df_classified.columns else 'blok'
    
    # Group by blok
    results = {}
    for blok, grup in df_classified.groupby(blok_col):
        total = len(grup)
        
        # Count detected based on Status_Risiko column
        # MERAH (KLUSTER AKTIF) dan ORANYE (CINCIN API) dianggap terdeteksi
        if 'Status_Risiko' in grup.columns:
            detected = len(grup[grup['Status_Risiko'].str.contains('MERAH|ORANYE', case=False, na=False)])
        elif 'RISK_TIER' in grup.columns:
            detected = len(grup[grup['RISK_TIER'].isin([1, 2])])
        elif 'Status_Ganoderma' in grup.columns:
            detected = len(grup[grup['Status_Ganoderma'].isin(['Suspect', 'High Risk'])])
        else:
            detected = 0
        
        blok_norm = normalize_block(str(blok))
        detection_pct = (detected / total * 100) if total > 0 else 0
        results[blok_norm] = {
            'detection_pct': detection_pct,
            'detected_count': detected,
            'total_count': total
        }
    
    return results


def generate_drilldown_data(df_classified: pd.DataFrame, divisi_name: str) -> dict:
    """
    Generate drilldown data per blok - daftar pohon yang terdeteksi untuk survey.
    
    Args:
        df_classified: DataFrame hasil klasifikasi algoritma
        divisi_name: Nama divisi
        
    Returns:
        Dict[blok] = {
            'trees': List[{n_baris, n_pokok, status, ndre}],
            'summary_per_baris': Dict[baris] = count
        }
    """
    blok_col = 'Blok' if 'Blok' in df_classified.columns else 'blok'
    baris_col = 'N_BARIS' if 'N_BARIS' in df_classified.columns else 'n_baris'
    pokok_col = 'N_POKOK' if 'N_POKOK' in df_classified.columns else 'n_pokok'
    ndre_col = 'NDRE125' if 'NDRE125' in df_classified.columns else 'ndre125'
    
    drilldown = {}
    
    for blok, grup in df_classified.groupby(blok_col):
        blok_norm = normalize_block(str(blok))
        
        # Filter only detected trees (MERAH dan ORANYE)
        if 'Status_Risiko' in grup.columns:
            detected_mask = grup['Status_Risiko'].str.contains('MERAH|ORANYE', case=False, na=False)
        else:
            continue
        
        detected_trees = grup[detected_mask].copy()
        
        if len(detected_trees) == 0:
            continue
        
        # Build tree list
        trees = []
        for _, row in detected_trees.iterrows():
            tree_info = {
                'n_baris': int(row.get(baris_col, 0)),
                'n_pokok': int(row.get(pokok_col, 0)),
                'status': row.get('Status_Risiko', 'Unknown'),
                'ndre': round(float(row.get(ndre_col, 0)), 4)
            }
            # Add ID if available
            if 'ObjectID' in row.index:
                tree_info['id'] = int(row['ObjectID'])
            elif 'objectid' in row.index:
                tree_info['id'] = int(row['objectid'])
            trees.append(tree_info)
        
        # Sort by baris, then pokok
        trees.sort(key=lambda x: (x['n_baris'], x['n_pokok']))
        
        # Summary per baris
        baris_summary = detected_trees.groupby(baris_col).size().to_dict()
        
        drilldown[blok_norm] = {
            'divisi': divisi_name,
            'blok': blok_norm,
            'total_detected': len(trees),
            'trees': trees,
            'summary_per_baris': {int(k): int(v) for k, v in baris_summary.items()}
        }
    
    return drilldown


def export_drilldown_csv(drilldown_data: dict, output_dir: Path) -> Path:
    """
    Export drilldown data ke CSV - daftar pohon yang perlu survey.
    """
    rows = []
    for blok, data in drilldown_data.items():
        for tree in data['trees']:
            rows.append({
                'Divisi': data['divisi'],
                'Blok': blok,
                'Baris': tree['n_baris'],
                'Pokok': tree['n_pokok'],
                'ID_Pokok': tree.get('id', '-'),
                'Status': tree['status'],
                'NDRE': tree['ndre']
            })
    
    df = pd.DataFrame(rows)
    output_path = output_dir / "drilldown_pohon_survey.csv"
    df.to_csv(output_path, index=False)
    return output_path


def generate_early_detection_report(
    algo_results: dict,
    census_data: dict,
    divisi: str,
    threshold: float = 2.0
) -> pd.DataFrame:
    """
    Generate report perbandingan algoritma vs sensus.
    
    Args:
        algo_results: Dict {blok: {detection_pct, detected_count, total_count}}
        census_data: Dict {blok: (stadium_3_4, total_ganoderma, serangan_pct)}
        divisi: Nama divisi
        threshold: Threshold untuk kategorisasi (default 2%)
        
    Returns:
        DataFrame dengan analisis early detection
    """
    results = []
    
    # Gabungkan semua blok dari kedua sumber
    all_blocks = set(algo_results.keys()) | set(census_data.keys())
    
    for blok in sorted(all_blocks):
        algo = algo_results.get(blok, {'detection_pct': 0, 'detected_count': 0, 'total_count': 0})
        census = census_data.get(blok, (0, 0, 0))
        
        algo_pct = algo['detection_pct']
        sensus_pct = census[2]  # serangan_pct
        
        diff = algo_pct - sensus_pct
        
        # Kategorisasi
        if algo['total_count'] == 0:
            category = "NO_ALGO_DATA"
            significance = "INFO"
        elif census[2] == 0 and algo_pct == 0:
            category = "BOTH_CLEAN"
            significance = "OK"
        elif abs(diff) <= threshold:
            category = "MATCH"
            significance = "OK"
        elif diff > threshold:
            # Algoritma deteksi lebih banyak dari sensus
            category = "EARLY_DETECT"
            significance = "GOLD" if diff > 5 else "POTENTIAL"
        else:  # diff < -threshold
            category = "UNDER_DETECT"
            significance = "WARNING"
        
        results.append({
            'divisi': divisi,
            'blok': blok,
            'algorithm_pct': round(algo_pct, 2),
            'census_pct': sensus_pct,
            'diff_pct': round(diff, 2),
            'algo_detected': algo['detected_count'],
            'algo_total': algo['total_count'],
            'census_ganoderma': census[1],  # total_ganoderma
            'category': category,
            'significance': significance
        })
    
    return pd.DataFrame(results)


def generate_html_report(df_all: pd.DataFrame, output_path: Path, charts: dict = None, drilldown_data: dict = None) -> None:
    """Generate HTML report dengan styling, charts, dan drilldown."""
    
    # Generate charts if not provided
    if charts is None:
        charts = generate_charts(df_all, output_path.parent)
    
    # Calculate summary stats
    early_detect = len(df_all[df_all['category'] == 'EARLY_DETECT'])
    gold_finds = len(df_all[df_all['significance'] == 'GOLD'])
    matches = len(df_all[df_all['category'] == 'MATCH'])
    under_detect = len(df_all[df_all['category'] == 'UNDER_DETECT'])
    
    html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Early Detection Report - Ground Truth Check</title>
    <style>
        :root {{
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-green: #00d26a;
            --accent-yellow: #ffc107;
            --accent-red: #ff4757;
            --accent-blue: #3498db;
            --accent-gold: #ffd700;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            padding: 20px;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        .header {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ color: rgba(255,255,255,0.8); }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: var(--bg-card);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }}
        
        .card h3 {{ color: var(--text-secondary); font-size: 0.85em; margin-bottom: 10px; }}
        .card .value {{ font-size: 2.2em; font-weight: bold; }}
        .card.green .value {{ color: var(--accent-green); }}
        .card.yellow .value {{ color: var(--accent-yellow); }}
        .card.red .value {{ color: var(--accent-red); }}
        .card.blue .value {{ color: var(--accent-blue); }}
        .card.gold .value {{ color: var(--accent-gold); }}
        
        .gold-box {{
            background: linear-gradient(135deg, #f5af19, #f12711);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .gold-box h2 {{ margin-bottom: 10px; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        th {{
            background: rgba(255,255,255,0.05);
            font-weight: 600;
            color: var(--text-secondary);
        }}
        
        tr:hover {{ background: rgba(255,255,255,0.05); }}
        
        .cat-match {{ color: var(--accent-green); }}
        .cat-early {{ color: var(--accent-gold); font-weight: bold; }}
        .cat-under {{ color: var(--accent-yellow); }}
        .cat-info {{ color: var(--text-secondary); }}
        
        .diff-positive {{ color: var(--accent-gold); font-weight: bold; }}
        .diff-negative {{ color: var(--accent-red); }}
        .diff-neutral {{ color: var(--text-secondary); }}
        
        .divisi-header {{
            background: linear-gradient(90deg, #f093fb, transparent);
            padding: 15px 20px;
            margin: 30px 0 15px 0;
            border-radius: 10px;
            font-size: 1.3em;
        }}
        
        .legend {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        
        .legend h3 {{ margin-bottom: 15px; }}
        .legend-item {{ display: flex; align-items: center; margin-bottom: 10px; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 5px; margin-right: 10px; }}
        
        .timestamp {{
            text-align: center;
            color: var(--text-secondary);
            margin-top: 30px;
            font-size: 0.9em;
        }}
        
        .charts-section {{
            margin: 30px 0;
        }}
        
        .charts-section h2 {{
            color: var(--text-primary);
            margin-bottom: 20px;
            padding-left: 10px;
            border-left: 4px solid #ffd700;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: var(--bg-card);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }}
        
        .chart-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }}
        
        .chart-card h4 {{
            color: var(--text-secondary);
            margin-bottom: 15px;
        }}
        
        /* Modal Popup Styles */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            overflow: auto;
        }}
        
        .modal-content {{
            background: var(--bg-card);
            margin: 5% auto;
            padding: 25px;
            border-radius: 15px;
            width: 90%;
            max-width: 900px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
            animation: modalIn 0.3s ease-out;
        }}
        
        @keyframes modalIn {{
            from {{ opacity: 0; transform: translateY(-50px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .modal-close {{
            position: absolute;
            right: 20px;
            top: 15px;
            font-size: 28px;
            cursor: pointer;
            color: var(--text-secondary);
        }}
        .modal-close:hover {{ color: var(--accent-red); }}
        
        .modal-header {{
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        
        .modal-header h2 {{ color: var(--accent-gold); }}
        
        .baris-group {{
            margin-bottom: 15px;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }}
        
        .baris-header {{
            font-weight: bold;
            margin-bottom: 8px;
            color: var(--accent-blue);
            font-size: 1.1em;
        }}
        
        .pokok-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .pokok-tag {{
            padding: 5px 12px;
            border-radius: 5px;
            font-size: 0.9em;
            cursor: default;
        }}
        
        .pokok-tag.merah {{
            background: var(--accent-red);
            color: white;
        }}
        
        .pokok-tag.oranye {{
            background: #f39c12;
            color: white;
        }}
        
        .drilldown-btn {{
            background: var(--accent-blue);
            color: white;
            border: none;
            padding: 5px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.85em;
        }}
        .drilldown-btn:hover {{
            background: #2980b9;
        }}
        
        .blok-link {{
            color: var(--accent-gold);
            cursor: pointer;
            text-decoration: underline;
        }}
        .blok-link:hover {{
            color: #fff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Early Detection Report</h1>
            <p>Ground Truth Check - Algoritma Cincin Api vs Data Sensus</p>
        </div>
        
        <div class="summary-cards">
            <div class="card gold">
                <h3>🏆 TEMUAN EMAS (&gt;5%)</h3>
                <div class="value">{gold_finds}</div>
                <small style="color: var(--text-secondary);">blok</small>
            </div>
            <div class="card yellow">
                <h3>Early Detect (2-5%)</h3>
                <div class="value">{early_detect - gold_finds}</div>
                <small style="color: var(--text-secondary);">blok</small>
            </div>
            <div class="card green">
                <h3>Match (±2%)</h3>
                <div class="value">{matches}</div>
                <small style="color: var(--text-secondary);">blok</small>
            </div>
            <div class="card red">
                <h3>Under Detect</h3>
                <div class="value">{under_detect}</div>
                <small style="color: var(--text-secondary);">blok</small>
            </div>
        </div>
        
        <div class="legend">
            <h3>📋 Panduan Interpretasi</h3>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--accent-gold);"></div>
                <span><strong>EARLY_DETECT (TEMUAN EMAS)</strong>: Algoritma mendeteksi lebih banyak dari sensus. 
                Ini indikasi infeksi baru yang lolos dari sensus manual!</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--accent-green);"></div>
                <span><strong>MATCH</strong>: Algoritma dan sensus sesuai (selisih ≤2%). Validasi berhasil.</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--accent-yellow);"></div>
                <span><strong>UNDER_DETECT</strong>: Algoritma mendeteksi kurang dari sensus. 
                Perlu cek: apakah pohon sudah dibongkar? atau perlu kalibrasi threshold?</span>
            </div>
        </div>
"""
    
    # Add Charts Section - Per Divisi Only (no combined Top 15)
    html += """
        <div class="charts-section">
            <h2>📊 Visualisasi Perbandingan Per Divisi</h2>
"""
    
    # Add chart for each divisi
    for chart_key, chart_data in charts.items():
        if chart_key.startswith('divisi_'):
            divisi_name = chart_key.replace('divisi_', '').replace('_', ' ').upper()
            html += f"""
            <div class="chart-card" style="margin-bottom: 30px;">
                <img src="data:image/png;base64,{chart_data}" alt="{divisi_name}" style="width: 100%; max-width: 1400px;">
            </div>
"""
    
    # Single comprehensive table - organized by divisi
    # Show all blocks with algorithm > census (EARLY_DETECT / GOLD)
    df_priority = df_all[df_all['category'] == 'EARLY_DETECT'].sort_values(
        ['divisi', 'diff_pct'], ascending=[True, False]
    )
    
    if len(df_priority) > 0:
        html += """
        <div class="gold-box">
            <h2>🏆 DAFTAR BLOK PRIORITAS SURVEY</h2>
            <p>Blok-blok berikut menunjukkan deteksi algoritma di atas sensus. 
            Klik tombol <strong>🔍 Detail</strong> untuk melihat daftar pohon yang perlu disurvey.</p>
        </div>
"""
        
        # Group by divisi
        for divisi in df_priority['divisi'].unique():
            df_div = df_priority[df_priority['divisi'] == divisi].copy()
            
            html += f"""
        <div class="divisi-header">📍 {divisi} ({len(df_div)} blok prioritas)</div>
        <table>
            <thead>
                <tr>
                    <th>No</th>
                    <th>Blok</th>
                    <th>🔴 Algoritma</th>
                    <th>🟢 Sensus</th>
                    <th>Selisih</th>
                    <th>Prioritas</th>
                    <th>Pohon</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
"""
            for idx, (_, row) in enumerate(df_div.iterrows(), 1):
                # Priority level based on diff
                if row['diff_pct'] >= 10:
                    priority = "🚨 SANGAT TINGGI"
                    priority_class = "diff-positive"
                elif row['diff_pct'] >= 5:
                    priority = "⚠️ TINGGI"
                    priority_class = "diff-positive"
                else:
                    priority = "📋 SEDANG"
                    priority_class = "diff-neutral"
                
                # Get tree count from drilldown
                blok = row['blok']
                tree_count = 0
                if drilldown_data and blok in drilldown_data:
                    tree_count = drilldown_data[blok]['total_detected']
                
                html += f"""
                <tr>
                    <td>{idx}</td>
                    <td><strong>{blok}</strong></td>
                    <td style="color: #e74c3c;">{row['algorithm_pct']:.1f}%</td>
                    <td style="color: #2ecc71;">{row['census_pct']:.1f}%</td>
                    <td class="{priority_class}">+{row['diff_pct']:.1f}%</td>
                    <td>{priority}</td>
                    <td><strong>{tree_count:,}</strong> pohon</td>
                    <td><button class="drilldown-btn" onclick="showDrilldown('{blok}')">🔍 Detail</button></td>
                </tr>
"""
            
            html += """
            </tbody>
        </table>
"""

    
    # Add summary for other categories if any
    df_match = df_all[df_all['category'] == 'MATCH']
    df_under = df_all[df_all['category'] == 'UNDER_DETECT']
    
    if len(df_match) > 0 or len(df_under) > 0:
        html += """
        <div style="margin-top: 30px; padding: 20px; background: var(--bg-card); border-radius: 10px;">
            <h3>📊 Ringkasan Kategori Lainnya</h3>
"""
        if len(df_match) > 0:
            html += f"""
            <p>✅ <strong>MATCH</strong> (selisih ±2%): {len(df_match)} blok - Algoritma dan sensus sesuai</p>
"""
        if len(df_under) > 0:
            html += f"""
            <p>⚠️ <strong>UNDER_DETECT</strong>: {len(df_under)} blok - Algoritma deteksi kurang dari sensus</p>
"""
        html += """
        </div>
"""
    

    # Add Modal Popup and JavaScript for Drilldown
    if drilldown_data and len(drilldown_data) > 0:
        total_trees = sum(d['total_detected'] for d in drilldown_data.values())
        
        # Build JavaScript data object
        import json
        js_data = {}
        for blok, data in drilldown_data.items():
            # Group trees by baris
            baris_dict = {}
            for tree in data['trees']:
                baris = tree['n_baris']
                if baris not in baris_dict:
                    baris_dict[baris] = []
                baris_dict[baris].append({
                    'pokok': tree['n_pokok'],
                    'id': tree.get('id', '-'),
                    'status': 'merah' if 'MERAH' in tree['status'].upper() else 'oranye',
                    'ndre': tree['ndre']
                })
            
            # Count by status
            merah_count = len([t for t in data['trees'] if 'MERAH' in t['status'].upper()])
            oranye_count = len([t for t in data['trees'] if 'ORANYE' in t['status'].upper()])
            
            js_data[blok] = {
                'divisi': data['divisi'],
                'total': data['total_detected'],
                'merah': merah_count,
                'oranye': oranye_count,
                'baris': baris_dict
            }
        
        html += f"""
    <!-- Modal Popup -->
    <div id="drilldownModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div class="modal-header">
                <h2 id="modalTitle">Loading...</h2>
                <p id="modalSubtitle"></p>
            </div>
            <div id="modalBody">
                <!-- Content will be injected by JavaScript -->
            </div>
        </div>
    </div>
    
    <script>
        // Drilldown Data
        var drilldownData = {json.dumps(js_data)};
        
        function showDrilldown(blok) {{
            var data = drilldownData[blok];
            if (!data) {{
                alert('Data tidak ditemukan untuk blok ' + blok);
                return;
            }}
            
            // Set header
            document.getElementById('modalTitle').innerHTML = '🔍 Blok ' + blok;
            document.getElementById('modalSubtitle').innerHTML = 
                '<strong>' + data.total + '</strong> pohon perlu survey | ' +
                '<span style="color:#e74c3c">' + data.merah + ' MERAH</span> | ' +
                '<span style="color:#f39c12">' + data.oranye + ' ORANYE</span>';
            
            // Build body content
            var html = '<p style="margin-bottom:10px;color:#a0a0a0">Divisi: ' + data.divisi + '</p>';
            
            // Add legend
            html += '<div style="display:flex;gap:20px;margin-bottom:20px;padding:12px;background:rgba(255,255,255,0.05);border-radius:8px;">';
            html += '<div style="display:flex;align-items:center;gap:8px;">';
            html += '<span style="background:#e74c3c;color:white;padding:4px 10px;border-radius:4px;font-size:0.85em;">MERAH</span>';
            html += '<span style="color:#a0a0a0;font-size:0.9em;">= Kluster Aktif (Prioritas Sanitasi)</span>';
            html += '</div>';
            html += '<div style="display:flex;align-items:center;gap:8px;">';
            html += '<span style="background:#f39c12;color:white;padding:4px 10px;border-radius:4px;font-size:0.85em;">ORANYE</span>';
            html += '<span style="color:#a0a0a0;font-size:0.9em;">= Cincin Api (Prioritas Monitoring)</span>';
            html += '</div>';
            html += '</div>';
            
            // Sort baris
            var barisKeys = Object.keys(data.baris).map(Number).sort((a,b) => a-b);
            
            for (var i = 0; i < barisKeys.length; i++) {{
                var baris = barisKeys[i];
                var trees = data.baris[baris];
                trees.sort((a,b) => a.pokok - b.pokok);
                
                var barisId = blok + '_baris_' + baris;
                
                // Collapsible baris group
                html += '<div class="baris-group">';
                html += '<div class="baris-header" onclick="toggleBaris(\\'' + barisId + '\\')" style="cursor:pointer;display:flex;justify-content:space-between;align-items:center;">';
                html += '<span>Baris ' + baris + ' (' + trees.length + ' pohon)</span>';
                html += '<span class="baris-toggle" id="toggle_' + barisId + '">▼</span>';
                html += '</div>';
                html += '<div class="pokok-grid" id="' + barisId + '" style="display:none;">';
                
                for (var j = 0; j < trees.length; j++) {{
                    var tree = trees[j];
                    var cls = tree.status;
                    html += '<span class="pokok-tag ' + cls + '" title="ID: ' + tree.id + ', NDRE: ' + tree.ndre.toFixed(4) + '">';
                    html += 'Pokok ' + tree.pokok;
                    html += '</span>';
                }}
                
                html += '</div></div>';
            }}
            
            // Add expand/collapse all buttons
            html += '<div style="margin-top:15px;display:flex;gap:10px;">';
            html += '<button onclick="expandAllBaris()" style="background:#3498db;color:white;border:none;padding:8px 15px;border-radius:5px;cursor:pointer;font-size:0.9em;">📂 Buka Semua</button>';
            html += '<button onclick="collapseAllBaris()" style="background:#7f8c8d;color:white;border:none;padding:8px 15px;border-radius:5px;cursor:pointer;font-size:0.9em;">📁 Tutup Semua</button>';
            html += '</div>';
            
            document.getElementById('modalBody').innerHTML = html;
            document.getElementById('drilldownModal').style.display = 'block';
        }}
        
        function toggleBaris(barisId) {{
            var content = document.getElementById(barisId);
            var toggle = document.getElementById('toggle_' + barisId);
            if (content.style.display === 'none') {{
                content.style.display = 'flex';
                toggle.innerHTML = '▲';
            }} else {{
                content.style.display = 'none';
                toggle.innerHTML = '▼';
            }}
        }}
        
        function expandAllBaris() {{
            var grids = document.querySelectorAll('.pokok-grid');
            var toggles = document.querySelectorAll('.baris-toggle');
            for (var i = 0; i < grids.length; i++) {{
                grids[i].style.display = 'flex';
            }}
            for (var i = 0; i < toggles.length; i++) {{
                toggles[i].innerHTML = '▲';
            }}
        }}
        
        function collapseAllBaris() {{
            var grids = document.querySelectorAll('.pokok-grid');
            var toggles = document.querySelectorAll('.baris-toggle');
            for (var i = 0; i < grids.length; i++) {{
                grids[i].style.display = 'none';
            }}
            for (var i = 0; i < toggles.length; i++) {{
                toggles[i].innerHTML = '▼';
            }}
        }}
        
        function closeModal() {{
            document.getElementById('drilldownModal').style.display = 'none';
        }}
        
        // Close modal when clicking outside
        window.onclick = function(event) {{
            var modal = document.getElementById('drilldownModal');
            if (event.target == modal) {{
                modal.style.display = 'none';
            }}
        }}
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                closeModal();
            }}
        }});
    </script>
    
    <p style="text-align:center;color:#a0a0a0;margin-top:20px;font-size:0.9em;">
        💡 Data lengkap tersedia di file: <code>drilldown_pohon_survey.csv</code> ({total_trees:,} pohon)
    </p>
"""

    
    html += f"""
        <p class="timestamp">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            POAC v3.3 - Algoritma Cincin Api - Ground Truth Check
        </p>
    </div>
</body>
</html>
"""


    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report saved to: {output_path}")


def main():
    """Main function untuk menjalankan Early Detection Report."""
    print("\n" + "="*70)
    print("EARLY DETECTION REPORT - MISI 1")
    print("Ground Truth Check: Algoritma vs Data Sensus")
    print("="*70)
    
    # Setup paths
    base_path = Path(__file__).parent
    data_path = base_path / "data" / "input"
    output_path = base_path / "data" / "output" / "early_detection"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load ground truth data (Excel file - AUTHORITATIVE SOURCE)
    ground_truth_file = data_path / "areal_inti_serangan_gano_AMEII_AMEIV.xlsx"
    print(f"\n[1/5] Loading ground truth data...")
    print(f"      Source: {ground_truth_file.name}")
    
    df_gt = load_ground_truth_excel(ground_truth_file)
    
    # Split by divisi
    df_ame002 = df_gt[df_gt['DIVISI'] == 'AME002']
    df_ame004 = df_gt[df_gt['DIVISI'] == 'AME004']
    
    census_ame002 = get_ground_truth_census_dict(df_ame002)
    census_ame004 = get_ground_truth_census_dict(df_ame004)
    
    print(f"  - AME002: {len(census_ame002)} blok, {df_ame002['TOTAL_PKK'].sum():,.0f} pohon")
    print(f"  - AME004: {len(census_ame004)} blok, {df_ame004['TOTAL_PKK'].sum():,.0f} pohon")
    
    # Load NDRE data
    print("\n[2/5] Loading NDRE data...")
    df_ndre_ame2 = load_and_clean_data(data_path / "tabelNDREnew.csv")
    df_ndre_ame4 = load_ame_iv_data(data_path / "AME_IV.csv")
    
    print(f"  - AME II: {len(df_ndre_ame2):,} pohon")
    print(f"  - AME IV: {len(df_ndre_ame4):,} pohon")
    
    # Run algorithm (using Standar preset for baseline)
    print("\n[3/5] Running Cincin Api algorithm (Standar preset)...")
    
    preset_config = {**CINCIN_API_CONFIG, **CINCIN_API_PRESETS['standar']}
    
    df_classified_ame2, _ = run_cincin_api_algorithm(
        df_ndre_ame2.copy(), 
        auto_tune=True, 
        config_override=preset_config
    )
    df_classified_ame4, _ = run_cincin_api_algorithm(
        df_ndre_ame4.copy(), 
        auto_tune=True, 
        config_override=preset_config
    )
    
    # Calculate detection rates
    print("\n[4/5] Calculating detection rates per block...")
    algo_ame002 = calculate_algorithm_detection_rate(df_classified_ame2)
    algo_ame004 = calculate_algorithm_detection_rate(df_classified_ame4)
    
    print(f"  - AME II: {len(algo_ame002)} blok")
    print(f"  - AME IV: {len(algo_ame004)} blok")
    
    # Generate drilldown data (daftar pohon per blok)
    print("\n[5/7] Generating drilldown data (pohon per blok)...")
    drilldown_ame2 = generate_drilldown_data(df_classified_ame2, "AME002 (AME II)")
    drilldown_ame4 = generate_drilldown_data(df_classified_ame4, "AME004 (AME IV)")
    
    # Combine drilldown
    drilldown_all = {**drilldown_ame2, **drilldown_ame4}
    
    total_trees = sum(d['total_detected'] for d in drilldown_all.values())
    print(f"  - Total pohon terdeteksi: {total_trees:,} pohon")
    print(f"  - Dari {len(drilldown_all)} blok")
    
    # Export drilldown CSV
    drilldown_csv = export_drilldown_csv(drilldown_all, output_path)
    print(f"  - Drilldown CSV saved: {drilldown_csv}")
    
    # Generate reports
    print("\n[6/7] Generating early detection reports...")
    
    df_report_ame2 = generate_early_detection_report(algo_ame002, census_ame002, "AME002 (AME II)")
    df_report_ame4 = generate_early_detection_report(algo_ame004, census_ame004, "AME004 (AME IV)")
    
    df_all = pd.concat([df_report_ame2, df_report_ame4], ignore_index=True)
    
    # Save CSV
    csv_path = output_path / "early_detection_report.csv"
    df_all.to_csv(csv_path, index=False)
    print(f"  - CSV saved: {csv_path}")
    
    # Generate HTML with drilldown
    print("\n[7/7] Generating HTML report with drilldown...")
    html_path = output_path / "early_detection_report.html"
    generate_html_report(df_all, html_path, drilldown_data=drilldown_all)

    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    early_detect = len(df_all[df_all['category'] == 'EARLY_DETECT'])
    gold_finds = len(df_all[df_all['significance'] == 'GOLD'])
    matches = len(df_all[df_all['category'] == 'MATCH'])
    under_detect = len(df_all[df_all['category'] == 'UNDER_DETECT'])
    
    print(f"\n🏆 TEMUAN EMAS (>5% diff): {gold_finds} blok")
    print(f"📍 Early Detect (2-5% diff): {early_detect - gold_finds} blok")
    print(f"✅ Match (±2%): {matches} blok")
    print(f"⚠️ Under Detect: {under_detect} blok")
    
    if gold_finds > 0:
        print("\n🏆 BLOK TEMUAN EMAS (prioritas survey tinggi):")
        df_gold = df_all[df_all['significance'] == 'GOLD'].sort_values('diff_pct', ascending=False)
        for _, row in df_gold.head(10).iterrows():
            print(f"  - {row['divisi']} {row['blok']}: Algo {row['algorithm_pct']:.1f}% vs Sensus {row['census_pct']:.1f}% (+{row['diff_pct']:.1f}%)")
    
    print(f"\n✅ Reports saved to: {output_path}")
    print("="*70)


if __name__ == "__main__":
    main()
