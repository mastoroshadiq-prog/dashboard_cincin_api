"""
POAC v3.3 - Clustering Module (Algoritma Cincin Api)
Implementasi dari Panduan Teknis Algoritma Cincin Api

Fitur:
1. Ranking Relatif (Percentile Rank per Blok)
2. Elbow Method Auto-Tuning
3. Deteksi Kluster dengan analisis tetangga (min 3 tetangga sakit)
4. Klasifikasi Baru:
   - MERAH: Kluster Aktif (persentil rendah + ≥3 tetangga sakit) → Tim Sanitasi
   - ORANYE: Cincin Api (tetangga langsung dari MERAH) → Tim APH
   - KUNING: Suspect Terisolasi (persentil rendah + 0-2 tetangga) → Investigasi
   - HIJAU: Sehat (persentil di atas threshold)
5. Kalkulasi Logistik (Asap Cair & Trichoderma)
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, List
from pathlib import Path
import sys

# Setup logging
logger = logging.getLogger(__name__)

# Add parent to path for config import
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from src.spatial import get_hex_neighbors
from config import CINCIN_API_CONFIG

# Status Labels (Updated - ORANYE sekarang Cincin Api, KUNING untuk noise)
STATUS_MERAH = "MERAH (KLUSTER AKTIF)"
STATUS_ORANYE = "ORANYE (CINCIN API)"      # BARU: Tetangga dari MERAH
STATUS_KUNING = "KUNING (SUSPECT TERISOLASI)"  # BARU: Noise/terisolasi
STATUS_HIJAU = "HIJAU (SEHAT)"

# Konstanta Logistik (liter per pohon)
ASAP_CAIR_PER_POHON = 3.0    # Untuk MERAH (Sanitasi)
TRICHODERMA_PER_POHON = 2.0  # Untuk ORANYE (APH/Proteksi)

# Load config values (can be overridden at runtime)
DEFAULT_MIN_SICK_NEIGHBORS = CINCIN_API_CONFIG.get("min_sick_neighbors", 3)
DEFAULT_THRESHOLD_MIN = CINCIN_API_CONFIG.get("threshold_min", 0.05)
DEFAULT_THRESHOLD_MAX = CINCIN_API_CONFIG.get("threshold_max", 0.30)
DEFAULT_THRESHOLD_STEP = CINCIN_API_CONFIG.get("threshold_step", 0.05)
DEFAULT_MIN_CLUSTERS = CINCIN_API_CONFIG.get("min_clusters_for_valid", 10)


def calculate_percentile_rank(df: pd.DataFrame) -> pd.DataFrame:
    """
    LANGKAH 1: NORMALISASI DATA (RANKING RELATIF)
    
    Memberikan nilai persentil (0.0 - 1.0) untuk setiap pohon 
    relatif terhadap bloknya.
    
    Pohon NDRE terendah di blok mendapat nilai 0.0, tertinggi 1.0
    """
    df_result = df.copy()
    
    # Calculate percentile rank per block (ascending - lower NDRE = lower percentile)
    df_result['Ranking_Persentil'] = df_result.groupby('Blok')['NDRE125'].transform(
        lambda x: x.rank(pct=True, method='average')
    )
    
    # Invert so that lowest NDRE gets lowest percentile (closer to 0)
    # rank(pct=True) gives 1 to lowest, we want 0 to lowest
    df_result['Ranking_Persentil'] = 1 - df_result['Ranking_Persentil']
    
    logger.info(f"Percentile rank calculated for {len(df_result)} trees")
    
    return df_result


def calculate_percentile_rank_split_merge(
    df: pd.DataFrame, 
    replant_ratios: Dict[str, float] = None,
    threshold_ratio: float = 0.20,
    ket_column: str = 'Keterangan'
) -> pd.DataFrame:
    """
    LANGKAH 1 ALTERNATIF: NORMALISASI DATA DENGAN SPLIT-MERGE
    
    Menggunakan kolom 'ket' (Keterangan) untuk membedakan pohon utama vs sisipan.
    Ranking persentil dihitung TERPISAH untuk masing-masing grup.
    
    Nilai 'ket':
    - "Pokok Utama" → Grup UTAMA (pohon induk)
    - "Tamb", "Sisip*" → Grup SISIPAN (pohon pengganti)
    - "Mati*", "Kosong*" → EXCLUDED (tidak dihitung)
    
    Args:
        df: DataFrame dengan kolom Blok, NDRE125, dan Keterangan
        replant_ratios: (Optional) Dict rasio sisipan per blok - tidak diperlukan jika ada kolom ket
        threshold_ratio: (Optional) Threshold untuk fallback mode
        ket_column: Nama kolom keterangan (default 'Keterangan')
        
    Returns:
        DataFrame dengan Ranking_Persentil, Tree_Type, dan Split_Merge_Applied
    """
    df_result = df.copy()
    
    # Initialize columns
    df_result['Ranking_Persentil'] = 0.0
    df_result['Tree_Type'] = 'UNKNOWN'
    df_result['Split_Merge_Applied'] = False
    
    # Check for ket column (might be 'Keterangan' or 'ket' depending on ingestion)
    ket_col = None
    for possible_col in [ket_column, 'ket', 'Ket', 'KET']:
        if possible_col in df_result.columns:
            ket_col = possible_col
            break
    
    if ket_col is None:
        logger.warning("No 'ket' column found. Falling back to normal percentile ranking.")
        return calculate_percentile_rank(df)
    
    logger.info(f"Using column '{ket_col}' for Split-Merge classification")
    
    # Classify tree types based on 'ket' column
    def classify_tree_type(ket_value):
        if pd.isna(ket_value):
            return 'UNKNOWN'
        ket = str(ket_value).strip().lower()
        
        if 'pokok utama' in ket or 'utama' in ket:
            return 'UTAMA'
        elif 'tamb' in ket or 'sisip' in ket:
            return 'SISIPAN'
        elif 'mati' in ket or 'kosong' in ket:
            return 'EXCLUDED'
        else:
            return 'UNKNOWN'
    
    df_result['Tree_Type'] = df_result[ket_col].apply(classify_tree_type)
    
    # Log distribution
    type_counts = df_result['Tree_Type'].value_counts()
    logger.info(f"Tree type distribution: {type_counts.to_dict()}")
    
    # Process each block
    split_count = 0
    normal_count = 0
    
    for blok, grup in df_result.groupby('Blok'):
        blok_indices = grup.index
        
        # Get UTAMA and SISIPAN indices
        utama_mask = grup['Tree_Type'] == 'UTAMA'
        sisipan_mask = grup['Tree_Type'] == 'SISIPAN'
        unknown_mask = grup['Tree_Type'] == 'UNKNOWN'
        excluded_mask = grup['Tree_Type'] == 'EXCLUDED'
        
        utama_indices = grup[utama_mask].index
        sisipan_indices = grup[sisipan_mask].index
        unknown_indices = grup[unknown_mask].index
        
        # Decide if split-merge should be applied
        has_both = len(utama_indices) > 0 and len(sisipan_indices) > 0
        sisipan_ratio = len(sisipan_indices) / (len(utama_indices) + len(sisipan_indices)) if (len(utama_indices) + len(sisipan_indices)) > 0 else 0
        
        if has_both and sisipan_ratio > 0.01:  # At least 1% sisipan to justify split
            # SPLIT-MERGE: Calculate percentile separately for each group
            
            # Grup UTAMA
            if len(utama_indices) > 0:
                utama_percentile = df_result.loc[utama_indices, 'NDRE125'].rank(pct=True, method='average')
                df_result.loc[utama_indices, 'Ranking_Persentil'] = 1 - utama_percentile
            
            # Grup SISIPAN
            if len(sisipan_indices) > 0:
                sisipan_percentile = df_result.loc[sisipan_indices, 'NDRE125'].rank(pct=True, method='average')
                df_result.loc[sisipan_indices, 'Ranking_Persentil'] = 1 - sisipan_percentile
            
            # Grup UNKNOWN - use block-level ranking
            if len(unknown_indices) > 0:
                unknown_percentile = df_result.loc[unknown_indices, 'NDRE125'].rank(pct=True, method='average')
                df_result.loc[unknown_indices, 'Ranking_Persentil'] = 1 - unknown_percentile
            
            # Mark as split-merge applied (except excluded)
            non_excluded = ~excluded_mask
            df_result.loc[grup[non_excluded].index, 'Split_Merge_Applied'] = True
            split_count += 1
            
        else:
            # NORMAL: No split, rank all trees together
            valid_indices = grup[~excluded_mask].index
            if len(valid_indices) > 0:
                percentile = df_result.loc[valid_indices, 'NDRE125'].rank(pct=True, method='average')
                df_result.loc[valid_indices, 'Ranking_Persentil'] = 1 - percentile
            normal_count += 1
    
    logger.info(f"Split-merge completed: {split_count} blocks with split-merge, {normal_count} blocks normal")
    
    return df_result




def count_sick_neighbors(
    df: pd.DataFrame, 
    row_idx: int, 
    threshold: float,
    coord_lookup: Dict
) -> int:
    """
    Menghitung jumlah tetangga yang sakit (di bawah threshold)
    menggunakan grid heksagonal.
    
    Args:
        df: DataFrame dengan Ranking_Persentil
        row_idx: Index baris yang sedang dianalisis
        threshold: Batas ambang persentil (misal 0.1 = 10% terbawah)
        coord_lookup: Dictionary lookup koordinat ke index
        
    Returns:
        int: Jumlah tetangga sakit
    """
    row = df.loc[row_idx]
    blok = row['Blok']
    baris = int(row['N_BARIS'])
    pokok = int(row['N_POKOK'])
    
    # Get hexagonal neighbors
    neighbors = get_hex_neighbors(baris, pokok)
    
    sick_count = 0
    for n_baris, n_pokok in neighbors:
        neighbor_key = (blok, n_baris, n_pokok)
        if neighbor_key in coord_lookup:
            neighbor_idx = coord_lookup[neighbor_key]
            neighbor_percentile = df.loc[neighbor_idx, 'Ranking_Persentil']
            # Tetangga dianggap sakit jika persentilnya <= threshold
            if neighbor_percentile <= threshold:
                sick_count += 1
    
    return sick_count


def simulate_thresholds(
    df: pd.DataFrame, 
    min_threshold: float = None,
    max_threshold: float = None,
    step: float = None,
    min_sick_neighbors: int = None
) -> pd.DataFrame:
    """
    LANGKAH 2-4: SIMULASI & ELBOW METHOD
    
    Mensimulasikan berbagai threshold dan menghitung efisiensi kluster
    untuk menemukan threshold optimal (Elbow Point).
    
    Args:
        df: DataFrame dengan Ranking_Persentil
        min_threshold: Batas bawah simulasi (default dari config)
        max_threshold: Batas atas simulasi (default dari config)
        step: Increment per step (default dari config)
        min_sick_neighbors: Minimum tetangga sakit untuk kluster (default dari config)
    """
    # Use defaults from config if not specified
    min_threshold = min_threshold if min_threshold is not None else DEFAULT_THRESHOLD_MIN
    max_threshold = max_threshold if max_threshold is not None else DEFAULT_THRESHOLD_MAX
    step = step if step is not None else DEFAULT_THRESHOLD_STEP
    min_sick_neighbors = min_sick_neighbors if min_sick_neighbors is not None else DEFAULT_MIN_SICK_NEIGHBORS
    
    logger.info(f"Running threshold simulation from {min_threshold*100:.0f}% to {max_threshold*100:.0f}%")
    
    # Build coordinate lookup
    coord_lookup = {}
    for idx, row in df.iterrows():
        key = (row['Blok'], int(row['N_BARIS']), int(row['N_POKOK']))
        coord_lookup[key] = idx
    
    results = []
    thresholds = np.arange(min_threshold, max_threshold + step, step)
    
    for threshold in thresholds:
        # Get suspects (trees below threshold)
        suspects = df[df['Ranking_Persentil'] <= threshold].copy()
        total_suspect = len(suspects)
        
        if total_suspect == 0:
            continue
        
        # Count sick neighbors for each suspect
        cluster_valid = 0
        for idx in suspects.index:
            sick_neighbors = count_sick_neighbors(df, idx, threshold, coord_lookup)
            if sick_neighbors >= min_sick_neighbors:
                cluster_valid += 1
        
        # Calculate efficiency ratio
        rasio_efisiensi = (cluster_valid / total_suspect) * 100 if total_suspect > 0 else 0
        
        results.append({
            'Batas_Ambang': threshold,
            'Persen_Ambang': f"{threshold*100:.0f}%",
            'Total_Suspect': total_suspect,
            'Kluster_Valid': cluster_valid,
            'Rasio_Efisiensi': rasio_efisiensi
        })
        
        logger.debug(f"Threshold {threshold*100:.0f}%: {total_suspect} suspects, {cluster_valid} clusters, {rasio_efisiensi:.2f}% efficiency")
    
    return pd.DataFrame(results)


def find_optimal_threshold(
    simulation_df: pd.DataFrame, 
    min_clusters: int = None,
    method: str = None
) -> float:
    """
    LANGKAH 5: MEMILIH THRESHOLD PEMENANG (AUTO-TUNING)
    
    Memilih threshold optimal menggunakan salah satu metode:
    - "efficiency": Pilih threshold dengan rasio efisiensi tertinggi (OLD - prone to over-detect)
    - "gradient": Pilih threshold di knee point menggunakan Kneedle algorithm (NEW - recommended)
    
    Args:
        simulation_df: DataFrame hasil simulasi threshold
        min_clusters: Minimum kluster valid (default dari config)
        method: Metode pemilihan - "efficiency" atau "gradient" (default dari config)
    """
    # Use defaults from config if not specified
    min_clusters = min_clusters if min_clusters is not None else DEFAULT_MIN_CLUSTERS
    method = method if method is not None else CINCIN_API_CONFIG.get("elbow_method", "efficiency")
    
    # Filter by minimum clusters
    valid_df = simulation_df[simulation_df['Kluster_Valid'] >= min_clusters].copy()
    
    if valid_df.empty:
        # Fallback: use threshold with most clusters
        logger.warning(f"No threshold with >={min_clusters} clusters. Using threshold with max clusters.")
        optimal_idx = simulation_df['Kluster_Valid'].idxmax()
        optimal_threshold = simulation_df.loc[optimal_idx, 'Batas_Ambang']
    elif method == "gradient":
        # =========================================================================
        # KNEEDLE ALGORITHM (Mencari Titik Siku / Knee Point)
        # =========================================================================
        # Konsep: Mencari titik di mana penambahan threshold tidak lagi memberikan
        # penambahan jumlah klaster yang signifikan (diminishing returns).
        # =========================================================================
        
        # Extract X (Threshold) dan Y (Kluster_Valid)
        x = valid_df['Batas_Ambang'].values
        y = valid_df['Kluster_Valid'].values
        
        if len(x) < 2:
            # Not enough points, use first valid threshold
            optimal_threshold = x[0]
        else:
            # Normalize X dan Y ke scale 0-1 agar sebanding
            x_min, x_max = x.min(), x.max()
            y_min, y_max = y.min(), y.max()
            
            # Avoid division by zero
            x_range = x_max - x_min if x_max > x_min else 1
            y_range = y_max - y_min if y_max > y_min else 1
            
            x_norm = (x - x_min) / x_range
            y_norm = (y - y_min) / y_range
            
            # Hitung jarak tegak lurus ke garis diagonal (dari titik pertama ke terakhir)
            # Untuk kurva yang naik, knee point adalah titik terjauh DI ATAS diagonal
            # Rumus sederhana: distance = y_norm - x_norm (untuk kurva concave)
            distances = y_norm - x_norm
            
            # Cari index dengan jarak maksimum (The Knee)
            optimal_idx = np.argmax(distances)
            optimal_threshold = x[optimal_idx]
            
            logger.info(f"Kneedle: Found knee at index {optimal_idx}, threshold {optimal_threshold*100:.0f}%")
            logger.info(f"Kneedle: Distances = {[f'{d:.3f}' for d in distances]}")
    else:
        # Default: efficiency-based selection (OLD method)
        optimal_idx = valid_df['Rasio_Efisiensi'].idxmax()
        optimal_threshold = valid_df.loc[optimal_idx, 'Batas_Ambang']
    
    logger.info(f"Optimal threshold found ({method}): {optimal_threshold*100:.0f}%")
    
    return optimal_threshold


def classify_trees_with_clustering(
    df: pd.DataFrame, 
    threshold: float,
    min_sick_neighbors: int = None
) -> pd.DataFrame:
    """
    LANGKAH 6: KLASIFIKASI AKHIR (LOGIKA BARU)
    
    Mengklasifikasikan setiap pohon dengan logika 2-tahap:
    
    TAHAP 1 - Dari Analisis NDRE:
    - HIJAU (SEHAT): Persentil > threshold
    - MERAH (KLUSTER AKTIF): Persentil <= threshold DAN >= min_sick_neighbors tetangga sakit
    - KUNING (SUSPECT TERISOLASI): Persentil <= threshold DAN 0 s/d (min_sick_neighbors-1) tetangga sakit
    
    TAHAP 2 - Dari Posisi Fisik (Cincin Api):
    - ORANYE (CINCIN API): Pohon yang BERTETANGGA LANGSUNG dengan MERAH
                          (apapun nilai NDRE-nya, KECUALI sudah MERAH)
    
    Args:
        df: DataFrame dengan Ranking_Persentil
        threshold: Batas ambang persentil optimal
        min_sick_neighbors: Minimum tetangga sakit untuk MERAH (default dari config)
    """
    # Use default from config if not specified
    min_sick_neighbors = min_sick_neighbors if min_sick_neighbors is not None else DEFAULT_MIN_SICK_NEIGHBORS
    
    df_result = df.copy()
    
    # Build coordinate lookup
    coord_lookup = {}
    for idx, row in df_result.iterrows():
        key = (row['Blok'], int(row['N_BARIS']), int(row['N_POKOK']))
        coord_lookup[key] = idx
    
    # Initialize columns
    df_result['Jumlah_Tetangga_Sakit'] = 0
    df_result['Status_Risiko'] = STATUS_HIJAU
    df_result['Skor_Kepadatan_Kluster'] = 0
    df_result['Is_Cincin_Api'] = False  # Flag untuk ORANYE (Cincin Api)
    
    # =========================================================================
    # TAHAP 1: Klasifikasi berdasarkan NDRE (MERAH dan KUNING)
    # =========================================================================
    suspect_mask = df_result['Ranking_Persentil'] <= threshold
    suspect_indices = df_result[suspect_mask].index
    
    logger.info(f"Classifying {len(suspect_indices)} suspect trees with threshold {threshold*100:.0f}%")
    
    # Count sick neighbors for all suspects
    for idx in suspect_indices:
        sick_neighbors = count_sick_neighbors(df_result, idx, threshold, coord_lookup)
        df_result.loc[idx, 'Jumlah_Tetangga_Sakit'] = sick_neighbors
        df_result.loc[idx, 'Skor_Kepadatan_Kluster'] = sick_neighbors
        
        # Classify based on neighbor count
        if sick_neighbors >= min_sick_neighbors:
            df_result.loc[idx, 'Status_Risiko'] = STATUS_MERAH
        else:
            # KUNING untuk suspect terisolasi (0 s/d min_sick_neighbors-1 tetangga)
            df_result.loc[idx, 'Status_Risiko'] = STATUS_KUNING
    
    # =========================================================================
    # TAHAP 2: Identifikasi CINCIN API (ORANYE) - Tetangga dari MERAH
    # =========================================================================
    # Dapatkan semua pohon MERAH
    merah_indices = df_result[df_result['Status_Risiko'] == STATUS_MERAH].index
    merah_coords = set()
    
    for idx in merah_indices:
        row = df_result.loc[idx]
        merah_coords.add((row['Blok'], int(row['N_BARIS']), int(row['N_POKOK'])))
    
    logger.info(f"Finding Cincin Api neighbors for {len(merah_indices)} MERAH trees")
    
    # Untuk setiap pohon MERAH, tandai tetangganya sebagai ORANYE (Cincin Api)
    cincin_api_count = 0
    for idx in merah_indices:
        row = df_result.loc[idx]
        blok = row['Blok']
        baris = int(row['N_BARIS'])
        pokok = int(row['N_POKOK'])
        
        # Get hexagonal neighbors
        neighbors = get_hex_neighbors(baris, pokok)
        
        for n_baris, n_pokok in neighbors:
            neighbor_key = (blok, n_baris, n_pokok)
            if neighbor_key in coord_lookup:
                neighbor_idx = coord_lookup[neighbor_key]
                current_status = df_result.loc[neighbor_idx, 'Status_Risiko']
                
                # Hanya ubah ke ORANYE jika BUKAN MERAH
                # (bisa mengubah HIJAU atau KUNING menjadi ORANYE)
                if current_status != STATUS_MERAH:
                    df_result.loc[neighbor_idx, 'Status_Risiko'] = STATUS_ORANYE
                    df_result.loc[neighbor_idx, 'Is_Cincin_Api'] = True
                    cincin_api_count += 1
    
    logger.info(f"Cincin Api (ORANYE) identified: {cincin_api_count} trees (may include duplicates)")
    
    # Log statistics
    status_counts = df_result['Status_Risiko'].value_counts()
    logger.info(f"Classification complete: {status_counts.to_dict()}")
    
    return df_result


def run_cincin_api_algorithm(
    df: pd.DataFrame,
    auto_tune: bool = True,
    manual_threshold: float = None,
    config_override: Dict = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Menjalankan algoritma Cincin Api lengkap.
    
    Args:
        df: DataFrame dengan data NDRE
        auto_tune: Gunakan Elbow Method untuk auto-tuning
        manual_threshold: Override threshold manual (0.0-1.0)
        config_override: Override konfigurasi (dict dengan keys dari CINCIN_API_CONFIG)
                        Contoh: {"min_sick_neighbors": 4, "threshold_max": 0.40}
        
    Returns:
        Tuple of (classified_df, metadata)
    """
    # Merge config override
    config = CINCIN_API_CONFIG.copy()
    if config_override:
        config.update(config_override)
        logger.info(f"Config override applied: {config_override}")
    
    # Extract parameters from config
    threshold_min = config.get("threshold_min", DEFAULT_THRESHOLD_MIN)
    threshold_max = config.get("threshold_max", DEFAULT_THRESHOLD_MAX)
    threshold_step = config.get("threshold_step", DEFAULT_THRESHOLD_STEP)
    min_sick_neighbors = config.get("min_sick_neighbors", DEFAULT_MIN_SICK_NEIGHBORS)
    min_clusters = config.get("min_clusters_for_valid", DEFAULT_MIN_CLUSTERS)
    elbow_method = config.get("elbow_method", "efficiency")
    
    logger.info("=" * 60)
    logger.info("ALGORITMA CINCIN API v1.0")
    logger.info("=" * 60)
    logger.info(f"Config: threshold_range=[{threshold_min*100:.0f}%-{threshold_max*100:.0f}%], "
                f"step={threshold_step*100:.0f}%, min_sick_neighbors={min_sick_neighbors}")
    
    # Step 1: Calculate percentile rank
    df_ranked = calculate_percentile_rank(df)
    
    # Step 2-5: Simulate and find optimal threshold
    if auto_tune and manual_threshold is None:
        simulation_df = simulate_thresholds(
            df_ranked,
            min_threshold=threshold_min,
            max_threshold=threshold_max,
            step=threshold_step,
            min_sick_neighbors=min_sick_neighbors
        )
        optimal_threshold = find_optimal_threshold(
            simulation_df,
            min_clusters=min_clusters,
            method=elbow_method
        )
    else:
        optimal_threshold = manual_threshold if manual_threshold else 0.10
        simulation_df = None
    
    # Step 6: Classify trees
    df_classified = classify_trees_with_clustering(
        df_ranked, 
        optimal_threshold,
        min_sick_neighbors=min_sick_neighbors
    )
    
    # Prepare metadata
    status_counts = df_classified['Status_Risiko'].value_counts().to_dict()
    
    # Hitung kebutuhan logistik
    merah_count = status_counts.get(STATUS_MERAH, 0)
    oranye_count = status_counts.get(STATUS_ORANYE, 0)
    kuning_count = status_counts.get(STATUS_KUNING, 0)
    hijau_count = status_counts.get(STATUS_HIJAU, 0)
    
    logistik = calculate_logistics(merah_count, oranye_count)
    
    metadata = {
        'optimal_threshold': optimal_threshold,
        'optimal_threshold_pct': f"{optimal_threshold*100:.0f}%",
        'total_trees': len(df_classified),
        'status_counts': status_counts,
        'merah_count': merah_count,
        'oranye_count': oranye_count,
        'kuning_count': kuning_count,
        'hijau_count': hijau_count,
        'simulation_data': simulation_df,
        # Logistik
        'logistik': logistik,
        'asap_cair_liter': logistik['asap_cair_liter'],
        'trichoderma_liter': logistik['trichoderma_liter']
    }
    
    logger.info(f"Threshold Optimal: {metadata['optimal_threshold_pct']}")
    logger.info(f"MERAH (Kluster Aktif): {metadata['merah_count']} → Asap Cair: {logistik['asap_cair_liter']:.0f} liter")
    logger.info(f"ORANYE (Cincin Api): {metadata['oranye_count']} → Trichoderma: {logistik['trichoderma_liter']:.0f} liter")
    logger.info(f"KUNING (Suspect Terisolasi): {metadata['kuning_count']}")
    logger.info(f"HIJAU (Sehat): {metadata['hijau_count']}")
    
    return df_classified, metadata


