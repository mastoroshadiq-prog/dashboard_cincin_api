
import pandas as pd
from pathlib import Path

def inspect_files():
    files = [
        'data/input/tabelNDREnew.csv',
        'data/input/AME_IV.csv',
        'data/input/data_baru.csv',
        'data/input/tableNDRE.csv'
    ]
    
    targets = ['A004', 'A005', 'A004A', 'A005A', 'A04', 'A05']
    
    for f in files:
        path = Path(f)
        if not path.exists(): path = Path('../' + f)
        
        if path.exists():
            print(f"\nScanning {path.name}...")
            try:
                if 'csv' in path.suffix:
                    try:
                        df = pd.read_csv(path, sep=None, engine='python', nrows=500000)
                    except:
                        df = pd.read_csv(path, sep=';', nrows=500000)
                else:
                    df = pd.read_excel(path, nrows=1000)
                    
                # Normalize cols
                df.columns = [str(c).upper().strip() for c in df.columns]
                
                # Look for column likely to be Block
                block_cols = [c for c in df.columns if 'BLOK' in c or 'BLOCK' in c]
                print(f"  Block Cols: {block_cols}")
                
                found = False
                for bc in block_cols:
                    sample = df[bc].astype(str).unique()[:5]
                    print(f"  Sample {bc}: {sample}")
                    
                    # Check for targets
                    mask = df[bc].astype(str).str.upper().apply(lambda x: any(t in x for t in targets))
                    matches = df[mask][bc].unique()
                    if len(matches) > 0:
                        print(f"  ✅ MATCHES FOUND in {bc}: {matches[:10]}")
                        found = True
                        
                if not found:
                    print("  ❌ No matches for A004/A005")
                    
            except Exception as e:
                print(f"  Error reading: {e}")

inspect_files()
