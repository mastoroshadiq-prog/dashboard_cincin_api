
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Add parent dir to path to find src
sys.path.insert(0, '.')

try:
    from src.ingestion import load_and_clean_data
except ImportError:
    # If run from poac_sim folder
    sys.path.insert(0, '..')
    from src.ingestion import load_and_clean_data

# -------------------------------------------------------------------------
# 1. LOAD DATA HELPERS (Copied/Adapted from dashboard_v8_interactive.py)
# -------------------------------------------------------------------------

def load_productivity_data():
    """Robust load of productivity data."""
    candidates = [
        Path('data/input/Realisasi vs Potensi PT SR.xlsx'),
        Path('../data/input/Realisasi vs Potensi PT SR.xlsx'),
         Path('data/input/data_gabungan.xlsx')
    ]
    file_path = None
    for p in candidates:
        if p.exists():
            file_path = p
            break
            
    if not file_path:
        print("❌ Productivity file not found.")
        return pd.DataFrame()
        
    print(f"📖 Loading Prod Data: {file_path.name}")
    print(f"📖 Loading Prod Data: {file_path.name}")
    try:
        # Read header area to find structure
        df_header = pd.read_excel(file_path, header=None, nrows=15)
        
        # 1. Find BLOK, Ha, and TT (Tahun Tanam) columns
        blok_col_idx = -1
        luas_col_idx = -1
        tt_col_idx = -1
        header_row_idx = -1
        
        for r in range(len(df_header)):
            row_vals = df_header.iloc[r].astype(str).str.upper().tolist()
            if 'BLOK' in row_vals:
                header_row_idx = r
                blok_col_idx = row_vals.index('BLOK')
                
                # Find Ha
                indices = [i for i, x in enumerate(row_vals) if 'HA' == x or 'LUAS' in x]
                if indices: luas_col_idx = indices[0]
                
                # Find TT
                indices_tt = [i for i, x in enumerate(row_vals) if 'TT' == x or 'TAHUN' in x]
                if indices_tt: tt_col_idx = indices_tt[0]
                break
        
        if blok_col_idx == -1:
            print("❌ Could not find 'BLOK' column header.")
            return pd.DataFrame()

        print(f"✅ Found Header at Row {header_row_idx}: Blok {blok_col_idx}, Luas {luas_col_idx}, TT {tt_col_idx}")

        # ... (Search for Prod/Potensi same as before) ...
        prod_col_idx = -1
        pot_col_idx = -1
        target_year = "2023"
        
        row_years = df_header.iloc[header_row_idx].astype(str).tolist()
        year_start_col = -1
        if "2024" in row_years: 
            target_year = "2024"; year_start_col = row_years.index("2024")
        elif "2023" in row_years:
            target_year = "2023"; year_start_col = row_years.index("2023")
            
        if year_start_col != -1:
             row_type = df_header.iloc[header_row_idx+1].astype(str).str.upper().tolist()
             row_unit = df_header.iloc[header_row_idx+2].astype(str).str.upper().tolist()
             
             for c in range(year_start_col, min(year_start_col+20, len(row_type))):
                typ = row_type[c]; unit = row_unit[c]
                if 'REAL' in typ and 'TON' in unit and prod_col_idx == -1: prod_col_idx = c
                if 'POTENSI' in typ and 'TON' in unit and 'REAL' not in typ and pot_col_idx == -1: pot_col_idx = c

        # 3. Load FULL Data
        data_start_row = header_row_idx + 3
        df = pd.read_excel(file_path, header=None, skiprows=data_start_row)
        
        extracted = pd.DataFrame()
        extracted['Blok_Prod'] = df.iloc[:, blok_col_idx]
        extracted['Luas_Ha'] = df.iloc[:, luas_col_idx] if luas_col_idx != -1 else 0
        extracted['Tahun_Tanam'] = df.iloc[:, tt_col_idx] if tt_col_idx != -1 else 0
        extracted['Produksi_Ton'] = df.iloc[:, prod_col_idx] if prod_col_idx != -1 else 0
        extracted['Potensi_Prod_Ton'] = df.iloc[:, pot_col_idx] if pot_col_idx != -1 else 0
        
        df = extracted
        
        # Stringify Block
        if 'Blok_Prod' in df.columns:
            df['Blok_Prod'] = df['Blok_Prod'].astype(str).str.strip().str.upper()
            df = df[df['Blok_Prod'].apply(lambda x: len(x) > 1 and x != 'NAN')]

        # Numeric
        for c in ['Luas_Ha', 'Produksi_Ton', 'Potensi_Prod_Ton', 'Tahun_Tanam']:
             df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
             
        # Age
        from datetime import datetime
        curr_year = datetime.now().year
        df['Umur_Tahun'] = curr_year - df['Tahun_Tanam']

        df['Yield_Real'] = df['Produksi_Ton'] / df['Luas_Ha']
        df['Potensi_Yield'] = df['Potensi_Prod_Ton'] / df['Luas_Ha']
        df['Gap'] = df['Potensi_Yield'] - df['Yield_Real']
        
        # Aliases for Dashboard
        df['Yield_TonHa'] = df['Yield_Real']
        df['Gap_Yield'] = df['Gap']
        
        return df
    except Exception as e:
        print(f"Error loading prod data: {e}")
        return pd.DataFrame()

