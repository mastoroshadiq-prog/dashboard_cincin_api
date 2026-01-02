
import pandas as pd

# Constants
HARGA_TBS = 2500000  # Asumsi harga TBS per Ton (Rp 2.5 Juta/Ton) - Bisa disesuaikan
# Note: User mentioned Rp 1,500/kg previously, but 2.5jt is more current. Let's stick to 2.5jt for impact or use user's 1.5jt?
# User's doc said "Assuming FFB price Rp 1,500/kg". I will use 1,500,000 per Ton.
HARGA_TBS = 1500000 

def calculate_scenarios():
    # Data from previous extraction
    blocks = {
        'D006A': {
            'ha': 23.0, 'trees': 2382, 'sph': 104,
            'gap_ton_ha': 16.51, 'core': 37, 'ring': 80, 'suspect': 244
        },
        'D007A': {
            'ha': 24.7, 'trees': 2586, 'sph': 105,
            'gap_ton_ha': 17.23, 'core': 57, 'ring': 107, 'suspect': 200
        }
    }
    
    print("# ANALISIS SKENARIO DAMPAK & KERUGIAN TOTAL")
    print(f"*Basis Harga TBS: Rp {HARGA_TBS:,}/Ton*")
    
    total_loss_divisi = 0
    total_ha_divisi = 0
    
    for name, data in blocks.items():
        # Current Real Loss (Factual)
        loss_per_ha = data['gap_ton_ha'] * HARGA_TBS
        loss_total_block = loss_per_ha * data['ha']
        
        total_loss_divisi += loss_total_block
        total_ha_divisi += data['ha']
        
        # Scenario Logic regarding INFECTION SPREAD (Yearly Projection if untreated)
        # Conservative: Ring stays stable, only Core dies (Minim) - Focus on Prod Gap
        # Standard: Ring becomes Core (Active Spread)
        # Aggressive: Suspect becomes Ring, Ring becomes Core (Exponential)
        
        # Tree value estimate (Loss per tree if dead)
        # Potensi Yield per Ha / SPH = Kg/Tree
        # (17.3 Ton/Ha * 1000) / 104 = ~166 Kg/Tree/Year
        avg_yield_tree = ((data['gap_ton_ha'] + 0.5) * 1000) / data['sph'] # Raw approx
        val_per_tree = (avg_yield_tree / 1000) * HARGA_TBS
        
        cost_std = data['ring'] * val_per_tree
        cost_agg = (data['ring'] + data['suspect']) * val_per_tree
        
        print(f"\n## BLOK {name}")
        print(f"- **Luas**: {data['ha']} Ha")
        print(f"- **Gap Produktivitas**: {data['gap_ton_ha']} Ton/Ha")
        print(f"- **Total Kerugian Saat Ini (Block)**: **Rp {loss_total_block/1_000_000:,.1f} Juta/Tahun**")
        
        print(f"\n### Proyeksi Risiko Tambahan (Jika Tidak Ada Parit Isolasi):")
        print(f"1. **Skenario Konservatif (Status Quo)**")
        print(f"   - Asumsi: Hanya Core yang mati, Ring lambat menyebar.")
        print(f"   - Fokus: Memperbaiki kultur teknis pada gap produksi.")
        print(f"   - Relevansi: **WAJIB**. Gap 95% sudah menunjukkan kondisi kritis.")
        
        print(f"2. **Skenario Standar (Ring of Fire)**")
        print(f"   - Asumsi: {data['ring']} pohon di 'Cincin Api' tertular dalam 1 tahun.")
        print(f"   - Potensi Hilang Tambahan: Rp {cost_std/1_000_000:,.1f} Juta")
        print(f"   - Relevansi: **SANGAT KRUSIAL**. SPH {data['sph']} akan turun menjadi {data['sph'] - (data['ring']/data['ha']):.0f}.")
        
        print(f"3. **Skenario Agresif (Outbreak)**")
        print(f"   - Asumsi: Infeksi meluas ke zona Suspect ({data['suspect']} pohon).")
        print(f"   - Potensi Hilang Tambahan: Rp {cost_agg/1_000_000:,.1f} Juta")
        print(f"   - Relevansi: **KATROPIS**. Blok harus di-replanting total.")

    print(f"\n---\n## SUMMARY DIVISI (D006A + D007A)")
    print(f"- Total Luas Terdampak: {total_ha_divisi} Ha")
    print(f"- **TOTAL POTENSI UANG HILANG**: **Rp {total_loss_divisi/1_000_000_000:,.2f} Miliar / Tahun**")
    print("- *Angka ini memvalidasi investasi pembuatan parit isolasi yang biayanya jauh lebih rendah (est. Rp 50-100 Juta).*")

if __name__ == "__main__":
    calculate_scenarios()
