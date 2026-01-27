import pandas as pd

# Load Excel to check available columns
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', nrows=5)

print("\n=== PRODUCTION COLUMNS (Historical & Current) ===\n")

# Look for production-related columns
production_keywords = ['2022', '2023', '2024', '2025', '2026', 'Real', 'Pot', 'Yield', 'Ton', 'KG']

matching_cols = []
for i, col in enumerate(df.columns):
    col_str = str(col)
    if any(keyword in col_str for keyword in production_keywords):
        matching_cols.append((i, col_str))

# Print first 100 matching columns
for idx, name in matching_cols[:100]:
    print(f"{idx:4d}: {name}")

print(f"\n=== TOTAL MATCHING COLUMNS: {len(matching_cols)} ===")
