
import pandas as pd
from pathlib import Path

def normalize(s):
    if not isinstance(s, str): return str(s)
    return s.strip().upper().replace(" ", "")

try:
    # 1. Load Data Gabungan (Reference)
    print("Loading Data Gabungan...")
    df_gab = pd.read_excel('data/input/data_gabungan.xlsx', header=None, skiprows=8)
    blocks_gab = df_gab[0].dropna().apply(normalize).unique().tolist()
    print(f"Sample Gabungan (Ref): {blocks_gab[:10]}")
    
    # 2. Load Data Baru (Alternative Ref)
    print("\nLoading Data Baru...")
    df_baru = pd.read_csv('data/input/data_baru.csv', header=4)
    # Find block col
    blk_col = [c for c in df_baru.columns if 'BARU' in str(c).upper()][0]
    blocks_baru = df_baru[blk_col].dropna().apply(normalize).unique().tolist()
    print(f"Sample Data Baru (Ref): {blocks_baru[:10]}")
    
    # 3. Load Data NDRE (Target)
    print("\nLoading NDRE Dataset...")
    df_ndre = pd.read_csv('data/input/tabelNDREnew.csv')
    blocks_ndre = df_ndre['Blok'].dropna().apply(normalize).unique().tolist()
    print(f"Sample NDRE (Target): {blocks_ndre[:10]}")
    
    # 4. Check Matches
    print("\nMATCHING CHECK (Target in Ref?):")
    
    match_gab = set(blocks_ndre).intersection(set(blocks_gab))
    print(f"NDRE found in Gabungan: {len(match_gab)} / {len(blocks_ndre)} ({len(match_gab)/len(blocks_ndre):.1%})")
    print(f"MISSING Sample: {list(set(blocks_ndre) - set(blocks_gab))[:5]}")
    
    match_baru = set(blocks_ndre).intersection(set(blocks_baru))
    print(f"NDRE found in Data Baru: {len(match_baru)} / {len(blocks_ndre)} ({len(match_baru)/len(blocks_ndre):.1%})")
    
except Exception as e:
    print(f"Error: {e}")
