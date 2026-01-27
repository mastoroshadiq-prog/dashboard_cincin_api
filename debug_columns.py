"""
Debug untuk identifikasi kolom yang benar
"""

import pandas as pd

INPUT_FILE = "poac_sim/data/input/data_gabungan.xlsx"

df = pd.read_excel(INPUT_FILE)

# Print columns around 2025 data (169-176)
print("Columns 165-177 (around 2025 data):")
for i in range(165, 177):
    if i < len(df.columns):
        col_name = df.columns[i]
        # Show header values from rows 0, 1, 2
        val_0 = df.iloc[0, i] if pd.notna(df.iloc[0, i]) else ""
        val_1 = df.iloc[1, i] if pd.notna(df.iloc[1, i]) else ""
        val_2 = df.iloc[2, i] if pd.notna(df.iloc[2, i]) else ""
        
        print(f"\n{i}. {col_name}")
        print(f"   Row 0: {val_0}")
        print(f"   Row 1: {val_1}")
        print(f"   Row 2: {val_2}")

# Sample AME02 data for these columns
print("\n" + "=" * 80)
print("Sample AME02 data for columns 169-176:")
print("=" * 80)

divisi_col = df.columns[5]
ame02_mask = df[divisi_col] == 'AME02'
ame02_sample = df[ame02_mask].iloc[0]  # First AME02 row

for i in range(169, 177):
    if i < len(df.columns):
        col_name = df.columns[i]
        value = ame02_sample.iloc[i] if i < len(ame02_sample) else "N/A"
        print(f"{i}. {col_name}: {value}")
