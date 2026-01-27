"""
Script untuk memeriksa struktur file Excel data_gabungan.xlsx
"""

import pandas as pd
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")

print("=" * 80)
print("INSPEKSI STRUKTUR FILE EXCEL")
print("=" * 80)

# Load file
print(f"\n📂 Loading: {INPUT_FILE}")
df = pd.read_excel(INPUT_FILE)

print(f"\n✅ Loaded {len(df)} rows")
print(f"✅ Shape: {df.shape}")

print("\n" + "=" * 80)
print("KOLOM YANG TERSEDIA:")
print("=" * 80)
for i, col in enumerate(df.columns, 1):
    print(f"{i:2}. {col}")

print("\n" + "=" * 80)
print("SAMPLE DATA (5 ROWS):")
print("=" * 80)
print(df.head())

print("\n" + "=" * 80)
print("INFO DATATYPES:")
print("=" * 80)
print(df.info())

print("\n" + "=" * 80)
print("STATISTIK DESKRIPTIF:")
print("=" * 80)
print(df.describe())
