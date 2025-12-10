"""
POAC v3.3 - All Presets Runner
Analisis Algoritma Cincin Api dengan SEMUA PRESET sekaligus
Dashboard HTML dengan Toggle Filter per Preset dan Superimpose Visualization

=================================================================
Fitur:
- Jalankan analisis untuk semua 3 preset (Konservatif, Standar, Agresif)
- Generate HTML dashboard dengan toggle filter per preset
- Superimpose visualization untuk perbandingan Top 10 blok
- Statistik perbandingan antar preset
=================================================================

Usage:
    python run_all_presets.py                    # Analisis semua preset
    python run_all_presets.py --divisi AME_II   # Hanya untuk divisi tertentu
"""

import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS
from src.ingestion import load_and_clean_data, load_ame_iv_data, validate_data_integrity, _clean_data
from src.clustering import run_cincin_api_algorithm, get_priority_targets
from src.dashboard import create_dashboard, create_mandor_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Preset display names and colors
PRESET_INFO = {
    "konservatif": {
        "display_name": "Konservatif",
        "color": "#3498db",  # Blue
        "icon": "🔵",
        "marker": "o"
    },
    "standar": {
        "display_name": "Standar", 
        "color": "#27ae60",  # Green
        "icon": "🟢",
        "marker": "s"
    },
    "agresif": {
        "display_name": "Agresif",
        "color": "#e74c3c",  # Red
        "icon": "🔴",
        "marker": "^"
    }
}


