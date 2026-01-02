import pandas as pd
import numpy as np

print('='*80)
print('🔍 ANALISIS KOMPREHENSIF: DISKREPANSI PKK vs NDRE')
print('='*80)

# Load data_gabungan.xlsx
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

# Load Cincin Api ranking
df_ranked = pd.read_csv('data/output/all_blocks_ranked_by_severity.csv')

print('\n📊 PART 1: ANALISIS D001A')
print('='*80)

# Get D001A data
d001a = df[df['Unnamed: 0'] == 'D001A'].iloc[0]

print(f'\nBLOK D001A - DATA DASAR:')
print(f'  Luas: {d001a["HA STATEMENT"]} Ha')
print(f'  TT: {d001a["TT"]}')

# Find Ganoderma columns for D001A
# Based on F008A pattern, look for values around 93, 13, 106
print('\n🔍 MENCARI DATA PKK (Manual Survey):')

# Check columns around 55-57 (based on F008A pattern)
col_55 = d001a.iloc[55] if len(d001a) > 55 else None
col_56 = d001a.iloc[56] if len(d001a) > 56 else None
col_57 = d001a.iloc[57] if len(d001a) > 57 else None

print(f'  Col 55 (SERANGAN GANODERMA): {col_55}')
print(f'  Col 56: {col_56}')
print(f'  Col 57: {col_57}')

# From NDRE data
d001a_ndre = df_ranked[df_ranked['blok'] == 'D01'].iloc[0]
total_trees_d001a = int(d001a_ndre['total_trees'])
merah_d001a = int(d001a_ndre['merah'])
oranye_d001a = int(d001a_ndre['oranye'])
kuning_d001a = int(d001a_ndre['kuning'])
hijau_d001a = int(d001a_ndre['hijau'])

total_infected_ndre = merah_d001a + oranye_d001a
pct_infected_ndre = (total_infected_ndre / total_trees_d001a) * 100

# Assuming col_57 is total PKK (like F008A pattern)
if col_57 and isinstance(col_57, (int, float)):
    total_pkk_d001a = int(col_57)
    pct_pkk_d001a = (total_pkk_d001a / total_trees_d001a) * 100
    
    print('\n📊 PERBANDINGAN DATA GANODERMA D001A:')
    print('\n1️⃣ DATA PKK (MANUAL SURVEY):')
    print(f'   Stadium 1 & 2: {col_55} pohon')
    print(f'   Stadium 3 & 4: {col_56} pohon')
    print(f'   Total Terserang: {total_pkk_d001a} pohon')
    print(f'   Total Pohon: {total_trees_d001a} pohon')
    print(f'   Persentase: {pct_pkk_d001a:.2f}%')
    
    print('\n2️⃣ DATA NDRE (DRONE):')
    print(f'   Merah (Inti): {merah_d001a} pohon')
    print(f'   Oranye (Cincin Api): {oranye_d001a} pohon')
    print(f'   Kuning (Suspect): {kuning_d001a} pohon')
    print(f'   Total Terinfeksi (Merah + Oranye): {total_infected_ndre} pohon')
    print(f'   Total Pohon: {total_trees_d001a} pohon')
    print(f'   Persentase: {pct_infected_ndre:.1f}%')
    
    print('\n⚠️  DISKREPANSI D001A:')
    gap_d001a = total_infected_ndre - total_pkk_d001a
    gap_multiplier_d001a = total_infected_ndre / total_pkk_d001a if total_pkk_d001a > 0 else 0
    gap_percentage_d001a = ((total_infected_ndre - total_pkk_d001a) / total_pkk_d001a) * 100 if total_pkk_d001a > 0 else 0
    
    print(f'   Gap Absolut: {gap_d001a} pohon')
    print(f'   Gap Multiplier: {gap_multiplier_d001a:.1f}x')
    print(f'   Gap Persentase: {gap_percentage_d001a:.0f}%')
    
    print(f'\n   🔥 NDRE mendeteksi {gap_multiplier_d001a:.1f}x LEBIH BANYAK pohon terinfeksi!')

print('\n' + '='*80)
print('📊 PART 2: MENCARI BLOK MIRIP F008A')
print('='*80)

# Get F008A stats
f008a_ndre = df_ranked[df_ranked['blok'] == 'F08'].iloc[0]

print(f'\nF008A Reference:')
print(f'  Spread Ratio: {f008a_ndre["spread_ratio"]:.0f}x')
print(f'  Infection %: {f008a_ndre["infection_pct"]:.1f}%')
print(f'  Severity Score: {f008a_ndre["severity_score"]:.0f}')

# Find blocks with similar characteristics
# Criteria: Spread Ratio >500x AND Infection >20%
similar_blocks = df_ranked[
    (df_ranked['spread_ratio'] > 500) & 
    (df_ranked['infection_pct'] > 20)
].head(10)

print(f'\n🔍 BLOK DENGAN KARAKTERISTIK MIRIP F008A:')
print(f'   (Spread Ratio >500x AND Infection >20%)')
print()

for idx, (i, row) in enumerate(similar_blocks.iterrows(), 1):
    print(f'{idx}. BLOK {row["blok"]}')
    print(f'   Spread Ratio: {row["spread_ratio"]:.0f}x')
    print(f'   Infection %: {row["infection_pct"]:.1f}%')
    print(f'   Severity Score: {row["severity_score"]:.0f}')
    print(f'   Merah: {int(row["merah"])} | Oranye: {int(row["oranye"])} | Kuning: {int(row["kuning"])}')
    print()

