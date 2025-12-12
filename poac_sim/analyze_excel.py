"""Debug get_book_count_dict"""
import pandas as pd
from pathlib import Path
from src.cost_control_loader import load_cost_control_data, normalize_block

# Load book data
df_csv = load_cost_control_data(Path('data/input/data_baru.csv'))
df_ame4 = df_csv[df_csv['DIVISI'] == 'AME004']

print("="*70)
print("DATA BUKU AME004")
print("="*70)
print(f"Rows: {len(df_ame4)}")
print(f"Sum TOTAL_PKK: {df_ame4['TOTAL_PKK'].sum():,.0f}")

print("\nAll rows dengan BLOK_NORM dan TOTAL_PKK:")
for idx, row in df_ame4.iterrows():
    blok_orig = row['BLOK']
    blok_norm = row['BLOK_NORM']
    pkk = row['TOTAL_PKK']
    print(f"  {blok_orig:10} -> {blok_norm:10} : {pkk:>8,.0f}")

# Check if there are duplicates
print("\n" + "="*70)
print("DUPLICATE CHECK")
print("="*70)
dups = df_ame4['BLOK_NORM'].value_counts()
dups_multi = dups[dups > 1]
if len(dups_multi) > 0:
    print("Duplicate BLOK_NORM found:")
    print(dups_multi)
else:
    print("No duplicates found")

# Sum by BLOK_NORM to see actual totals
print("\n" + "="*70)
print("GROUPED BY BLOK_NORM")
print("="*70)
grouped = df_ame4.groupby('BLOK_NORM')['TOTAL_PKK'].sum()
print(f"Total blok: {len(grouped)}")
print(f"Sum: {grouped.sum():,.0f}")
for blok, pkk in sorted(grouped.items()):
    print(f"  {blok}: {pkk:,.0f}")
