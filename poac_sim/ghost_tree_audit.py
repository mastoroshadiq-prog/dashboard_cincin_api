"""
Ghost Tree Audit - Misi 3: Audit Aset

Script ini membandingkan jumlah pohon per blok antara:
- Data Buku (TOTAL_PKK dari data_baru.csv)
- Data Drone (jumlah baris di file NDRE)

Output:
- ghost_tree_audit.csv: Detail per blok
- ghost_tree_audit.html: Laporan visual dengan highlight anomaly

Ghost Trees = Data Buku - Drone Count
Jika positif: Ada pohon di buku yang tidak terdeteksi drone (mati/tumbang tidak terlapor)
Jika negatif: Ada pohon terdeteksi drone tapi tidak di buku (sisipan tidak terlapor)
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

from src.cost_control_loader import (
    load_cost_control_data, get_book_count_dict, normalize_block,
    load_ground_truth_excel, get_ground_truth_book_dict
)
from src.ingestion import load_and_clean_data, load_ame_iv_data


def generate_ghost_tree_charts(df_all: pd.DataFrame) -> dict:
    """Generate charts untuk Ghost Tree Audit."""
    charts = {}
    plt.style.use('dark_background')
    plt.rcParams['font.size'] = 12
    
    # Color scheme
    COLOR_BOOK = '#3498db'    # Blue for Book
    COLOR_DRONE = '#2ecc71'   # Green for Drone
    COLOR_GHOST = '#e74c3c'   # Red for Ghost Trees
    COLOR_EXTRA = '#f39c12'   # Orange for Extra Trees
    
    # Chart 1: Book vs Drone per Divisi - LARGER with proper legend
    fig, ax = plt.subplots(figsize=(14, 8))
    
    divisi_list = df_all['divisi'].unique()
    x = np.arange(len(divisi_list))
    width = 0.35
    
    book_totals = []
    drone_totals = []
    diff_totals = []
    
    for divisi in divisi_list:
        df_div = df_all[df_all['divisi'] == divisi]
        book_totals.append(df_div['book_count'].sum())
        drone_totals.append(df_div['drone_count'].sum())
        diff_totals.append(df_div['ghost_trees'].sum())
    
    # Side by side bars
    bars_book = ax.bar(x - width/2, book_totals, width, label='📚 Data Buku', 
                       color=COLOR_BOOK, edgecolor='white', linewidth=2)
    bars_drone = ax.bar(x + width/2, drone_totals, width, label='🛩️ Deteksi Drone', 
                        color=COLOR_DRONE, edgecolor='white', linewidth=2)
    
    # Labels on bars
    for i, (book, drone, diff) in enumerate(zip(book_totals, drone_totals, diff_totals)):
        ax.text(x[i] - width/2, book + 500, f'{book:,}', ha='center', va='bottom', 
               fontsize=12, fontweight='bold', color=COLOR_BOOK)
        ax.text(x[i] + width/2, drone + 500, f'{drone:,}', ha='center', va='bottom', 
               fontsize=12, fontweight='bold', color=COLOR_DRONE)
        # Difference label
        diff_color = COLOR_GHOST if diff > 0 else COLOR_EXTRA
        ax.text(x[i], max(book, drone) + 2500, f'Selisih: {diff:+,}', ha='center', 
               va='bottom', fontsize=11, color=diff_color, fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels([d.replace('(', '\n(') for d in divisi_list], fontsize=13)
    ax.set_ylabel('Jumlah Pohon', fontsize=14)
    ax.set_title('📚 Data Buku vs 🛩️ Deteksi Drone per Divisi', fontsize=18, fontweight='bold', pad=25)
    ax.legend(loc='upper right', fontsize=13, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Set y limit
    max_val = max(max(book_totals), max(drone_totals))
    ax.set_ylim(0, max_val * 1.25)
    
    # Subtitle
    fig.text(0.5, 0.01, '🔴 Selisih Positif = Ghost Trees (ada di buku, tidak terdeteksi drone) | 🟠 Selisih Negatif = Extra Trees (terdeteksi drone, tidak ada di buku)',
            fontsize=11, ha='center', color='#bdc3c7')
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    charts['book_vs_drone'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # Chart 2: Top 15 Anomali - SUPERIMPOSE Style
    df_anomaly = df_all[df_all['status'] != 'OK'].copy()
    df_anomaly['_diff_abs'] = df_anomaly['ghost_trees'].abs()
    df_anomaly = df_anomaly.sort_values('_diff_abs', ascending=True).tail(15)
    
    if len(df_anomaly) > 0:
        fig, ax = plt.subplots(figsize=(16, 10))
        
        y_pos = np.arange(len(df_anomaly))
        height = 0.7
        
        # Superimpose: Buku di belakang (biru), Drone di depan (hijau)
        bars_book = ax.barh(y_pos, df_anomaly['book_count'], height, 
                           label='📚 Data Buku', color=COLOR_BOOK, alpha=0.6,
                           edgecolor='white', linewidth=1.5)
        bars_drone = ax.barh(y_pos, df_anomaly['drone_count'], height * 0.55, 
                            label='🛩️ Deteksi Drone', color=COLOR_DRONE, alpha=0.95,
                            edgecolor='white', linewidth=1.5)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"{row['blok']} ({row['divisi'][:6]})" for _, row in df_anomaly.iterrows()], 
                          fontsize=12, fontweight='bold')
        ax.set_xlabel('Jumlah Pohon', fontsize=14)
        ax.set_title('👻 Top 15 Anomali Ghost Tree\nPerbandingan Buku vs Drone', 
                    fontsize=18, fontweight='bold', pad=25)
        ax.legend(loc='lower right', fontsize=13, framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        
        # Double labels on right side
        max_x = max(df_anomaly['book_count'].max(), df_anomaly['drone_count'].max())
        label_x = max_x + max_x * 0.05
        
        for i, (_, row) in enumerate(df_anomaly.iterrows()):
            book_val = row['book_count']
            drone_val = row['drone_count']
            ghost = row['ghost_trees']
            
            # Labels
            ax.text(label_x, y_pos[i], f'{book_val:,}', va='center', ha='left', 
                   fontsize=10, color=COLOR_BOOK, fontweight='bold')
            ax.text(label_x + max_x * 0.12, y_pos[i], f'{drone_val:,}', va='center', ha='left', 
                   fontsize=10, color=COLOR_DRONE, fontweight='bold')
            # Ghost difference
            diff_color = COLOR_GHOST if ghost > 0 else COLOR_EXTRA
            ax.text(label_x + max_x * 0.24, y_pos[i], f'{ghost:+,}', va='center', ha='left', 
                   fontsize=10, color=diff_color, fontweight='bold')
        
        # Header labels
        ax.text(label_x + max_x * 0.12, len(df_anomaly) - 0.3, 'Buku    Drone   Selisih', 
               fontsize=10, ha='center', va='bottom', color='#a0a0a0', style='italic')
        
        ax.set_xlim(0, max_x * 1.45)
        
        # Subtitle
        fig.text(0.5, 0.01, '🔵 Bar Biru = Data Buku | 🟢 Bar Hijau = Deteksi Drone | Positif = Ghost, Negatif = Extra',
                fontsize=12, ha='center', color='#bdc3c7')
        
        plt.tight_layout(rect=[0, 0.04, 1, 1])
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#1a1a2e')
        buf.seek(0)
        charts['anomaly_bar'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    # Chart 3: Scatter - Book vs Drone Count - LARGER with better annotations
    fig, ax = plt.subplots(figsize=(16, 12))
    colors_map = {'OK': '#00d26a', 'GHOST_TREES': '#ff4757', 'EXTRA_TREES': '#ffc107'}
    labels_map = {'OK': '✅ OK (Match)', 'GHOST_TREES': '👻 Ghost Trees', 'EXTRA_TREES': '🌳 Extra Trees'}
    
    for status, color in colors_map.items():
        mask = df_all['status'] == status
        if mask.sum() > 0:
            ax.scatter(df_all.loc[mask, 'book_count'], df_all.loc[mask, 'drone_count'],
                      c=color, label=labels_map[status], alpha=0.7, s=120, edgecolors='white', linewidth=1.5)
    
    max_val = max(df_all['book_count'].max(), df_all['drone_count'].max()) + 1000
    ax.plot([0, max_val], [0, max_val], 'w--', linewidth=3, label='Garis Ideal (Buku = Drone)', alpha=0.6)
    
    # Add zone labels
    ax.text(max_val * 0.7, max_val * 0.3, '👻 ZONA GHOST TREES\n(Buku > Drone)', 
           fontsize=14, ha='center', va='center', color='#ff4757', alpha=0.8,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor='#ff4757', alpha=0.9))
    ax.text(max_val * 0.3, max_val * 0.7, '🌳 ZONA EXTRA TREES\n(Drone > Buku)', 
           fontsize=14, ha='center', va='center', color='#ffc107', alpha=0.8,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor='#ffc107', alpha=0.9))
    
    ax.set_xlabel('Data Buku (pohon)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Deteksi Drone (pohon)', fontsize=16, fontweight='bold')
    ax.set_title('Scatter Plot: Perbandingan Per Blok\nSetiap titik = 1 blok', 
                fontsize=20, fontweight='bold', pad=25)
    ax.legend(loc='upper left', fontsize=14, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Subtitle explanation
    fig.text(0.5, 0.01, 
            '📌 Titik di ATAS garis putus = Drone deteksi lebih banyak (Extra Trees) | Titik di BAWAH garis = Buku lebih banyak (Ghost Trees)',
            fontsize=12, ha='center', color='#bdc3c7')
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    charts['scatter'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return charts




def count_trees_per_block_ndre(df_ndre: pd.DataFrame, blok_column: str = 'blok') -> dict:
    """
    Hitung jumlah pohon per blok dari data NDRE.
    
    Args:
        df_ndre: DataFrame NDRE
        blok_column: Nama kolom blok
        
    Returns:
        Dict[blok_normalized, count]
    """
    # Normalize blok names
    df_ndre = df_ndre.copy()
    df_ndre['blok_norm'] = df_ndre[blok_column].apply(normalize_block)
    
    # Count per blok
    counts = df_ndre.groupby('blok_norm').size().to_dict()
    
    return counts


def generate_ghost_tree_report(
    book_data: dict,
    drone_data: dict,
    divisi: str
) -> pd.DataFrame:
    """
    Generate report perbandingan data buku vs drone.
    
    Args:
        book_data: Dict {blok: total_pkk}
        drone_data: Dict {blok: drone_count}
        divisi: Nama divisi untuk labeling
        
    Returns:
        DataFrame dengan analisis ghost tree
    """
    results = []
    
    # Gabungkan semua blok dari kedua sumber
    all_blocks = set(book_data.keys()) | set(drone_data.keys())
    
    for blok in sorted(all_blocks):
        book_count = book_data.get(blok, 0)
        drone_count = drone_data.get(blok, 0)
        
        # Skip blok yang tidak ada di kedua sumber
        if book_count == 0 and drone_count == 0:
            continue
            
        ghost = book_count - drone_count
        ghost_pct = (ghost / book_count * 100) if book_count > 0 else 0
        
        # Kategorisasi
        if book_count == 0:
            status = "NO_BOOK_DATA"
            severity = "INFO"
        elif drone_count == 0:
            status = "NO_DRONE_DATA"
            severity = "WARNING"
        elif abs(ghost_pct) <= 5:
            status = "OK"
            severity = "OK"
        elif ghost_pct > 5:
            status = "GHOST_TREES"
            severity = "CRITICAL" if ghost_pct > 10 else "WARNING"
        else:  # ghost_pct < -5
            status = "EXTRA_TREES"
            severity = "INFO"
        
        results.append({
            'divisi': divisi,
            'blok': blok,
            'book_count': int(book_count),
            'drone_count': int(drone_count),
            'ghost_trees': int(ghost),
            'ghost_pct': round(ghost_pct, 2),
            'status': status,
            'severity': severity
        })
    
    return pd.DataFrame(results)


def generate_html_report(df_all: pd.DataFrame, output_path: Path) -> None:
    """Generate HTML report dengan styling dan charts."""
    
    # Generate charts
    charts = generate_ghost_tree_charts(df_all)
    
    # Calculate summary stats
    total_book = df_all['book_count'].sum()
    total_drone = df_all['drone_count'].sum()
    total_ghost = df_all['ghost_trees'].sum()
    
    ghost_blocks = len(df_all[df_all['status'] == 'GHOST_TREES'])
    critical_blocks = len(df_all[df_all['severity'] == 'CRITICAL'])
    
    html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Tree Audit Report</title>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ color: rgba(255,255,255,0.8); }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: var(--bg-card);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }}
        
        .card h3 {{ color: var(--text-secondary); font-size: 0.9em; margin-bottom: 10px; }}
        .card .value {{ font-size: 2.2em; font-weight: bold; }}
        .card.green .value {{ color: var(--accent-green); }}
        .card.yellow .value {{ color: var(--accent-yellow); }}
        .card.red .value {{ color: var(--accent-red); }}
        .card.blue .value {{ color: var(--accent-blue); }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
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
        
        .status-ok {{ color: var(--accent-green); }}
        .status-warning {{ color: var(--accent-yellow); }}
        .status-critical {{ color: var(--accent-red); }}
        .status-info {{ color: var(--accent-blue); }}
        
        .ghost-positive {{ color: var(--accent-red); font-weight: bold; }}
        .ghost-negative {{ color: var(--accent-blue); }}
        .ghost-zero {{ color: var(--text-secondary); }}
        
        .divisi-header {{
            background: linear-gradient(90deg, #667eea, transparent);
            padding: 15px 20px;
            margin: 30px 0 15px 0;
            border-radius: 10px;
            font-size: 1.3em;
        }}
        
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
            border-left: 4px solid #667eea;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👻 Ghost Tree Audit Report</h1>
            <p>Perbandingan Data Buku vs Deteksi Drone</p>
        </div>
        
        <div class="summary-cards">
            <div class="card blue">
                <h3>Total Pohon (Buku)</h3>
                <div class="value">{total_book:,}</div>
            </div>
            <div class="card green">
                <h3>Total Terdeteksi Drone</h3>
                <div class="value">{total_drone:,}</div>
            </div>
            <div class="card red">
                <h3>Total Ghost Trees</h3>
                <div class="value">{total_ghost:,}</div>
            </div>
            <div class="card yellow">
                <h3>Blok Anomaly</h3>
                <div class="value">{ghost_blocks}</div>
            </div>
            <div class="card red">
                <h3>Blok Critical (&gt;10%)</h3>
                <div class="value">{critical_blocks}</div>
            </div>
        </div>
"""
    
    # Add Charts Section
    html += """
        <div class="charts-section">
            <h2>📊 Visualisasi Data</h2>
            <div class="charts-grid">
"""
    
    if 'book_vs_drone' in charts:
        html += f"""
                <div class="chart-card" style="grid-column: span 2;">
                    <h4>Perbandingan Total Per Divisi</h4>
                    <img src="data:image/png;base64,{charts['book_vs_drone']}" alt="Book vs Drone" style="width: 100%;">
                </div>
"""
    
    if 'anomaly_bar' in charts:
        html += f"""
                <div class="chart-card" style="grid-column: span 2;">
                    <h4>👻 Top 15 Anomali - Perbandingan Buku vs Drone</h4>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; gap: 30px; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="background: #3498db; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">Buku</span>
                            <span style="color: #a0a0a0;">= Jumlah pohon tercatat di data buku</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="background: #2ecc71; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">Drone</span>
                            <span style="color: #a0a0a0;">= Jumlah pohon terdeteksi oleh drone</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="background: #e74c3c; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">Selisih</span>
                            <span style="color: #a0a0a0;">= Buku - Drone (Positif=Ghost, Negatif=Extra)</span>
                        </div>
                    </div>
                    <img src="data:image/png;base64,{charts['anomaly_bar']}" alt="Anomaly Bar" style="width: 100%;">
                </div>
"""

    
    if 'scatter' in charts:
        html += f"""
                <div class="chart-card" style="grid-column: span 2;">
                    <h4>📊 Scatter Plot: Analisis Visual Per Blok</h4>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px 20px; border-radius: 8px; margin-bottom: 15px;">
                        <p style="color: #a0a0a0; margin-bottom: 10px;"><strong>Cara Membaca Chart:</strong></p>
                        <ul style="color: #a0a0a0; margin: 0; padding-left: 20px; list-style-type: none;">
                            <li style="margin-bottom: 5px;">📍 <strong>Setiap titik</strong> = 1 blok (posisi menunjukkan jumlah pohon Buku vs Drone)</li>
                            <li style="margin-bottom: 5px;">📏 <strong>Garis putus-putus</strong> = Garis ideal dimana Buku = Drone (perfect match)</li>
                            <li style="margin-bottom: 5px;">🔴 <strong>Titik di BAWAH garis</strong> = Ghost Trees (Buku > Drone, ada pohon yang tidak terdeteksi)</li>
                            <li style="margin-bottom: 5px;">🟡 <strong>Titik di ATAS garis</strong> = Extra Trees (Drone > Buku, ada pohon tidak tercatat)</li>
                            <li>🟢 <strong>Titik di sekitar garis</strong> = OK, data match</li>
                        </ul>
                    </div>
                    <img src="data:image/png;base64,{charts['scatter']}" alt="Scatter Plot" style="width: 100%;">
                </div>
"""


    
    html += """
            </div>
        </div>
"""
    
    # Add tables per divisi
    for divisi in df_all['divisi'].unique():
        df_div = df_all[df_all['divisi'] == divisi].copy()
        
        html += f"""
        <div class="divisi-header">📍 {divisi}</div>
        <table>
            <thead>
                <tr>
                    <th>Blok</th>
                    <th>Data Buku</th>
                    <th>Drone Count</th>
                    <th>Ghost Trees</th>
                    <th>Ghost %</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
        for _, row in df_div.iterrows():
            # Styling for ghost trees
            if row['ghost_trees'] > 0:
                ghost_class = "ghost-positive"
            elif row['ghost_trees'] < 0:
                ghost_class = "ghost-negative"
            else:
                ghost_class = "ghost-zero"
            
            # Styling for severity
            severity_class = f"status-{row['severity'].lower()}"
            
            html += f"""
                <tr>
                    <td>{row['blok']}</td>
                    <td>{row['book_count']:,}</td>
                    <td>{row['drone_count']:,}</td>
                    <td class="{ghost_class}">{row['ghost_trees']:+,}</td>
                    <td class="{ghost_class}">{row['ghost_pct']:+.1f}%</td>
                    <td class="{severity_class}">{row['status']}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
