"""
CORRECT EXTRACTION - User showed me the exact columns!
Column P (index 15) = Realisasi Ton (P109)
Column P+3 (index 18) = Potensi Ton (P112)  
Column P+6 (index 21) = Gap Ton (P115)
"""
import json
import pandas as pd

print("📊 EXTRACTING PRODUCTION DATA - CORRECT COLUMNS")
print("="*70)

# Load the raw data I already extracted
with open('data/output/all_36_blocks_raw_rows.json') as f:
    raw_data = json.load(f)

print(f"✅ Loaded {len(raw_data)} blocks\n")

# Based on screenshot:
# Real (Realisasi): Column P = index 15 (for Ton)
# Potensi: Column P+3 (Real has 3 sub-cols: BJR Kg, Jum Jlg, Ton) = index 15+3 = 18
# Gap: Column P+6 = index 15+6 = 21

# But wait, let me verify the structure first
print("Checking F008A columns around index 15:")
f008_vals = raw_data['F008A']['values']
for i in range(10, 25):
    print(f"Col {i}: {f008_vals[i]}")

print("\n" + "="*70)
print("Checking D001A columns around index 15:")
d001_vals = raw_data['D001A']['values']
for i in range(10, 25):
    print(f"Col {i}: {d001_vals[i]}")

# Now let me re-load the Excel to get proper column mapping
print("\n" + "="*70)
print("Re-loading Excel to verify column structure...")

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

# Find F008A row
for i in range(len(df)):
    if str(df.iloc[i, 0]).strip() == 'F008A':
        print(f"\n✅ Found F008A at row {i}")
        print(f"\nColumns 105-120 (around P which is col 15 in 0-indexed):")
        for col_idx in range(105, 120):
            if col_idx < len(df.columns):
                val = df.iloc[i, col_idx]
                print(f"  Col {col_idx}: {val}")
        break
