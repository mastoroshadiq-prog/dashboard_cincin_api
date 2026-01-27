"""
ANALISA AME II (AME02) - PILOT PROJECT
Gap Yield, Attack Rate Ganoderma, Avg Yield

Kolom target dari Excel:
- Col 5 (Unnamed: 5): DIVISI
- Col 8 (Unnamed: 8): BLOK
- Col 55-58: Gano Stadium 1&2, 3&4, Total, % Serangan
- Real vs Potensi columns untuk gap yield
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_FILE = Path("poac_sim/data/output/ame02_analysis.json")

# Default TBS price
DEFAULT_TBS_PRICE = 2500  # Rupiah per KG

def analyze_ame02(tbs_price=DEFAULT_TBS_PRICE):
    """
    Analisa AME02 untuk:
    1. Gap Yield (Potensi - Realisasi)
    2. Loss/Kerugian financial
    3. Attack Rate Ganoderma
    4. Average Yield
    """
    
    print("=" * 80)
    print("ANALISA AME II (AME02) - PILOT PROJECT")
    print("=" * 80)
    
    # Load data
    df = pd.read_excel(INPUT_FILE)
    print(f"\n[OK] Total data: {len(df)} rows")
    
    # Filter untuk AME02
    # Skip header rows (row 0-2 are headers)
    df_cleaned = df[3:].copy()  # Skip first 3 rows
    df_cleaned.columns = df.iloc[2]  # Use row 2 as header
    
    # Identify DIVISI column
    divisi_col = df.columns[5]  # Unnamed: 5
    blok_col = df.columns[8]    # Unnamed: 8
    
    print(f"[INFO] Divisi column: {divisi_col}")
    print(f"[INFO] Blok column: {blok_col}")
    
    # Filter AME02
    ame02_data = df[df[divisi_col] == 'AME02'].copy()
    
    print(f"\n[OK] AME02 blocks found: {len(ame02_data)}")
    
    if len(ame02_data) == 0:
        print("[ERROR] No AME02 data found!")
        return None
    
    # Extract Ganoderma data (columns 55-58)
    gano_stad_12_col = df.columns[55]  # Stadium 1&2
    gano_stad_34_col = df.columns[56]  # Stadium 3&4
    gano_total_col = df.columns[57]    # Total
    gano_pct_col = df.columns[58]      # % Serangan
    
    # Extract 2025 data (last year in dataset)
    # Real: columns 169-171 (BJR, JumJJg, Ton)
    # Potensi: columns 172-174 (BJR, JumJJg, Ton)
    real_bjr_2025 = df.columns[169]
    real_jjg_2025 = df.columns[170]
    real_ton_2025 = df.columns[171]
    
    pot_bjr_2025 = df.columns[172]
    pot_jjg_2025 = df.columns[173]
    pot_ton_2025 = df.columns[174]
    
    # Calculate metrics
    results = {
        'division': 'AME02',
        'division_name': 'AME II',
        'total_blocks': len(ame02_data),
        'tbs_price_per_kg': tbs_price,
        'metrics': {}
    }
    
    # 1. GAP YIELD & LOSS
    ame02_data['real_ton_2025'] = pd.to_numeric(ame02_data[real_ton_2025], errors='coerce').fillna(0)
    ame02_data['pot_ton_2025'] = pd.to_numeric(ame02_data[pot_ton_2025], errors='coerce').fillna(0)
    ame02_data['gap_yield_ton'] = ame02_data['pot_ton_2025'] - ame02_data['real_ton_2025']
    ame02_data['gap_yield_kg'] = ame02_data['gap_yield_ton'] * 1000
    ame02_data['loss_rp'] = ame02_data['gap_yield_kg'] * tbs_price
    
    total_gap_kg = ame02_data['gap_yield_kg'].sum()
    total_loss_rp = ame02_data['loss_rp'].sum()
    
    results['metrics']['gap_yield'] = {
        'total_gap_kg': float(total_gap_kg),
        'total_gap_ton': float(total_gap_kg / 1000),
        'total_loss_rp': float(total_loss_rp),
        'avg_gap_per_block_kg': float(total_gap_kg / len(ame02_data))
    }
    
    # 2. ATTACK RATE GANODERMA
    ame02_data['gano_pct'] = pd.to_numeric(ame02_data[gano_pct_col], errors='coerce').fillna(0)
    avg_attack_rate = ame02_data['gano_pct'].mean() * 100  # Convert to percentage
    
    results['metrics']['ganoderma'] = {
        'avg_attack_rate_pct': float(avg_attack_rate),
        'blocks_with_ganoderma': int((ame02_data['gano_pct'] > 0).sum())
    }
    
    # 3. AVG YIELD
    total_real_ton = ame02_data['real_ton_2025'].sum()
    total_pot_ton = ame02_data['pot_ton_2025'].sum()
    
    results['metrics']['yield'] = {
        'avg_real_yield_ton_per_block': float(total_real_ton / len(ame02_data)),
        'avg_pot_yield_ton_per_block': float(total_pot_ton / len(ame02_data)),
        'total_real_ton': float(total_real_ton),
        'total_pot_ton': float(total_pot_ton)
    }
    
    # Save to JSON
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {OUTPUT_FILE}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("RINGKASAN ANALISA AME II")
    print("=" * 80)
    
    print(f"\n1. GAP YIELD (Potensi - Realisasi) 2025:")
    print(f"   Total Gap: {total_gap_kg:,.0f} KG ({total_gap_kg/1000:,.2f} Ton)")
    print(f"   Rata-rata per Blok: {total_gap_kg/len(ame02_data):,.0f} KG")
    
    print(f"\n2. KERUGIAN FINANCIAL:")
    print(f"   Harga TBS: Rp {tbs_price:,}/KG")
    print(f"   Total Loss: Rp {total_loss_rp:,.0f}")
    print(f"   Total Loss: Rp {total_loss_rp/1_000_000:,.2f} Juta")
    
    print(f"\n3. GANODERMA ATTACK RATE:")
    print(f"   Avg Attack Rate: {avg_attack_rate:.2f}%")
    print(f"   Blok Terserang: {(ame02_data['gano_pct'] > 0).sum()} / {len(ame02_data)}")
    
    print(f"\n4. AVERAGE YIELD:")
    print(f"   Realisasi: {total_real_ton/len(ame02_data):,.2f} Ton/Blok")
    print(f"   Potensi: {total_pot_ton/len(ame02_data):,.2f} Ton/Blok")
    print(f"   Total Realisasi: {total_real_ton:,.2f} Ton")
    print(f"   Total Potensi: {total_pot_ton:,.2f} Ton")
    
    print("\n" + "=" * 80)
    
    return results

def main():
    results = analyze_ame02()
    
    if results:
        print("\n[SUCCESS] Analisa AME02 selesai!")
        print(f"[INFO] Check JSON file: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
