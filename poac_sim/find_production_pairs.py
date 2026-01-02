import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

f008a = df[df['Unnamed: 0'] == 'F008A'].iloc[0]
d001a = df[df['Unnamed: 0'] == 'D001A'].iloc[0]

luas_f008a = 29.6
luas_d001a = 25.8

print('='*80)
print('🔍 MENCARI KOLOM PRODUKSI 2025 YANG BENAR')
print('='*80)
print('\nMencari kolom dengan total produksi (Ton) yang masuk akal:')
print('Expected range: 200-800 Ton untuk luas 25-30 Ha')
print('Expected Ton/Ha: 10-30 Ton/Ha')
print()

candidates = []

for i in range(len(f008a)):
    val_f008a = f008a.iloc[i]
    val_d001a = d001a.iloc[i]
    
    if pd.notna(val_f008a) and isinstance(val_f008a, (int, float)):
        if 200 < val_f008a < 1000:
            ton_ha_f008a = val_f008a / luas_f008a
            ton_ha_d001a = val_d001a / luas_d001a if pd.notna(val_d001a) else None
            
            # Check if Ton/Ha is in reasonable range (10-30)
            if 10 < ton_ha_f008a < 30:
                candidates.append({
                    'col': i,
                    'col_name': df.columns[i],
                    'f008a_ton': val_f008a,
                    'f008a_ton_ha': ton_ha_f008a,
                    'd001a_ton': val_d001a,
                    'd001a_ton_ha': ton_ha_d001a
                })

print(f'Found {len(candidates)} candidate columns:\n')
for c in candidates:
    print(f"Col {c['col']} ({c['col_name']}):")
    print(f"  F008A: {c['f008a_ton']:.2f} Ton → {c['f008a_ton_ha']:.2f} Ton/Ha")
    if c['d001a_ton_ha']:
        print(f"  D001A: {c['d001a_ton']:.2f} Ton → {c['d001a_ton_ha']:.2f} Ton/Ha")
    print()

# Now let's look for pairs (Real and Potensi)
print('='*80)
print('🎯 MENCARI PASANGAN REAL DAN POTENSI')
print('='*80)

# Typically, Real and Potensi are 3 columns apart (BJR Kg, Jum Jlg, Ton)
# So if Real Ton is at column X, Potensi Ton should be at X+3

for c in candidates:
    col_idx = c['col']
    
    # Check if there's another candidate 3 columns away
    for c2 in candidates:
        if c2['col'] == col_idx + 3:
            print(f"\n✅ POSSIBLE PAIR FOUND:")
            d001a_real_str = f"{c['d001a_ton_ha']:.2f}" if c['d001a_ton_ha'] else 'N/A'
            d001a_potensi_str = f"{c2['d001a_ton_ha']:.2f}" if c2['d001a_ton_ha'] else 'N/A'
            print(f"  Real (Col {col_idx}): F008A={c['f008a_ton_ha']:.2f} Ton/Ha, D001A={d001a_real_str} Ton/Ha")
            print(f"  Potensi (Col {c2['col']}): F008A={c2['f008a_ton_ha']:.2f} Ton/Ha, D001A={d001a_potensi_str} Ton/Ha")
            
            # Calculate gap
            gap_f008a = c['f008a_ton_ha'] - c2['f008a_ton_ha']
            gap_pct_f008a = (gap_f008a / c2['f008a_ton_ha']) * 100
            
            if c['d001a_ton_ha'] and c2['d001a_ton_ha']:
                gap_d001a = c['d001a_ton_ha'] - c2['d001a_ton_ha']
                gap_pct_d001a = (gap_d001a / c2['d001a_ton_ha']) * 100
                
                print(f"\n  GAP:")
                print(f"    F008A: {gap_f008a:.2f} Ton/Ha ({gap_pct_f008a:.1f}%)")
                print(f"    D001A: {gap_d001a:.2f} Ton/Ha ({gap_pct_d001a:.1f}%)")

print('\n✅ Selesai!')
