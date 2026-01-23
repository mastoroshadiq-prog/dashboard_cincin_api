"""
Analyze blocks without yield data - check if they are TBM (Tanaman Belum Menghasilkan)
Based on sisipan (replanting) data in data_gabungan.xlsx
"""
import pandas as pd
import json

# Blocks without yield data
blocks_no_yield = [
    # AME01
    'A005C', 'A006A', 'A007A', 'B007D', 'B008E', 'B009G',
    # AME04
    'B015D', 'B016G', 'B017F',
    # DBE01
    'C027B', 'D027I', 'D028F', 'D029B', 'D033A', 'D034A', 'E032B', 'F029G', 'F030F', 'F031E',
    # OLE03
    'J021A'
]

print("="*70)
print("ANALYSIS: BLOK TANPA DATA YIELD - CEK STATUS TBM")
print("="*70)

# Load data_gabungan.xlsx
print("\nLoading data_gabungan.xlsx...")
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

# Find column headers - sisipan columns
# From previous analysis: col 35 is SISIP for one year, and there might be more
# Let's find all SISIP columns
print("\nSearching for SISIP and TANAM columns...")

sisip_cols = {}
tanam_cols = {}
for col in range(df.shape[1]):
    val = str(df.iloc[5, col]).strip() if pd.notna(df.iloc[5, col]) else ''
    if val == 'SISIP':
        # Get the year from row above (row 4 or 3)
        year = None
        for row in [4, 3, 2]:
            yr_val = df.iloc[row, col]
            if pd.notna(yr_val) and str(yr_val).isdigit():
                year = int(yr_val)
                break
            elif pd.notna(yr_val):
                # Try to extract year from string
                yr_str = str(yr_val)
                if '202' in yr_str or '201' in yr_str:
                    for y in range(2015, 2026):
                        if str(y) in yr_str:
                            year = y
                            break
        sisip_cols[col] = year
        print(f"  Found SISIP at col {col}, year: {year}")
    
    if val == 'TANAM':
        year = None
        for row in [4, 3, 2]:
            yr_val = df.iloc[row, col]
            if pd.notna(yr_val) and str(yr_val).isdigit():
                year = int(yr_val)
                break
        tanam_cols[col] = year

# Find block code column
print("\nFinding block code column...")
block_col = None
for col in range(20):
    for row in range(10, 50):
        val = str(df.iloc[row, col]).strip() if pd.notna(df.iloc[row, col]) else ''
        if val in blocks_no_yield:
            block_col = col
            print(f"  Found block column at col {col}, sample: {val}")
            break
    if block_col is not None:
        break

# Also check tahun tanam column
tt_col = None
for col in range(20):
    val = str(df.iloc[5, col]).strip() if pd.notna(df.iloc[5, col]) else ''
    if 'TANAM' in val.upper() and col < 10:
        tt_col = col
        print(f"  Tahun Tanam column might be at col {col}")

# Extract data for blocks without yield
print("\n" + "="*70)
print("RESULTS: STATUS BLOK TANPA DATA YIELD")
print("="*70)

results = []
if block_col is not None:
    for i in range(10, len(df)):
        block = str(df.iloc[i, block_col]).strip() if pd.notna(df.iloc[i, block_col]) else ''
        
        if block in blocks_no_yield:
            # Get tahun tanam
            tt = df.iloc[i, 1] if pd.notna(df.iloc[i, 1]) else 'N/A'
            
            # Get sisipan data for each year
            sisip_data = {}
            total_sisip = 0
            latest_sisip_year = None
            latest_sisip_count = 0
            
            for col, year in sisip_cols.items():
                val = df.iloc[i, col]
                if pd.notna(val):
                    try:
                        count = int(float(val))
                        if count > 0:
                            sisip_data[year] = count
                            total_sisip += count
                            if year and (latest_sisip_year is None or year > latest_sisip_year):
                                latest_sisip_year = year
                                latest_sisip_count = count
                    except:
                        pass
            
            # Determine status
            if latest_sisip_year and latest_sisip_year >= 2022:
                # Sisipan 2022 or later - still TBM in 2025 (sawit butuh 3-4 tahun untuk TM)
                status = "TBM (Tanaman Belum Menghasilkan)"
                reason = f"Sisipan {latest_sisip_year}: {latest_sisip_count} pohon"
            elif latest_sisip_year and latest_sisip_year >= 2020:
                status = "TBM/Transisi"
                reason = f"Sisipan {latest_sisip_year}: {latest_sisip_count} pohon - mulai menghasilkan"
            else:
                status = "Perlu Investigasi"
                reason = "Tidak ada data sisipan terbaru"
            
            results.append({
                'block': block,
                'tahun_tanam': tt,
                'total_sisip': total_sisip,
                'latest_sisip_year': latest_sisip_year,
                'latest_sisip_count': latest_sisip_count,
                'status': status,
                'reason': reason
            })
            
            print(f"\n{block}:")
            print(f"  Tahun Tanam: {tt}")
            print(f"  Total Sisipan: {total_sisip}")
            print(f"  Sisipan Terbaru: {latest_sisip_year} ({latest_sisip_count} pohon)")
            print(f"  STATUS: {status}")
            print(f"  Reason: {reason}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
tbm_count = len([r for r in results if 'TBM' in r['status']])
perlu_investigasi = len([r for r in results if 'Investigasi' in r['status']])
print(f"TBM/TBM Transisi: {tbm_count} blok")
print(f"Perlu Investigasi: {perlu_investigasi} blok")

# Save to JSON
with open('tbm_blocks_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved to tbm_blocks_analysis.json")
