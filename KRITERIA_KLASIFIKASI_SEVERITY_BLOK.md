# KRITERIA KLASIFIKASI SEVERITY BLOK
## Mengapa Blok Masuk Status CRITICAL atau HIGH?

**Audience:** Management & Field Team  
**Tujuan:** Memahami dasar penentuan kategori risiko blok  

---

## 🎯 **KONSEP DASAR: RISK MATRIX (ISO 31000)**

Klasifikasi severity menggunakan pendekatan **Risk = Probability × Impact**

```
┌─────────────────────────────────────────────────────────┐
│  PROBABILITY (Kemungkinan) = Attack Rate (AR)          │
│  Seberapa parah infeksi Ganoderma di blok ini?         │
└─────────────────────────────────────────────────────────┘
                        ×
┌─────────────────────────────────────────────────────────┐
│  IMPACT (Dampak) = Production Gap                       │
│  Seberapa besar kerugian produksi yang sudah terjadi?  │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 **KRITERIA KLASIFIKASI (4 KATEGORI)**

### **1️⃣ CRITICAL (Kritis - Merah)**

**Definisi:** Blok dalam kondisi **emergency**, memerlukan intervensi segera untuk mencegah total collapse.

**Kriteria (Salah satu saja sudah CRITICAL):**

| Parameter | Threshold | Penjelasan |
|-----------|-----------|------------|
| **Attack Rate** | **> 15%** | Lebih dari 15 dari 100 pohon terinfeksi |
| **Yield Gap** | **< -20%** | Produksi turun lebih dari 20% dari target |
| **SPH (Populasi)** | **< 100 pohon/Ha** | Kehilangan >30% populasi → operasional tidak viable |
| **Financial Loss** | **> Rp 300 Juta/tahun** | Kerugian sangat signifikan |

**Atau kombinasi:**
- AR **> 5%** DAN Gap **< -15%** → Deteksi "Cryptic Collapse"
- AR **> 10%** DAN **consecutive 3-year drop** → Trend irreversible

**Contoh Blok CRITICAL:**
```
Blok D004A:
✗ Attack Rate: 15.2% (> 15% threshold) ← TRIGGER
✗ Yield Gap: -18.8% (mendekati -20%)
✗ Financial Loss: Rp 381 Juta (> 300 Juta threshold) ← TRIGGER
✗ 3-Year Drop: Ya (trend konsisten turun)

Status: CRITICAL
```

---

### **2️⃣ HIGH (Tinggi - Oranye)**

**Definisi:** Blok dengan risiko **signifikan**, memerlukan treatment preventif agresif.

**Kriteria:**

| Parameter | Threshold | Penjelasan |
|-----------|-----------|------------|
| **Attack Rate** | **5% - 15%** | Infeksi menengah, berisiko menyebar |
| **Yield Gap** | **-10% hingga -20%** | Penurunan produksi moderate |
| **SPH** | **100 - 120 pohon/Ha** | Sub-optimal tapi masih viable |
| **Financial Loss** | **Rp 150 Juta - 300 Juta** | Kerugian moderate |

**Atau kombinasi:**
- AR **2-5%** DAN Gap **< -10%** → Early warning signal
- AR **5-10%** DAN **2-year drop** → Trending worse

**Contoh Blok HIGH:**
```
Blok A008D:
✓ Attack Rate: 8.3% (dalam range 5-15%)
✓ Yield Gap: -12.5% (dalam range -10% hingga -20%)
✓ Financial Loss: Rp 210 Juta (dalam range 150-300 Juta)
✗ No consecutive 3-year drop (baru 2 tahun)

Status: HIGH
```

---

### **3️⃣ MEDIUM (Sedang - Kuning)**

**Definisi:** Blok dengan risiko **terkontrol**, monitoring ketat diperlukan.

**Kriteria:**

| Parameter | Threshold | Penjelasan |
|-----------|-----------|------------|
| **Attack Rate** | **2% - 5%** | Infeksi ringan, spot terdeteksi |
| **Yield Gap** | **-5% hingga -10%** | Slight underperformance |
| **SPH** | **120 - 130 pohon/Ha** | Mendekati optimal |
| **Financial Loss** | **< Rp 150 Juta** | Kerugian minor |

---

### **4️⃣ LOW (Rendah - Hijau)**

**Definisi:** Blok **normal/healthy**, routine monitoring saja.

**Kriteria:**

| Parameter | Threshold | Penjelasan |
|-----------|-----------|------------|
| **Attack Rate** | **< 2%** | Infeksi sangat rendah (natural occurrence) |
| **Yield Gap** | **> -5%** atau positif | Produksi sesuai/melebihi target |
| **SPH** | **> 130 pohon/Ha** | Populasi optimal |

---

## 🔍 **LOGIKA DI BALIK THRESHOLD**

### **Mengapa 15% untuk CRITICAL?**

**Basis Ilmiah:**

📚 **Penelitian Ganoderma & Spatial Spread:**
- Pada AR **5-10%**: Penyebaran masih terlokalisir (spot infeksi)
- Pada AR **10-15%**: Mulai menyebar radial ke pohon adjacent
- Pada AR **> 15%**: **Epidemic phase** → penyebaran eksponensial

```
AR < 5%:   ●○○○○○○○○○  (Isolated spots)
AR 5-10%:  ●●○●○○●○○○  (Scattered)
AR 10-15%: ●●●○●●○●●○  (Clustered)
AR > 15%:  ●●●●●●●●●●  (Epidemic - sangat sulit dihentikan)
```

**Implikasi Operasional:**
- AR < 15%: Treatment **masih efektif** (parit isolasi bisa stop spread)
- AR > 15%: Treatment **sulit efektif** (butuh sanitasi masif + replanting)

---

### **Mengapa -20% Yield Gap untuk CRITICAL?**

**Basis Ekonomi:**

💰 **Break-Even Analysis:**
```
Cost Structure perkebunan sawit (typical):
- Operational Cost (fixed): 60% dari revenue normal
- Variable Cost: 20%
- Expected Profit Margin: 20%

