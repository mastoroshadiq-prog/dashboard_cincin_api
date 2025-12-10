"""
POAC v3.3 - Multi Divisi Runner
Analisis Algoritma Cincin Api untuk multiple divisi (AME II & AME IV)
Dengan output HTML yang memiliki tab per divisi

=================================================================
Fitur:
- Load data dari multiple file divisi
- Analisis terpisah per divisi
- Generate HTML report dengan tabs (AME II | AME IV)
- Statistik perbandingan antar divisi
=================================================================
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import CINCIN_API_CONFIG, CINCIN_API_PRESETS
from src.ingestion import load_and_clean_data, load_ame_iv_data, validate_data_integrity, _clean_data
from src.clustering import run_cincin_api_algorithm, get_priority_targets
from src.dashboard import create_dashboard, create_mandor_report
from src.report_generator import generate_readme, generate_html_report_multi_divisi

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Default input files
DEFAULT_FILES = {
    "AME II": "data/input/tabelNDREnew.csv",
    "AME IV": "data/input/AME_IV.csv"
}


def run_analysis_per_divisi(df, divisi_name: str, preset: str, output_dir: Path, final_config: dict):
    """Run cincin api analysis for a single divisi."""
    logger.info(f"\n{'='*60}")
    logger.info(f"ANALISIS {divisi_name}")
    logger.info(f"{'='*60}")
    
    # Validate data
    stats = validate_data_integrity(df)
    logger.info(f"Total Pohon: {stats['total_rows']:,}")
    logger.info(f"Total Blok: {stats['total_blocks']}")
    
    # Run algorithm
    df_classified, metadata = run_cincin_api_algorithm(
        df,
        auto_tune=True,
        manual_threshold=None,
        config_override=final_config
    )
    
    # Add stats info to metadata
    metadata['divisi'] = divisi_name
    metadata['divisi_list'] = [divisi_name]
    metadata['stats'] = stats
    
    # Save divisi-specific outputs
    divisi_dir = output_dir / divisi_name.replace(" ", "_")
    divisi_dir.mkdir(parents=True, exist_ok=True)
    
    # Export CSV
    df_classified.to_csv(divisi_dir / "hasil_klasifikasi_lengkap.csv", index=False)
    
    # Get priority targets  
    priority_df = get_priority_targets(df_classified, top_n=1000)
    priority_df.to_csv(divisi_dir / "target_prioritas.csv", index=False)
    
    # Block summary
    block_summary = df_classified.groupby('Blok')['Status_Risiko'].value_counts().unstack(fill_value=0)
    block_summary.to_csv(divisi_dir / "ringkasan_per_blok.csv")
    
    logger.info(f"Output {divisi_name} saved to: {divisi_dir}")
    
    return df_classified, metadata


def main(preset: str = "standar"):
    """
    Main entry point untuk analisis multi-divisi.
    """
    print("\n" + "=" * 70)
    print("🔥 POAC v3.3 - ALGORITMA CINCIN API (MULTI-DIVISI)")
    print("Deteksi Kluster Ganoderma - AME II & AME IV")
    print("=" * 70 + "\n")
    
    # Get config
    final_config = CINCIN_API_PRESETS.get(preset, CINCIN_API_PRESETS['standar']).copy()
    print(f"📋 Using preset: {preset.upper()}")
    print(f"   {final_config.get('description', '')}")
    
    # Create output folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_folder_name = f"{timestamp}_multi_divisi_{preset}"
    output_dir = Path(__file__).parent / "data" / "output" / "cincin_api" / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output folder: {output_folder_name}")
    
    # Store results per divisi
    results = {}
    
    # =========================================================================
    # LOAD AND PROCESS AME II
    # =========================================================================
    print("\n" + "=" * 70)
    print("📂 LOADING DATA AME II")
    print("-" * 40)
    
    ame2_path = Path(__file__).parent / DEFAULT_FILES["AME II"]
    df_ame2 = load_and_clean_data(ame2_path)
    df_ame2_classified, metadata_ame2 = run_analysis_per_divisi(
        df_ame2, "AME II", preset, output_dir, final_config
    )
    results["AME II"] = {
        "df": df_ame2_classified,
        "metadata": metadata_ame2
    }
    
    # =========================================================================
    # LOAD AND PROCESS AME IV
    # =========================================================================
    print("\n" + "=" * 70)
    print("📂 LOADING DATA AME IV")
    print("-" * 40)
    
    ame4_path = Path(__file__).parent / DEFAULT_FILES["AME IV"]
    df_ame4_raw = load_ame_iv_data(ame4_path)
    df_ame4 = _clean_data(df_ame4_raw)
    df_ame4_classified, metadata_ame4 = run_analysis_per_divisi(
        df_ame4, "AME IV", preset, output_dir, final_config
    )
    results["AME IV"] = {
        "df": df_ame4_classified,
        "metadata": metadata_ame4
    }
    
    # =========================================================================
    # PRINT COMPARISON SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("📊 PERBANDINGAN HASIL ANALISIS")
    print("=" * 70)
    
    print(f"""
