"""
POAC v3.3 - Adaptive Detection Methods
=======================================
Modul untuk metode deteksi adaptif berdasarkan hasil 3 preset existing.

Opsi 1: Age-Based Preset Selection - Pilih preset berdasarkan umur tanaman
Opsi 2: Ensemble Scoring + Age Weight - Kombinasi dengan bobot umur
Opsi 3: Ensemble Scoring Pure - Confidence level tanpa faktor umur
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Age-Based Config
AGE_BASED_CONFIG = {
    "old_threshold": 12,      # Umur > 12 tahun = pakai Agresif
    "medium_threshold": 8,    # Umur 8-12 tahun = pakai Standar
    # Umur < 8 tahun = pakai Konservatif
    "reference_year": 2025,   # Tahun referensi untuk hitung umur
}

# Ensemble Scoring Config
ENSEMBLE_CONFIG = {
    "weights_default": {
        "konservatif": 0.33,
        "standar": 0.34,
        "agresif": 0.33,
    },
    # Age-weighted: bobot berubah berdasarkan umur
    "weights_old": {      # Umur > 12 tahun - favor agresif
        "konservatif": 0.15,
        "standar": 0.30,
        "agresif": 0.55,
    },
    "weights_medium": {   # Umur 8-12 tahun - balanced
        "konservatif": 0.25,
        "standar": 0.50,
        "agresif": 0.25,
    },
    "weights_young": {    # Umur < 8 tahun - favor konservatif
        "konservatif": 0.55,
        "standar": 0.30,
        "agresif": 0.15,
    },
}

# Status mapping untuk deteksi
RISK_STATUSES = [
    'MERAH (KLUSTER AKTIF)',
    'ORANYE (CINCIN API)',
    'KUNING (SUSPECT TERISOLASI)',
]

# Preset names
PRESET_NAMES = ['konservatif', 'standar', 'agresif']


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_tree_age(tahun_tanam: int, reference_year: int = 2025) -> int:
    """
    Hitung umur tanaman.
    
    Args:
        tahun_tanam: Tahun tanam
        reference_year: Tahun referensi (default 2025)
        
    Returns:
        Umur tanaman dalam tahun
    """
    if pd.isna(tahun_tanam) or tahun_tanam <= 0:
        return 0
    return reference_year - int(tahun_tanam)


def get_age_category(age: int) -> str:
    """
    Kategorikan umur tanaman: 'old', 'medium', 'young'.
    
    Args:
        age: Umur tanaman dalam tahun
        
    Returns:
        Kategori umur
    """
    if age > AGE_BASED_CONFIG["old_threshold"]:
        return "old"
    elif age >= AGE_BASED_CONFIG["medium_threshold"]:
        return "medium"
    else:
        return "young"


def get_preset_for_age_category(age_category: str) -> str:
    """
    Dapatkan preset optimal untuk kategori umur.
    
    Args:
        age_category: Kategori umur ('old', 'medium', 'young')
        
    Returns:
        Nama preset
    """
    mapping = {
        "old": "agresif",       # Blok tua -> perlu deteksi agresif
        "medium": "standar",   # Blok medium -> standar
        "young": "konservatif" # Blok muda -> konservatif
    }
    return mapping.get(age_category, "standar")


def is_detected(status: str) -> bool:
    """
    Check apakah status terdeteksi sebagai risiko.
    
    Args:
        status: Status risiko pohon
        
    Returns:
        True jika terdeteksi sebagai risiko
    """
    return status in RISK_STATUSES[:3]  # MERAH, ORANYE, KUNING


def get_detection_score(status: str) -> float:
    """
    Dapatkan skor deteksi berdasarkan status.
    
    Args:
        status: Status risiko pohon
        
    Returns:
        Skor deteksi (0-1)
    """
    if status == 'MERAH (KLUSTER AKTIF)':
        return 1.0
    elif status == 'ORANYE (CINCIN API)':
        return 0.75
    elif status == 'KUNING (SUSPECT TERISOLASI)':
        return 0.5
    else:
        return 0.0


# =============================================================================
# OPSI 1: AGE-BASED PRESET SELECTION
# =============================================================================

def age_based_preset_selection(
    all_results: Dict,
    df_original: pd.DataFrame
) -> Tuple[pd.DataFrame, Dict]:
    """
    Age-Based Preset Selection.
    
    Otomatis pilih hasil preset berdasarkan umur tanaman per blok.
    - Umur > 12 tahun -> Agresif
    - Umur 8-12 tahun -> Standar
    - Umur < 8 tahun -> Konservatif
    
    Args:
        all_results: Dictionary hasil semua preset {'konservatif': {...}, ...}
        df_original: DataFrame original dengan kolom T_Tanam
        
    Returns:
        Tuple (DataFrame hasil, metadata dict)
    """
    logger.info("Running Age-Based Preset Selection...")
    
    # Get block-level tahun tanam dari original data
    # Cari kolom T_Tanam (case insensitive)
    t_tanam_col = None
    for col in df_original.columns:
        if col.lower() in ['t_tanam', 'tahun_tanam']:
            t_tanam_col = col
            break
    
    if t_tanam_col is None:
        logger.warning("Column T_Tanam not found, defaulting to Standar preset")
        return all_results['standar']['df'].copy(), {
            'method': 'age_based',
            'warning': 'T_Tanam column not found, using Standar as default'
        }
    
    # Get unique blocks and their tahun tanam
    blok_col = None
    for col in df_original.columns:
        if col.lower() == 'blok':
            blok_col = col
            break
    
    if blok_col is None:
        blok_col = 'Blok'
    
    # Get first T_Tanam per blok
    block_tanam = df_original.groupby(blok_col)[t_tanam_col].first().to_dict()
    
    # Build result DataFrame by selecting appropriate preset per block
    result_dfs = []
    block_assignments = {}
    
    for blok, tahun_tanam in block_tanam.items():
        age = calculate_tree_age(tahun_tanam)
        age_category = get_age_category(age)
        selected_preset = get_preset_for_age_category(age_category)
        
        block_assignments[blok] = {
            'tahun_tanam': tahun_tanam,
            'age': age,
            'age_category': age_category,
            'selected_preset': selected_preset
        }
        
        # Get data for this block from selected preset
        preset_df = all_results[selected_preset]['df']
        block_data = preset_df[preset_df['Blok'] == blok].copy()
        block_data['Adaptive_Method'] = 'Age-Based'
        block_data['Selected_Preset'] = selected_preset
        block_data['Age_Category'] = age_category
        block_data['Tree_Age'] = age
        
        result_dfs.append(block_data)
    
    # Combine all blocks
    if result_dfs:
        result_df = pd.concat(result_dfs, ignore_index=True)
    else:
        result_df = all_results['standar']['df'].copy()
    
    # Calculate statistics
    metadata = {
        'method': 'age_based',
        'method_name': 'Age-Based Preset Selection',
        'description': 'Otomatis pilih preset berdasarkan umur tanaman',
        'total_trees': len(result_df),
        'total_blocks': len(block_assignments),
        'block_assignments': block_assignments,
        'preset_distribution': {},
        'merah_count': len(result_df[result_df['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)']),
        'oranye_count': len(result_df[result_df['Status_Risiko'] == 'ORANYE (CINCIN API)']),
        'kuning_count': len(result_df[result_df['Status_Risiko'] == 'KUNING (SUSPECT TERISOLASI)']),
        'hijau_count': len(result_df[result_df['Status_Risiko'] == 'HIJAU (SEHAT)']),
    }
    
    # Count preset distribution
    for preset in PRESET_NAMES:
        count = sum(1 for v in block_assignments.values() if v['selected_preset'] == preset)
        metadata['preset_distribution'][preset] = count
    
    logger.info(f"  Age-Based: {metadata['preset_distribution']}")
    logger.info(f"  MERAH: {metadata['merah_count']}, ORANYE: {metadata['oranye_count']}")
    
    return result_df, metadata


# =============================================================================
# OPSI 2: ENSEMBLE SCORING + AGE WEIGHT (OPTIMIZED)
# =============================================================================

def ensemble_scoring_with_age(
    all_results: Dict,
    df_original: pd.DataFrame
) -> Tuple[pd.DataFrame, Dict]:
    """
    Ensemble Scoring dengan Age Weight - OPTIMIZED VERSION.
    
    Menggunakan vectorized operations untuk performa optimal.
    """
    logger.info("Running Ensemble Scoring with Age Weight (Optimized)...")
    
    # Get T_Tanam column
    t_tanam_col = None
    for col in df_original.columns:
        if col.lower() in ['t_tanam', 'tahun_tanam']:
            t_tanam_col = col
            break
    
    blok_col = None
    for col in df_original.columns:
        if col.lower() == 'blok':
            blok_col = col
            break
    if blok_col is None:
        blok_col = 'Blok'
    
    # Get block tahun tanam mapping
    block_tanam = {}
    if t_tanam_col:
        block_tanam = df_original.groupby(blok_col)[t_tanam_col].first().to_dict()
    
    # Use standar as base
    base_df = all_results['standar']['df'].copy()
    key_cols = ['Blok', 'N_BARIS', 'N_POKOK']
    
    # Create score mapping for each status
    score_map = {
        'MERAH (KLUSTER AKTIF)': 1.0,
        'ORANYE (CINCIN API)': 0.75,
        'KUNING (SUSPECT TERISOLASI)': 0.5,
        'HIJAU (SEHAT)': 0.0
    }
    
    # For each preset, create a temporary df with scores
    preset_scores = {}
    for preset_name in PRESET_NAMES:
        pdf = all_results[preset_name]['df'][key_cols + ['Status_Risiko']].copy()
        pdf[f'score_{preset_name}'] = pdf['Status_Risiko'].map(score_map).fillna(0)
        pdf[f'detected_{preset_name}'] = pdf['Status_Risiko'].isin(RISK_STATUSES).astype(int)
        preset_scores[preset_name] = pdf[key_cols + [f'score_{preset_name}', f'detected_{preset_name}']]
    
    # Merge all preset scores into base_df
    result_df = base_df.copy()
    for preset_name in PRESET_NAMES:
        result_df = result_df.merge(
            preset_scores[preset_name],
            on=key_cols,
            how='left'
        )
    
    # Fill NaN scores with 0
    for preset_name in PRESET_NAMES:
        result_df[f'score_{preset_name}'] = result_df[f'score_{preset_name}'].fillna(0)
        result_df[f'detected_{preset_name}'] = result_df[f'detected_{preset_name}'].fillna(0)
    
    # Calculate age and age category for each block
    result_df['Tree_Age'] = result_df['Blok'].map(
        lambda b: calculate_tree_age(block_tanam.get(b, 2015))
    )
    result_df['Age_Category'] = result_df['Tree_Age'].apply(get_age_category)
    
    # Calculate weighted score based on age category
    def calc_weighted_score(row):
        age_cat = row['Age_Category']
        if age_cat == 'old':
            weights = ENSEMBLE_CONFIG['weights_old']
        elif age_cat == 'medium':
            weights = ENSEMBLE_CONFIG['weights_medium']
        else:
            weights = ENSEMBLE_CONFIG['weights_young']
        
        score = (
            row['score_konservatif'] * weights['konservatif'] +
            row['score_standar'] * weights['standar'] +
            row['score_agresif'] * weights['agresif']
        )
        return score
    
    result_df['Ensemble_Score'] = result_df.apply(calc_weighted_score, axis=1)
    result_df['Votes_Count'] = (
        result_df['detected_konservatif'] + 
        result_df['detected_standar'] + 
        result_df['detected_agresif']
    ).astype(int)
    
    # Determine confidence level
    result_df['Confidence_Level'] = pd.cut(
        result_df['Ensemble_Score'],
        bins=[-0.001, 0, 0.34, 0.67, 1.1],
        labels=['NONE', 'LOW', 'MEDIUM', 'HIGH']
    )
    
    result_df['Adaptive_Method'] = 'Ensemble+Age'
    
    # Clean up temp columns
    for preset_name in PRESET_NAMES:
        result_df.drop(columns=[f'score_{preset_name}', f'detected_{preset_name}'], inplace=True)
    
    # Calculate statistics
    metadata = {
        'method': 'ensemble_age',
        'method_name': 'Ensemble Scoring + Age Weight',
        'description': 'Kombinasi 3 preset dengan bobot berdasarkan umur',
        'total_trees': len(result_df),
        'high_confidence': len(result_df[result_df['Confidence_Level'] == 'HIGH']),
        'medium_confidence': len(result_df[result_df['Confidence_Level'] == 'MEDIUM']),
        'low_confidence': len(result_df[result_df['Confidence_Level'] == 'LOW']),
        'no_detection': len(result_df[result_df['Confidence_Level'] == 'NONE']),
        'avg_ensemble_score': result_df['Ensemble_Score'].mean(),
        'merah_count': len(result_df[result_df['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)']),
        'oranye_count': len(result_df[result_df['Status_Risiko'] == 'ORANYE (CINCIN API)']),
        'kuning_count': len(result_df[result_df['Status_Risiko'] == 'KUNING (SUSPECT TERISOLASI)']),
        'hijau_count': len(result_df[result_df['Status_Risiko'] == 'HIJAU (SEHAT)']),
    }
    
    logger.info(f"  Ensemble+Age: HIGH={metadata['high_confidence']}, "
                f"MEDIUM={metadata['medium_confidence']}, LOW={metadata['low_confidence']}")
    
    return result_df, metadata


# =============================================================================
# OPSI 3: ENSEMBLE SCORING PURE (OPTIMIZED)
# =============================================================================

def ensemble_scoring_pure(
    all_results: Dict,
    df_original: pd.DataFrame = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Ensemble Scoring Murni - OPTIMIZED VERSION.
    
    Menggunakan vectorized operations untuk performa optimal.
    """
    logger.info("Running Ensemble Scoring Pure (Optimized)...")
    
    # Use standar as base
    base_df = all_results['standar']['df'].copy()
    key_cols = ['Blok', 'N_BARIS', 'N_POKOK']
    
    # Create score mapping
    score_map = {
        'MERAH (KLUSTER AKTIF)': 1.0,
        'ORANYE (CINCIN API)': 0.75,
        'KUNING (SUSPECT TERISOLASI)': 0.5,
        'HIJAU (SEHAT)': 0.0
    }
    
    weights = ENSEMBLE_CONFIG['weights_default']
    
    # For each preset, create temp df with scores
    preset_scores = {}
    for preset_name in PRESET_NAMES:
        pdf = all_results[preset_name]['df'][key_cols + ['Status_Risiko']].copy()
        pdf[f'score_{preset_name}'] = pdf['Status_Risiko'].map(score_map).fillna(0)
        pdf[f'detected_{preset_name}'] = pdf['Status_Risiko'].isin(RISK_STATUSES).astype(int)
        preset_scores[preset_name] = pdf[key_cols + [f'score_{preset_name}', f'detected_{preset_name}']]
    
    # Merge all preset scores into base_df
    result_df = base_df.copy()
    for preset_name in PRESET_NAMES:
        result_df = result_df.merge(
            preset_scores[preset_name],
            on=key_cols,
            how='left'
        )
    
    # Fill NaN with 0
    for preset_name in PRESET_NAMES:
        result_df[f'score_{preset_name}'] = result_df[f'score_{preset_name}'].fillna(0)
        result_df[f'detected_{preset_name}'] = result_df[f'detected_{preset_name}'].fillna(0)
    
    # Calculate weighted score (equal weights)
    result_df['Ensemble_Score'] = (
        result_df['score_konservatif'] * weights['konservatif'] +
        result_df['score_standar'] * weights['standar'] +
        result_df['score_agresif'] * weights['agresif']
    )
    
    # Count votes
    result_df['Votes_Count'] = (
        result_df['detected_konservatif'] + 
        result_df['detected_standar'] + 
        result_df['detected_agresif']
    ).astype(int)
    
    # Determine confidence level based on votes
    vote_to_conf = {0: 'NONE', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
    result_df['Confidence_Level'] = result_df['Votes_Count'].map(vote_to_conf)
    
    # Create voting detail
    result_df['Voting_Detail'] = ''
    mask_k = result_df['detected_konservatif'] == 1
    mask_s = result_df['detected_standar'] == 1
    mask_a = result_df['detected_agresif'] == 1
    
    def make_vote_detail(row):
        parts = []
        if row['detected_konservatif'] == 1:
            parts.append('K')
        if row['detected_standar'] == 1:
            parts.append('S')
        if row['detected_agresif'] == 1:
            parts.append('A')
        return ','.join(parts) if parts else '-'
    
    result_df['Voting_Detail'] = result_df.apply(make_vote_detail, axis=1)
    
    result_df['Adaptive_Method'] = 'Ensemble Pure'
    
    # Clean up temp columns
    for preset_name in PRESET_NAMES:
        result_df.drop(columns=[f'score_{preset_name}', f'detected_{preset_name}'], inplace=True)
    
    # Calculate statistics
    metadata = {
        'method': 'ensemble_pure',
        'method_name': 'Ensemble Scoring Pure',
        'description': 'Voting murni dari 3 preset (tanpa faktor umur)',
        'total_trees': len(result_df),
        'high_confidence': len(result_df[result_df['Confidence_Level'] == 'HIGH']),
        'medium_confidence': len(result_df[result_df['Confidence_Level'] == 'MEDIUM']),
        'low_confidence': len(result_df[result_df['Confidence_Level'] == 'LOW']),
        'no_detection': len(result_df[result_df['Confidence_Level'] == 'NONE']),
        'votes_3': len(result_df[result_df['Votes_Count'] == 3]),
        'votes_2': len(result_df[result_df['Votes_Count'] == 2]),
        'votes_1': len(result_df[result_df['Votes_Count'] == 1]),
        'votes_0': len(result_df[result_df['Votes_Count'] == 0]),
        'avg_ensemble_score': result_df['Ensemble_Score'].mean(),
        'merah_count': len(result_df[result_df['Status_Risiko'] == 'MERAH (KLUSTER AKTIF)']),
        'oranye_count': len(result_df[result_df['Status_Risiko'] == 'ORANYE (CINCIN API)']),
        'kuning_count': len(result_df[result_df['Status_Risiko'] == 'KUNING (SUSPECT TERISOLASI)']),
        'hijau_count': len(result_df[result_df['Status_Risiko'] == 'HIJAU (SEHAT)']),
    }
    
    logger.info(f"  Ensemble Pure: HIGH(3/3)={metadata['high_confidence']}, "
                f"MEDIUM(2/3)={metadata['medium_confidence']}, LOW(1/3)={metadata['low_confidence']}")
    
    return result_df, metadata



# =============================================================================
# MAIN FUNCTION - RUN ALL ADAPTIVE METHODS
# =============================================================================

def run_all_adaptive_methods(
    all_results: Dict,
    df_original: pd.DataFrame
) -> Dict:
    """
    Run semua metode adaptif dan kembalikan hasilnya.
    
    Args:
        all_results: Dictionary hasil semua preset {'konservatif': {...}, ...}
        df_original: DataFrame original dengan data lengkap
        
    Returns:
        Dictionary dengan hasil semua metode adaptif
    """
    logger.info("="*60)
    logger.info("RUNNING ADAPTIVE DETECTION METHODS")
    logger.info("="*60)
    
    adaptive_results = {}
    
    # Opsi 1: Age-Based
    df_age_based, meta_age_based = age_based_preset_selection(all_results, df_original)
    adaptive_results['age_based'] = {
        'df': df_age_based,
        'metadata': meta_age_based
    }
    
    # Opsi 2: Ensemble + Age
    df_ensemble_age, meta_ensemble_age = ensemble_scoring_with_age(all_results, df_original)
    adaptive_results['ensemble_age'] = {
        'df': df_ensemble_age,
        'metadata': meta_ensemble_age
    }
    
    # Opsi 3: Ensemble Pure
    df_ensemble_pure, meta_ensemble_pure = ensemble_scoring_pure(all_results, df_original)
    adaptive_results['ensemble_pure'] = {
        'df': df_ensemble_pure,
        'metadata': meta_ensemble_pure
    }
    
    logger.info("="*60)
    logger.info("ADAPTIVE DETECTION COMPLETE")
    logger.info("="*60)
    
    return adaptive_results