# Get production data for top similar blocks
print('='*80)
print('📊 PART 3: DATA PRODUKSI BLOK MIRIP F008A')
print('='*80)

# Get top 3 similar blocks (excluding F008A itself)
top_similar = similar_blocks[similar_blocks['blok'] != 'F08'].head(3)

for idx, (i, row) in enumerate(top_similar.iterrows(), 1):
    blok_code = row['blok']
    
    # Convert to format for data_gabungan (e.g., D01 -> D 01)
    blok_formatted = f'{blok_code[0]} {blok_code[1:]}'
    
    # Find in data_gabungan
    blok_row = df[df['BLOK'] == blok_formatted]
    
    if len(blok_row) > 0:
        blok_data = blok_row.iloc[0]
        blok_code_full = blok_data['Unnamed: 0']
        luas = blok_data['HA STATEMENT']
        
        # Get production data (col 170 = Real, col 173 = Potensi)
        real_ton = blok_data.iloc[170] if len(blok_data) > 170 else None
        potensi_ton = blok_data.iloc[173] if len(blok_data) > 173 else None
        
        if real_ton and potensi_ton and luas:
            real_ton_ha = real_ton / luas
            potensi_ton_ha = potensi_ton / luas
            gap_ton_ha = real_ton_ha - potensi_ton_ha
            gap_pct = (gap_ton_ha / potensi_ton_ha) * 100
            
            print(f'\n{idx}. BLOK {blok_code_full} ({blok_formatted}):')
            print(f'   Luas: {luas} Ha')
            print(f'   Spread Ratio: {row["spread_ratio"]:.0f}x | Infection: {row["infection_pct"]:.1f}%')
            print(f'   Real: {real_ton_ha:.2f} Ton/Ha')
            print(f'   Potensi: {potensi_ton_ha:.2f} Ton/Ha')
            print(f'   Gap: {gap_ton_ha:.2f} Ton/Ha ({gap_pct:.1f}%)')
            
            # Check PKK data
            col_57_val = blok_data.iloc[57] if len(blok_data) > 57 else None
            if col_57_val:
                total_trees = int(row['total_trees'])
                pkk_pct = (col_57_val / total_trees) * 100
                ndre_pct = row['infection_pct']
                gap_multiplier = ndre_pct / pkk_pct if pkk_pct > 0 else 0
                
                print(f'   PKK: {col_57_val:.0f} pohon ({pkk_pct:.1f}%)')
                print(f'   NDRE: {int(row["merah"] + row["oranye"])} pohon ({ndre_pct:.1f}%)')
                print(f'   Diskrepansi: {gap_multiplier:.1f}x')

print('\n' + '='*80)
print('📊 SUMMARY PERBANDINGAN')
print('='*80)

# Create summary table
summary_data = []

# F008A
f008a_prod = df[df['Unnamed: 0'] == 'F008A'].iloc[0]
f008a_real = f008a_prod.iloc[170] / f008a_prod['HA STATEMENT']
f008a_potensi = f008a_prod.iloc[173] / f008a_prod['HA STATEMENT']
f008a_gap_pct = ((f008a_real - f008a_potensi) / f008a_potensi) * 100

summary_data.append({
    'Blok': 'F008A',
    'Spread_Ratio': f008a_ndre['spread_ratio'],
    'Infection_Pct': f008a_ndre['infection_pct'],
    'Gap_Produksi_Pct': f008a_gap_pct
})

# D001A
d001a_prod = df[df['Unnamed: 0'] == 'D001A'].iloc[0]
d001a_real = d001a_prod.iloc[170] / d001a_prod['HA STATEMENT']
d001a_potensi = d001a_prod.iloc[173] / d001a_prod['HA STATEMENT']
d001a_gap_pct = ((d001a_real - d001a_potensi) / d001a_potensi) * 100

summary_data.append({
    'Blok': 'D001A',
    'Spread_Ratio': d001a_ndre['spread_ratio'],
    'Infection_Pct': d001a_ndre['infection_pct'],
    'Gap_Produksi_Pct': d001a_gap_pct
})

# Top 3 similar blocks
for idx, (i, row) in enumerate(top_similar.iterrows()):
    blok_code = row['blok']
    blok_formatted = f'{blok_code[0]} {blok_code[1:]}'
    blok_row = df[df['BLOK'] == blok_formatted]
    
    if len(blok_row) > 0:
        blok_data = blok_row.iloc[0]
        blok_code_full = blok_data['Unnamed: 0']
        luas = blok_data['HA STATEMENT']
        real_ton = blok_data.iloc[170]
        potensi_ton = blok_data.iloc[173]
        
        if real_ton and potensi_ton and luas:
            real_ton_ha = real_ton / luas
            potensi_ton_ha = potensi_ton / luas
            gap_pct = ((real_ton_ha - potensi_ton_ha) / potensi_ton_ha) * 100
            
            summary_data.append({
                'Blok': blok_code_full,
                'Spread_Ratio': row['spread_ratio'],
                'Infection_Pct': row['infection_pct'],
                'Gap_Produksi_Pct': gap_pct
            })

print('\nTabel Summary:')
print(f"{'Blok':<10} {'Spread Ratio':<15} {'Infection %':<15} {'Gap Produksi %':<15}")
print('-' * 60)
for data in summary_data:
    print(f"{data['Blok']:<10} {data['Spread_Ratio']:>10.0f}x     {data['Infection_Pct']:>10.1f}%     {data['Gap_Produksi_Pct']:>10.1f}%")

print('\n✅ Analisis selesai!')
