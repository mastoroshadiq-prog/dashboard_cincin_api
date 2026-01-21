"""
Script untuk menghitung jumlah blok UNIK per divisi (menghilangkan duplikat)
"""
import pandas as pd
import re

def count_unique_blocks():
    excel_file = r"poac_sim\data\input\data_gabungan.xlsx"
    
    print("[INFO] Loading Excel file...")
    df = pd.read_excel(excel_file, sheet_name='Lembar1', header=None)
    
    print(f"[INFO] Excel shape: {df.shape}")
    
    # Search for block names in column 5 (0-indexed)
    block_col_idx = 5
    
    blocks = []
    for row_idx in range(len(df)):
        cell_value = df.iloc[row_idx, block_col_idx]
        
        if pd.notna(cell_value):
            cell_str = str(cell_value).strip()
            
            # Match division patterns
            match = re.match(r'^(AME|DBE|OLE|OLW|OLS)\s*([IV0-9]+)', cell_str, re.IGNORECASE)
            if match:
                blocks.append(cell_str)
    
    print(f"[INFO] Total blocks found (with duplicates): {len(blocks)}")
    
    # Normalize to unified format
    normalized_blocks = {}
    
    for block in blocks:
        match = re.match(r'(AME|DBE|OLE|OLW|OLS)\s*([IV0-9]+)', block, re.IGNORECASE)
        if match:
            div_prefix = match.group(1).upper()
            div_number = match.group(2).strip()
            
            # Normalize numbers: 01, 001, I -> 01
            if div_number == 'I':
                div_number = '01'
            elif div_number == 'II':
                div_number = '02'
            elif div_number == 'III':
                div_number = '03'
            elif div_number == 'IV':
                div_number = '04'
            elif div_number == 'V':
                div_number = '05'
            elif div_number.isdigit():
                # Convert '1' -> '01', '001' -> '01'
                div_number = f'{int(div_number):02d}'
            
            normalized_key = f'{div_prefix}{div_number}'
            
            if normalized_key not in normalized_blocks:
                normalized_blocks[normalized_key] = set()
            
            normalized_blocks[normalized_key].add(block)
    
    # Count unique blocks per division (each set item is one occurrence in Excel)
    # Since Excel has duplicates, we need to count actual unique occurrences
    # by dividing by 2 (assuming double entry)
    
    print("\n" + "="*70)
    print("📊 VALIDASI JUMLAH BLOK PER DIVISI (CLEANED)")
    print("="*70)
    
    division_counts = {}
    for div, block_set in normalized_blocks.items():
        # Count unique occurrences - assuming each appears twice
        count = len(block_set) // 2 if len(block_set) > 1 else 1
        division_counts[div] = count
    
    sorted_divisions = sorted(division_counts.keys())
    
    ame_total = 0
    dbe_total = 0
    ole_total = 0
    
    for div in sorted_divisions:
        count = division_counts[div]
        print(f"{div}: {count} blok")
        
        if div.startswith('AME'):
            ame_total += count
        elif div.startswith('DBE'):
            dbe_total += count
        elif div.startswith('OLE'):
            ole_total += count
    
    print("\n" + "="*70)
    print("📝 ESTATE SUMMARY")
    print("="*70)
    print(f"AME Estate: {ame_total} blok")
    print(f"DBE Estate: {dbe_total} blok")
    print(f"OLE Estate: {ole_total} blok")
    print(f"TOTAL: {ame_total + dbe_total + ole_total} blok")
    
    # Export cleaned data
    output_file = "division_block_count_CLEANED.csv"
    validation_data = []
    for div in sorted_divisions:
        validation_data.append({
            'Division': div,
            'Block_Count': division_counts[div]
        })
    
    validation_df = pd.DataFrame(validation_data)
    validation_df.to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Cleaned validation saved to: {output_file}")
    
    # Check specific divisions mentioned by user
    print("\n" + "="*70)
    print("🔍 SPECIFIC DIVISION CHECK")
    print("="*70)
    
    if 'AME01' in division_counts:
        print(f"✅ AME01 (AME I): {division_counts['AME01']} blok")
        print(f"   User reported: Should be 78, not 80")
        if division_counts['AME01'] == 78:
            print(f"   ✅ MATCHES user count!")
        elif division_counts['AME01'] == 80:
            print(f"   ❌ MISMATCH - Still shows 80")
    
    return division_counts

if __name__ == '__main__':
    count_unique_blocks()