def run_cincin_api(df_ndre, z_core=-1.5, z_neighbor=-1.0, min_neighbors=3):
    """Aggregation of Cincin Api stats per block with Red/Orange/Yellow breakdown."""
    results = []
    
    # Pre-group by block
    for blok, group in df_ndre.groupby('Blok'):
        # 1. Z-Score normalization per block
        ndvi = group['NDRE125']
        mean_val = ndvi.mean()
        std_val = ndvi.std()
        
        if std_val == 0: continue
        
        group = group.copy() # Safe copy
        group['z'] = (group['NDRE125'] - mean_val) / std_val
        
        # 2. Build Tree Map
        tree_map = {}
        for _, row in group.iterrows():
            key = f"{int(row['N_POKOK'])},{int(row['N_BARIS'])}"
            tree_map[key] = {'z': row['z'], 'status': 'HIJAU'}
            
        # 3. Detect Status
        offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        keys = list(tree_map.keys())
        
        # Red (Core)
        cores = set()
        for k in keys:
            if tree_map[k]['z'] < z_core:
                x,y = map(int, k.split(','))
                count = 0
                for o in offsets:
                    nk = f"{x+o[0]},{y+o[1]}"
                    if nk in tree_map and tree_map[nk]['z'] < z_neighbor:
                        count += 1
                if count >= min_neighbors:
                    tree_map[k]['status'] = 'MERAH'
                    cores.add(k)
        
        # Orange (Ring)
        queue = list(cores)
        visited = set(cores)
        while queue:
            k = queue.pop(0)
            cx, cy = map(int, k.split(','))
            for o in offsets:
                nk = f"{cx+o[0]},{cy+o[1]}"
                if nk in tree_map and nk not in visited:
                    if tree_map[nk]['z'] < z_neighbor:
                        if tree_map[nk]['status'] != 'MERAH':
                            tree_map[nk]['status'] = 'ORANYE'
                        visited.add(nk)
                        queue.append(nk)
        
        # Yellow (Suspect)
        for k in keys:
            if tree_map[k]['status'] == 'HIJAU' and tree_map[k]['z'] < z_neighbor:
                tree_map[k]['status'] = 'KUNING'

        # Count
        c_red = 0; c_orange = 0; c_yellow = 0;
        for k in keys:
            s = tree_map[k]['status']
            if s == 'MERAH': c_red += 1
            elif s == 'ORANYE': c_orange += 1
            elif s == 'KUNING': c_yellow += 1
            
        total = len(group)
        results.append({
            'Blok': str(blok).strip().upper(),
            'Tree_Count': total,
            'Merah': c_red,
            'Merah_Pct': (c_red/total)*100,
            'Oranye': c_orange,
            'Oranye_Pct': (c_orange/total)*100,
            'Kuning': c_yellow,
            'Kuning_Pct': (c_yellow/total)*100,
            'Infected_Pct': ((c_red+c_orange)/total) * 100 # Broad definition
        })
        
    return pd.DataFrame(results)