┌───────────────────────────────────────────────────────────────────────────────┐
│                         PERBANDINGAN AME II vs AME IV                          │
├───────────────────────────────────────┬───────────────────────────────────────┤
│              AME II                   │              AME IV                   │
├───────────────────────────────────────┼───────────────────────────────────────┤
│  Threshold: {metadata_ame2['optimal_threshold_pct']:>10}                   │  Threshold: {metadata_ame4['optimal_threshold_pct']:>10}                   │
│  Total Pohon: {metadata_ame2['total_trees']:>10,}                │  Total Pohon: {metadata_ame4['total_trees']:>10,}                │
├───────────────────────────────────────┼───────────────────────────────────────┤
│  🔴 MERAH: {metadata_ame2['merah_count']:>10,} ({metadata_ame2['merah_count']/metadata_ame2['total_trees']*100:>5.1f}%)       │  🔴 MERAH: {metadata_ame4['merah_count']:>10,} ({metadata_ame4['merah_count']/metadata_ame4['total_trees']*100:>5.1f}%)       │
│  🟠 ORANYE: {metadata_ame2['oranye_count']:>10,} ({metadata_ame2['oranye_count']/metadata_ame2['total_trees']*100:>5.1f}%)      │  🟠 ORANYE: {metadata_ame4['oranye_count']:>10,} ({metadata_ame4['oranye_count']/metadata_ame4['total_trees']*100:>5.1f}%)      │
│  🟡 KUNING: {metadata_ame2['kuning_count']:>10,} ({metadata_ame2['kuning_count']/metadata_ame2['total_trees']*100:>5.1f}%)      │  🟡 KUNING: {metadata_ame4['kuning_count']:>10,} ({metadata_ame4['kuning_count']/metadata_ame4['total_trees']*100:>5.1f}%)      │
│  🟢 HIJAU: {metadata_ame2['hijau_count']:>10,} ({metadata_ame2['hijau_count']/metadata_ame2['total_trees']*100:>5.1f}%)       │  🟢 HIJAU: {metadata_ame4['hijau_count']:>10,} ({metadata_ame4['hijau_count']/metadata_ame4['total_trees']*100:>5.1f}%)       │
├───────────────────────────────────────┼───────────────────────────────────────┤
│  📦 Asap Cair: {metadata_ame2['asap_cair_liter']:>10,.0f} L            │  📦 Asap Cair: {metadata_ame4['asap_cair_liter']:>10,.0f} L            │
│  📦 Trichoderma: {metadata_ame2['trichoderma_liter']:>10,.0f} L          │  📦 Trichoderma: {metadata_ame4['trichoderma_liter']:>10,.0f} L          │
└───────────────────────────────────────┴───────────────────────────────────────┘
""")
    
    # =========================================================================
    # GENERATE VISUALIZATIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("📊 GENERATING VISUALIZATIONS")
    print("-" * 40)
    
    # Generate dashboard for each divisi (but don't show plots)
    for divisi_name, data in results.items():
        divisi_dir = output_dir / divisi_name.replace(" ", "_")
        create_dashboard(data["df"], data["metadata"], divisi_dir, show_plots=False)
        print(f"✅ Dashboard {divisi_name} complete")
    
    # =========================================================================
    # GENERATE MULTI-DIVISI HTML REPORT
    # =========================================================================
    print("\n" + "=" * 70)
    print("📝 GENERATING MULTI-DIVISI HTML REPORT")
    print("-" * 40)
    
    html_path = generate_html_report_multi_divisi(
        output_dir=output_dir,
        results=results,
        preset=preset
    )
    print(f"🌐 HTML Report: {html_path}")
    print("   → Buka file ini di browser untuk laporan interaktif dengan tabs!")
    
    # =========================================================================
    # GENERATE COMBINED README
    # =========================================================================
    combined_metadata = {
        'total_trees': metadata_ame2['total_trees'] + metadata_ame4['total_trees'],
        'merah_count': metadata_ame2['merah_count'] + metadata_ame4['merah_count'],
        'oranye_count': metadata_ame2['oranye_count'] + metadata_ame4['oranye_count'],
        'kuning_count': metadata_ame2['kuning_count'] + metadata_ame4['kuning_count'],
        'hijau_count': metadata_ame2['hijau_count'] + metadata_ame4['hijau_count'],
        'asap_cair_liter': metadata_ame2['asap_cair_liter'] + metadata_ame4['asap_cair_liter'],
        'trichoderma_liter': metadata_ame2['trichoderma_liter'] + metadata_ame4['trichoderma_liter'],
        'optimal_threshold_pct': f"{metadata_ame2['optimal_threshold_pct']} / {metadata_ame4['optimal_threshold_pct']}",
        'divisi_list': ['AME II', 'AME IV'],
        'logistik': {
            'asap_cair_liter': metadata_ame2['asap_cair_liter'] + metadata_ame4['asap_cair_liter'],
            'trichoderma_liter': metadata_ame2['trichoderma_liter'] + metadata_ame4['trichoderma_liter']
        },
        'per_divisi': {
            'AME II': metadata_ame2,
            'AME IV': metadata_ame4
        }
    }
    
    generate_readme(output_dir, combined_metadata, preset=preset)
    print(f"📄 README.md generated")
    
    print("\n" + "=" * 70)
    print("✅ ANALISIS MULTI-DIVISI SELESAI!")
    print(f"📁 Semua file tersimpan di: {output_dir}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='POAC v3.3 - Multi Divisi Analysis')
    parser.add_argument('--preset', type=str, default='standar',
                       choices=['konservatif', 'standar', 'agresif'],
                       help='Preset konfigurasi (default: standar)')
    
    args = parser.parse_args()
    main(preset=args.preset)
