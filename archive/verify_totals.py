import pandas as pd

df = pd.read_csv('poac_sim/data/input/tabelNDREnew.csv')

f008a = df[df['blok_b'] == 'F008A']
d001a = df[df['blok_b'] == 'D001A']

print("="*60)
print("VERIFIKASI DATA DARI CSV:")
print("="*60)
print("\nF008A:")
print(f"  Total pohon: {len(f008a)}")
print(f"  TT (Tahun Tanam): {f008a['t_tanam'].iloc[0]}")

print("\nD001A:")
print(f"  Total pohon: {len(d001a)}")
print(f"  TT (Tahun Tanam): {d001a['t_tanam'].iloc[0]}")

print("\n" + "="*60)
print("DATA DARI V8 ALGORITHM JSON:")
print("="*60)

import json
with open('data/output/cincin_api_stats_v8_algorithm.json', 'r') as f:
    v8_data = json.load(f)
    
print("\nF008A (V8):")
for key, val in v8_data['F008A'].items():
    print(f"  {key}: {val}")

print("\nD001A (V8):")
for key, val in v8_data['D001A'].items():
    print(f"  {key}: {val}")

print("\n" + "="*60)
print("ANALISIS:")
print("="*60)

# Calculate hijau if total is different
f_total_csv = len(f008a)
f_total_v8 = v8_data['F008A']['total_trees']
f_merah = v8_data['F008A']['merah']
f_oranye = v8_data['F008A']['oranye']
f_kuning = v8_data['F008A']['kuning']
f_hijau_v8 = v8_data['F008A']['hijau']

print(f"\nF008A:")
print(f"  CSV total: {f_total_csv}")
print(f"  V8 total: {f_total_v8}")
print(f"  Selisih: {f_total_csv - f_total_v8}")
print(f"  Merah+Oranye+Kuning: {f_merah + f_oranye + f_kuning}")
print(f"  Hijau (V8): {f_hijau_v8}")
print(f"  Hijau (recalc): {f_total_csv - (f_merah + f_oranye + f_kuning)}")

d_total_csv = len(d001a)
d_total_v8 = v8_data['D001A']['total_trees']
d_merah = v8_data['D001A']['merah']
d_oranye = v8_data['D001A']['oranye']
d_kuning = v8_data['D001A']['kuning']
d_hijau_v8 = v8_data['D001A']['hijau']

print(f"\nD001A:")
print(f"  CSV total: {d_total_csv}")
print(f"  V8 total: {d_total_v8}")
print(f"  Selisih: {d_total_csv - d_total_v8}")
print(f"  Merah+Oranye+Kuning: {d_merah + d_oranye + d_kuning}")
print(f"  Hijau (V8): {d_hijau_v8}")
print(f"  Hijau (recalc): {d_total_csv - (d_merah + d_oranye + d_kuning)}")