def calculate_logistics(merah_count: int, oranye_count: int) -> Dict:
    """
    Menghitung kebutuhan logistik berdasarkan jumlah pohon per kategori.
    
    MERAH → Asap Cair (3 liter/pohon) - Tim Sanitasi
    ORANYE → Trichoderma (2 liter/pohon) - Tim APH
    
    Args:
        merah_count: Jumlah pohon MERAH (Kluster Aktif)
        oranye_count: Jumlah pohon ORANYE (Cincin Api)
        
    Returns:
        Dict dengan estimasi kebutuhan logistik
    """
    asap_cair_liter = merah_count * ASAP_CAIR_PER_POHON
    trichoderma_liter = oranye_count * TRICHODERMA_PER_POHON
    
    return {
        'merah_count': merah_count,
        'oranye_count': oranye_count,
        'asap_cair_per_pohon': ASAP_CAIR_PER_POHON,
        'trichoderma_per_pohon': TRICHODERMA_PER_POHON,
        'asap_cair_liter': asap_cair_liter,
        'trichoderma_liter': trichoderma_liter,
        'total_liter': asap_cair_liter + trichoderma_liter
    }
    
    return df_classified, metadata


def get_priority_targets(df: pd.DataFrame, top_n: int = 100) -> pd.DataFrame:
    """
    Mendapatkan daftar target prioritas untuk Mandor.
    
    Prioritas:
    1. MERAH (Kluster Aktif) - Target Sanitasi (Asap Cair)
    2. ORANYE (Cincin Api) - Target APH (Trichoderma)
    
    Diurutkan berdasarkan:
    1. Status (MERAH > ORANYE)
    2. Skor Kepadatan Kluster (lebih tinggi = lebih prioritas)
    """
    # Filter MERAH dan ORANYE (target intervensi utama)
    priority_df = df[df['Status_Risiko'].isin([STATUS_MERAH, STATUS_ORANYE])].copy()
    
    # Sort by status (MERAH first, then ORANYE) then by density score
    status_order = {STATUS_MERAH: 0, STATUS_ORANYE: 1}
    priority_df['_status_order'] = priority_df['Status_Risiko'].map(status_order)
    priority_df = priority_df.sort_values(
        ['_status_order', 'Skor_Kepadatan_Kluster'], 
        ascending=[True, False]
    )
    priority_df = priority_df.drop('_status_order', axis=1)
    
    return priority_df.head(top_n)


