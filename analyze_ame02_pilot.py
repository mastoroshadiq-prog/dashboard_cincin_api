"""
PILOT ANALYSIS: AME II (AME02)
Analisa Gap Yield, Attack Rate Ganoderma, dan Avg Yield untuk divisi AME II

Metrics:
1. Gap Yield = Potensi Produksi - Realisasi Produksi
2. Loss/Kerugian = Gap Yield × Harga TBS
3. Avg Attack Rate Ganoderma (stadium 1-4)
4. Avg Yield per blok
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths
INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_FILE = Path("poac_sim/data/output/ame02_analysis.json")

# Default TBS price (akan bisa di-adjust via slider di dashboard)
DEFAULT_TBS_PRICE = 2500  # Rupiah per KG

def analyze_ame02(tbs_price=DEFAULT_TBS_PRICE):
    """
    Analisa AME II (AME02) untuk:
    - Gap Yield (Potensi - Realisasi)
    - Loss/Kerugian financial
    - Attack Rate Ganoderma
    - Average Yield
    """
    
    print("=" * 80)
    print("PILOT ANALYSIS: AME II (AME02)")
    print("=" * 80)
    
    # Load data
    print(f"\n[*] Loading data dari: {INPUT_FILE}")
    df = pd.read_excel(INPUT_FILE)
    
    print(f"[OK] Total data loaded: {len(df)} rows")
    print(f"\n[INFO] Kolom tersedia ({len(df.columns)}):")
    for i, col in enumerate(df.columns[:20], 1):  # Show first 20 columns
        print(f"   {i:2}. {col}")
    if len(df.columns) > 20:
        print(f"   ... dan {len(df.columns) - 20} kolom lainnya")
    
    # Sample first row to understand structure
    print("\n" + "=" * 80)
    print("SAMPLE DATA (First Row):")
    print("=" * 80)
    first_row = df.iloc[0]
    for col, val in first_row.items():
        if pd.notna(val):
            print(f"{col}: {val}")
    
    # Try to identify division column
    print("\n" + "=" * 80)
    print("MENCARI KOLOM DIVISI...")
    print("=" * 80)
    
    division_col = None
    possible_div_cols = ['divisi', 'division', 'div', 'estate', 'afdeling', 'blok']
    
    for col in df.columns:
        col_lower = str(col).lower()
        if any(div_name in col_lower for div_name in possible_div_cols):
            print(f"[OK] Kandidat kolom divisi: '{col}'")
            print(f"   Sample values: {df[col].unique()[:10]}")
            
    return df

def main():
    df = analyze_ame02()
    
    print("\n" + "=" * 80)
    print("[INFO] Silakan periksa output di atas untuk identifikasi kolom yang benar")
    print("=" * 80)

if __name__ == "__main__":
    main()
