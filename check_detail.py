import pandas as pd

# Baca file Excel dengan header di baris 0
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')

print("Showing first 3 rows and first 30 columns:")
print("="*80)
print(df.iloc[:3, :30].to_string())

print("\n\nSearching for relevant columns:")
print("="*80)
for i, col in enumerate(df.columns):
    col_str = str(col).lower()
    if any(keyword in col_str for keyword in ['blok', 'sisip', 'tt', 'tanam', 'f008', 'd001']):
        print(f"Column {i}: {col}")
        if i < len(df.columns):
            print(f"  Sample values: {df[col].dropna().head(3).tolist()}")
