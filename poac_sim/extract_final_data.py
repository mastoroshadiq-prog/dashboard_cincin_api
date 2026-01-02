
import pandas as pd

path = 'data/input/data_gabungan.xlsx'
df = pd.read_excel(path, header=3)

# Function to safe get value
def get_val(row, col_name, offset=0):
    try:
        col_idx = df.columns.get_loc(col_name)
        return row.iloc[col_idx + offset]
    except:
        return None

# Filter D006A, D007A
df['BLOK_CLEAN'] = df.iloc[:, 2].astype(str).str.strip().str.upper() # Assume Col 2 is BLOK based on finding
targets = ['D006A', 'D007A']

print("=== FINAL DATA EXTRACTION ===")
for t in targets:
    row = df[df['BLOK_CLEAN'] == t]
    if not row.empty:
        r = row.iloc[0]
        # Extract Agronomy (using explicit headers if possible or indices based on brute force)
        # Brute force: TT is col 'TT'
        tt = r['TT']
        
        # Brute: Ha is col index 3 (Unnamed: 3 likely if header failed, or search 'Ha')
        # Let's search by index from BLOK (idx 2)
        # BLOK (2) -> Ha (3?) -> TT (4?) -> Pokok (5?) -> SPH (6?)
        # Header dump said: BLOK, TT, VARIET.. LUAS
        # But Brute said: Unnamed: 3 (23.0) which is Ha.
        # Let's trust values.
        
        ha = r.iloc[3] # Ha
        # TT is at index 3? Wait. 
        # In brute output: BLOK: D006A, Unnamed: 3: 23.0, TT: 2009
        # So TT is a named column.
        
        pokok = r.iloc[5] # Unnamed: 5 (2391)
        sph = r.iloc[6] # Unnamed: 6 (103.95)
        
        # Production 2024
        # Column '2024' exists
        real_2024 = r['2024']
        pot_2024 = get_val(r, '2024', 2) # Unnamed: 162 (Offset 2 from 2024 col 160)
        gap_2024 = get_val(r, '2024', 5) # Unnamed: 165 (Offset 5 from 2024 col 160)
        
        print(f"\nBLOCK: {t}")
        print(f"  Tahun Tanam: {tt}")
        print(f"  Luas: {ha} Ha")
        print(f"  Pokok: {pokok}")
        print(f"  SPH: {sph}")
        print(f"  Prod 2024 (Real): {real_2024} Ton/Ha")
        print(f"  Prod 2024 (Potensi): {pot_2024} Ton/Ha")
        print(f"  Gap 2024: {gap_2024} Ton/Ha")
        
    else:
        print(f"Block {t} not found.")
