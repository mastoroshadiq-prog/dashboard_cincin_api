import pandas as pd

# Read Excel with different approaches
file_path = r'f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\poac_sim\data\input\data_gabungan.xlsx'

print("Attempting to read Excel with skip rows...")
df = pd.read_excel(file_path, skiprows=2)  # Skip first 2 rows (headers)

print(f"\nTotal rows: {len(df)}")
print(f"\nColumns ({len(df.columns)} total):")
for i, col in enumerate(df.columns[:30]):
    print(f"  {i+1}. {col}")

# Display first rows
print("\n" + "=" * 80)
print("FIRST 10 ROWS:")
print("=" * 80)
print(df.head(10))

# Check for data with division/block info
print("\n" + "=" * 80)
print("CHECKING FOR BLOCK/DIVISION DATA:")
print("=" * 80)

# Save to CSV for easier inspection
df.to_csv('data_gabungan_sample.csv', index=False, encoding='utf-8-sig')
print("\nData exported to: data_gabungan_sample.csv")

# Try to identify key columns
print("\nSearching for key patterns in column names...")
for i, col in enumerate(df.columns):
    col_str = str(col).lower()
    if any(x in col_str for x in ['div', 'afd', 'block', 'blok', 'prod', 'status', 'tbm', 'tanam']):
        print(f"  Column {i}: {col}")

print("\nDone!")
