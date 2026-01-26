import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    
    # Baca header baris 3 (index 2) dan 7 (index 6)
    df_head3 = pd.read_excel(file_path, header=None, skiprows=3, nrows=1)
    df_head7 = pd.read_excel(file_path, header=None, skiprows=7, nrows=1)
    
    print("=== HEADER KOLOM 54 VS 68 ===")
    
    h3_54 = df_head3.iloc[0, 54]
    h3_68 = df_head3.iloc[0, 68]
    
    h7_54 = df_head7.iloc[0, 54] # Baris ke-7
    # Baris ke-8 adalah data pertama (row 8 di excel, index 7 di pandas jika header=None)
    # Tadi saya skiprows=8 untuk data, berarti header paling bawah adalah baris 7 (index 6)
    
    # Label Row 3 (Index 2)
    print(f"Row 3 Index 54: {h3_54}")
    print(f"Row 3 Index 68: {h3_68}")
    
    # Label Row 7 (Index 6)
    print(f"Row 7 Index 54: {df_head7.iloc[0, 54]}")
    print(f"Row 7 Index 68: {df_head7.iloc[0, 68]}")

except Exception as e:
    print(f"Error: {e}")
