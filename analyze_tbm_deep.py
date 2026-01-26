import pandas as pd
import numpy as np

# Read the Excel file from the correct location
file_path = r'f:\PythonProjects\poac_cincin_api\poac_sim\data\input\data_gabungan.xlsx'

print("="*80)
print("ANALYZING TBM BLOCKS IN EXCEL DATA")
print("="*80)

# Try to read with different approaches to handle merged cells
try:
    # Read all sheets
    xls = pd.ExcelFile(file_path)
    print(f"\nSheets available: {xls.sheet_names}")
    
    # Read the first sheet
    df = pd.read_excel(file_path, sheet_name=0, header=None)
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # Display first 30 rows to understand structure
    print("\n" + "="*80)
    print("FIRST 30 ROWS (to understand header structure):")
    print("="*80)
    
    for idx in range(min(30, len(df))):
        row_data = df.iloc[idx].tolist()
        # Show non-null values
        non_null = [(i, v) for i, v in enumerate(row_data) if pd.notna(v)]
        if non_null:
            print(f"\nRow {idx}: {len(non_null)} non-null values")
            for col_idx, val in non_null[:10]:  # Show first 10
                print(f"  Col {col_idx}: {val}")
    
    # Try to find column headers
    print("\n" + "="*80)
    print("SEARCHING FOR KEY COLUMNS:")
    print("="*80)
    
    # Search for specific keywords in all cells
    keywords = ['2023', '2024', '2025', 'tanam', 'blok', 'afdeling', 'divisi', 'AME', 'TBM']
    
    for keyword in keywords:
        print(f"\nSearching for '{keyword}':")
        found = False
        for row_idx in range(min(50, len(df))):
            for col_idx in range(df.shape[1]):
                cell_value = df.iloc[row_idx, col_idx]
                if pd.notna(cell_value) and keyword.lower() in str(cell_value).lower():
                    print(f"  Found at Row {row_idx}, Col {col_idx}: '{cell_value}'")
                    found = True
                    if keyword in ['2023', '2024', '2025']:
                        # Check surrounding cells
                        print(f"    Context: Row {row_idx-1}: {df.iloc[row_idx-1, col_idx]}")
        
        if not found:
            print(f"  Not found in first 50 rows")
    
    # Save raw data for inspection
    df.to_csv('excel_raw_data.csv', index=False, encoding='utf-8-sig')
    print(f"\n\nRaw data saved to: excel_raw_data.csv")
    
except Exception as e:
    print(f"\nError reading Excel: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Analysis complete!")
print("="*80)