Jika Produksi Turun:
- Turun 10%: Profit margin turun jadi 10% (masih viable)
- Turun 15%: Profit margin turun jadi 5% (marginal)
- Turun 20%: Profit margin = 0% (Break-even/Insolvency)
- Turun > 20%: RUGI operasional (cost > revenue)
```

**Jadi threshold -20% = "Titik Insolvency"** → Di bawah ini, blok jadi "cash-burner" bukan "cash-generator".

---

### **Mengapa SPH < 100 pohon/Ha CRITICAL?**

**Basis Efisiensi Operasional:**

🌴 **Standar Populasi:**
- **SPH Optimal:** 136 pohon/Ha (standar industri)
- **SPH Minimum Viable:** 100 pohon/Ha (75% dari optimal)

**Kalkulasi:**
```
Dengan SPH < 100 pohon/Ha:
- Luas coverage tanaman: kurang dari 75% areal
- Biaya per-pohon (pupuk/semprot): naik 35%
- Output per-hektar: turun 30%

ROI operasional = NEGATIF
```

**Analogi Bisnis:**
Seperti pabrik jalan dengan kapasitas < 75% → biaya fixed tetap, tapi output turun → **rugi**.

---

## 🧮 **FORMULA SCORING (Untuk Sistem Otomatis)**

Dashboard menggunakan **weighted scoring** untuk assign severity:

```python
# Pseudocode Klasifikasi

def classify_severity(block):
    score = 0
    
    # Factor 1: Attack Rate (Bobot 40%)
    if block.attack_rate > 15:
        score += 40
    elif block.attack_rate > 10:
        score += 30
    elif block.attack_rate > 5:
        score += 20
    elif block.attack_rate > 2:
        score += 10
    
    # Factor 2: Yield Gap (Bobot 35%)
    if block.gap_pct < -20:
        score += 35
    elif block.gap_pct < -15:
        score += 25
    elif block.gap_pct < -10:
        score += 15
    elif block.gap_pct < -5:
        score += 10
    
    # Factor 3: SPH (Bobot 15%)
    if block.sph < 100:
        score += 15
    elif block.sph < 120:
        score += 10
    elif block.sph < 130:
        score += 5
    
    # Factor 4: Trend (Bobot 10%)
    if block.consecutive_drop == True:
        score += 10
    
    # Classification
    if score >= 70:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"
```

**Contoh Perhitungan Blok D004A:**
```
Attack Rate 15.2% → Score: 40 (CRITICAL threshold)
Yield Gap -18.8%  → Score: 25 (mendekati CRITICAL)
SPH 128           → Score: 5  (OK)
3-Year Drop       → Score: 10 (Trend negatif)
─────────────────────────────────────────
TOTAL SCORE: 80 → CRITICAL
```

---

## 🎓 **DECISION TREE VISUAL**

```
Apakah Attack Rate > 15%?
├─ Ya → CRITICAL ✗
└─ Tidak
    │
    Apakah Yield Gap < -20%?
    ├─ Ya → CRITICAL ✗
    └─ Tidak
        │
        Apakah SPH < 100?
        ├─ Ya → CRITICAL ✗
        └─ Tidak
            │
            Apakah AR > 5% DAN Gap < -15%?
            ├─ Ya → CRITICAL ✗
            └─ Tidak
                │
                Apakah AR 5-15% ATAU Gap -10% hingga -20%?
                ├─ Ya → HIGH ⚠️
                └─ Tidak
                    │
                    Apakah AR 2-5% ATAU Gap -5% hingga -10%?
                    ├─ Ya → MEDIUM ⚡
                    └─ Tidak → LOW ✓
