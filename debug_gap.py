"""
Quick debug: Check actual gap values from Excel column 176
"""

import pandas as pd

df = pd.read_excel("poac_sim/data/input/data_gabungan.xlsx")

# Filter AME02
divisi_col = df.columns[5]
ame02 = df[df[divisi_col] == 'AME02'].copy()

# Get columns
real_col = df.columns[170]  # Real Ton
pot_col = df.columns[173]   # Potensi Ton  
gap_col = df.columns[176]   # Gap from Excel

print(f"AME02 Sample (first 5 rows):")
print("="*80)

for idx in range(min(5, len(ame02))):
    row = ame02.iloc[idx]
    real = row[real_col]
    pot = row[pot_col]
    gap_excel = row[gap_col]
    
    gap_calc_pot_minus_real = pot - real if pd.notna(pot) and pd.notna(real) else 0
    gap_calc_real_minus_pot = real - pot if pd.notna(pot) and pd.notna(real) else 0
    
    print(f"\n Row {idx+1}:")
    print(f"   Real: {real}")
    print(f"   Pot:  {pot}")
    print(f"   Gap (Excel col 176): {gap_excel}")
    print(f"   Gap (pot - real):    {gap_calc_pot_minus_real:.2f}")
    print(f"   Gap (real - pot):    {gap_calc_real_minus_pot:.2f}")

print("\n" + "="*80)
print("TOTALS:")
real_total = pd.to_numeric(ame02[real_col], errors='coerce').sum()
pot_total = pd.to_numeric(ame02[pot_col], errors='coerce').sum()
gap_excel_total = pd.to_numeric(ame02[gap_col], errors='coerce').sum()

print(f"Total Real:  {real_total:,.2f} Ton")
print(f"Total Pot:   {pot_total:,.2f} Ton")
print(f"Total Gap (Excel): {gap_excel_total:,.2f} Ton")
print(f"Total Gap (pot-real): {pot_total - real_total:,.2f} Ton")
print(f"Total Gap (real-pot): {real_total - pot_total:,.2f} Ton")
