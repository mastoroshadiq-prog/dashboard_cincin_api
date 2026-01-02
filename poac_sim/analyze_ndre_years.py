
import pandas as pd

df = pd.read_csv('data/input/tabelNDREnew.csv')

blocks = ['D006A', 'D007A']

for block in blocks:
    print(f"\n--- {block} ---")
    # Filter block
    # Check 'blok_b' first
    subset = df[df['blok_b'].astype(str).str.upper() == block]
    
    if subset.empty:
        print("Not found in blok_b, checking 'blok'")
        subset = df[df['blok'].astype(str).str.upper() == block]
        
    if not subset.empty:
        # Check Distribution of 't_tanam'
        if 't_tanam' in subset.columns:
            counts = subset['t_tanam'].value_counts()
            print("Tahun Tanam Distribution:")
            print(counts)
            
            # If multiple years, we can infer Pokok vs Sisip
            years = sorted(counts.index.tolist())
            if len(years) > 0:
                oldest = years[0]
                pokok = counts[oldest]
                sisip = sum(counts[y] for y in years if y != oldest)
                print(f"POKOK (Year {oldest}): {pokok}")
                print(f"SISIP (Other Years): {sisip}")
        else:
            print("Column t_tanam not found")
            
        print(f"Total entries: {len(subset)}")
    else:
        print("No data found in NDRE.")
