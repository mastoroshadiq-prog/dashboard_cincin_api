"""
Script untuk menghitung blok unik dengan melihat nama blok lengkap (termasuk suffix)
"""
import pandas as pd
import re

def analyze_blocks_detailed():
    excel_file = r"poac_sim\data\input\data_gabungan.xlsx"
    
    print("[INFO] Loading Excel file...")
    df = pd.read_excel(excel_file, sheet_name='Lembar1', header=None)
    
    # Column 5 contains block names
    block_col_idx = 5
    
    all_blocks = []
    for row_idx in range(len(df)):
        cell_value = df.iloc[row_idx, block_col_idx]
        
        if pd.notna(cell_value):
            cell_str = str(cell_value).strip()
            
            # Match full block pattern including suffix (e.g., AME I A001A, DBE003 B001A)
            if re.search(r'(AME|DB E|OLE)', cell_str, re.IGNORECASE):
                all_blocks.append(cell_str)
    
    print(f"[INFO] Total rows with division names: {len(all_blocks)}")
    
    # Group by division
    division_blocks = {}
    
    for block_name in all_blocks:
        # Extract division using various patterns
        # Patterns: "AME I", "AME01", "AME 001", "DBE 001", etc.
        match = re.match(r'^\s*(AME|DBE|OLE)\s*([IV0-9]+)', block_name, re.IGNORECASE)
        
        if match:
            div_prefix = match.group(1).upper().replace(' ', '')
            div_number = match.group(2).strip()
            
            # Normalize roman numerals
            roman_map = {'I': '01', 'II': '02', 'III': '03', 'IV': '04', 'V': '05'}
            if div_number in roman_map:
                div_number = roman_map[div_number]
            elif div_number.isdigit():
                div_number = f'{int(div_number):02d}'
            
            div_key = f'{div_prefix}{div_number}'
            
            if div_key not in division_blocks:
                division_blocks[div_key] = []
            
            division_blocks[div_key].append(block_name)
    
    # Print results
    print("\n" + "="*80)
    print("📊 JUMLAH BLOK PER DIVISI (dari Excel data_gabungan.xlsx)")
    print("="*80)
    
    sorted_divs = sorted(division_blocks.keys())
    
    for div in sorted_divs:
        blocks = division_blocks[div]
        print(f"\n{div}: {len(blocks)} entries")
        
        # Show first 5 block names
        if len(blocks) <= 5:
            for b in blocks:
                print(f"  - {b}")
        else:
            for b in blocks[:3]:
                print(f"  - {b}")
            print(f"  ... and {len(blocks)-3} more")
    
    # Save to CSV
    output_file = "division_block_analysis.csv"
    rows = []
    for div in sorted_divs:
        blocks = division_blocks[div]
        rows.append({
            'Division': div,
            'Total_Entries': len(blocks),
            'Sample_Blocks': ', '.join(blocks[:5])
        })
    
    pd.DataFrame(rows).to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Analysis saved to: {output_file}")
    
    # Special check for AME01
    print("\n" + "="*80)
    print("🔍 AME I (AME01) DETAILED CHECK")
    print("="*80)
    
    if 'AME01' in division_blocks:
        ame01_blocks = division_blocks['AME01']
        print(f"Total entries for AME01: {len(ame01_blocks)}")
        print(f"User expected: 78 blok")
        
        # Check for unique block codes (e.g., A001A, A002A, etc.)
        unique_codes = set()
        for block in ame01_blocks:
            # Extract suffix like "A001A", "B003B"
            suffix_match = re.search(r'([A-Z]\d+[A-Z])', block)
            if suffix_match:
                unique_codes.add(suffix_match.group(1))
        
        print(f"Unique block codes found: {len(unique_codes)}")
        
        if len(unique_codes) <= 10:
            print(f"Block codes: {sorted(unique_codes)}")
    
    return division_blocks

if __name__ == '__main__':
    analyze_blocks_detailed()
