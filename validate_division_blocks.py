"""
Script untuk validasi jumlah blok per divisi dari data_gabungan.xlsx
"""
import pandas as pd
import re

def validate_blocks_per_division():
    excel_file = r"poac_sim\data\input\data_gabungan.xlsx"
    
    print("[INFO] Loading Excel file...")
    df = pd.read_excel(excel_file, sheet_name='Lembar1', header=None)
    
    print(f"[INFO] Excel shape: {df.shape}")
    print(f"[INFO] Total rows: {len(df)}, Total columns: {len(df.columns)}")
    
    # Search for column containing block names
    print("\n[INFO] Searching for block/division column...")
    
    # Look for patterns like AME, DBE, OLE followed by blok codes
    division_pattern = re.compile(r'^(AME|DBE|OLE|OLW|OLS)\s*[IV0-9]+', re.IGNORECASE)
    
    blocks_found = []
    block_column_idx = None
    
    # Search first 10 columns for block names
    for col_idx in range(min(10, len(df.columns))):
        for row_idx in range(len(df)):
            cell_value = df.iloc[row_idx, col_idx]
            
            if pd.notna(cell_value):
                cell_str = str(cell_value).strip()
                
                # Check if matches division pattern
                if division_pattern.match(cell_str):
                    if block_column_idx is None:
                        block_column_idx = col_idx
                        print(f"[FOUND] Block column at index {col_idx}")
                    
                    blocks_found.append({
                        'row': row_idx,
                        'col': col_idx,
                        'block': cell_str
                    })
    
    print(f"\n[INFO] Total blocks found: {len(blocks_found)}")
    
    if len(blocks_found) == 0:
        print("[ERROR] No blocks found! Showing first 20 rows of first 5 columns:")
        print(df.iloc[:20, :5])
        return
    
    # Extract division from block name
    print("\n[INFO] Extracting divisions...")
    for item in blocks_found:
        block_name = item['block']
        # Extract division code (AME01, DBE02, etc)
        match = re.match(r'(AME|DBE|OLE|OLW|OLS)\s*([IV0-9]+)', block_name, re.IGNORECASE)
        if match:
            div_prefix = match.group(1).upper()
            div_number = match.group(2).strip()
            
            # Convert roman numerals if needed
            roman_map = {'I': '01', 'II': '02', 'III': '03', 'IV': '04', 'V': '05'}
            if div_number in roman_map:
                div_number = roman_map[div_number]
            elif div_number.isdigit() and len(div_number) == 1:
                div_number = f'0{div_number}'
            
            item['division'] = f'{div_prefix}{div_number}'
        else:
            item['division'] = 'UNKNOWN'
    
    # Count blocks per division
    division_counts = {}
    for item in blocks_found:
        div = item['division']
        if div not in division_counts:
            division_counts[div] = []
        division_counts[div].append(item['block'])
    
    # Sort divisions
    sorted_divisions = sorted(division_counts.keys())
    
    print("\n" + "="*60)
    print("📊 VALIDASI JUMLAH BLOK PER DIVISI")
    print("="*60)
    
    for div in sorted_divisions:
        blocks = division_counts[div]
        print(f"\n{div}: {len(blocks)} blok")
        if len(blocks) <= 10:
            print(f"  Blocks: {', '.join(blocks)}")
    
    print("\n" + "="*60)
    print("📝 SUMMARY")
    print("="*60)
    
    total_blocks = sum(len(blocks) for blocks in division_counts.values())
    print(f"Total Divisions: {len(division_counts)}")
    print(f"Total Blocks: {total_blocks}")
    
    # Export to CSV for verification
    output_file = "division_block_count_validation.csv"
    validation_data = []
    for div in sorted_divisions:
        validation_data.append({
            'Division': div,
            'Count': len(division_counts[div]),
            'Blocks': ', '.join(division_counts[div])
        })
    
    validation_df = pd.DataFrame(validation_data)
    validation_df.to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Validation saved to: {output_file}")
    
    return division_counts

if __name__ == '__main__':
    validate_blocks_per_division()
