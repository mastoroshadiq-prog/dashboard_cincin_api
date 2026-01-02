import pandas as pd
import numpy as np

print('='*80)
print('📊 EKSTRAKSI DATA PRODUKSI 2025 - F008A & D001A')
print('='*80)

# Load data_gabungan.xlsx
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)

print(f'\nTotal columns: {len(df.columns)}')
print(f'Total rows: {len(df)}')

# Find F008A and D001A
f008a_row = df[df['Unnamed: 0'] == 'F008A']
d001a_row = df[df['Unnamed: 0'] == 'D001A']

print(f'\nF008A found: {len(f008a_row) > 0}')
print(f'D001A found: {len(d001a_row) > 0}')

if len(f008a_row) > 0 and len(d001a_row) > 0:
    f008a_data = f008a_row.iloc[0]
    d001a_data = d001a_row.iloc[0]
    
    # Based on screenshot:
    # 2025 Real: P107-P109 (columns around index 107-109)
    # 2025 Potensi: P110-P112 (columns around index 110-112)
    # 2025 Real vs Potensi: P113-P115 (columns around index 113-115)
    
    # Let's check column names around those indices
    print('\n📋 Column names around production data (index 100-120):')
    for i in range(100, min(120, len(df.columns))):
        print(f'  Index {i}: {df.columns[i]}')
    
    print('\n' + '='*80)
    print('📊 F008A - DATA PRODUKSI 2025')
    print('='*80)
    
    print(f'\nBlok: {f008a_data["Unnamed: 0"]}')
    print(f'Luas: {f008a_data["HA STATEMENT"]} Ha')
    
    # Extract production data from columns 107-115
    print('\nData dari kolom 107-115:')
    for i in range(107, min(116, len(df.columns))):
        val = f008a_data.iloc[i] if i < len(f008a_data) else None
        col_name = df.columns[i] if i < len(df.columns) else f'Col_{i}'
        if pd.notna(val):
            print(f'  Col {i} ({col_name}): {val}')
    
    print('\n' + '='*80)
    print('📊 D001A - DATA PRODUKSI 2025')
    print('='*80)
    
    print(f'\nBlok: {d001a_data["Unnamed: 0"]}')
    print(f'Luas: {d001a_data["HA STATEMENT"]} Ha')
    
    print('\nData dari kolom 107-115:')
    for i in range(107, min(116, len(df.columns))):
        val = d001a_data.iloc[i] if i < len(d001a_data) else None
        col_name = df.columns[i] if i < len(df.columns) else f'Col_{i}'
        if pd.notna(val):
            print(f'  Col {i} ({col_name}): {val}')
    
    # Try to identify which columns are Real Ton, Potensi Ton, Gap
    print('\n' + '='*80)
    print('🔍 IDENTIFIKASI KOLOM PRODUKSI')
    print('='*80)
    
    # Based on screenshot, columns should be:
    # Real: BJR Kg, Jum Jlg, Ton
    # Potensi: BJR Kg, Jum Jlg, Ton
    # Real vs Potensi: BJR Kg, Jum Jlg, Ton
    
    # Let's look for Ton columns (should have reasonable values)
    print('\nMencari kolom Ton (Real, Potensi, Gap):')
    
    ton_candidates = []
    for i in range(100, min(120, len(df.columns))):
        val_f008a = f008a_data.iloc[i] if i < len(f008a_data) else None
        val_d001a = d001a_data.iloc[i] if i < len(d001a_data) else None
        
        # Check if values are in reasonable range for production (Ton)
        if pd.notna(val_f008a) and isinstance(val_f008a, (int, float)):
            if -1000 < val_f008a < 10000:  # Reasonable range for Ton
                ton_candidates.append({
                    'index': i,
                    'column': df.columns[i],
                    'F008A': val_f008a,
                    'D001A': val_d001a if pd.notna(val_d001a) else None
                })
    
    print(f'\nFound {len(ton_candidates)} candidate columns:')
    for cand in ton_candidates:
        print(f"  Col {cand['index']} ({cand['column']}): F008A={cand['F008A']}, D001A={cand['D001A']}")

else:
    print('\n❌ Blok tidak ditemukan!')

print('\n✅ Selesai!')
