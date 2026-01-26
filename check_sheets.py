import pandas as pd

try:
    file_path = r'poac_sim\data\input\data_gabungan.xlsx'
    xl = pd.ExcelFile(file_path)
    print("=== DAFTAR SHEET ===")
    print(xl.sheet_names)
except Exception as e:
    print(f"Error: {e}")