def run_single_preset_analysis(df: pd.DataFrame, preset_name: str, divisi_name: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Run analysis for a single preset.
    
    Args:
        df: Input DataFrame
        preset_name: Name of preset (konservatif, standar, agresif)
        divisi_name: Name of divisi
        
    Returns:
        Tuple of (classified DataFrame, metadata dict)
    """
    preset_config = CINCIN_API_PRESETS.get(preset_name, {})
    final_config = {**CINCIN_API_CONFIG, **preset_config}
    
    logger.info(f"Running {preset_name.upper()} preset for {divisi_name}...")
    logger.info(f"  Threshold: {final_config['threshold_min']*100:.0f}% - {final_config['threshold_max']*100:.0f}%")
    logger.info(f"  Min Sick Neighbors: {final_config['min_sick_neighbors']}")
    
    # Run algorithm
    df_classified, metadata = run_cincin_api_algorithm(
        df.copy(),
        auto_tune=True,
        manual_threshold=None,
        config_override=final_config
    )
    
    # Add metadata info
    metadata['preset'] = preset_name
    metadata['divisi'] = divisi_name
    metadata['config'] = final_config
    
    return df_classified, metadata


def create_superimpose_visualization(all_results: Dict, output_dir: Path):
    """
    Create superimposed visualizations for top 10 blocks across all presets.
    
    Args:
        all_results: Dictionary with results per preset
        output_dir: Output directory for images
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    
    logger.info("Creating superimpose visualizations for top blocks...")
    
    # Get all blocks and their MERAH counts per preset
    block_merah_counts = {}
    
    for preset_name, result in all_results.items():
        df_classified = result['df']
        merah_per_block = df_classified[
            df_classified['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)'
        ].groupby('Blok').size()
        
        for blok, count in merah_per_block.items():
            if blok not in block_merah_counts:
                block_merah_counts[blok] = {}
            block_merah_counts[blok][preset_name] = count
    
    # Get union of top 10 blocks from all presets
    all_top_blocks = set()
    for preset_name, result in all_results.items():
        df_classified = result['df']
        merah_per_block = df_classified[
            df_classified['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)'
        ].groupby('Blok').size().sort_values(ascending=False)
        all_top_blocks.update(merah_per_block.head(10).index.tolist())
    
    # Sort by total MERAH across all presets
    block_total = {blok: sum(counts.values()) for blok, counts in block_merah_counts.items() if blok in all_top_blocks}
    sorted_blocks = sorted(block_total.keys(), key=lambda x: block_total[x], reverse=True)[:15]
    
    # =========================================================================
    # 1. Bar Chart Comparison
    # =========================================================================
    fig, ax = plt.subplots(figsize=(16, 10))
    
    x = np.arange(len(sorted_blocks))
    width = 0.25
    
    preset_names = list(PRESET_INFO.keys())
    
    for i, preset_name in enumerate(preset_names):
        counts = [block_merah_counts.get(blok, {}).get(preset_name, 0) for blok in sorted_blocks]
        bars = ax.bar(
            x + (i - 1) * width, 
            counts, 
            width, 
            label=f"{PRESET_INFO[preset_name]['icon']} {PRESET_INFO[preset_name]['display_name']}",
            color=PRESET_INFO[preset_name]['color'],
            alpha=0.8
        )
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.annotate(
                    f'{count}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=8,
                    fontweight='bold'
                )
    
    ax.set_xlabel('Blok', fontsize=12, fontweight='bold')
    ax.set_ylabel('Jumlah Pohon MERAH (Kluster Aktif)', fontsize=12, fontweight='bold')
    ax.set_title('🔥 PERBANDINGAN DETEKSI KLUSTER AKTIF (MERAH) PER PRESET\nTop 15 Blok Terparah', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_blocks, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(output_dir / "superimpose_bar_comparison.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"  Saved: superimpose_bar_comparison.png")
    
    # =========================================================================
    # 2. Line Chart Trend
    # =========================================================================
    fig, ax = plt.subplots(figsize=(16, 10))
    
    for preset_name in preset_names:
        counts = [block_merah_counts.get(blok, {}).get(preset_name, 0) for blok in sorted_blocks]
        ax.plot(
            sorted_blocks, 
            counts, 
            marker=PRESET_INFO[preset_name]['marker'],
            markersize=10,
            linewidth=2.5,
            label=f"{PRESET_INFO[preset_name]['icon']} {PRESET_INFO[preset_name]['display_name']}",
            color=PRESET_INFO[preset_name]['color']
        )
    
    ax.set_xlabel('Blok', fontsize=12, fontweight='bold')
    ax.set_ylabel('Jumlah Pohon MERAH', fontsize=12, fontweight='bold')
    ax.set_title('📈 TREND DETEKSI KLUSTER AKTIF ANTAR PRESET\nTop 15 Blok', 
                 fontsize=14, fontweight='bold')
    ax.set_xticklabels(sorted_blocks, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Fill between to show range
    konservatif_counts = [block_merah_counts.get(blok, {}).get('konservatif', 0) for blok in sorted_blocks]
    agresif_counts = [block_merah_counts.get(blok, {}).get('agresif', 0) for blok in sorted_blocks]
    ax.fill_between(range(len(sorted_blocks)), konservatif_counts, agresif_counts, 
                    alpha=0.15, color='gray', label='Rentang Deteksi')
    
    plt.tight_layout()
    fig.savefig(output_dir / "superimpose_line_trend.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"  Saved: superimpose_line_trend.png")
    
    # =========================================================================
    # 3. Stacked Area Chart - Status Distribution
    # =========================================================================
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    
    status_colors = {
        'MERAH (KLUSTER AKTIF)': '#e74c3c',
        'ORANYE (CINCIN API)': '#f39c12', 
        'KUNING (SUSPECT TERISOLASI)': '#f1c40f',
        'HIJAU (SEHAT)': '#27ae60'
    }
    
    for idx, preset_name in enumerate(preset_names):
        ax = axes[idx]
        result = all_results[preset_name]
        df = result['df']
        
        status_by_block = df.groupby(['Blok', 'Status_Risiko']).size().unstack(fill_value=0)
        
        # Only top 10 blocks by total infected
        status_by_block['infected_total'] = status_by_block.get('MERAH (KLUSTER AKTIF)', 0) + \
                                            status_by_block.get('ORANYE (CINCIN API)', 0)
        top_blocks = status_by_block.nlargest(10, 'infected_total').index.tolist()
        status_by_block = status_by_block.loc[top_blocks].drop(columns=['infected_total'])
        
        # Reorder columns
        ordered_cols = ['MERAH (KLUSTER AKTIF)', 'ORANYE (CINCIN API)', 
                       'KUNING (SUSPECT TERISOLASI)', 'HIJAU (SEHAT)']
        existing_cols = [c for c in ordered_cols if c in status_by_block.columns]
        status_by_block = status_by_block[existing_cols]
        
        colors = [status_colors.get(c, 'gray') for c in existing_cols]
        
        status_by_block.plot(
            kind='bar',
            stacked=True,
            ax=ax,
            color=colors,
            width=0.8
        )
        
        ax.set_title(f"{PRESET_INFO[preset_name]['icon']} {PRESET_INFO[preset_name]['display_name'].upper()}", 
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Blok', fontsize=10)
        ax.set_ylabel('Jumlah Pohon', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(axis='y', alpha=0.3)
    
    fig.suptitle('📊 DISTRIBUSI STATUS PER BLOK - PERBANDINGAN PRESET\nTop 10 Blok Terinfeksi', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(output_dir / "superimpose_stacked_status.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"  Saved: superimpose_stacked_status.png")
    
    # =========================================================================
    # 4. Radar Chart - Overall Comparison
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    categories = ['MERAH\n(Kluster)', 'ORANYE\n(Cincin Api)', 'KUNING\n(Suspect)', 
                  'HIJAU\n(Sehat)', 'Total\nIntervention']
    N = len(categories)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the polygon
    
    for preset_name in preset_names:
        metadata = all_results[preset_name]['metadata']
        
        # Normalize values to percentage
        total = metadata['total_trees']
        values = [
            metadata['merah_count'] / total * 100,
            metadata['oranye_count'] / total * 100,
            metadata['kuning_count'] / total * 100,
            metadata['hijau_count'] / total * 100,
            (metadata['merah_count'] + metadata['oranye_count']) / total * 100
        ]
        values += values[:1]  # Close the polygon
        
        ax.plot(angles, values, linewidth=2.5, linestyle='solid',
                label=f"{PRESET_INFO[preset_name]['icon']} {PRESET_INFO[preset_name]['display_name']}",
                color=PRESET_INFO[preset_name]['color'])
        ax.fill(angles, values, alpha=0.15, color=PRESET_INFO[preset_name]['color'])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    ax.set_title('🎯 RADAR PERBANDINGAN PRESET\n(Persentase dari Total Pohon)', 
                 fontsize=14, fontweight='bold', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
    
    plt.tight_layout()
    fig.savefig(output_dir / "superimpose_radar_comparison.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"  Saved: superimpose_radar_comparison.png")
    
    # =========================================================================
    # 5. Logistics Comparison
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # Asap Cair
    ax1 = axes[0]
    asap_values = [all_results[p]['metadata']['asap_cair_liter'] for p in preset_names]
    bars1 = ax1.bar(
        [PRESET_INFO[p]['display_name'] for p in preset_names],
        asap_values,
        color=[PRESET_INFO[p]['color'] for p in preset_names],
        alpha=0.8
    )
    ax1.set_ylabel('Liter', fontsize=12)
    ax1.set_title('💧 Kebutuhan Asap Cair\n(MERAH × 3L)', fontsize=12, fontweight='bold')
    for bar, val in zip(bars1, asap_values):
        ax1.annotate(f'{val:,.0f} L', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points', ha='center', fontsize=11, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Trichoderma
    ax2 = axes[1]
    tricho_values = [all_results[p]['metadata']['trichoderma_liter'] for p in preset_names]
    bars2 = ax2.bar(
        [PRESET_INFO[p]['display_name'] for p in preset_names],
        tricho_values,
        color=[PRESET_INFO[p]['color'] for p in preset_names],
        alpha=0.8
    )
    ax2.set_ylabel('Liter', fontsize=12)
    ax2.set_title('🧬 Kebutuhan Trichoderma\n(ORANYE × 2L)', fontsize=12, fontweight='bold')
    for bar, val in zip(bars2, tricho_values):
        ax2.annotate(f'{val:,.0f} L', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points', ha='center', fontsize=11, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    fig.suptitle('📦 PERBANDINGAN KEBUTUHAN LOGISTIK ANTAR PRESET', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(output_dir / "superimpose_logistics_comparison.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"  Saved: superimpose_logistics_comparison.png")
    
    return sorted_blocks


def generate_block_cluster_maps(all_results: Dict, output_dir: Path, top_n: int = 5):
    """
    Generate cluster maps for top N blocks for each preset.
    Uses the same format as dashboard.py with hexagonal layout.
    
    Args:
        all_results: Dictionary with results per preset
        output_dir: Output directory
        top_n: Number of top blocks to visualize
        
    Returns:
        Dictionary mapping preset -> list of block image paths
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    logger.info(f"Generating cluster maps for top {top_n} blocks per preset...")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    block_maps = {}
    
    for preset_name, result in all_results.items():
        df = result['df']
        preset_info = PRESET_INFO[preset_name]
        
        # Get top N blocks by MERAH count
        merah_per_block = df[
            df['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)'
        ].groupby('Blok').size().sort_values(ascending=False)
        
        top_blocks = merah_per_block.head(top_n).index.tolist()
        block_maps[preset_name] = []
        
        for idx, blok in enumerate(top_blocks, 1):
            df_block = df[df['Blok'] == blok].copy().reset_index(drop=True)
            
            if len(df_block) == 0:
                continue
            
            # Figure size like dashboard.py
            fig, ax = plt.subplots(figsize=(14, 12))
            
            # Prepare colors, sizes, edge colors based on status (like dashboard.py)
            colors = []
            sizes = []
            edge_colors = []
            edge_widths = []
            
            for _, row in df_block.iterrows():
                status = row['Status_Risiko']
                if status == 'MERAH (KLUSTER AKTIF)':
                    colors.append('#e74c3c')
                    sizes.append(60)
                    edge_colors.append('darkred')
                    edge_widths.append(1)
                elif status == 'ORANYE (CINCIN API)':
                    colors.append('#e67e22')
                    sizes.append(60)
                    edge_colors.append('darkorange')
                    edge_widths.append(1)
                elif status == 'KUNING (SUSPECT TERISOLASI)':
                    colors.append('#f1c40f')
                    sizes.append(60)
                    edge_colors.append('olive')
                    edge_widths.append(1)
                else:  # HIJAU
                    colors.append('#27ae60')
                    sizes.append(60)
                    edge_colors.append('darkgreen')
                    edge_widths.append(0.5)
            
            # Apply hexagonal offset (like dashboard.py)
            x_coords = []
            y_coords = []
            for _, row in df_block.iterrows():
                baris = row['N_BARIS']
                pokok = row['N_POKOK']
                x_offset = 0.5 if baris % 2 == 0 else 0
                x_coords.append(pokok + x_offset)
                y_coords.append(baris)
            
            # Plot in layers (like dashboard.py)
            status_order = ['HIJAU (SEHAT)', 'KUNING (SUSPECT TERISOLASI)', 'ORANYE (CINCIN API)', 'MERAH (KLUSTER AKTIF)']
            
            for status in status_order:
                mask = df_block['Status_Risiko'] == status
                if mask.any():
                    indices = df_block[mask].index.tolist()
                    x_plot = [x_coords[i] for i in indices]
                    y_plot = [y_coords[i] for i in indices]
                    s_plot = [sizes[i] for i in indices]
                    c_plot = [colors[i] for i in indices]
                    ec_plot = [edge_colors[i] for i in indices]
                    ew_plot = [edge_widths[i] for i in indices]
                    
                    ax.scatter(x_plot, y_plot, c=c_plot, s=s_plot, alpha=0.85,
                              edgecolors=ec_plot, linewidths=ew_plot, zorder=status_order.index(status)+1)
            
            # Count statistics
            merah_count = len(df_block[df_block['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)'])
            oranye_count = len(df_block[df_block['Status_Risiko'] == 'ORANYE (CINCIN API)'])
            kuning_count = len(df_block[df_block['Status_Risiko'] == 'KUNING (SUSPECT TERISOLASI)'])
            hijau_count = len(df_block[df_block['Status_Risiko'] == 'HIJAU (SEHAT)'])
            total_count = len(df_block)
            
            # Create legend (like dashboard.py)
            legend_elements = [
                mpatches.Patch(color='#e74c3c', label=f'MERAH - Kluster Aktif ({merah_count})'),
                mpatches.Patch(color='#e67e22', label=f'ORANYE - Cincin Api ({oranye_count})'),
                mpatches.Patch(color='#f1c40f', label=f'KUNING - Suspect ({kuning_count})'),
                mpatches.Patch(color='#27ae60', label=f'HIJAU - Sehat ({hijau_count})')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=11,
                     framealpha=0.9, fancybox=True, shadow=True)
            
            ax.set_xlabel('Nomor Pokok (N_POKOK)', fontsize=12)
            ax.set_ylabel('Nomor Baris (N_BARIS)', fontsize=12)
            
            # Title with preset info
            ax.set_title(
                f'#{idx:02d} - BLOK {blok} - PETA KLUSTER GANODERMA\n'
                f'Total Pohon: {total_count} | MERAH: {merah_count} | KUNING: {kuning_count} | ORANYE: {oranye_count}',
                fontsize=14, fontweight='bold', color='darkred' if idx <= 3 else 'black'
            )
            
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_aspect('equal')
            ax.tick_params(axis='both', which='major', labelsize=10)
            
            # Add rank badge in corner (like dashboard.py)
            ax.text(0.02, 0.98, f'RANK #{idx}', transform=ax.transAxes, fontsize=16,
                   fontweight='bold', color='white',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='#e74c3c' if idx <= 3 else '#f39c12',
                            edgecolor='black', linewidth=2),
                   verticalalignment='top')
            
            # Add preset badge
            ax.text(0.98, 0.98, f'{preset_info["display_name"].upper()}',
                   transform=ax.transAxes, fontsize=12, fontweight='bold',
                   color='white', horizontalalignment='right', verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=preset_info['color'],
                            edgecolor='black', linewidth=1))
            
            plt.tight_layout()
            
            # Save
            filename = f"cluster_map_{preset_name}_{idx:02d}_{blok}.png"
            filepath = output_dir / filename
            fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            
            block_maps[preset_name].append({
                'filename': filename,
                'blok': blok,
                'merah': merah_count,
                'oranye': oranye_count
            })
            
            logger.info(f"  Saved: {filename}")
    
    return block_maps


def generate_html_report_all_presets(output_dir: Path, all_results: Dict, divisi_name: str, block_maps: Dict = None):
    """
    Generate interactive HTML report with toggle filters for each preset.
    
    Args:
        output_dir: Output directory
        all_results: Dictionary with results per preset
        divisi_name: Name of divisi being analyzed
        block_maps: Dictionary of block cluster map images per preset
    """
    logger.info("Generating interactive HTML report with toggle filters...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Calculate combined statistics
    combined_stats = {
        'total_trees': all_results['standar']['metadata']['total_trees'],
        'total_blocks': all_results['standar']['metadata']['stats']['total_blocks']
    }
    
    # Build preset cards HTML
    preset_cards_html = ""
    for preset_name in ['konservatif', 'standar', 'agresif']:
        result = all_results[preset_name]
        meta = result['metadata']
        preset_info = PRESET_INFO[preset_name]
        
        total_intervention = meta['merah_count'] + meta['oranye_count']
        total_logistics = meta['asap_cair_liter'] + meta['trichoderma_liter']
        
        preset_cards_html += f'''
        <div class="preset-card" id="card-{preset_name}" data-preset="{preset_name}">
            <div class="preset-header" style="background: {preset_info['color']};">
                <span class="preset-icon">{preset_info['icon']}</span>
                <span class="preset-name">{preset_info['display_name'].upper()}</span>
                <span class="preset-threshold">Threshold: {meta['optimal_threshold_pct']}</span>
            </div>
            <div class="preset-body">
                <div class="config-info">
                    <small>Min Sick Neighbors: {meta['config']['min_sick_neighbors']}</small>
                </div>
                <div class="status-grid">
                    <div class="status-item merah">
                        <span class="status-label">🔴 MERAH</span>
                        <span class="status-value">{meta['merah_count']:,}</span>
                        <span class="status-pct">({meta['merah_count']/meta['total_trees']*100:.1f}%)</span>
                    </div>
                    <div class="status-item oranye">
                        <span class="status-label">🟠 ORANYE</span>
                        <span class="status-value">{meta['oranye_count']:,}</span>
                        <span class="status-pct">({meta['oranye_count']/meta['total_trees']*100:.1f}%)</span>
                    </div>
                    <div class="status-item kuning">
                        <span class="status-label">🟡 KUNING</span>
                        <span class="status-value">{meta['kuning_count']:,}</span>
                        <span class="status-pct">({meta['kuning_count']/meta['total_trees']*100:.1f}%)</span>
                    </div>
                    <div class="status-item hijau">
                        <span class="status-label">🟢 HIJAU</span>
                        <span class="status-value">{meta['hijau_count']:,}</span>
                        <span class="status-pct">({meta['hijau_count']/meta['total_trees']*100:.1f}%)</span>
                    </div>
                </div>
                <div class="logistics-section">
                    <h4>📦 Kebutuhan Logistik</h4>
                    <div class="logistics-grid">
                        <div class="logistics-item">
                            <span>Asap Cair:</span>
                            <strong>{meta['asap_cair_liter']:,.0f} L</strong>
                        </div>
                        <div class="logistics-item">
                            <span>Trichoderma:</span>
                            <strong>{meta['trichoderma_liter']:,.0f} L</strong>
                        </div>
                        <div class="logistics-item total">
                            <span>Total:</span>
                            <strong>{total_logistics:,.0f} L</strong>
                        </div>
                    </div>
                </div>
                <div class="intervention-summary">
                    <span>🎯 Target Intervensi:</span>
                    <strong>{total_intervention:,} pohon</strong>
                </div>
            </div>
        </div>
        '''
    
    # Build comparison table
    comparison_table = """
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Metrik</th>
                <th>🔵 Konservatif</th>
                <th>🟢 Standar</th>
                <th>🔴 Agresif</th>
                <th>Selisih (Agr-Kon)</th>
            </tr>
        </thead>
        <tbody>
    """
    
    metrics = [
        ('Threshold Optimal', 'optimal_threshold_pct', ''),
        ('MERAH (Kluster)', 'merah_count', ''),
        ('ORANYE (Cincin Api)', 'oranye_count', ''),
        ('KUNING (Suspect)', 'kuning_count', ''),
        ('HIJAU (Sehat)', 'hijau_count', ''),
        ('Asap Cair', 'asap_cair_liter', ' L'),
        ('Trichoderma', 'trichoderma_liter', ' L'),
    ]
    
    for metric_name, key, suffix in metrics:
        kon_val = all_results['konservatif']['metadata'].get(key, 0)
        std_val = all_results['standar']['metadata'].get(key, 0)
        agr_val = all_results['agresif']['metadata'].get(key, 0)
        
        if isinstance(kon_val, str):
            diff = "-"
            kon_disp = kon_val
            std_disp = std_val
            agr_disp = agr_val
        else:
            diff = agr_val - kon_val
            diff_sign = "+" if diff > 0 else ""
            diff = f"{diff_sign}{diff:,.0f}{suffix}"
            kon_disp = f"{kon_val:,.0f}{suffix}" if isinstance(kon_val, (int, float)) else kon_val
            std_disp = f"{std_val:,.0f}{suffix}" if isinstance(std_val, (int, float)) else std_val
            agr_disp = f"{agr_val:,.0f}{suffix}" if isinstance(agr_val, (int, float)) else agr_val
        
        comparison_table += f"""
            <tr>
                <td><strong>{metric_name}</strong></td>
                <td>{kon_disp}</td>
                <td>{std_disp}</td>
                <td>{agr_disp}</td>
                <td class="diff-cell">{diff}</td>
            </tr>
        """
    
    comparison_table += "</tbody></table>"
    
    html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 POAC v3.3 - Perbandingan Preset Algoritma Cincin Api</title>
    <style>
        :root {{
            --merah: #e74c3c;
            --oranye: #f39c12;
            --kuning: #f1c40f;
            --hijau: #27ae60;
            --konservatif: #3498db;
            --standar: #27ae60;
            --agresif: #e74c3c;
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-light: #eee;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg-dark) 0%, #0f0f23 100%);
            color: var(--text-light);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #2d3436 0%, #1a1a2e 100%);
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        header .subtitle {{
            color: #aaa;
            font-size: 1.1em;
        }}
        
        header .meta-info {{
            margin-top: 15px;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            display: flex;
            justify-content: center;
            gap: 40px;
        }}
        
        header .meta-item {{
            display: flex;
            flex-direction: column;
        }}
        
        header .meta-item span:first-child {{
            font-size: 0.85em;
            color: #888;
        }}
        
        header .meta-item span:last-child {{
            font-size: 1.3em;
            font-weight: bold;
        }}
        
        /* Toggle Filter Section */
        .filter-section {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        
        .filter-section h3 {{
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .toggle-container {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .toggle-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px 25px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .toggle-item:hover {{
            background: rgba(255,255,255,0.1);
        }}
        
        .toggle-item.active {{
            border-color: currentColor;
            background: rgba(255,255,255,0.1);
        }}
        
        .toggle-item.konservatif {{ color: var(--konservatif); }}
        .toggle-item.standar {{ color: var(--standar); }}
        .toggle-item.agresif {{ color: var(--agresif); }}
        
        .toggle-switch {{
            width: 50px;
            height: 26px;
            background: #555;
            border-radius: 13px;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .toggle-switch::after {{
            content: '';
            position: absolute;
            width: 22px;
            height: 22px;
            background: white;
            border-radius: 50%;
            top: 2px;
            left: 2px;
            transition: all 0.3s ease;
        }}
        
        .toggle-item.active .toggle-switch {{
            background: currentColor;
        }}
        
        .toggle-item.active .toggle-switch::after {{
            left: 26px;
        }}
        
        /* Preset Cards */
        .preset-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .preset-card {{
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .preset-card.hidden {{
            display: none;
        }}
        
        .preset-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .preset-header {{
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .preset-icon {{
            font-size: 2em;
        }}
        
        .preset-name {{
            font-size: 1.5em;
            font-weight: bold;
            flex: 1;
        }}
        
        .preset-threshold {{
            background: rgba(0,0,0,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .preset-body {{
            padding: 20px;
        }}
        
        .config-info {{
            text-align: center;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            margin-bottom: 15px;
            color: #888;
        }}
        
        .status-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .status-item {{
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .status-item.merah {{ background: rgba(231, 76, 60, 0.2); border-left: 4px solid var(--merah); }}
        .status-item.oranye {{ background: rgba(243, 156, 18, 0.2); border-left: 4px solid var(--oranye); }}
        .status-item.kuning {{ background: rgba(241, 196, 15, 0.2); border-left: 4px solid var(--kuning); }}
        .status-item.hijau {{ background: rgba(39, 174, 96, 0.2); border-left: 4px solid var(--hijau); }}
        
        .status-label {{
            display: block;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .status-value {{
            display: block;
            font-size: 1.8em;
            font-weight: bold;
        }}
        
        .status-pct {{
            display: block;
            font-size: 0.85em;
            color: #888;
        }}
        
        .logistics-section {{
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
        
        .logistics-section h4 {{
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .logistics-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        
        .logistics-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 5px;
        }}
        
        .logistics-item.total {{
            grid-column: span 2;
            background: rgba(255,255,255,0.1);
        }}
        
        .intervention-summary {{
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, rgba(231,76,60,0.2), rgba(243,156,18,0.2));
            border-radius: 10px;
            font-size: 1.1em;
        }}
        
        .intervention-summary strong {{
            font-size: 1.3em;
            margin-left: 10px;
        }}
        
        /* Comparison Table */
        .comparison-section {{
            background: var(--bg-card);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        
        .comparison-section h3 {{
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .comparison-table th,
        .comparison-table td {{
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .comparison-table th {{
            background: rgba(255,255,255,0.1);
            font-weight: bold;
        }}
        
        .comparison-table th:nth-child(2) {{ color: var(--konservatif); }}
        .comparison-table th:nth-child(3) {{ color: var(--standar); }}
        .comparison-table th:nth-child(4) {{ color: var(--agresif); }}
        
        .comparison-table tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        
        .diff-cell {{
            font-weight: bold;
            color: #f39c12;
        }}
        
        /* Visualizations */
        .visualizations {{
            background: var(--bg-card);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        
        .visualizations h3 {{
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }}
        
        .viz-item {{
            text-align: center;
        }}
        
        .viz-item img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .viz-item h4 {{
            margin-top: 10px;
            color: #aaa;
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 30px;
        }}
        
        /* Lightbox for fullscreen zoom */
        .lightbox {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }}
        
        .lightbox.active {{
            display: flex;
        }}
        
        .lightbox-content {{
            max-width: 95%;
            max-height: 85%;
            position: relative;
        }}
        
        .lightbox-content img {{
            max-width: 100%;
            max-height: 80vh;
            border-radius: 10px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.5);
        }}
        
        .lightbox-title {{
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 1.2em;
        }}
        
        .lightbox-close {{
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 40px;
            color: white;
            cursor: pointer;
            z-index: 10000;
            transition: all 0.3s ease;
        }}
        
        .lightbox-close:hover {{
            color: #e74c3c;
            transform: scale(1.2);
        }}
        
        .lightbox-nav {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            font-size: 50px;
            color: white;
            cursor: pointer;
            padding: 20px;
            transition: all 0.3s ease;
            user-select: none;
        }}
        
        .lightbox-nav:hover {{
            color: #3498db;
        }}
        
        .lightbox-prev {{
            left: 20px;
        }}
        
        .lightbox-next {{
            right: 20px;
        }}
        
        .lightbox-counter {{
            color: #888;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .lightbox-zoom-controls {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
        }}
        
        .lightbox-zoom-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }}
        
        .lightbox-zoom-btn:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        /* Image container with zoom icon */
        .viz-item {{
            text-align: center;
            position: relative;
        }}
        
        .viz-item img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .viz-item img:hover {{
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }}
        
        .viz-item .zoom-icon {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 14px;
            opacity: 0;
            transition: all 0.3s ease;
            pointer-events: none;
        }}
        
        .viz-item:hover .zoom-icon {{
            opacity: 1;
        }}
        
        .viz-item h4 {{
            margin-top: 10px;
            color: #aaa;
        }}
        
        /* Block Maps Section */
        .block-maps {{
            background: var(--bg-card);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        
        .block-maps h3 {{
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .block-maps-tabs {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .block-maps-tab {{
            padding: 12px 25px;
            border: 2px solid transparent;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        
        .block-maps-tab.konservatif {{
            background: rgba(52, 152, 219, 0.2);
            color: var(--konservatif);
        }}
        
        .block-maps-tab.standar {{
            background: rgba(39, 174, 96, 0.2);
            color: var(--standar);
        }}
        
        .block-maps-tab.agresif {{
            background: rgba(231, 76, 60, 0.2);
            color: var(--agresif);
        }}
        
        .block-maps-tab.active {{
            border-color: currentColor;
            transform: scale(1.05);
        }}
        
        .block-maps-tab:hover {{
            transform: scale(1.05);
        }}
        
        .block-maps-content {{
            display: none;
        }}
        
        .block-maps-content.active {{
            display: block;
        }}
        
        .block-maps-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .block-map-item {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .block-map-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .block-map-item img {{
            width: 100%;
            cursor: pointer;
        }}
        
        .block-map-info {{
            padding: 15px;
            text-align: center;
        }}
        
        .block-map-info h4 {{
            margin-bottom: 5px;
        }}
        
        .block-map-info .stats {{
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 0.9em;
        }}
        
        .block-map-info .stat-merah {{
            color: var(--merah);
        }}
        
        .block-map-info .stat-oranye {{
            color: var(--oranye);
        }}
        
        @media (max-width: 768px) {{
            .preset-cards {{
                grid-template-columns: 1fr;
            }}
            
            .toggle-container {{
                flex-direction: column;
            }}
            
            .viz-grid {{
                grid-template-columns: 1fr;
            }}
            
            header .meta-info {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .block-maps-grid {{
                grid-template-columns: 1fr;
            }}
            
            .lightbox-nav {{
                font-size: 30px;
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 POAC v3.3 - Algoritma Cincin Api</h1>
            <p class="subtitle">Perbandingan Hasil Analisis Semua Preset</p>
            <div class="meta-info">
                <div class="meta-item">
                    <span>Divisi</span>
                    <span>{divisi_name}</span>
                </div>
                <div class="meta-item">
                    <span>Total Pohon</span>
                    <span>{combined_stats['total_trees']:,}</span>
                </div>
                <div class="meta-item">
                    <span>Total Blok</span>
                    <span>{combined_stats['total_blocks']}</span>
                </div>
                <div class="meta-item">
                    <span>Generated</span>
                    <span>{timestamp}</span>
                </div>
            </div>
        </header>
        
        <!-- Toggle Filter Section -->
        <section class="filter-section">
            <h3>🎚️ Filter Preset (Klik untuk Toggle)</h3>
            <div class="toggle-container">
                <div class="toggle-item konservatif active" data-preset="konservatif" onclick="togglePreset('konservatif')">
                    <span class="toggle-switch"></span>
                    <span>🔵 Konservatif</span>
                    <small>(Deteksi Ketat)</small>
                </div>
                <div class="toggle-item standar active" data-preset="standar" onclick="togglePreset('standar')">
                    <span class="toggle-switch"></span>
                    <span>🟢 Standar</span>
                    <small>(Seimbang)</small>
                </div>
                <div class="toggle-item agresif active" data-preset="agresif" onclick="togglePreset('agresif')">
                    <span class="toggle-switch"></span>
                    <span>🔴 Agresif</span>
                    <small>(Deteksi Luas)</small>
                </div>
            </div>
        </section>
        
        <!-- Preset Cards -->
        <section class="preset-cards">
            {preset_cards_html}
        </section>
        
        <!-- Comparison Table -->
        <section class="comparison-section">
            <h3>📊 Tabel Perbandingan Detail</h3>
            {comparison_table}
        </section>
        
        <!-- Superimpose Visualizations -->
        <section class="visualizations">
            <h3>📈 Visualisasi Perbandingan (Superimpose) - Klik gambar untuk fullscreen</h3>
            <div class="viz-grid">
                <div class="viz-item" onclick="openLightbox(0)">
                    <span class="zoom-icon">🔍 Klik untuk zoom</span>
                    <img src="superimpose_bar_comparison.png" alt="Bar Comparison" data-title="Perbandingan Deteksi Kluster Aktif per Blok">
                    <h4>Perbandingan Deteksi Kluster Aktif per Blok</h4>
                </div>
                <div class="viz-item" onclick="openLightbox(1)">
                    <span class="zoom-icon">🔍 Klik untuk zoom</span>
                    <img src="superimpose_line_trend.png" alt="Line Trend" data-title="Trend Deteksi Antar Preset">
                    <h4>Trend Deteksi Antar Preset</h4>
                </div>
                <div class="viz-item" onclick="openLightbox(2)">
                    <span class="zoom-icon">🔍 Klik untuk zoom</span>
                    <img src="superimpose_stacked_status.png" alt="Stacked Status" data-title="Distribusi Status per Blok">
                    <h4>Distribusi Status per Blok</h4>
                </div>
                <div class="viz-item" onclick="openLightbox(3)">
                    <span class="zoom-icon">🔍 Klik untuk zoom</span>
                    <img src="superimpose_radar_comparison.png" alt="Radar Comparison" data-title="Radar Perbandingan Preset">
                    <h4>Radar Perbandingan Preset</h4>
                </div>
                <div class="viz-item" style="grid-column: span 2;" onclick="openLightbox(4)">
                    <span class="zoom-icon">🔍 Klik untuk zoom</span>
                    <img src="superimpose_logistics_comparison.png" alt="Logistics Comparison" data-title="Perbandingan Kebutuhan Logistik">
                    <h4>Perbandingan Kebutuhan Logistik</h4>
                </div>
            </div>
        </section>'''
    
    # Build block maps section if available
    block_maps_html = ""
    if block_maps:
        tabs_html = ""
        contents_html = ""
        
        for preset_name in ['konservatif', 'standar', 'agresif']:
            preset_info = PRESET_INFO[preset_name]
            active_class = "active" if preset_name == "standar" else ""
            
            tabs_html += f'''
                <div class="block-maps-tab {preset_name} {active_class}" 
                     onclick="switchBlockMapTab('{preset_name}')">
                    {preset_info['icon']} {preset_info['display_name']}
                </div>
            '''
            
            maps_grid = ""
            if preset_name in block_maps:
                for map_info in block_maps[preset_name]:
                    maps_grid += f'''
                        <div class="block-map-item">
                            <img src="{map_info['filename']}" 
                                 alt="Blok {map_info['blok']}"
                                 onclick="openBlockMapLightbox('{map_info['filename']}', 'Blok {map_info['blok']} - {preset_info['display_name']}')">
                            <div class="block-map-info">
                                <h4>Blok {map_info['blok']}</h4>
                                <div class="stats">
                                    <span class="stat-merah">🔴 MERAH: {map_info['merah']}</span>
                                    <span class="stat-oranye">🟠 ORANYE: {map_info['oranye']}</span>
                                </div>
                            </div>
                        </div>
                    '''
            
            contents_html += f'''
                <div class="block-maps-content {preset_name} {active_class}">
                    <div class="block-maps-grid">
                        {maps_grid}
                    </div>
                </div>
            '''
        
        block_maps_html = f'''
        <!-- Block Cluster Maps -->
        <section class="block-maps">
            <h3>🗺️ Peta Kluster Ganoderma per Blok (Top 5) - Klik gambar untuk fullscreen</h3>
            <div class="block-maps-tabs">
                {tabs_html}
            </div>
            {contents_html}
        </section>
        '''
    
    html_content += block_maps_html
    
    html_content += f'''
        <footer>
            <p>Generated by POAC v3.3 Simulation Engine - Algoritma Cincin Api</p>
            <p>© 2025 - Ganoderma Detection System</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                💡 Tips: Tekan tombol 1, 2, 3 untuk toggle preset | Klik gambar untuk fullscreen | ESC untuk keluar
            </p>
        </footer>
    </div>
    
    <!-- Lightbox Modal -->
    <div class="lightbox" id="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <span class="lightbox-nav lightbox-prev" onclick="navigateLightbox(-1)">&#10094;</span>
        <span class="lightbox-nav lightbox-next" onclick="navigateLightbox(1)">&#10095;</span>
        <div class="lightbox-content">
            <img id="lightbox-img" src="" alt="">
            <div class="lightbox-title" id="lightbox-title"></div>
            <div class="lightbox-counter" id="lightbox-counter"></div>
        </div>
        <div class="lightbox-zoom-controls">
            <button class="lightbox-zoom-btn" onclick="zoomLightbox(0.8)">➖ Zoom Out</button>
            <button class="lightbox-zoom-btn" onclick="zoomLightbox(1)">↺ Reset</button>
            <button class="lightbox-zoom-btn" onclick="zoomLightbox(1.2)">➕ Zoom In</button>
            <button class="lightbox-zoom-btn" onclick="downloadImage()">💾 Download</button>
        </div>
    </div>
    
    <script>
        // Toggle preset visibility
        const activePresets = new Set(['konservatif', 'standar', 'agresif']);
        
        function togglePreset(preset) {{
            const toggleItem = document.querySelector(`.toggle-item.${{preset}}`);
            const card = document.querySelector(`#card-${{preset}}`);
            
            if (activePresets.has(preset)) {{
                activePresets.delete(preset);
                toggleItem.classList.remove('active');
                card.classList.add('hidden');
            }} else {{
                activePresets.add(preset);
                toggleItem.classList.add('active');
                card.classList.remove('hidden');
            }}
        }}
        
        // Block maps tab switching
        function switchBlockMapTab(preset) {{
            document.querySelectorAll('.block-maps-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.block-maps-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(`.block-maps-tab.${{preset}}`).classList.add('active');
            document.querySelector(`.block-maps-content.${{preset}}`).classList.add('active');
        }}
        
        // Lightbox functionality
        const images = [
            {{ src: 'superimpose_bar_comparison.png', title: 'Perbandingan Deteksi Kluster Aktif per Blok' }},
            {{ src: 'superimpose_line_trend.png', title: 'Trend Deteksi Antar Preset' }},
            {{ src: 'superimpose_stacked_status.png', title: 'Distribusi Status per Blok' }},
            {{ src: 'superimpose_radar_comparison.png', title: 'Radar Perbandingan Preset' }},
            {{ src: 'superimpose_logistics_comparison.png', title: 'Perbandingan Kebutuhan Logistik' }}
        ];
        
        let currentImageIndex = 0;
        let currentZoom = 1;
        
        function openLightbox(index) {{
            currentImageIndex = index;
            currentZoom = 1;
            updateLightbox();
            document.getElementById('lightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        
        function openBlockMapLightbox(src, title) {{
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox-img').style.transform = 'scale(1)';
            document.getElementById('lightbox-title').textContent = title;
            document.getElementById('lightbox-counter').textContent = '';
            document.querySelector('.lightbox-prev').style.display = 'none';
            document.querySelector('.lightbox-next').style.display = 'none';
            document.getElementById('lightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
            currentZoom = 1;
        }}
        
        function updateLightbox() {{
            const img = document.getElementById('lightbox-img');
            img.src = images[currentImageIndex].src;
            img.style.transform = `scale(${{currentZoom}})`;
            document.getElementById('lightbox-title').textContent = images[currentImageIndex].title;
            document.getElementById('lightbox-counter').textContent = `${{currentImageIndex + 1}} / ${{images.length}}`;
            document.querySelector('.lightbox-prev').style.display = 'block';
            document.querySelector('.lightbox-next').style.display = 'block';
        }}
        
        function closeLightbox() {{
            document.getElementById('lightbox').classList.remove('active');
            document.body.style.overflow = 'auto';
        }}
        
        function navigateLightbox(direction) {{
            currentImageIndex = (currentImageIndex + direction + images.length) % images.length;
            currentZoom = 1;
            updateLightbox();
        }}
        
        function zoomLightbox(factor) {{
            if (factor === 1) {{
                currentZoom = 1;
            }} else {{
                currentZoom *= factor;
                currentZoom = Math.max(0.5, Math.min(3, currentZoom));
            }}
            document.getElementById('lightbox-img').style.transform = `scale(${{currentZoom}})`;
        }}
        
        function downloadImage() {{
            const img = document.getElementById('lightbox-img');
            const link = document.createElement('a');
            link.href = img.src;
            link.download = img.src.split('/').pop();
            link.click();
        }}
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {{
            if (e.key === '1') togglePreset('konservatif');
            if (e.key === '2') togglePreset('standar');
            if (e.key === '3') togglePreset('agresif');
            
            // Lightbox navigation
            if (document.getElementById('lightbox').classList.contains('active')) {{
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') navigateLightbox(-1);
                if (e.key === 'ArrowRight') navigateLightbox(1);
                if (e.key === '+' || e.key === '=') zoomLightbox(1.2);
                if (e.key === '-') zoomLightbox(0.8);
                if (e.key === '0') zoomLightbox(1);
            }}
        }});
        
        // Close lightbox when clicking outside image
        document.getElementById('lightbox').addEventListener('click', (e) => {{
            if (e.target.id === 'lightbox') {{
                closeLightbox();
            }}
        }});
    </script>
</body>
</html>
'''
    
    html_path = output_dir / "report_all_presets.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"HTML Report generated: {html_path}")
    return html_path


def main(divisi: str = "AME_II"):
    """
    Main entry point untuk analisis semua preset.
    
    Args:
        divisi: Divisi yang akan dianalisis ("AME_II", "AME_IV", atau "ALL")
    """
    print("\n" + "=" * 70)
    print("🔥 POAC v3.3 - ALGORITMA CINCIN API (ALL PRESETS)")
    print("Analisis dengan Konservatif, Standar, dan Agresif")
    print("=" * 70 + "\n")
    
    base_dir = Path(__file__).parent
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = base_dir / "data" / "output" / "cincin_api" / f"{timestamp}_all_presets_{divisi}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output folder: {output_dir.name}\n")
    
    # Load data based on divisi
    print("=" * 70)
    print(f"📂 LOADING DATA {divisi}")
    print("-" * 40)
    
    if divisi == "AME_II":
        input_path = base_dir / "data" / "input" / "tabelNDREnew.csv"
        df = load_and_clean_data(input_path)
        divisi_name = "AME II"
    elif divisi == "AME_IV":
        input_path = base_dir / "data" / "input" / "AME_IV.csv"
        df = load_ame_iv_data(input_path)
        divisi_name = "AME IV"
    elif divisi == "ALL":
        # Load and combine both divisions
        print("Loading AME II...")
        input_path_ii = base_dir / "data" / "input" / "tabelNDREnew.csv"
        df_ii = load_and_clean_data(input_path_ii)
        
        print("Loading AME IV...")
        input_path_iv = base_dir / "data" / "input" / "AME_IV.csv"
        df_iv = load_ame_iv_data(input_path_iv)
        
        # Combine dataframes
        df = pd.concat([df_ii, df_iv], ignore_index=True)
        divisi_name = "ALL (AME II + AME IV)"
    else:
        print(f"ERROR: Divisi '{divisi}' tidak dikenali. Gunakan AME_II, AME_IV, atau ALL")
        return
    
    # Validate data
    stats = validate_data_integrity(df)
    print(f"\n✅ Data loaded: {stats['total_rows']:,} pohon, {stats['total_blocks']} blok")
    
    # Run analysis for each preset
    all_results = {}
    presets = ['konservatif', 'standar', 'agresif']
    
    print("\n" + "=" * 70)
    print("🔄 RUNNING ANALYSIS FOR ALL PRESETS")
    print("=" * 70)
    
    for preset_name in presets:
        print(f"\n{'─' * 50}")
        df_classified, metadata = run_single_preset_analysis(df, preset_name, divisi_name)
        metadata['stats'] = stats
        
        all_results[preset_name] = {
            'df': df_classified,
            'metadata': metadata
        }
        
        # Print summary
        print(f"  ✅ {preset_name.upper()} complete:")
        print(f"     Threshold: {metadata['optimal_threshold_pct']}")
        print(f"     MERAH: {metadata['merah_count']:,} | ORANYE: {metadata['oranye_count']:,}")
        print(f"     Logistik: {metadata['asap_cair_liter']:,.0f}L Asap + {metadata['trichoderma_liter']:,.0f}L Tricho")
        
        # Save per-preset CSV
        preset_dir = output_dir / preset_name
        preset_dir.mkdir(parents=True, exist_ok=True)
        df_classified.to_csv(preset_dir / "hasil_klasifikasi.csv", index=False)
    
    # Print comparison
    print("\n" + "=" * 70)
    print("📊 PERBANDINGAN HASIL ANALISIS")
    print("=" * 70)
    
    print("\n┌" + "─" * 82 + "┐")
    print("│" + " " * 20 + "PERBANDINGAN KONSERVATIF vs STANDAR vs AGRESIF" + " " * 17 + "│")
    print("├" + "─" * 26 + "┬" + "─" * 18 + "┬" + "─" * 18 + "┬" + "─" * 17 + "┤")
    print("│         Metrik           │   Konservatif    │     Standar      │     Agresif     │")
    print("├" + "─" * 26 + "┼" + "─" * 18 + "┼" + "─" * 18 + "┼" + "─" * 17 + "┤")
    
    for label, key in [("Threshold", "optimal_threshold_pct"), 
                       ("🔴 MERAH", "merah_count"),
                       ("🟠 ORANYE", "oranye_count"),
                       ("🟡 KUNING", "kuning_count"),
                       ("🟢 HIJAU", "hijau_count"),
                       ("📦 Asap Cair", "asap_cair_liter"),
                       ("📦 Trichoderma", "trichoderma_liter")]:
        
        kon = all_results['konservatif']['metadata'][key]
        std = all_results['standar']['metadata'][key]
        agr = all_results['agresif']['metadata'][key]
        
        if isinstance(kon, str):
            print(f"│  {label:<22}  │  {kon:^14}  │  {std:^14}  │  {agr:^13}  │")
        else:
            print(f"│  {label:<22}  │  {kon:>12,.0f}    │  {std:>12,.0f}    │  {agr:>11,.0f}   │")
    
    print("└" + "─" * 26 + "┴" + "─" * 18 + "┴" + "─" * 18 + "┴" + "─" * 17 + "┘")
    
    # Generate superimpose visualizations
    print("\n" + "=" * 70)
    print("📈 GENERATING SUPERIMPOSE VISUALIZATIONS")
    print("-" * 40)
    
    create_superimpose_visualization(all_results, output_dir)
    
    # Generate block cluster maps
    print("\n" + "=" * 70)
    print("🗺️ GENERATING BLOCK CLUSTER MAPS")
    print("-" * 40)
    
    block_maps = generate_block_cluster_maps(all_results, output_dir, top_n=5)
    
    # Generate HTML report
    print("\n" + "=" * 70)
    print("📝 GENERATING INTERACTIVE HTML REPORT")
    print("-" * 40)
    
    html_path = generate_html_report_all_presets(output_dir, all_results, divisi_name, block_maps)
    
    print(f"\n🌐 HTML Report: {html_path}")
    print("   → Buka file ini di browser untuk laporan interaktif dengan toggle filter!")
    print("   → Klik gambar untuk zoom/fullscreen!")
    print("   → Gunakan keyboard: 1/2/3 untuk toggle preset, ←/→ untuk navigasi, +/- untuk zoom")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ANALISIS SEMUA PRESET SELESAI!")
    print(f"📁 Semua file tersimpan di: {output_dir}")
    print("=" * 70)
    
    return all_results, output_dir


def run_multi_divisi_analysis():
    """
    Jalankan analisis untuk SEMUA divisi secara bersamaan,
    dengan hasil terpisah per divisi di dashboard.
    """
    print("\n" + "=" * 70)
    print("🔥 POAC v3.3 - ALGORITMA CINCIN API (MULTI-DIVISI)")
    print("Analisis AME II dan AME IV secara bersamaan")
    print("=" * 70 + "\n")
    
    base_dir = Path(__file__).parent
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = base_dir / "data" / "output" / "cincin_api" / f"{timestamp}_multi_divisi"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output folder: {output_dir.name}\n")
    
    # Load data for both divisions
    print("=" * 70)
    print("📂 LOADING DATA FOR ALL DIVISIONS")
    print("-" * 40)
    
    # Load AME II
    print("\n📍 Loading AME II...")
    input_path_ii = base_dir / "data" / "input" / "tabelNDREnew.csv"
    df_ame_ii = load_and_clean_data(input_path_ii)
    stats_ii = validate_data_integrity(df_ame_ii)
    print(f"   ✅ AME II: {stats_ii['total_rows']:,} pohon, {stats_ii['total_blocks']} blok")
    
    # Load AME IV
    print("\n📍 Loading AME IV...")
    input_path_iv = base_dir / "data" / "input" / "AME_IV.csv"
    df_ame_iv = load_ame_iv_data(input_path_iv)
    stats_iv = validate_data_integrity(df_ame_iv)
    print(f"   ✅ AME IV: {stats_iv['total_rows']:,} pohon, {stats_iv['total_blocks']} blok")
    
    # Store all results per division
    all_divisi_results = {}
    all_block_maps = {}
    presets = ['konservatif', 'standar', 'agresif']
    
    # Analyze AME II
    print("\n" + "=" * 70)
    print("🔄 ANALYZING AME II")
    print("=" * 70)
    
    all_divisi_results['AME II'] = {}
    for preset_name in presets:
        print(f"\n{'─' * 50}")
        df_classified, metadata = run_single_preset_analysis(df_ame_ii, preset_name, "AME II")
        metadata['stats'] = stats_ii
        
        all_divisi_results['AME II'][preset_name] = {
            'df': df_classified,
            'metadata': metadata
        }
        
        print(f"  ✅ AME II - {preset_name.upper()}:")
        print(f"     Threshold: {metadata['optimal_threshold_pct']}")
        print(f"     MERAH: {metadata['merah_count']:,} | ORANYE: {metadata['oranye_count']:,}")
    
    # Generate block maps for AME II
    print(f"\n📸 Generating cluster maps for AME II...")
    all_block_maps['AME II'] = generate_block_cluster_maps(all_divisi_results['AME II'], output_dir / "AME_II", top_n=5)
    
    # Analyze AME IV
    print("\n" + "=" * 70)
    print("🔄 ANALYZING AME IV")
    print("=" * 70)
    
    all_divisi_results['AME IV'] = {}
    for preset_name in presets:
        print(f"\n{'─' * 50}")
        df_classified, metadata = run_single_preset_analysis(df_ame_iv, preset_name, "AME IV")
        metadata['stats'] = stats_iv
        
        all_divisi_results['AME IV'][preset_name] = {
            'df': df_classified,
            'metadata': metadata
        }
        
        print(f"  ✅ AME IV - {preset_name.upper()}:")
        print(f"     Threshold: {metadata['optimal_threshold_pct']}")
        print(f"     MERAH: {metadata['merah_count']:,} | ORANYE: {metadata['oranye_count']:,}")
    
    # Generate block maps for AME IV
    print(f"\n📸 Generating cluster maps for AME IV...")
    all_block_maps['AME IV'] = generate_block_cluster_maps(all_divisi_results['AME IV'], output_dir / "AME_IV", top_n=5)
    
    # Print comparison tables
    print("\n" + "=" * 70)
    print("📊 PERBANDINGAN HASIL ANALISIS")
    print("=" * 70)
    
    for divisi_name in ['AME II', 'AME IV']:
        results = all_divisi_results[divisi_name]
        print(f"\n┌{'─' * 80}┐")
        print(f"│{divisi_name:^80}│")
        print(f"├{'─' * 26}┬{'─' * 17}┬{'─' * 17}┬{'─' * 17}┤")
        print(f"│{'Metrik':^26}│{'Konservatif':^17}│{'Standar':^17}│{'Agresif':^17}│")
        print(f"├{'─' * 26}┼{'─' * 17}┼{'─' * 17}┼{'─' * 17}┤")
        
        print(f"│  {'Threshold':<24}│{results['konservatif']['metadata']['optimal_threshold_pct']:^17}│{results['standar']['metadata']['optimal_threshold_pct']:^17}│{results['agresif']['metadata']['optimal_threshold_pct']:^17}│")
        print(f"│  {'🔴 MERAH':<24}│{results['konservatif']['metadata']['merah_count']:>13,}    │{results['standar']['metadata']['merah_count']:>13,}    │{results['agresif']['metadata']['merah_count']:>13,}    │")
        print(f"│  {'🟠 ORANYE':<24}│{results['konservatif']['metadata']['oranye_count']:>13,}    │{results['standar']['metadata']['oranye_count']:>13,}    │{results['agresif']['metadata']['oranye_count']:>13,}    │")
        print(f"│  {'🟡 KUNING':<24}│{results['konservatif']['metadata']['kuning_count']:>13,}    │{results['standar']['metadata']['kuning_count']:>13,}    │{results['agresif']['metadata']['kuning_count']:>13,}    │")
        print(f"│  {'🟢 HIJAU':<24}│{results['konservatif']['metadata']['hijau_count']:>13,}    │{results['standar']['metadata']['hijau_count']:>13,}    │{results['agresif']['metadata']['hijau_count']:>13,}    │")
        print(f"│  {'📦 Asap Cair':<24}│{results['konservatif']['metadata']['asap_cair_liter']:>13,.0f}    │{results['standar']['metadata']['asap_cair_liter']:>13,.0f}    │{results['agresif']['metadata']['asap_cair_liter']:>13,.0f}    │")
        print(f"│  {'📦 Trichoderma':<24}│{results['konservatif']['metadata']['trichoderma_liter']:>13,.0f}    │{results['standar']['metadata']['trichoderma_liter']:>13,.0f}    │{results['agresif']['metadata']['trichoderma_liter']:>13,.0f}    │")
        print(f"└{'─' * 26}┴{'─' * 17}┴{'─' * 17}┴{'─' * 17}┘")
    
    # Generate superimpose visualizations per divisi
    print("\n" + "=" * 70)
    print("📈 GENERATING VISUALIZATIONS")
    print("-" * 40)
    
    for divisi_name in ['AME II', 'AME IV']:
        divisi_folder = divisi_name.replace(' ', '_')
        divisi_output = output_dir / divisi_folder
        divisi_output.mkdir(exist_ok=True)
        
        print(f"\n📊 Creating visualizations for {divisi_name}...")
        create_superimpose_visualization(all_divisi_results[divisi_name], divisi_output)
    
    # Generate multi-divisi HTML report
    print("\n" + "=" * 70)
    print("📝 GENERATING MULTI-DIVISI HTML REPORT")
    print("-" * 40)
    
    html_path = generate_multi_divisi_html_report(output_dir, all_divisi_results, all_block_maps)
    
    print(f"\n🌐 HTML Report: {html_path}")
    print("   → Buka file ini di browser untuk laporan interaktif!")
    print("   → Dashboard dengan tab terpisah untuk AME II dan AME IV")
    print("   → Klik gambar untuk zoom/fullscreen!")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ANALISIS MULTI-DIVISI SELESAI!")
    print(f"📁 Semua file tersimpan di: {output_dir}")
    print("=" * 70)
    
    return all_divisi_results, output_dir


def generate_multi_divisi_html_report(output_dir: Path, all_divisi_results: Dict, all_block_maps: Dict):
    """
    Generate HTML report dengan tab terpisah untuk setiap divisi.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Build divisi tabs and content
    divisi_tabs_html = ""
    divisi_content_html = ""
    
    for idx, (divisi_name, results) in enumerate(all_divisi_results.items()):
        divisi_id = divisi_name.replace(' ', '_')
        active_class = "active" if idx == 0 else ""
        
        # Tab button
        divisi_tabs_html += f'''
            <button class="divisi-tab {active_class}" onclick="switchDivisi('{divisi_id}')" data-divisi="{divisi_id}">
                📍 {divisi_name}
            </button>
        '''
        
        # Stats for this divisi
        stats = results['standar']['metadata']['stats']
        
        # Build preset cards for this divisi
        preset_cards = ""
        for preset_name in ['konservatif', 'standar', 'agresif']:
            meta = results[preset_name]['metadata']
            preset_info = PRESET_INFO[preset_name]
            total_intervention = meta['merah_count'] + meta['oranye_count']
            total_logistics = meta['asap_cair_liter'] + meta['trichoderma_liter']
            
            preset_cards += f'''
            <div class="preset-card" data-preset="{preset_name}">
                <div class="preset-header" style="background: {preset_info['color']};">
                    <span class="preset-icon">{preset_info['icon']}</span>
                    <span class="preset-name">{preset_info['display_name'].upper()}</span>
                    <span class="preset-threshold">Threshold: {meta['optimal_threshold_pct']}</span>
                </div>
                <div class="preset-body">
                    <div class="status-grid">
                        <div class="status-item merah">
                            <span class="status-label">🔴 MERAH</span>
                            <span class="status-value">{meta['merah_count']:,}</span>
                        </div>
                        <div class="status-item oranye">
                            <span class="status-label">🟠 ORANYE</span>
                            <span class="status-value">{meta['oranye_count']:,}</span>
                        </div>
                        <div class="status-item kuning">
                            <span class="status-label">🟡 KUNING</span>
                            <span class="status-value">{meta['kuning_count']:,}</span>
                        </div>
                        <div class="status-item hijau">
                            <span class="status-label">🟢 HIJAU</span>
                            <span class="status-value">{meta['hijau_count']:,}</span>
                        </div>
                    </div>
                    <div class="logistics-section">
                        <h4>📦 Kebutuhan Logistik</h4>
                        <div class="logistics-grid">
                            <div class="logistics-item">
                                <span>Asap Cair:</span>
                                <strong>{meta['asap_cair_liter']:,.0f} L</strong>
                            </div>
                            <div class="logistics-item">
                                <span>Trichoderma:</span>
                                <strong>{meta['trichoderma_liter']:,.0f} L</strong>
                            </div>
                        </div>
                    </div>
                    <div class="intervention-summary">
                        <span>🎯 Target Intervensi:</span>
                        <strong>{total_intervention:,} pohon</strong>
                    </div>
                </div>
            </div>
            '''
        
        # Build comparison table for this divisi
        comparison_rows = ""
        for metric_name, key, suffix in [
            ('Threshold', 'optimal_threshold_pct', ''),
            ('MERAH', 'merah_count', ''),
            ('ORANYE', 'oranye_count', ''),
            ('KUNING', 'kuning_count', ''),
            ('HIJAU', 'hijau_count', ''),
            ('Asap Cair', 'asap_cair_liter', ' L'),
            ('Trichoderma', 'trichoderma_liter', ' L'),
        ]:
            kon = results['konservatif']['metadata'].get(key, 0)
            std = results['standar']['metadata'].get(key, 0)
            agr = results['agresif']['metadata'].get(key, 0)
            
            if isinstance(kon, str):
                comparison_rows += f"<tr><td><strong>{metric_name}</strong></td><td>{kon}</td><td>{std}</td><td>{agr}</td></tr>"
            else:
                comparison_rows += f"<tr><td><strong>{metric_name}</strong></td><td>{kon:,.0f}{suffix}</td><td>{std:,.0f}{suffix}</td><td>{agr:,.0f}{suffix}</td></tr>"
        
        # Build block maps gallery for this divisi
        block_maps_html = ""
        block_maps = all_block_maps.get(divisi_name, {})
        for preset_name in ['konservatif', 'standar', 'agresif']:
            preset_info = PRESET_INFO[preset_name]
            maps = block_maps.get(preset_name, [])
            
            maps_items = ""
            for m in maps:
                maps_items += f'''
                    <div class="map-item" onclick="openLightbox('{divisi_id}/{m['filename']}')">
                        <img src="{divisi_id}/{m['filename']}" alt="Cluster Map {m['blok']}">
                        <div class="map-label">{m['blok']} - 🔴{m['merah']} 🟠{m['oranye']}</div>
                    </div>
                '''
            
            block_maps_html += f'''
            <div class="maps-preset-section">
                <h4 style="color: {preset_info['color']}">{preset_info['icon']} {preset_info['display_name']}</h4>
                <div class="maps-grid">
                    {maps_items}
                </div>
            </div>
            '''
        
        # Content for this divisi
        divisi_content_html += f'''
        <div class="divisi-content {active_class}" id="content-{divisi_id}" data-divisi="{divisi_id}">
            <div class="divisi-header">
                <h2>📍 {divisi_name}</h2>
                <div class="divisi-stats">
                    <span>🌳 {stats['total_rows']:,} pohon</span>
                    <span>📦 {stats['total_blocks']} blok</span>
                </div>
            </div>
            
            <section class="preset-cards-section">
                <h3>📊 Perbandingan 3 Preset</h3>
                <div class="preset-cards-container">
                    {preset_cards}
                </div>
            </section>
            
            <section class="comparison-section">
                <h3>📋 Tabel Perbandingan</h3>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Metrik</th>
                            <th style="color: var(--konservatif)">🔵 Konservatif</th>
                            <th style="color: var(--standar)">🟢 Standar</th>
                            <th style="color: var(--agresif)">🔴 Agresif</th>
                        </tr>
                    </thead>
                    <tbody>
                        {comparison_rows}
                    </tbody>
                </table>
            </section>
            
            <section class="visualizations-section">
                <h3>📈 Visualisasi Superimpose</h3>
                <div class="viz-grid">
                    <div class="viz-item" onclick="openLightbox('{divisi_id}/superimpose_bar_comparison.png')">
                        <img src="{divisi_id}/superimpose_bar_comparison.png" alt="Bar Comparison">
                    </div>
                    <div class="viz-item" onclick="openLightbox('{divisi_id}/superimpose_line_trend.png')">
                        <img src="{divisi_id}/superimpose_line_trend.png" alt="Line Trend">
                    </div>
                    <div class="viz-item" onclick="openLightbox('{divisi_id}/superimpose_stacked_status.png')">
                        <img src="{divisi_id}/superimpose_stacked_status.png" alt="Stacked Status">
                    </div>
                    <div class="viz-item" onclick="openLightbox('{divisi_id}/superimpose_radar_comparison.png')">
                        <img src="{divisi_id}/superimpose_radar_comparison.png" alt="Radar Comparison">
                    </div>
                    <div class="viz-item" onclick="openLightbox('{divisi_id}/superimpose_logistics_comparison.png')">
                        <img src="{divisi_id}/superimpose_logistics_comparison.png" alt="Logistics">
                    </div>
                </div>
            </section>
            
            <section class="block-maps-section">
                <h3>🗺️ Peta Kluster per Blok</h3>
                {block_maps_html}
            </section>
        </div>
        '''
    
    # Build combined summary
    total_trees_all = sum(r['standar']['metadata']['total_trees'] for r in all_divisi_results.values())
    total_blocks_all = sum(r['standar']['metadata']['stats']['total_blocks'] for r in all_divisi_results.values())
    
    # Summary per divisi per preset
    summary_rows = ""
    for divisi_name, results in all_divisi_results.items():
        for preset_name in ['konservatif', 'standar', 'agresif']:
            meta = results[preset_name]['metadata']
            summary_rows += f'''
            <tr>
                <td>{divisi_name}</td>
                <td>{PRESET_INFO[preset_name]['display_name']}</td>
                <td>{meta['optimal_threshold_pct']}</td>
                <td>{meta['merah_count']:,}</td>
                <td>{meta['oranye_count']:,}</td>
                <td>{meta['asap_cair_liter']:,.0f}</td>
                <td>{meta['trichoderma_liter']:,.0f}</td>
            </tr>
            '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 POAC v3.3 - Multi-Divisi Dashboard</title>
    <style>
        :root {{
            --merah: #e74c3c;
            --oranye: #f39c12;
            --kuning: #f1c40f;
            --hijau: #27ae60;
            --konservatif: #3498db;
            --standar: #27ae60;
            --agresif: #e74c3c;
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --bg-content: #0f3460;
            --text-light: #eee;
            --border-color: #2d4a6f;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text-light);
            min-height: 100vh;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-content) 100%);
            padding: 30px;
            text-align: center;
            border-bottom: 3px solid var(--oranye);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 15px;
        }}
        
        .header-stats span {{
            background: rgba(255,255,255,0.1);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 1.1em;
        }}
        
        /* Divisi Tabs */
        .divisi-tabs {{
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 20px;
            background: var(--bg-card);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 2px solid var(--border-color);
        }}
        
        .divisi-tab {{
            padding: 15px 40px;
            font-size: 1.2em;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: var(--bg-content);
            color: var(--text-light);
        }}
        
        .divisi-tab:hover {{
            background: var(--oranye);
            transform: translateY(-2px);
        }}
        
        .divisi-tab.active {{
            background: linear-gradient(135deg, var(--oranye), var(--merah));
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4);
        }}
        
        /* Divisi Content */
        .divisi-content {{
            display: none;
            padding: 30px;
            animation: fadeIn 0.3s ease;
        }}
        
        .divisi-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .divisi-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--bg-card);
            border-radius: 15px;
            border-left: 5px solid var(--oranye);
        }}
        
        .divisi-header h2 {{
            font-size: 2em;
        }}
        
        .divisi-stats {{
            display: flex;
            gap: 20px;
        }}
        
        .divisi-stats span {{
            background: var(--bg-content);
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }}
        
        /* Sections */
        section {{
            margin-bottom: 40px;
        }}
        
        section h3 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-color);
        }}
        
        /* Preset Cards */
        .preset-cards-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}
        
        .preset-card {{
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
            transition: transform 0.3s ease;
        }}
        
        .preset-card:hover {{
            transform: translateY(-5px);
        }}
        
        .preset-header {{
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }}
        
        .preset-icon {{
            font-size: 1.5em;
        }}
        
        .preset-name {{
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .preset-body {{
            padding: 20px;
        }}
        
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .status-item {{
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .status-label {{
            display: block;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .status-value {{
            display: block;
            font-size: 1.3em;
            font-weight: bold;
        }}
        
        .status-item.merah {{ border-left: 3px solid var(--merah); }}
        .status-item.oranye {{ border-left: 3px solid var(--oranye); }}
        .status-item.kuning {{ border-left: 3px solid var(--kuning); }}
        .status-item.hijau {{ border-left: 3px solid var(--hijau); }}
        
        .logistics-section {{
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }}
        
        .logistics-section h4 {{
            margin-bottom: 10px;
        }}
        
        .logistics-grid {{
            display: flex;
            justify-content: space-around;
        }}
        
        .logistics-item {{
            text-align: center;
        }}
        
        .logistics-item strong {{
            display: block;
            font-size: 1.2em;
            color: var(--oranye);
        }}
        
        .intervention-summary {{
            margin-top: 15px;
            padding: 10px;
            background: linear-gradient(135deg, var(--merah), var(--oranye));
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }}
        
        /* Comparison Table */
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .comparison-table th, .comparison-table td {{
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .comparison-table th {{
            background: var(--bg-content);
            font-weight: bold;
        }}
        
        .comparison-table tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        
        /* Visualizations */
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}
        
        .viz-item {{
            background: var(--bg-card);
            border-radius: 10px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        
        .viz-item:hover {{
            transform: scale(1.02);
        }}
        
        .viz-item img {{
            width: 100%;
            height: auto;
        }}
        
        /* Block Maps */
        .maps-preset-section {{
            margin-bottom: 30px;
        }}
        
        .maps-preset-section h4 {{
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .maps-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
        }}
        
        .map-item {{
            background: var(--bg-card);
            border-radius: 10px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        
        .map-item:hover {{
            transform: scale(1.05);
        }}
        
        .map-item img {{
            width: 100%;
            height: auto;
        }}
        
        .map-label {{
            padding: 8px;
            text-align: center;
            font-size: 0.9em;
            background: rgba(0,0,0,0.3);
        }}
        
        /* Combined Summary Section */
        .summary-section {{
            padding: 30px;
            background: var(--bg-card);
            margin: 20px 30px;
            border-radius: 15px;
        }}
        
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .summary-table th, .summary-table td {{
            padding: 12px;
            text-align: center;
            border: 1px solid var(--border-color);
        }}
        
        .summary-table th {{
            background: var(--bg-content);
        }}
        
        /* Lightbox with Zoom Controls */
        .lightbox {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }}
        
        .lightbox.active {{
            display: flex;
        }}
        
        .lightbox-content {{
            position: relative;
            max-width: 95%;
            max-height: 85%;
            overflow: auto;
        }}
        
        .lightbox-content img {{
            max-width: 100%;
            transition: transform 0.3s ease;
            transform-origin: center center;
            cursor: grab;
        }}
        
        .lightbox-content img:active {{
            cursor: grabbing;
        }}
        
        .lightbox-title {{
            color: white;
            font-size: 1.2em;
            text-align: center;
            padding: 10px;
            background: rgba(0,0,0,0.7);
            border-radius: 8px;
            margin-top: 10px;
        }}
        
        .lightbox-close {{
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 40px;
            color: white;
            cursor: pointer;
            z-index: 1002;
            transition: color 0.3s;
        }}
        
        .lightbox-close:hover {{
            color: #e74c3c;
        }}
        
        .lightbox-nav {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            font-size: 50px;
            color: white;
            cursor: pointer;
            z-index: 1001;
            padding: 20px;
            transition: all 0.3s;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }}
        
        .lightbox-nav:hover {{
            background: rgba(243, 156, 18, 0.8);
        }}
        
        .lightbox-prev {{
            left: 20px;
        }}
        
        .lightbox-next {{
            right: 20px;
        }}
        
        .lightbox-counter {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 1.1em;
            background: rgba(0,0,0,0.5);
            padding: 8px 20px;
            border-radius: 20px;
        }}
        
        .lightbox-zoom-controls {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 1002;
        }}
        
        .lightbox-zoom-btn {{
            background: rgba(0,0,0,0.7);
            color: white;
            border: 2px solid white;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .lightbox-zoom-btn:hover {{
            background: var(--oranye);
            border-color: var(--oranye);
        }}
        
        .zoom-level {{
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }}
        
        /* Color Guide Section */
        .color-guide-section {{
            background: var(--bg-card);
            margin: 20px 30px;
            padding: 25px;
            border-radius: 15px;
        }}
        
        .color-guide-section h3 {{
            text-align: center;
            margin-bottom: 25px;
            font-size: 1.5em;
            color: var(--oranye);
        }}
        
        .color-guide-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }}
        
        .color-guide-card {{
            background: var(--bg-content);
            border-radius: 12px;
            padding: 20px;
            border-left: 5px solid;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .color-guide-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        
        .color-guide-card.merah {{
            border-left-color: var(--merah);
        }}
        
        .color-guide-card.oranye {{
            border-left-color: var(--oranye);
        }}
        
        .color-guide-card.kuning {{
            border-left-color: var(--kuning);
        }}
        
        .color-guide-card.hijau {{
            border-left-color: var(--hijau);
        }}
        
        .color-guide-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .color-dot {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: inline-block;
        }}
        
        .color-dot.merah {{ background: var(--merah); }}
        .color-dot.oranye {{ background: var(--oranye); }}
        .color-dot.kuning {{ background: var(--kuning); }}
        .color-dot.hijau {{ background: var(--hijau); }}
        
        .color-guide-title {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        .color-guide-title.merah {{ color: var(--merah); }}
        .color-guide-title.oranye {{ color: var(--oranye); }}
        .color-guide-title.kuning {{ color: var(--kuning); }}
        .color-guide-title.hijau {{ color: var(--hijau); }}
        
        .color-guide-content {{
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .color-guide-content p {{
            margin: 8px 0;
        }}
        
        .color-guide-content strong {{
            color: var(--text-light);
        }}
        
        .color-guide-criteria {{
            background: rgba(255,255,255,0.05);
            padding: 10px 12px;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 0.9em;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .color-guide-action {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .priority-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
        }}
        
        .priority-badge.utama {{
            background: var(--merah);
            color: white;
        }}
        
        .priority-badge.kedua {{
            background: var(--oranye);
            color: white;
        }}
        
        /* Responsive */
        @media (max-width: 1200px) {{
            .preset-cards-container {{
                grid-template-columns: 1fr;
            }}
            .viz-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .maps-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            .color-guide-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .color-guide-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>🔥 POAC v3.3 - Algoritma Cincin Api</h1>
        <p>Multi-Divisi Analysis Dashboard</p>
        <div class="header-stats">
            <span>🌳 Total: {total_trees_all:,} pohon</span>
            <span>📦 {total_blocks_all} blok</span>
            <span>📅 {timestamp}</span>
        </div>
    </header>
    
    <nav class="divisi-tabs">
        {divisi_tabs_html}
    </nav>
    
    <main>
        {divisi_content_html}
    </main>
    
    <!-- Color Interpretation Guide -->
    <section class="color-guide-section">
        <h3>🎨 Panduan Interpretasi Warna</h3>
        <div class="color-guide-grid">
            <!-- MERAH -->
            <div class="color-guide-card merah">
                <div class="color-guide-header">
                    <span class="color-dot merah"></span>
                    <span class="color-dot" style="background: #c0392b;"></span>
                    <span class="color-guide-title merah">MERAH</span>
                </div>
                <div class="color-guide-content">
                    <p><strong>Arti:</strong> Pohon terdeteksi dalam kluster aktif Ganoderma</p>
                    <div class="color-guide-criteria">
                        <strong>Kriteria:</strong> Persentil ≤ threshold DAN ≥3 tetangga sakit
                    </div>
                    <div class="color-guide-action">
                        <span class="priority-badge utama">PRIORITAS UTAMA</span><br>
                        <strong>Tindakan:</strong> Tim Sanitasi, aplikasi Asap Cair (3 liter/pohon)
                    </div>
                </div>
            </div>
            
            <!-- ORANYE -->
            <div class="color-guide-card oranye">
                <div class="color-guide-header">
                    <span class="color-dot oranye"></span>
                    <span class="color-dot" style="background: #d35400;"></span>
                    <span class="color-guide-title oranye">ORANYE</span>
                </div>
                <div class="color-guide-content">
                    <p><strong>Arti:</strong> Pohon sehat yang bertetangga langsung dengan MERAH (Cincin Api)</p>
                    <div class="color-guide-criteria">
                        <strong>Kriteria:</strong> Tetangga langsung dari pohon MERAH (apapun nilai NDRE)
                    </div>
                    <div class="color-guide-action">
                        <span class="priority-badge kedua">PRIORITAS KEDUA</span><br>
                        <strong>Tindakan:</strong> Tim APH, aplikasi Trichoderma (2 liter/pohon)
                    </div>
                </div>
            </div>
            
            <!-- KUNING -->
            <div class="color-guide-card kuning">
                <div class="color-guide-header">
                    <span class="color-dot kuning"></span>
                    <span class="color-dot" style="background: #d4ac0d;"></span>
                    <span class="color-guide-title kuning">KUNING</span>
                </div>
                <div class="color-guide-content">
                    <p><strong>Arti:</strong> Pohon suspect tapi terisolasi (tidak membentuk kluster)</p>
                    <div class="color-guide-criteria">
                        <strong>Kriteria:</strong> Persentil ≤ threshold DAN 0-2 tetangga sakit, bukan tetangga MERAH
                    </div>
                    <div class="color-guide-action">
                        <strong>Tindakan:</strong> Investigasi lapangan untuk konfirmasi kondisi
                    </div>
                </div>
            </div>
            
            <!-- HIJAU -->
            <div class="color-guide-card hijau">
                <div class="color-guide-header">
                    <span class="color-dot hijau"></span>
                    <span class="color-dot" style="background: #1e8449;"></span>
                    <span class="color-guide-title hijau">HIJAU</span>
                </div>
                <div class="color-guide-content">
                    <p><strong>Arti:</strong> Pohon dalam kondisi sehat/normal</p>
                    <div class="color-guide-criteria">
                        <strong>Kriteria:</strong> Persentil > threshold
                    </div>
                    <div class="color-guide-action">
                        <strong>Tindakan:</strong> Tidak perlu tindakan, monitoring rutin
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="summary-section">
        <h3>📊 Ringkasan Semua Divisi</h3>
        <table class="summary-table">
            <thead>
                <tr>
                    <th>Divisi</th>
                    <th>Preset</th>
                    <th>Threshold</th>
                    <th>🔴 MERAH</th>
                    <th>🟠 ORANYE</th>
                    <th>Asap Cair (L)</th>
                    <th>Trichoderma (L)</th>
                </tr>
            </thead>
            <tbody>
                {summary_rows}
            </tbody>
        </table>
    </section>
    
    <!-- Lightbox with Zoom Controls -->
    <div class="lightbox" id="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <div class="lightbox-zoom-controls">
            <button class="lightbox-zoom-btn" onclick="zoomOut(event)" title="Zoom Out (-)">−</button>
            <span class="zoom-level" id="zoom-level">100%</span>
            <button class="lightbox-zoom-btn" onclick="zoomIn(event)" title="Zoom In (+)">+</button>
            <button class="lightbox-zoom-btn" onclick="resetZoom(event)" title="Reset (0)">↺</button>
        </div>
        <span class="lightbox-nav lightbox-prev" onclick="navigateLightbox(event, -1)">❮</span>
        <div class="lightbox-content" id="lightbox-content">
            <img id="lightbox-img" src="" alt="Enlarged image">
        </div>
        <span class="lightbox-nav lightbox-next" onclick="navigateLightbox(event, 1)">❯</span>
        <div class="lightbox-title" id="lightbox-title"></div>
        <div class="lightbox-counter" id="lightbox-counter"></div>
    </div>
    
    <script>
        // Image gallery for lightbox navigation
        let allImages = [];
        let currentImageIndex = 0;
        let currentZoom = 1;
        const ZOOM_STEP = 0.25;
        const MIN_ZOOM = 0.5;
        const MAX_ZOOM = 4;
        
        // Collect all images on page load
        document.addEventListener('DOMContentLoaded', function() {{
            const mapItems = document.querySelectorAll('.map-item');
            mapItems.forEach((item, index) => {{
                const img = item.querySelector('img');
                const label = item.querySelector('.map-label');
                if (img) {{
                    allImages.push({{
                        src: img.src,
                        title: label ? label.textContent : 'Image ' + (index + 1)
                    }});
                }}
            }});
        }});
        
        function switchDivisi(divisiId) {{
            // Update tabs
            document.querySelectorAll('.divisi-tab').forEach(tab => {{
                tab.classList.remove('active');
                if (tab.dataset.divisi === divisiId) {{
                    tab.classList.add('active');
                }}
            }});
            
            // Update content
            document.querySelectorAll('.divisi-content').forEach(content => {{
                content.classList.remove('active');
                if (content.dataset.divisi === divisiId) {{
                    content.classList.add('active');
                }}
            }});
            
            // Re-collect images for active divisi
            allImages = [];
            const activeContent = document.querySelector('.divisi-content.active');
            if (activeContent) {{
                const mapItems = activeContent.querySelectorAll('.map-item');
                mapItems.forEach((item, index) => {{
                    const img = item.querySelector('img');
                    const label = item.querySelector('.map-label');
                    if (img) {{
                        allImages.push({{
                            src: img.src,
                            title: label ? label.textContent : 'Image ' + (index + 1)
                        }});
                    }}
                }});
            }}
        }}
        
        function openLightbox(imgSrc, title) {{
            // Find index
            currentImageIndex = allImages.findIndex(img => img.src.includes(imgSrc.split('/').pop()));
            if (currentImageIndex === -1) currentImageIndex = 0;
            
            showImage(currentImageIndex);
            resetZoom();
            document.getElementById('lightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        
        function showImage(index) {{
            if (allImages.length === 0) return;
            
            currentImageIndex = (index + allImages.length) % allImages.length;
            const img = allImages[currentImageIndex];
            
            document.getElementById('lightbox-img').src = img.src;
            document.getElementById('lightbox-title').textContent = img.title;
            document.getElementById('lightbox-counter').textContent = 
                (currentImageIndex + 1) + ' / ' + allImages.length;
        }}
        
        function closeLightbox() {{
            document.getElementById('lightbox').classList.remove('active');
            document.body.style.overflow = '';
            resetZoom();
        }}
        
        function navigateLightbox(event, direction) {{
            event.stopPropagation();
            showImage(currentImageIndex + direction);
            resetZoom();
        }}
        
        function zoomIn(event) {{
            if (event) event.stopPropagation();
            if (currentZoom < MAX_ZOOM) {{
                currentZoom += ZOOM_STEP;
                applyZoom();
            }}
        }}
        
        function zoomOut(event) {{
            if (event) event.stopPropagation();
            if (currentZoom > MIN_ZOOM) {{
                currentZoom -= ZOOM_STEP;
                applyZoom();
            }}
        }}
        
        function resetZoom(event) {{
            if (event) event.stopPropagation();
            currentZoom = 1;
            applyZoom();
        }}
        
        function applyZoom() {{
            const img = document.getElementById('lightbox-img');
            img.style.transform = 'scale(' + currentZoom + ')';
            document.getElementById('zoom-level').textContent = Math.round(currentZoom * 100) + '%';
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {{
            const lightbox = document.getElementById('lightbox');
            const isLightboxActive = lightbox.classList.contains('active');
            
            if (e.key === 'Escape') closeLightbox();
            
            if (isLightboxActive) {{
                if (e.key === 'ArrowLeft') navigateLightbox(e, -1);
                if (e.key === 'ArrowRight') navigateLightbox(e, 1);
                if (e.key === '+' || e.key === '=') zoomIn();
                if (e.key === '-') zoomOut();
                if (e.key === '0') resetZoom();
            }} else {{
                if (e.key === '1') switchDivisi('AME_II');
                if (e.key === '2') switchDivisi('AME_IV');
            }}
        }});
        
        // Mouse wheel zoom
        document.getElementById('lightbox-content').addEventListener('wheel', function(e) {{
            e.preventDefault();
            if (e.deltaY < 0) {{
                zoomIn();
            }} else {{
                zoomOut();
            }}
        }});
        
        // Close on background click
        document.getElementById('lightbox').addEventListener('click', function(e) {{
            if (e.target === this) {{
                closeLightbox();
            }}
        }});
    </script>
</body>
</html>'''
    
    html_path = output_dir / "report_multi_divisi.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"HTML Report generated: {html_path}")
    return html_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="POAC v3.3 - Run All Presets Analysis"
    )
    parser.add_argument(
        "--divisi",
        type=str,
        default="AME_II",
        choices=["AME_II", "AME_IV", "ALL", "MULTI"],
        help="Divisi: AME_II, AME_IV, ALL (gabung), atau MULTI (terpisah per divisi)"
    )
    
    args = parser.parse_args()
    
    if args.divisi == "MULTI":
        run_multi_divisi_analysis()
    else:
        main(divisi=args.divisi)