"""
Analisa Kerugian Produksi per Divisi
Menghitung total kerugian akibat penurunan produksi untuk:
1. Tahun 2025 (actual loss)
2. Tren 2023-2025 (2 tahun)
3. Proyeksi 2025-2027 (2 tahun ke depan jika tidak ada treatment)
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths
INPUT_FILE = Path("poac_sim/data/input/data_gabungan.xlsx")
OUTPUT_FILE = Path("poac_sim/data/output/production_loss_analysis.json")

# Asumsi harga TBS per KG (dalam Rupiah)
HARGA_TBS_PER_KG = 2500  # Adjust sesuai harga pasar aktual

def calculate_production_loss(df):
    """
    Menghitung kerugian produksi berdasarkan penurunan dari tahun ke tahun
    """
    results = {}
    
    # Group by divisi
    divisions = df['divisi'].unique()
    
    for div in divisions:
        div_data = df[df['divisi'] == div].copy()
        
        # Initialize division results
        div_results = {
            'division_code': div,
            'division_name': f"AME {div.replace('AME', '')}",
            'total_blocks': len(div_data),
            'loss_2025': 0,
            'loss_2023_2025': 0,
            'projected_loss_2025_2027': 0,
            'declining_blocks': 0,
            'blocks_detail': []
        }
        
        for idx, row in div_data.iterrows():
            block_code = row['kode_blok']
            
            # Get production data
            prod_2023 = row.get('prod_2023', 0) or 0
            prod_2024 = row.get('prod_2024', 0) or 0
            prod_2025 = row.get('prod_2025', 0) or 0
            
            # Calculate losses (only for declining blocks)
            loss_2024 = max(0, prod_2023 - prod_2024)  # Kerugian 2024 vs 2023
            loss_2025 = max(0, prod_2024 - prod_2025)  # Kerugian 2025 vs 2024
            
            # Calculate trend for projection
            if prod_2023 > 0 and prod_2024 > 0 and prod_2025 > 0:
                # Average decline rate per year
                decline_rate_2024 = (prod_2023 - prod_2024) / prod_2023 if prod_2023 > 0 else 0
                decline_rate_2025 = (prod_2024 - prod_2025) / prod_2024 if prod_2024 > 0 else 0
                avg_decline_rate = (decline_rate_2024 + decline_rate_2025) / 2
                
                # Project 2026 and 2027
                if avg_decline_rate > 0:
                    prod_2026_proj = prod_2025 * (1 - avg_decline_rate)
                    prod_2027_proj = prod_2026_proj * (1 - avg_decline_rate)
                    
                    loss_2026_proj = max(0, prod_2025 - prod_2026_proj)
                    loss_2027_proj = max(0, prod_2026_proj - prod_2027_proj)
                else:
                    loss_2026_proj = 0
                    loss_2027_proj = 0
            else:
                avg_decline_rate = 0
                loss_2026_proj = 0
                loss_2027_proj = 0
            
            # Convert to Rupiah (KG * Harga per KG)
            loss_2025_rp = loss_2025 * HARGA_TBS_PER_KG
            loss_2023_2025_rp = (loss_2024 + loss_2025) * HARGA_TBS_PER_KG
            loss_2025_2027_proj_rp = (loss_2025 + loss_2026_proj + loss_2027_proj) * HARGA_TBS_PER_KG
            
            # Only count if there's actual loss
            if loss_2025 > 0 or loss_2024 > 0:
                div_results['declining_blocks'] += 1
                div_results['loss_2025'] += loss_2025_rp
                div_results['loss_2023_2025'] += loss_2023_2025_rp
                div_results['projected_loss_2025_2027'] += loss_2025_2027_proj_rp
                
                div_results['blocks_detail'].append({
                    'block_code': block_code,
                    'prod_2023': prod_2023,
                    'prod_2024': prod_2024,
                    'prod_2025': prod_2025,
                    'loss_kg_2025': loss_2025,
                    'loss_rp_2025': loss_2025_rp,
                    'decline_rate': avg_decline_rate * 100
                })
        
        results[div] = div_results
    
    # Calculate grand total
    grand_total = {
        'total_loss_2025': sum(d['loss_2025'] for d in results.values()),
        'total_loss_2023_2025': sum(d['loss_2023_2025'] for d in results.values()),
        'total_projected_loss_2025_2027': sum(d['projected_loss_2025_2027'] for d in results.values()),
        'total_declining_blocks': sum(d['declining_blocks'] for d in results.values()),
        'total_blocks': sum(d['total_blocks'] for d in results.values())
    }
    
    # Format for output
    output = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'assumptions': {
            'tbs_price_per_kg': HARGA_TBS_PER_KG,
            'currency': 'IDR'
        },
        'grand_total': grand_total,
        'divisions': results
    }
    
    return output

def format_rupiah(value):
    """Format number to Rupiah string"""
    if value >= 1_000_000_000:
        return f"Rp {value/1_000_000_000:.2f} M"
    elif value >= 1_000_000:
        return f"Rp {value/1_000_000:.2f} Jt"
    else:
        return f"Rp {value:,.0f}"

def main():
    print("=" * 80)
    print("ANALISA KERUGIAN PRODUKSI PER DIVISI")
    print("=" * 80)
    
    # Load data
    print(f"\n📂 Loading data from: {INPUT_FILE}")
    df = pd.read_excel(INPUT_FILE)
    print(f"✅ Loaded {len(df)} blocks")
    
    # Calculate losses
    print("\n📊 Calculating production losses...")
    results = calculate_production_loss(df)
    
    # Save to JSON
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to: {OUTPUT_FILE}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("RINGKASAN KERUGIAN PRODUKSI")
    print("=" * 80)
    
    gt = results['grand_total']
    
    print(f"\n💰 TOTAL KERUGIAN 2025:")
    print(f"   {format_rupiah(gt['total_loss_2025'])}")
    
    print(f"\n💰 TOTAL KERUGIAN 2023-2025 (2 Tahun):")
    print(f"   {format_rupiah(gt['total_loss_2023_2025'])}")
    
    print(f"\n💰 PROYEKSI KERUGIAN 2025-2027 (Tanpa Treatment):")
    print(f"   {format_rupiah(gt['total_projected_loss_2025_2027'])}")
    
    print(f"\n📉 Blok dengan Penurunan: {gt['total_declining_blocks']} / {gt['total_blocks']}")
    
    print("\n" + "=" * 80)
    print("KERUGIAN PER DIVISI")
    print("=" * 80)
    
    for div_code, div_data in results['divisions'].items():
        print(f"\n🏢 {div_data['division_name']} ({div_code})")
        print(f"   Blok Menurun: {div_data['declining_blocks']} / {div_data['total_blocks']}")
        print(f"   Kerugian 2025: {format_rupiah(div_data['loss_2025'])}")
        print(f"   Kerugian 2023-2025: {format_rupiah(div_data['loss_2023_2025'])}")
        print(f"   Proyeksi 2025-2027: {format_rupiah(div_data['projected_loss_2025_2027'])}")
    
    print("\n" + "=" * 80)
    print("✅ ANALISA SELESAI!")
    print("=" * 80)

if __name__ == "__main__":
    main()