"""
    
    html += f"""
        <p class="timestamp">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            POAC v3.3 - Algoritma Cincin Api
        </p>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report saved to: {output_path}")


def main():
    """Main function untuk menjalankan Ghost Tree Audit."""
    print("\n" + "="*70)
    print("GHOST TREE AUDIT - MISI 3")
    print("Perbandingan Data Buku vs Deteksi Drone")
    print("="*70)
    
    # Setup paths
    base_path = Path(__file__).parent
    data_path = base_path / "data" / "input"
    output_path = base_path / "data" / "output" / "ghost_tree_audit"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load ground truth data (Excel file - AUTHORITATIVE SOURCE)
    ground_truth_file = data_path / "areal_inti_serangan_gano_AMEII_AMEIV.xlsx"
    print(f"\n[1/4] Loading ground truth book data...")
    print(f"      Source: {ground_truth_file.name}")
    
    df_gt = load_ground_truth_excel(ground_truth_file)
    
    # Split by divisi
    df_ame002 = df_gt[df_gt['DIVISI'] == 'AME002']
    df_ame004 = df_gt[df_gt['DIVISI'] == 'AME004']
    
    book_ame002 = get_ground_truth_book_dict(df_ame002)
    book_ame004 = get_ground_truth_book_dict(df_ame004)
    
    print(f"  - AME002: {len(book_ame002)} blok, {sum(book_ame002.values()):,} pohon (buku)")
    print(f"  - AME004: {len(book_ame004)} blok, {sum(book_ame004.values()):,} pohon (buku)")
    
    # Load NDRE data (drone data)
    print("\n[2/4] Loading NDRE data (drone detections)...")
    df_ndre_ame2 = load_and_clean_data(data_path / "tabelNDREnew.csv")
    df_ndre_ame4 = load_ame_iv_data(data_path / "AME_IV.csv")
    
    drone_ame002 = count_trees_per_block_ndre(df_ndre_ame2, 'Blok')
    drone_ame004 = count_trees_per_block_ndre(df_ndre_ame4, 'Blok')
    
    print(f"  - AME II: {len(drone_ame002)} blok, {sum(drone_ame002.values()):,} pohon (drone)")
    print(f"  - AME IV: {len(drone_ame004)} blok, {sum(drone_ame004.values()):,} pohon (drone)")
    
    # Generate reports
    print("\n[3/4] Generating ghost tree reports...")
    
    df_report_ame2 = generate_ghost_tree_report(book_ame002, drone_ame002, "AME002 (AME II)")
    df_report_ame4 = generate_ghost_tree_report(book_ame004, drone_ame004, "AME004 (AME IV)")
    
    df_all = pd.concat([df_report_ame2, df_report_ame4], ignore_index=True)
    
    # Save CSV
    csv_path = output_path / "ghost_tree_audit.csv"
    df_all.to_csv(csv_path, index=False)
    print(f"  - CSV saved: {csv_path}")
    
    # Generate HTML
    print("\n[4/4] Generating HTML report...")
    html_path = output_path / "ghost_tree_audit.html"
    generate_html_report(df_all, html_path)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    total_ghost = df_all['ghost_trees'].sum()
    ghost_blocks = len(df_all[df_all['status'] == 'GHOST_TREES'])
    critical = len(df_all[df_all['severity'] == 'CRITICAL'])
    
    print(f"\nTotal Ghost Trees: {total_ghost:,} pohon")
    print(f"Blok dengan Ghost Trees (>5%): {ghost_blocks}")
    print(f"Blok Critical (>10%): {critical}")
    
    if critical > 0:
        print("\n⚠️ BLOK CRITICAL (Ghost >10%):")
        df_critical = df_all[df_all['severity'] == 'CRITICAL'].sort_values('ghost_pct', ascending=False)
        for _, row in df_critical.head(10).iterrows():
            print(f"  - {row['divisi']} {row['blok']}: {row['ghost_trees']:+,} ({row['ghost_pct']:+.1f}%)")
    
    print(f"\n✅ Reports saved to: {output_path}")
    print("="*70)


if __name__ == "__main__":
    main()