def get_sanitasi_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mendapatkan daftar target untuk Tim Sanitasi (MERAH).
    
    Returns:
        DataFrame pohon MERAH untuk Asap Cair
    """
    return df[df['Status_Risiko'] == STATUS_MERAH].copy()


def get_aph_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mendapatkan daftar target untuk Tim APH (ORANYE - Cincin Api).
    
    Returns:
        DataFrame pohon ORANYE untuk Trichoderma
    """
    return df[df['Status_Risiko'] == STATUS_ORANYE].copy()


# =============================================================================
# CONSENSUS VOTING (Filter Akhir Multi-Preset)
# =============================================================================

def apply_consensus_voting(
    results_dict: Dict[str, pd.DataFrame],
    min_votes: int = None,
    status_column: str = 'Status_Risiko'
) -> pd.DataFrame:
    """
    CONSENSUS VOTING: Filter hasil dari multiple preset.
    
    Sebuah pohon hanya divonis sebagai target (G3/MERAH) jika disepakati 
    oleh minimal min_votes preset.
    
    Args:
        results_dict: Dictionary dengan key=preset_name, value=DataFrame hasil klasifikasi
                     Contoh: {'konservatif': df1, 'standar': df2, 'agresif': df3}
        min_votes: Minimum jumlah preset yang harus setuju (default: 2)
        status_column: Nama kolom status (default: 'Status_Risiko')
        
    Returns:
        DataFrame dengan kolom tambahan:
        - 'vote_count': Jumlah preset yang menandai pohon sebagai MERAH
        - 'consensus_status': Status akhir setelah voting (APPROVED/REJECTED)
        - 'voting_presets': List preset yang menandai MERAH
    """
    min_votes = min_votes if min_votes is not None else CINCIN_API_CONFIG.get("min_votes", 2)
    
    logger.info(f"Applying Consensus Voting with min_votes={min_votes}")
    
    # Collect all unique tree IDs across all presets
    all_trees = set()
    preset_results = {}
    
    for preset_name, df in results_dict.items():
        # Create unique tree key
        df = df.copy()
        df['tree_key'] = df['Blok'].astype(str) + '_' + df['N_BARIS'].astype(str) + '_' + df['N_POKOK'].astype(str)
        
        # Get MERAH trees
        merah_trees = set(df[df[status_column].str.contains('MERAH', na=False)]['tree_key'].tolist())
        preset_results[preset_name] = merah_trees
        all_trees.update(df['tree_key'].tolist())
        
        logger.info(f"  {preset_name}: {len(merah_trees)} MERAH trees")
    
    # Count votes for each tree
    vote_counter = {}
    voting_presets = {}
    
    for preset_name, merah_trees in preset_results.items():
        for tid in merah_trees:
            if tid not in vote_counter:
                vote_counter[tid] = 0
                voting_presets[tid] = []
            vote_counter[tid] += 1
            voting_presets[tid].append(preset_name)
    
    # Use first preset's DataFrame as base
    first_preset = list(results_dict.keys())[0]
    base_df = results_dict[first_preset].copy()
    base_df['tree_key'] = base_df['Blok'].astype(str) + '_' + base_df['N_BARIS'].astype(str) + '_' + base_df['N_POKOK'].astype(str)
    
    # Add voting results
    base_df['vote_count'] = base_df['tree_key'].map(lambda x: vote_counter.get(x, 0))
    base_df['voting_presets'] = base_df['tree_key'].map(lambda x: ','.join(voting_presets.get(x, [])))
    base_df['consensus_status'] = base_df['vote_count'].apply(
        lambda v: 'APPROVED' if v >= min_votes else 'REJECTED'
    )
    
    # Count results
    approved_count = len(base_df[base_df['consensus_status'] == 'APPROVED'])
    
    logger.info(f"Consensus Voting Results:")
    logger.info(f"  Total trees: {len(base_df)}")
    logger.info(f"  Votes >= {min_votes}: {approved_count} APPROVED")
    
    # Log vote distribution
    for v in range(len(results_dict) + 1):
        count = len(base_df[base_df['vote_count'] == v])
        logger.info(f"  {v} votes: {count} trees")
    
    return base_df
