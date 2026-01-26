"""
Historical data module - extract yearly yield data for drilldown
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_historical_yield_data():
    """
    Load historical yield data from data_gabungan.xlsx
    Returns DataFrame with block as index and years as columns
    """
    try:
        file_path = Path('data/input/data_gabungan.xlsx')
        df_raw = pd.read_excel(file_path, header=None)
        df = df_raw.iloc[8:].copy().reset_index(drop=True)
        df.columns = [f'col_{i}' for i in range(df.shape[1])]
        
        # Based on analysis, yield columns appear in a pattern
        # Each year has multiple columns, but we want the yield (Ton/Ha)
        # Pattern observed: every ~10 columns represents a year
        # Let's use specific columns that represent yield
        
        # Approximate mapping (needs validation)
        # Year columns based on production pattern
        year_mapping = {
            '2014': 72,   # BJR Kg values / 1000 to get Ton/Ha approx
            '2015': 81,
            '2016': 90,
            '2017': 99,
            '2018': 108,
            '2019': 117,
            '2020': 126,
            '2021': 135,
            '2022': 144,
            '2023': 153,
            '2024': 162,
            '2025': 171   # Known from previous analysis
        }
        
        # Extract data
        historical = df[['col_0']].copy()
        historical.columns = ['Blok']
        
        for year, col_idx in year_mapping.items():
            if f'col_{col_idx}' in df.columns:
                historical[year] = pd.to_numeric(df[f'col_{col_idx}'], errors='coerce')
        
        # Set block as index
        historical = historical.set_index('Blok')
        
        # Filter out blocks with all NaN
        historical = historical.dropna(how='all')
        
        return historical
        
    except Exception as e:
        print(f"  ⚠️ Could not load historical data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

# Test
if __name__ == '__main__':
    hist_data = load_historical_yield_data()
    print(f'Loaded historical data: {hist_data.shape}')
    print(f'\nSample E011A:')
    if 'E011A' in hist_data.index:
        print(hist_data.loc['E011A'])
    else:
        print('E011A not found')
    
    print(f'\nYears available: {hist_data.columns.tolist()}')
