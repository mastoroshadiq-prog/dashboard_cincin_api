"""
Analyze all 20 blocks without yield data
Check TANAM (new planting) per year to determine TBM status
"""
import pandas as pd
import json

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Blocks without yield data
blocks_no_yield = [
    'A005C', 'A006A', 'A007A', 'B007D', 'B008E', 'B009G',
    'B015D', 'B016G', 'B017F',
    'C027B', 'D027I', 'D028F', 'D029B', 'D033A', 'D034A', 'E032B', 'F029G', 'F030F', 'F031E',
    'J021A'
]

# Year columns based on header analysis
# Col 34-35: THN 2020 (TANAM, SISIP)
# Col 36-37: THN 2021 (TANAM, SISIP)
# Col 38-39: THN 2022 (TANAM, SISIP)
# Col 40-42: THN 2023 (TANAM, SISIP, SISIP KENTOSAN)
# Col 43-46: THN 2024 (TANAM, SISIP, SISIP KENTOSAN, ...)
# Col 47-52: THN 2025 (TANAM, SISIP, ...)

year_cols = {
    2020: {'tanam': 34, 'sisip': 35},
    2021: {'tanam': 36, 'sisip': 37},
    2022: {'tanam': 38, 'sisip': 39},
    2023: {'tanam': 40, 'sisip': 41},
    2024: {'tanam': 43, 'sisip': 44},
    2025: {'tanam': 47, 'sisip': 48},
}

# TT SISIP column (Tahun Tanam Sisipan) at col 65
tt_sisip_col = 65

# Tahun Tanam original at col 1
tt_col = 1

# Find block data
print("="*80)
print("ANALISIS BLOK TANPA DATA YIELD - STATUS TBM")
print("="*80)

results = []
for target_block in blocks_no_yield:
    # Find row
    for row in range(10, len(df)):
        block = str(df.iloc[row, 0]).strip() if pd.notna(df.iloc[row, 0]) else ''
        if block == target_block:
            # Get tahun tanam original
            tt_original = df.iloc[row, tt_col]
            tt_original = int(tt_original) if pd.notna(tt_original) else 0
            
            # Get TT SISIP
            tt_sisip = df.iloc[row, tt_sisip_col]
            
            # Get planting data per year
            yearly_data = {}
            latest_tanam_year = None
            total_tanam = 0
            
            for year, cols in year_cols.items():
                tanam = df.iloc[row, cols['tanam']]
                sisip = df.iloc[row, cols['sisip']]
                tanam = int(tanam) if pd.notna(tanam) and tanam > 0 else 0
                sisip = int(sisip) if pd.notna(sisip) and sisip > 0 else 0
                
                if tanam > 0 or sisip > 0:
                    yearly_data[year] = {'tanam': tanam, 'sisip': sisip}
                    if tanam > 0:
                        latest_tanam_year = year
                        total_tanam += tanam
            
            # Determine status
            if latest_tanam_year and latest_tanam_year >= 2022:
                # Sawit butuh 3-4 tahun untuk TM
                years_since_tanam = 2025 - latest_tanam_year
                if years_since_tanam < 3:
                    status = "TBM"
                    reason = f"Tanam baru {latest_tanam_year} ({total_tanam} pohon), umur {years_since_tanam} tahun"
                else:
                    status = "TBM/Transisi"
                    reason = f"Tanam {latest_tanam_year}, mulai produktif"
            elif tt_original and tt_original >= 2022:
                status = "TBM"
                reason = f"Tahun tanam original {tt_original}, umur {2025 - tt_original} tahun"
            else:
                status = "Perlu Investigasi"
                reason = f"TT original: {tt_original}, tidak ada tanam baru"
            
            result = {
                'block': target_block,
                'tt_original': tt_original,
                'tt_sisip': str(tt_sisip) if pd.notna(tt_sisip) else 'N/A',
                'yearly_data': yearly_data,
                'latest_tanam_year': latest_tanam_year,
                'total_tanam': total_tanam,
                'status': status,
                'reason': reason
            }
            results.append(result)
            
            print(f"\n{target_block}:")
            print(f"  TT Original: {tt_original}")
            print(f"  Data per tahun: {yearly_data}")
            print(f"  STATUS: {status}")
            print(f"  Reason: {reason}")
            break

# Summary by status
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

tbm = [r for r in results if r['status'] == 'TBM']
transisi = [r for r in results if r['status'] == 'TBM/Transisi']
investigasi = [r for r in results if r['status'] == 'Perlu Investigasi']

print(f"\nTBM (Tanaman Belum Menghasilkan): {len(tbm)} blok")
for r in tbm:
    print(f"  {r['block']}: {r['reason']}")

print(f"\nTBM/Transisi: {len(transisi)} blok")
for r in transisi:
    print(f"  {r['block']}: {r['reason']}")

print(f"\nPerlu Investigasi: {len(investigasi)} blok")
for r in investigasi:
    print(f"  {r['block']}: {r['reason']}")

# Save results
with open('tbm_blocks_analysis.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("\n\nResults saved to tbm_blocks_analysis.json")
