"""
AME02 Analysis - Final Version
Identifikasi kolom Real dan Potensi 2025 dengan benar
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_FILE = Path("poac_sim/data/output/ame02_analysis.json")

DEFAULT_TBS_PRICE = 2500  # Rupiah per KG

def find_2025_columns(df):
    """
    Cari kolom untuk 2025 Real dan Potensi
    """
    print("\n[INFO] Mencari kolom 2025...")
    
    # Check headers in row 1 and row 2 for patterns
    results = {
        'year_col': None,
        'real_bjr': None,
        'real_jjg': None,
        'real_ton': None,
        'pot_bjr': None,
        'pot_jjg': None,
        'pot_ton': None
    }
    
    # Find column with "2025" in row 2
    for i, col in enumerate(df.columns):
        val_row2 = str(df.iloc[2, i]) if pd.notna(df.iloc[2, i]) else ""
        
        if val_row2 == "2025":
            results['year_col'] = i
            print(f"[OK] Found 2025 at column {i}")
            
            # Pattern: Real (BJR, JJG, Ton), then Potensi (BJR, JJG, Ton)
            # Check next few columns for "Real", "Potensi"
            for j in range(i, min(i+10, len(df.columns))):
                val_row1 = str(df.iloc[1, j]) if pd.notna(df.iloc[1, j]) else ""
                val_row2_check = str(df.iloc[2, j]) if pd.notna(df.iloc[2, j]) else ""
                
                print(f"  Col {j}: Row1='{val_row1}', Row2='{val_row2_check}'")
                
                # Real columns
                if "Real" in val_row1:
                    if "BJR" in val_row2_check or "Kg" in val_row2_check:
                        results['real_bjr'] = j
                    elif "Jum" in val_row2_check or "JJg" in val_row2_check:
                        results['real_jjg'] = j
                    elif "Ton" in val_row2_check:
                        results['real_ton'] = j
                
                # Potensi columns
                if "Potensi" in val_row1:
                    if "BJR" in val_row2_check or "Kg" in val_row2_check:
                        results['pot_bjr'] = j
                    elif "Jum" in val_row2_check or "JJg" in val_row2_check:
                        results['pot_jjg'] = j
                    elif "Ton" in val_row2_check:
                        results['pot_ton'] = j
            
            break
    
    return results

def analyze_ame02(tbs_price=DEFAULT_TBS_PRICE):
    """
    Analisa AME02:
    1. Gap Yield (Potensi - Realisasi) 
    2. Loss/Kerugian financial
    3. Attack Rate Ganoderma
    4. Average Yield
    """
    
    print("=" * 80)
    print("ANALISA AME II (AME02) - COMPREHENSIVE")
    print("=" * 80)
    
    # Load data
    df = pd.read_excel(INPUT_FILE)
    print(f"\n[OK] Total data: {len(df)} rows, {len(df.columns)} columns")
    
    # Find 2025 columns
    cols_2025 = find_2025_columns(df)
    
    if cols_2025['real_ton'] is None or cols_2025['pot_ton'] is None:
        print("\n[ERROR] Could not find Real/Potensi Ton columns for 2025!")
        print(f"Found columns: {cols_2025}")
        return None
    
    print(f"\n[OK] Column mapping:")
    print(f"  Real Ton (2025): Column {cols_2025['real_ton']}")
    print(f"  Potensi Ton (2025): Column {cols_2025['pot_ton']}")
    
    # Get column references
    divisi_col = df.columns[5]  # Unnamed: 5
    blok_col = df.columns[8]    # Unnamed: 8
    
    # Ganoderma columns
    gano_pct_col = df.columns[58]  # % Serangan
    
    # Filter AME02 (skip first 3 header rows)
    ame02_mask = df[divisi_col] == 'AME02'
    ame02_data = df[ame02_mask].copy()
    
    print(f"\n[OK] AME02 blocks found: {len(ame02_data)}")
    
    if len(ame02_data) == 0:
        print("[ERROR] No AME02 data found!")
        return None
    
    # Extract Real and Potensi Ton
    real_col = df.columns[cols_2025['real_ton']]
    pot_col = df.columns[cols_2025['pot_ton']]
    
    ame02_data['real_ton_2025'] = pd.to_numeric(ame02_data[real_col], errors='coerce').fillna(0)
    ame02_data['pot_ton_2025'] = pd.to_numeric(ame02_data[pot_col], errors='coerce').fillna(0)
    
    # Calculate Gap Yield
    ame02_data['gap_yield_ton'] = ame02_data['pot_ton_2025'] - ame02_data['real_ton_2025']
    ame02_data['gap_yield_kg'] = ame02_data['gap_yield_ton'] * 1000
    ame02_data['loss_rp'] = ame02_data['gap_yield_kg'] * tbs_price
    
    # Sum metrics
    total_real_ton = ame02_data['real_ton_2025'].sum()
    total_pot_ton = ame02_data['pot_ton_2025'].sum()
    total_gap_ton = ame02_data['gap_yield_ton'].sum()
    total_gap_kg = total_gap_ton * 1000
    total_loss_rp = ame02_data['loss_rp'].sum()
    
    # Ganoderma
    ame02_data['gano_pct'] = pd.to_numeric(ame02_data[gano_pct_col], errors='coerce').fillna(0)
    avg_attack_rate = ame02_data['gano_pct'].mean() * 100  # Convert to %
    blocks_with_gano = (ame02_data['gano_pct'] > 0).sum()
    
    # Build results
    results = {
        'division': 'AME02',
        'division_name': 'AME II',
        'total_blocks': len(ame02_data),
        'tbs_price_per_kg': tbs_price,
        'metrics': {
            'gap_yield': {
                'total_real_ton': float(total_real_ton),
                'total_pot_ton': float(total_pot_ton),
                'total_gap_ton': float(total_gap_ton),
                'total_gap_kg': float(total_gap_kg),
                'avg_gap_per_block_kg': float(total_gap_kg / len(ame02_data)),
                'avg_gap_per_block_ton': float(total_gap_ton / len(ame02_data))
            },
            'financial_loss': {
                'total_loss_rp': float(total_loss_rp),
                'total_loss_juta': float(total_loss_rp / 1_000_000),
                'total_loss_miliar': float(total_loss_rp / 1_000_000_000),
                'avg_loss_per_block_rp': float(total_loss_rp / len(ame02_data))
            },
            'ganoderma': {
                'avg_attack_rate_pct': float(avg_attack_rate),
                'blocks_with_ganoderma': int(blocks_with_gano),
                'blocks_clean': int(len(ame02_data) - blocks_with_gano)
            },
            'yield': {
                'avg_real_yield_ton_per_block': float(total_real_ton / len(ame02_data)),
                'avg_pot_yield_ton_per_block': float(total_pot_ton / len(ame02_data)),
                'total_real_ton': float(total_real_ton),
                'total_pot_ton': float(total_pot_ton),
                'yield_efficiency_pct': float((total_real_ton / total_pot_ton * 100) if total_pot_ton > 0 else 0)
            }
        }
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
    
    print(f"\n1. YIELD PERFORMANCE:")
    print(f"   Realisasi Total: {total_real_ton:,.2f} Ton")
    print(f"   Potensi Total: {total_pot_ton:,.2f} Ton")
    print(f"   Efficiency: {(total_real_ton/total_pot_ton*100) if total_pot_ton > 0 else 0:.2f}%")
    
    print(f"\n2. GAP YIELD (Potensi - Realisasi):")
    print(f"   Total Gap: {total_gap_ton:,.2f} Ton ({total_gap_kg:,.0f} KG)")
    print(f"   Rata-rata per Blok: {total_gap_ton/len(ame02_data):,.2f} Ton")
    
    print(f"\n3. KERUGIAN FINANCIAL:")
    print(f"   Harga TBS: Rp {tbs_price:,}/KG")
    print(f"   Total Loss: Rp {total_loss_rp:,.0f}")
    print(f"   Total Loss: Rp {total_loss_rp/1_000_000:,.2f} Juta")
    if total_loss_rp >= 1_000_000_000:
        print(f"   Total Loss: Rp {total_loss_rp/1_000_000_000:,.2f} Miliar")
    
    print(f"\n4. GANODERMA ATTACK:")
    print(f"   Avg Attack Rate: {avg_attack_rate:.2f}%")
    print(f"   Blok Terserang: {blocks_with_gano} / {len(ame02_data)}")
    print(f"   Blok Bersih: {len(ame02_data) - blocks_with_gano}")
    
    print("\n" + "=" * 80)
    
    return results

def main():
    results = analyze_ame02()
    
    if results:
        print("\n[SUCCESS] Analisa AME02 selesai!")
        print(f"[INFO] Check JSON: {OUTPUT_FILE}")
    else:
        print("\n[FAILED] Analisa gagal!")

if __name__ == "__main__":
    main()