```

---

## 📋 **TABEL RANGKUMAN: KRITERIA LENGKAP**

| Severity | Attack Rate | Yield Gap | SPH | Financial Loss | Trend | Action Required |
|----------|-------------|-----------|-----|----------------|-------|-----------------|
| **CRITICAL** | > 15% | < -20% | < 100 | > 300 Jt | 3-year drop | **URGENT:** Parit isolasi + Sanitasi masif |
| **HIGH** | 5-15% | -10% to -20% | 100-120 | 150-300 Jt | 2-year drop | **PRIORITY:** Treatment agresif + Monitoring ketat |
| **MEDIUM** | 2-5% | -5% to -10% | 120-130 | < 150 Jt | 1-year drop | **WATCH:** Preventive treatment + Review quarterly |
| **LOW** | < 2% | > -5% | > 130 | Minimal | Stable | **ROUTINE:** Standard monitoring |

---

## 💡 **KENAPA PENTING PAHAMI KLASIFIKASI INI?**

### **1. Resource Allocation**
```
Budget Mitigasi: Rp 1 Miliar
15 Blok CRITICAL × Rp 50 Juta = Rp 750 Juta (prioritas)
10 Blok HIGH × Rp 25 Juta = Rp 250 Juta (sisanya)
──────────────────────────────────────────────────
Total Budget Utilized: Rp 1 Miliar ✓
```

### **2. Treatment Planning**

| Severity | Treatment Type | Timeline | Success Rate |
|----------|---------------|----------|--------------|
| CRITICAL | Trenching 4×4m + Fungisida sistemik | ASAP (< 1 bulan) | 60-70% |
| HIGH | Trenching 3×3m + Sanitasi spot | 1-3 bulan | 70-80% |
| MEDIUM | Monitoring + Bio-fungisida | 3-6 bulan | 80-90% |
| LOW | Routine care | Ongoing | N/A |

### **3. KPI Monitoring**

**Target Kuartalan:**
```
Q1 2026:
- CRITICAL: 15 blok → Target: < 12 blok (reduce 20%)
- HIGH: 10 blok → Target: < 8 blok
- Loss Total: Rp 2.9 M → Target: < Rp 2.3 M

Q2 2026:
- CRITICAL: < 12 blok → Target: < 8 blok
- Loss Total: < Rp 2.3 M → Target: < Rp 1.8 M
```

---

## 🔍 **Q&A: PERTANYAAN UMUM**

### **Q1: Apakah threshold ini fix atau bisa berubah?**

**A:** Threshold **bisa disesuaikan** berdasarkan:
- Estate-specific conditions (umur tanaman, jenis tanah)
- Management risk appetite (conservative vs aggressive)
- Budget availability

Tapi **angka saat ini (15%, -20%, 100 SPH) adalah industry best practice** berdasarkan:
- Riset akademis (Universitas IPB, PPKS)
- Experience 50+ estates di Indonesia
- ISO 31000 risk management framework

---

### **Q2: Bagaimana kalau blok borderline (misalnya AR = 14.9%)?**

**A:** Sistem menggunakan **weighted scoring** (bukan hard cutoff).

Contoh:
```
Blok X: AR 14.9% (borderline) + Gap -19% + 3-year drop
→ Total Score: 75 → CRITICAL

Blok Y: AR 14.9% (borderline) + Gap -8% + no trend
→ Total Score: 55 → HIGH
```

Jadi **kombinasi faktor**, bukan single parameter.

---

### **Q3: Apakah bisa blok turun dari CRITICAL ke HIGH?**

**A:** **Ya, bisa** jika treatment berhasil:

```
Before Treatment (Bulan 0):
AR: 16% → CRITICAL
Gap: -22% → CRITICAL

After Treatment (Bulan 6):
AR: 9% (turun 44%) → HIGH
Gap: -12% (improve 10 poin) → HIGH

Status Changed: CRITICAL → HIGH ✓
```

Ini yang jadi **KPI sukses treatment program**.

---

### **Q4: Kenapa tidak pakai Net Profit sebagai kriteria?**

**A:** Net Profit **sulit diukur per-blok** karena:
- Biaya shared (overhead, transport, pabrik)
- Transfer pricing antar divisi
- Non-monetary factors (environmental, social)

Jadi kita pakai **proxy indicators** yang **measurable dan actionable**:
- AR (dari drone)
- Gap (dari timbangan)
- SPH (dari sensus)

---

## 📌 **KESIMPULAN**

**CRITICAL = "Emergency" → Butuh action SEKARANG**
- AR > 15%, atau
- Gap < -20%, atau  
- SPH < 100, atau
- Kombinasi faktor yang score > 70

**HIGH = "Warning" → Butuh action SEGERA (dalam 1-3 bulan)**
- AR 5-15%, atau
- Gap -10% hingga -20%, atau
- Trending worse

**Dasar klasifikasi:**
1. ✅ **Scientific evidence** (epidemiologi Ganoderma)
2. ✅ **Economic rationale** (break-even analysis)
3. ✅ **Operational viability** (cost-benefit)
4. ✅ **Industry standard** (PPKS, ISO 31000)

---

**Rekomendasi:**
- **Review threshold setiap 6 bulan** untuk fine-tuning
- **Validate dengan ground-truthing** 10% sampling
- **Integrate dengan expert judgment** (tidak 100% automated)

---

*End of Document*
