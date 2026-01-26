import pandas as pd

# Read Excel
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=None)

print("="*80)
print("INVESTIGATING D003A DATA ACCURACY")
print("="*80)

# Find D003A
d003a_rows = df[df[0] == 'D003A']
print(f"\nFound {len(d003a_rows)} row(s) for D003A")

if len(d003a_rows) > 0:
    row_idx = d003a_rows.index[0]
    print(f"Row index: {row_idx}")
    
    # Check area columns
    print("\n--- AREA DATA ---")
    print(f"Column 11: {df.iloc[row_idx, 11]} Ha")
    print(f"Column 12: {df.iloc[row_idx, 12]}")
    print(f"Column 13: {df.iloc[row_idx, 13]}")
    print(f"Column 14: {df.iloc[row_idx, 14]}")
    
    # Check 2023 production data
    print("\n--- 2023 PRODUCTION DATA ---")
    print(f"Column 150 (header row 3): {df.iloc[3, 150]}")
    print(f"Column 150 (header row 4): {df.iloc[4, 150]}")
    print(f"Column 150 (header row 5): {df.iloc[5, 150]}")
    print(f"Column 150 (D003A value): {df.iloc[row_idx, 150]}")
    
    print(f"\nColumn 151 (D003A): {df.iloc[row_idx, 151]}")
    print(f"Column 152 (D003A): {df.iloc[row_idx, 152]} <- This should be Total Ton")
    print(f"Column 153 (D003A): {df.iloc[row_idx, 153]}")
    
    # Calculate Ton/Ha
    luas = df.iloc[row_idx, 11]
    total_ton_2023 = df.iloc[row_idx, 152]
    
    if pd.notna(luas) and pd.notna(total_ton_2023):
        ton_ha = total_ton_2023 / luas
        print(f"\n🧮 CALCULATION:")
        print(f"   Total Ton (2023): {total_ton_2023}")
        print(f"   Luas: {luas} Ha")
        print(f"   Ton/Ha: {total_ton_2023} / {luas} = {ton_ha:.2f}")
    
    # USER says correct is:
    print("\n" + "="*80)
    print("USER'S CORRECT DATA (D003A 2023):")
    print("="*80)
    print("  Luas: 21.6 Ha")
    print("  Potensi: 22.6 Ton/Ha")
    print("  Realisasi: 13.9 Ton/Ha")
    print("  Gap: 8.7 Ton/Ha")
    
    # Check if potensi column exists
    print("\n--- CHECKING POTENSI (2023) ---")
    print(f"Column 153 (Poten header row 4): {df.iloc[4, 153]}")
    print(f"Column 153 (D003A value): {df.iloc[row_idx, 153]}")
    print(f"Column 154 (D003A): {df.iloc[row_idx, 154]}")
    print(f"Column 155 (D003A): {df.iloc[row_idx, 155]}")

# Search for luas 21.6 anywhere
print("\n" + "="*80)
print("SEARCHING FOR LUAS 21.6 Ha IN ENTIRE SHEET")
print("="*80)

col_11_values = df.iloc[7:, 11]  # Start from row 7 (after headers)
matching = df.iloc[7:][col_11_values == 21.6]

if len(matching) > 0:
    print(f"\nFo und {len(matching)} blocks with luas 21.6 Ha:")
    for idx in matching.index[:5]:
        block = df.iloc[idx, 0]
        year = df.iloc[idx, 1]
        print(f"  Row {idx}: {block}, Year {year}")
else:
    print("\n❌ No blocks found with luas = 21.6 Ha in column 11")
    
    # Check if 21.6 appears in other columns
    print("\nSearching ALL columns for value 21.6...")
    for col in range(10, 20):
        matching_col = df[np.isclose(df[col], 21.6, atol=0.01)]
        if len(matching_col) > 0:
            print(f"  Found in column {col}: {len(matching_col)} rows")
