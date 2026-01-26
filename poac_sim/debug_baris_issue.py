import pandas as pd

# Load sample AME II
df_ii = pd.read_csv('data/input/tabelNDREnew.csv', nrows=5)
print("=== AME II (tabelNDREnew.csv) Sample ===")
print(df_ii.head())
print("\nColumn types:")
print(df_ii.dtypes)

# Load sample AME IV with semicolon delimiter
df_iv = pd.read_csv('data/input/AME_IV.csv', sep=';', nrows=5)
print("\n=== AME IV (AME_IV.csv) Sample ===")
print(df_iv.head())
print("\nColumn types:")
print(df_iv.dtypes)

# Check unique values for 'baris' if exists
print("\n=== Unique Baris Values Analysis ===")
try:
    df_iv_full = pd.read_csv('data/input/AME_IV.csv', sep=';')
    col_baris = None
    if 'N_BARIS' in df_iv_full.columns:
        col_baris = 'N_BARIS'
    elif 'baris' in df_iv_full.columns:
        col_baris = 'baris'
    
    if col_baris:
        print(f"AME IV '{col_baris}' min: {df_iv_full[col_baris].min()}")
        print(f"AME IV '{col_baris}' max: {df_iv_full[col_baris].max()}")
        print(f"AME IV '{col_baris}' sample: {df_iv_full[col_baris].unique()[:10]}")
    else:
        print(f"Column 'N_BARIS' or 'baris' not found. Available: {df_iv_full.columns.tolist()}")
except Exception as e:
    print(f"Error reading AME IV: {e}")
