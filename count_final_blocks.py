"""
Final script untuk menghitung blok UNIK per divisi
Menggunakan kolom NOMOR (kode blok) dan kolom DIVISI
"""
import pandas as pd

def count_final_blocks():
    excel_file = r"poac_sim\data\input\data_gabungan.xlsx"
    
    print("[INFO] Loading Excel file...")
    df = pd.read_excel(excel_file, sheet_name='Lembar1', header=None)
    
    # Based on inspection:
    # Column 2: NOMOR (block code like A001A, B002B, etc.)
    # Column 5: DIVISI (division like AME01, DBE02, etc.)
    
    # Find header row
    header_row_idx = None
    for i in range(min(20, len(df))):
        if df.iloc[i, 2] == 'NOMOR':
            header_row_idx = i
            break
    
    if header_row_idx is None:
        print("[ERROR] Could not find header row with 'NOMOR'")
        return
    
    print(f"[INFO] Found header row at index: {header_row_idx}")
    
    # Reload with proper header
    df = pd.read_excel(excel_file, sheet_name='Lembar1', header=header_row_idx)
    
    print(f"[INFO] Data shape after header: {df.shape}")
    print(f"[INFO] Columns: {list(df.columns[:15])}")
    
    # Check if required columns exist
    if 'NOMOR' not in df.columns or 'DIVISI' not in df.columns:
        # Try alternative column detection
        nomor_col = None
        divisi_col = None
        
        for col in df.columns:
            if 'NOMOR' in str(col).upper():
                nomor_col = col
            if 'DIVISI' in str(col).upper() or col == 5:
                divisi_col = col
        
        print(f"[INFO] Using nomor_col: {nomor_col}, divisi_col: {divisi_col}")
    else:
        nomor_col = 'NOMOR'
        divisi_col = 'DIVISI'
    
    # Filter valid rows
    valid_data = df[[nomor_col, divisi_col]].copy()
    valid_data = valid_data.dropna()
    
    # Remove header duplicates
    valid_data = valid_data[valid_data[nomor_col] != 'NOMOR']
    valid_data = valid_data[valid_data[divisi_col] != 'DIVISI']
    
    print(f"[INFO] Valid rows: {len(valid_data)}")
    
    # Count unique blocks per division
    division_counts = valid_data.groupby(divisi_col)[nomor_col].nunique().to_dict()
    
    # Also get total blocks per division (including duplicates if any)
    division_total = valid_data.groupby(divisi_col)[nomor_col].count().to_dict()
    
    print("\n" + "="*80)
    print("📊 JUMLAH BLOK UNIK PER DIVISI (FINAL VALIDATION)")
    print("="*80)
    
    sorted_divs = sorted(division_counts.keys())
    
    ame_total = 0
    dbe_total = 0
    ole_total = 0
    
    for div in sorted_divs:
        unique_count = division_counts[div]
        total_count = division_total[div]
        
        print(f"{div}: {unique_count} blok unik (total entries: {total_count})")
        
        if str(div).startswith('AME'):
            ame_total += unique_count
        elif str(div).startswith('DBE'):
            dbe_total += unique_count
        elif str(div).startswith('OLE'):
            ole_total += unique_count
    
    print("\n" + "="*80)
    print("📝 ESTATE-WIDE SUMMARY")
    print("="*80)
    print(f"AME Estate: {ame_total} blok")
    print(f"DBE Estate: {dbe_total} blok")
    print(f"OLE Estate: {ole_total} blok")
    print(f"TOTAL: {ame_total + dbe_total + ole_total} blok")
    
    # Check AME01 specifically
    print("\n" + "="*80)
    print("🔍 AME01 (AME I) VERIFICATION")
    print("="*80)
    
    ame01_variants = ['AME01', 'AME 01', 'AME I', 'AME001', 'AME 001']
    ame01_count = 0
    ame01_key = None
    
    for variant in ame01_variants:
        if variant in division_counts:
            ame01_count = division_counts[variant]
            ame01_key = variant
            break
    
    if ame01_count > 0:
        print(f"✅ Found AME01 as '{ame01_key}': {ame01_count} blok unik")
        print(f"📋 User reported: Should be 78 blok")
        
        if ame01_count == 78:
            print(f"✅ MATCH! Count is correct at 78 blok")
        elif ame01_count == 80:
            print(f"❌ MISMATCH! Excel shows 80, but user says should be 78")
            print(f"   Need to verify which 2 blocks should be excluded")
    
    # Export results
    output_file = "division_blocks_FINAL.csv"
    result_data = []
    for div in sorted_divs:
        result_data.append({
            'Division': div,
            'Unique_Blocks': division_counts[div],
            'Total_Entries': division_total[div]
        })
    
    pd.DataFrame(result_data).to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Final results saved to: {output_file}")
    
    return division_counts

if __name__ == '__main__':
    count_final_blocks()
