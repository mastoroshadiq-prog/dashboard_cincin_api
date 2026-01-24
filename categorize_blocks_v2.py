
import pandas as pd
import json
import numpy as np

try:
    # 1. Load Data Yield/Produksi (dari hasil generate sebelumnya dashboard_data.json atau raw)
    # Kita pakai raw excel lagi biar akurat 100%
    input_file = r'poac_sim\data\input\data_gabungan.xlsx'
    df = pd.read_excel(input_file, header=None, skiprows=8)

    # 2. Load Data TBM Valid (yang sudah kita filter ketat tadi)
    with open(r'data\output\tbm_stats_real.json', 'r') as f:
        tbm_valid_data = json.load(f)
    tbm_valid_codes = set(tbm_valid_data.keys())

    categories = {
        "declining": [],
        "stable": [],
        "increasing": [],
        "tbm": [],
        "empty": []
    }
    
    summary_stats = {
        "declining": {"count": 0, "avg_change": 0, "total_area": 0, "avg_prod_2023": 0, "avg_prod_2025": 0},
        "stable": {"count": 0},
        "increasing": {"count": 0},
        "tbm": {"count": 0},
        "empty": {"count": 0, "total_area": 0}
    }

    print("=== MULAI KATEGORISASI BLOK V2 (5 KATEGORI) ===")

    for _, row in df.iterrows():
        block_code = row[0]
        if pd.isna(block_code) or not isinstance(block_code, str):
            continue

        # Ambil Data Produksi (Yield) - Index 12, 16, 20 (Simulasi/Sesuai Logika Generate Data sebelumnya)
        # TAPI di sistem ini data yield dihitung di script analyze.
        # Kita pakai analisis sederhana di sini atau ambil data output dashboard sebelumnya?
        # Agar konsisten, kita baca 'dashboard_data.json' jika ada, tapi karena mungkin beda format,
        # Kita hitung manual yield dari kolom SPH/Pohon * BJR?
        # UNTUK KECEPATAN & KONSISTENSI dengan visualisasi chart sebelumnya:
        # Kita baca data 'HISTORICAL_YIELDS' dari HTML atau file 'dashboard_data.json' kalau ada.
        
        # Opsi terbaik: Gunakan kolom Excel yang sama dengan script analyze.
        # Index 12: Yield 2023
        # Index 16: Yield 2024
        # Index 20: Yield 2025
        
        try:
            y23 = float(row[12]) if pd.notna(row[12]) else 0
            y24 = float(row[16]) if pd.notna(row[16]) else 0
            y25 = float(row[20]) if pd.notna(row[20]) else 0
            luas = float(row[2]) if pd.notna(row[2]) else 0
        except:
            y23, y24, y25, luas = 0, 0, 0, 0

        total_yield = y23 + y24 + y25
        
        # LOGIC KATEGORISASI UTAMA
        
        # 1. Cek Apakah TBM Valid?
        if block_code in tbm_valid_codes:
            categories["tbm"].append({
                "block_code": block_code, 
                "val": 0, # Placeholder
                "desc": "Tahun Tanam: " + str(tbm_valid_data[block_code]['year'])
            })
            continue
            
        # 2. Cek Apakah KOSONG? (Produksi 0 dan Bukan TBM)
        if total_yield == 0:
            categories["empty"].append({
                "block_code": block_code,
                "val": 0,
                "desc": f"Luas: {luas} Ha (Tanpa Tanaman)"
            })
            summary_stats["empty"]["total_area"] += luas
            continue
            
        # 3. Kategori Produksi (Declining/Stable/Increasing)
        colors = []
        change_pct = 0
        
        if y23 > 0:
            change_pct = ((y25 - y23) / y23) * 100
        else:
            change_pct = 100 # Dari 0 jadi ada = Increasing
            
        item = {
            "block_code": block_code,
            "val": round(change_pct, 1),
            "desc": f"{y23:.1f} ➝ {y25:.1f} T/Ha"
        }
        
        if change_pct < -5:
            categories["declining"].append(item)
            # Hitung stats untuk declining
            summary_stats["declining"]["avg_prod_2023"] += y23
            summary_stats["declining"]["avg_prod_2025"] += y25
            summary_stats["declining"]["total_area"] += luas
            summary_stats["declining"]["avg_change"] += change_pct
        elif change_pct > 5:
            categories["increasing"].append(item)
        else:
            categories["stable"].append(item)

    # Finalize Stats
    decl_count = len(categories["declining"])
    if decl_count > 0:
        summary_stats["declining"]["avg_prod_2023"] = round(summary_stats["declining"]["avg_prod_2023"] / decl_count, 1)
        summary_stats["declining"]["avg_prod_2025"] = round(summary_stats["declining"]["avg_prod_2025"] / decl_count, 1)
        summary_stats["declining"]["avg_change"] = round(summary_stats["declining"]["avg_change"] / decl_count, 1)
        summary_stats["declining"]["total_area"] = round(summary_stats["declining"]["total_area"], 1)
    
    summary_stats["declining"]["count"] = decl_count
    summary_stats["stable"]["count"] = len(categories["stable"])
    summary_stats["increasing"]["count"] = len(categories["increasing"])
    summary_stats["tbm"]["count"] = len(categories["tbm"])
    summary_stats["empty"]["count"] = len(categories["empty"])
    summary_stats["empty"]["total_area"] = round(summary_stats["empty"]["total_area"], 1)

    print(f"Empty Blocks Found: {summary_stats['empty']['count']}")

    # Save output
    output_data = {
        "categories": categories,
        "summary": summary_stats
    }
    
    with open(r'data\output\block_breakdown_v2.json', 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print("Done. Saved to block_breakdown_v2.json")

except Exception as e:
    print(f"Error: {e}")