# -------------------------------------------------------------------------
# 2. MAIN LOGIC
# -------------------------------------------------------------------------

def main():
    print("\n🔬 ANALYSIS: Cincin Api Relevance Check (Standard Preset)")
    print("="*60)
    
    # 1. Load NDRE (Sample AME II)
    path_ame2 = Path('data/input/tabelNDREnew.csv')
    if not path_ame2.exists(): path_ame2 = Path('../data/input/tabelNDREnew.csv')
    
    if path_ame2.exists():
        print("Loading AME II NDRE Data...")
        df_ndre = load_and_clean_data(path_ame2)
        # Fix column names if needed
        if 'Blok' not in df_ndre.columns and 'BLOK' in df_ndre.columns:
            df_ndre['Blok'] = df_ndre['BLOK']
        
        # Run Algo
        print("Running Cincin Api Algorithm...")
        df_algo = run_cincin_api(df_ndre)
        print(f"Algorithm processed {len(df_algo)} blocks.")
    else:
        print("❌ NDRE Data not found")
        return

    # 2. Load Productivity
    df_prod = load_productivity_data()
    print(f"Productivity Data: {len(df_prod)} blocks loaded.")
    
    # 3. Merge
    print("Merging Datasets...")
    # Normalize block names in df_prod for better matching (remove spaces, etc if needed)
    # df_prod['Blok_Prod'] already upper/string
    
    if 'Blok_Prod' not in df_prod.columns:
        print(f"❌ 'Blok_Prod' column missing from Productivity Data. Available: {df_prod.columns.tolist()}")
        return

    merged = pd.merge(df_algo, df_prod, left_on='Blok', right_on='Blok_Prod', how='inner')
    
    print(f"Matches found: {len(merged)} blocks.")
    
    if len(merged) == 0:
        print("❌ No overlapping blocks found between NDRE and Productivity Data.")
        print("Sample NDRE Blocks:", df_algo['Blok'].unique()[:5])
        print("Sample Prod Blocks:", df_prod['Blok_Prod'].unique()[:5])
        return

    # 4. Correlation Analysis
    corr_yield = merged['Infected_Pct'].corr(merged['Yield_Real'])
    corr_gap = merged['Infected_Pct'].corr(merged['Gap'])
    
    print("\n📊 CORRELATION STATISTICS")
    print("-" * 30)
    print(f"Correlation (Infection % vs Yield): {corr_yield:.4f}")
    print(f"Correlation (Infection % vs Gap)  : {corr_gap:.4f}")
    print("(Note: Negative corr with Yield is EXPECTED. Positive with Gap is EXPECTED.)")
    
    # 5. Show Top 2 Sample Blocks (Readable Format)
    print("\n📝 SAMPLE BLOCK DETAILS (Format Mudah Dibaca)")
    print("=" * 60)
    
    # Sort by Infection Rate Descending
    top_infected = merged.sort_values('Infected_Pct', ascending=False).head(2)
    
    for _, row in top_infected.iterrows():
        print(f"\nBLOCK: {row['Blok']}")
        print(f"  • Populasi Pohon : {int(row['Tree_Count']):,}")
        print(f"  • 🔴 Merah (Core): {int(row['Merah']):,} ({row['Merah_Pct']:.1f}%)")
        print(f"  • 🟠 Oranye (Ring): {int(row['Oranye']):,} ({row['Oranye_Pct']:.1f}%)")
        print(f"  • 🟡 Kuning (Suspect): {int(row['Kuning']):,} ({row['Kuning_Pct']:.1f}%)")
        print(f"  • infected Total : {row['Infected_Pct']:.1f}%")
        print(f"  • Realisasi Yield: {row['Yield_Real']:.2f} Ton/Ha")
        print(f"  • Potensi Yield  : {row['Potensi_Yield']:.2f} Ton/Ha")
        print(f"  • GAP (Loss)     : {row['Gap']:.2f} Ton/Ha")
        
        trench_needed = "SANGAT PERLU (Prioritas Tinggi)" if row['Merah_Pct'] > 5 else "PERLU PENGAWASAN"
        print(f"  • KRUSIALITAS PARIT: [{trench_needed}]")

main()
