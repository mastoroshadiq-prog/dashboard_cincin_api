"""
Data Loader untuk data_baru.csv (Cost Control Data)

Modul ini menyediakan fungsi untuk memuat dan memparse data dari file
data_baru.csv yang memiliki struktur header kompleks.

Kolom yang di-extract:
- DIVISI: AME002 atau AME004
- BLOK: Kode blok (D001A, K18A, dll)
- TT: Tahun Tanam
- LUAS_TANAM: Luas tanam (ha)
- TOTAL_TANAM: Jumlah pohon tanam awal
- SISIP: Jumlah pohon sisipan
- SISIP_KENTOSAN: Jumlah sisipan kentosan
- TOTAL_PKK: Total pohon (tanam + sisip)
- SPH: Stands Per Hectare
- STADIUM_1_2: Pohon Ganoderma stadium 1&2
- STADIUM_3_4: Pohon Ganoderma stadium 3&4
- TOTAL_GANODERMA: Total pohon Ganoderma
- SERANGAN_PCT: Persentase serangan
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import re


def parse_number(value) -> float:
    """Parse number dari format Excel yang mungkin memiliki koma dan spasi."""
    if pd.isna(value) or value == '-' or value == '' or str(value).strip() == '-':
        return 0.0
    
    # Convert ke string dan bersihkan
    s = str(value).strip()
    
    # Hapus karakter non-numeric kecuali titik dan koma
    s = s.replace(' ', '').replace(',', '')
    
    # Hapus tanda persen jika ada
    s = s.replace('%', '')
    
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_percentage(value) -> float:
    """Parse persentase dari format '3.04%' atau '0.00%'."""
    if pd.isna(value) or value == '-' or value == '':
        return 0.0
    
    s = str(value).strip().replace('%', '').replace(',', '.')
    
    try:
        return float(s)
    except ValueError:
        return 0.0


def load_cost_control_data(filepath: Path) -> pd.DataFrame:
    """
    Load dan parse data_baru.csv dengan struktur header kompleks.
    
    Args:
        filepath: Path ke file data_baru.csv
        
    Returns:
        DataFrame dengan kolom yang sudah dinormalisasi
    """
    # Baca raw data, skip header rows
    df_raw = pd.read_csv(filepath, skiprows=7, header=None, encoding='utf-8')
    
    # Definisikan nama kolom berdasarkan struktur yang sudah dianalisis
    # Kolom: 0-ESTATE_LAMA, 1-ESTATE_BARU, 2-DIVISI, 3-BLOK, 4-TT, 
    #        5-LUAS_2024, 6-PENAMBAHAN, 7-LUAS_2025, 8-TOTAL_TANAM, 
    #        9-SISIP, 10-SISIP_KENTOSAN, 11-TOTAL_PKK, 12-SPH,
    #        13-STADIUM_1_2, 14-STADIUM_3_4, 15-TOTAL_GANODERMA, 16-SERANGAN_PCT
    
    columns = [
        'ESTATE_LAMA', 'ESTATE_BARU', 'DIVISI', 'BLOK', 'TT',
        'LUAS_2024', 'PENAMBAHAN', 'LUAS_2025', 'TOTAL_TANAM',
        'SISIP', 'SISIP_KENTOSAN', 'TOTAL_PKK', 'SPH',
        'STADIUM_1_2', 'STADIUM_3_4', 'TOTAL_GANODERMA', 'SERANGAN_PCT'
    ]
    
    # Assign column names (hanya ambil yang ada)
    df_raw.columns = columns[:len(df_raw.columns)]
    
    # Filter baris yang valid (memiliki DIVISI)
    df = df_raw[df_raw['DIVISI'].notna() & (df_raw['DIVISI'] != '')].copy()
    
    # Parse numeric columns
    numeric_cols = ['TT', 'LUAS_2024', 'PENAMBAHAN', 'LUAS_2025', 'TOTAL_TANAM',
                    'SISIP', 'SISIP_KENTOSAN', 'TOTAL_PKK', 'SPH',
                    'STADIUM_1_2', 'STADIUM_3_4', 'TOTAL_GANODERMA']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_number)
    
    # Parse percentage
    if 'SERANGAN_PCT' in df.columns:
        df['SERANGAN_PCT'] = df['SERANGAN_PCT'].apply(parse_percentage)
    
    # Hitung rasio sisipan
    df['RASIO_SISIP'] = np.where(
        df['TOTAL_PKK'] > 0,
        (df['SISIP'] + df['SISIP_KENTOSAN']) / df['TOTAL_PKK'] * 100,
        0
    )
    
    # Normalisasi blok untuk matching
    df['BLOK_NORM'] = df['BLOK'].apply(normalize_block)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df


def normalize_block(blok: str) -> str:
    """
    Normalisasi kode blok untuk matching.
    D001A -> D01, K18A -> K18
    """
    if pd.isna(blok) or not blok:
        return ''
    
    blok = str(blok).strip().upper()
    
    # Extract letter prefix dan angka
    match = re.match(r'([A-Z]+)(\d+)', blok)
    if match:
        letter = match.group(1)
        number = int(match.group(2))
        return f"{letter}{number:02d}"
    
    return blok


def get_replant_ratio_dict(df: pd.DataFrame) -> Dict[str, float]:
    """
    Menghasilkan dictionary rasio sisipan per blok.
    
    Args:
        df: DataFrame dari load_cost_control_data()
        
    Returns:
        Dict[blok_normalized, rasio_sisipan]
    """
    return dict(zip(df['BLOK_NORM'], df['RASIO_SISIP'] / 100))


def get_book_count_dict(df: pd.DataFrame) -> Dict[str, int]:
    """
    Menghasilkan dictionary jumlah pohon per blok (data buku).
    
    Args:
        df: DataFrame dari load_cost_control_data()
        
    Returns:
        Dict[blok_normalized, total_pkk]
        
    Note:
        Jika ada multiple rows dengan BLOK_NORM sama (misal A12A, A12B, A12C -> A12),
        maka TOTAL_PKK akan dijumlahkan.
    """
    # Group by BLOK_NORM dan sum TOTAL_PKK untuk handle duplicate blok
    return df.groupby('BLOK_NORM')['TOTAL_PKK'].sum().astype(int).to_dict()


def get_census_data_dict(df: pd.DataFrame) -> Dict[str, Tuple[int, int, float]]:
    """
    Menghasilkan dictionary data sensus per blok.
    
    Args:
        df: DataFrame dari load_cost_control_data()
        
    Returns:
        Dict[blok_normalized, (stadium_3_4, total_ganoderma, serangan_pct)]
    """
    result = {}
    for _, row in df.iterrows():
        blok = row['BLOK_NORM']
        result[blok] = (
            int(row['STADIUM_3_4']),
            int(row['TOTAL_GANODERMA']),
            row['SERANGAN_PCT']
        )
    return result


def summarize_cost_control_data(df: pd.DataFrame) -> None:
    """Print summary dari data cost control."""
    print("\n" + "="*70)
    print("SUMMARY DATA COST CONTROL (data_baru.csv)")
    print("="*70)
    
    for divisi in df['DIVISI'].unique():
        df_div = df[df['DIVISI'] == divisi]
        print(f"\n{divisi}:")
        print(f"  - Blok: {len(df_div)}")
        print(f"  - Total PKK: {df_div['TOTAL_PKK'].sum():,.0f}")
        print(f"  - Rata-rata Rasio Sisip: {df_div['RASIO_SISIP'].mean():.1f}%")
        print(f"  - Blok dengan Sisip >20%: {len(df_div[df_div['RASIO_SISIP'] > 20])}")
        print(f"  - Total Ganoderma: {df_div['TOTAL_GANODERMA'].sum():,.0f}")
        print(f"  - Rata-rata % Serangan: {df_div['SERANGAN_PCT'].mean():.2f}%")


def load_ground_truth_excel(filepath: Path) -> pd.DataFrame:
    """
    Load data ground truth dari file Excel (areal_inti_serangan_gano_AMEII_AMEIV.xlsx).
    
    File ini adalah sumber data yang benar untuk:
    - TOTAL_PKK: Jumlah pohon per blok
    - STADIUM_1_2: Ganoderma stadium awal
    - STADIUM_3_4: Ganoderma stadium lanjut
    - TOTAL_GANODERMA: Total pohon terinfeksi
    - SERANGAN_PCT: Persentase serangan
    
    Args:
        filepath: Path ke file Excel
        
    Returns:
        DataFrame dengan kolom yang sudah dinormalisasi
    """
    # Read Excel with header at row 1 (0-indexed = row 2)
    df = pd.read_excel(filepath, sheet_name='Sheet1', header=1)
    
    # Assign proper column names based on structure
    # Columns: DIVISI, BLOK, TT, LUAS_TANAM, ?, ?, TOTAL_PKK, ?, ?, SPH, 
    #          STADIUM_12, STADIUM_34, TOTAL_GANODERMA, SERANGAN_PCT, ?
    df.columns = ['DIVISI', 'BLOK', 'TT', 'LUAS_TANAM', 'C4', 'C5', 
                  'TOTAL_PKK', 'C7', 'C8', 'SPH', 'STADIUM_1_2', 
                  'STADIUM_3_4', 'TOTAL_GANODERMA', 'SERANGAN_PCT', 'C14']
    
    # Filter only AME002 and AME004
    df = df[df['DIVISI'].isin(['AME002', 'AME004'])].copy()
    
    # Convert numeric columns
    for col in ['TOTAL_PKK', 'STADIUM_1_2', 'STADIUM_3_4', 'TOTAL_GANODERMA', 'SPH']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Convert percentage
    df['SERANGAN_PCT'] = pd.to_numeric(df['SERANGAN_PCT'], errors='coerce').fillna(0) * 100
    
    # Normalize block names for matching
    df['BLOK_NORM'] = df['BLOK'].apply(normalize_block)
    
    return df


def get_ground_truth_book_dict(df: pd.DataFrame) -> Dict[str, int]:
    """
    Menghasilkan dictionary jumlah pohon per blok dari ground truth Excel.
    
    Args:
        df: DataFrame dari load_ground_truth_excel()
        
    Returns:
        Dict[blok_normalized, total_pkk]
    """
    return df.groupby('BLOK_NORM')['TOTAL_PKK'].sum().astype(int).to_dict()


def get_ground_truth_census_dict(df: pd.DataFrame) -> Dict[str, Tuple[int, int, float]]:
    """
    Menghasilkan dictionary data sensus per blok dari ground truth Excel.
    
    Args:
        df: DataFrame dari load_ground_truth_excel()
        
    Returns:
        Dict[blok_normalized, (stadium_3_4, total_ganoderma, serangan_pct)]
        
    Note:
        Jika ada multiple rows dengan BLOK_NORM sama, nilai akan dijumlahkan.
    """
    # Group by BLOK_NORM dan sum values
    grouped = df.groupby('BLOK_NORM').agg({
        'STADIUM_3_4': 'sum',
        'TOTAL_GANODERMA': 'sum',
        'TOTAL_PKK': 'sum'
    })
    
    result = {}
    for blok, row in grouped.iterrows():
        total_pkk = row['TOTAL_PKK']
        total_gano = row['TOTAL_GANODERMA']
        serangan_pct = (total_gano / total_pkk * 100) if total_pkk > 0 else 0
        result[blok] = (
            int(row['STADIUM_3_4']),
            int(total_gano),
            serangan_pct
        )
    return result



if __name__ == "__main__":
    # Test loading
    data_path = Path(__file__).parent / "data" / "input" / "data_baru.csv"
    
    if data_path.exists():
        df = load_cost_control_data(data_path)
        summarize_cost_control_data(df)
        
        print("\n" + "="*70)
        print("Sample Data (first 5 rows):")
        print("="*70)
        print(df[['DIVISI', 'BLOK', 'TT', 'TOTAL_PKK', 'SISIP', 'RASIO_SISIP', 
                  'TOTAL_GANODERMA', 'SERANGAN_PCT']].head(10).to_string())
    else:
        print(f"File not found: {data_path}")
