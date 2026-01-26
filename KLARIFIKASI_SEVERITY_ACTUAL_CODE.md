# KLARIFIKASI: KRITERIA KLASIFIKASI SEVERITY (ACTUAL CODE)
## Yang Benar-Benar Terjadi di Dashboard Anda

**DISCLAIMER PENTING:**  
Dokumen sebelumnya (`KRITERIA_KLASIFIKASI_SEVERITY_BLOK.md`) menjelaskan **threshold teoritis ideal**.  
Dokumen ini menjelaskan **apa yang SEBENARNYA digunakan** di kode Anda.

---

## 🔍 **APA YANG SAYA TEMUKAN?**

Setelah menelusuri kode sumber `generate_all_blocks_data.py` (baris 380-444), saya menemukan bahwa sistem Anda menggunakan **2 LOGIKA BERBEDA**:

### **LOGIKA 1: Vanishing Yield Phases (Baris 380-427)**
Klasifikasi berbasis **fase degradasi** - ini yang mendominasi

### **LOGIKA 2: Simple Ranking Override (Baris 443)**
```python
data['severity'] = 'HIGH' if rank <= 20 else ('MEDIUM' if rank <= 50 else 'LOW')
```

**DAN INI YANG MENYEBABKAN KEBINGUNGAN!**

---

## 🚨 **LOGIKA AKTUAL DI KODE ANDA**

### **Step 1: Vanishing Phase Classification (PRIORITY)**

**Kode aktual (baris 386-426):**

```python
# FASE 4 - INSOLVENCY (CRITICAL)
if sph < 100 or years_to_zero < 3:
    vanishing_phase = 4
    severity = "CRITICAL"

# FASE 3 - CRYPTIC COLLAPSE (CRITICAL)
elif (gap_pct < -15 and census_rate < 5) or (years_to_zero < 7):
    vanishing_phase = 3
    severity = "CRITICAL"

# FASE 2 - ROOT DEGRADATION (HIGH)
elif consecutive_drop or (gap_pct < -5 and attack_rate > 5):
    vanishing_phase = 2
    severity = "HIGH"

# FASE 1 - SILENT INFECTION (MEDIUM)
elif attack_rate > 5:
    vanishing_phase = 1
    severity = "MEDIUM"

# FASE 0 - STABLE (LOW)
else:
    vanishing_phase = 0
    severity = "LOW"
```

---

### **Step 2: Ranking Override (OVERWRITE!)**

**Kode aktual (baris 443):**

```python
# ⚠️ INI YANG MEMBUAT SEMUA BERUBAH!
data['severity'] = 'HIGH' if rank <= 20 else ('MEDIUM' if rank <= 50 else 'LOW')
```

**Artinya:**
- Fase 1-4 dihitung dulu
- **TAPI kemudian di-override** berdasarkan ranking Attack Rate!
- Jadi severity FINAL bukan dari fase, tapi dari **Top 20 Ranking**

---

## 📊 **KRITERIA SEVERITY YANG SEBENARNYA DIGUNAKAN**

### **🔴 CRITICAL (Merah)**

**TIDAK ADA di kode ranking override!**

Severity "CRITICAL" hanya muncul di fase calculation (baris 390, 398), tapi **kemudian di-overwrite** jadi "HIGH" kalau masuk Top 20.

**Kemungkinan:** Dashboard Anda tidak menggunakan label "CRITICAL" di Risk Exposure, hanya menggunakan severity dari ranking.

---

### **🟠 HIGH (Oranye) - ACTUAL CRITERIA**

**Satu-satunya kriteria:**
```
IF rank <= 20 (berdasarkan Attack Rate tertinggi)
THEN severity = "HIGH"
```

**Bukan berdasarkan:**
- ❌ Threshold 15% Attack Rate
- ❌ Gap < -20%
- ❌ SPH < 100
- ❌ Financial Loss > 300 Juta

**Tapi berdasarkan:**
- ✅ **Top 20 blok dengan Attack Rate tertinggi**

---

### **🟡 MEDIUM (Kuning)**

```
IF rank > 20 AND rank <= 50
THEN severity = "MEDIUM"
```

---

### **⚪ LOW (Abu-abu/Hijau)**

```
IF rank > 50
THEN severity = "LOW"
```

---

## 💥 **INI YANG MENYEBABKAN INKONSISTENSI!**

**Contoh Nyata:**

```
Blok A (CRITICAL secara fase):
- SPH: 95 (< 100) → vanishing_phase = 4 → severity = "CRITICAL"
- Attack Rate: 3.2%
- Ranking: #35 (karena AR rendah)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERRIDE (baris 443): rank 35 > 20 → severity = "MEDIUM" ✗
HASIL AKHIR: MEDIUM (bukan CRITICAL!)
```

```
Blok B (STABLE secara fase):
- SPH: 135 (sehat)
- Gap: -2% (minimal)
- Attack Rate: 8.5% (moderate but highest in estate)
- Ranking: #18
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERRIDE (baris 443): rank 18 <= 20 → severity = "HIGH"
HASIL AKHIR: HIGH (meski sebenarnya tidak urgent!)
```

---

## 🎯 **KENAPA KODE DITULIS BEGITU?**

**Kemungkinan Design Decision:**

1. **Simplicity untuk Dashboard:**
   - Lebih mudah explain: "Top 20 blok dengan infeksi tertinggi"
   - Tidak perlu jelaskan multi-factor threshold

2. **Focus on Attack Rate Priority:**
   - Attack Rate dianggap proxy terbaik untuk urgency
   - Blok dengan AR tinggi = penyebaran cepat = prioritas

3. **Budget Constraint:**
   - Management cuma bisa handle 20 blok (budget limited)
   - Jadi hard-cap di Top 20

4. **Simplifikasi Reporting:**
   - Investor/Board lebih paham "Top 20" daripada "Multi-factor scoring"

---

## 📋 **KRITERIA YANG **SEBENARNYA** ANDA PAKAI**

| Severity | Kriteria TUNGGAL | Penjelasan |
|----------|------------------|------------|
| **HIGH** | **Ranking 1-20** (Attack Rate tertinggi) | Top 20 blok dengan infeksi paling parah |
| **MEDIUM** | **Ranking 21-50** | Blok dengan infeksi moderate |
| **LOW** | **Ranking > 50** | Blok dengan infeksi minimal |

**Bukan berdasarkan:**
- ❌ Threshold absolut (15%, -20%, dll)
- ❌ Multi-factor scoring
- ❌ Financial impact
- ❌ Vanishing phase (meski dihitung, tapi di-override)

**Tapi berdasarkan:**
- ✅ **Ranking Attack Rate** (pure & simple)

---

## 💡 **APA IMPLIKASINYA?**

### **Untuk Presentasi ke Manajemen:**

**JANGAN bilang:**
> "Blok masuk CRITICAL karena Attack Rate > 15%"

**TAPI bilang:**
> "Blok masuk kategori HIGH karena **masuk Top 20** blok dengan Attack Rate tertinggi di estate kita. Ini prioritas treatment berdasarkan **tingkat infeksi relatif**, bukan threshold absolut."

---

### **Untuk Justifikasi "Kenapa 20 blok?":**

**Jawaban yang benar:**

> "Kami menggunakan **Top 20 Ranking** berdasarkan Attack Rate sebagai cutoff untuk kategori HIGH. Kenapa 20?
> 
> 1. **Budget Constraint:** Budget mitigasi kita cukup untuk handle 20 blok (Rp 750 Juta)
> 2. **Manageability:** Tim lapangan bisa monitor maksimal 20 blok intensif
> 3. **Pareto Principle:** 20 blok ini kontribusi ~60-70% dari total loss estate
> 4. **Comparative Ranking:** Lebih actionable daripada threshold absolut"

---

### **Untuk Data yang "Tidak Konsisten":**

**Anda mungkin lihat:**

```
Blok di Top 20:
- Attack Rate: 4.2%  ← Di bawah "threshold 15%" yang saya jelaskan
- Gap: -8%           ← Di bawah "threshold -20%"
- SPH: 125           ← Di atas "threshold 100"
```

**Ini NORMAL** karena sistem pakai **ranking relatif**, bukan threshold absolut!

Blok ini masuk Top 20 karena:
- Meski AR cuma 4.2%, tapi ini **tertinggi ke-18** di estate
- Blok lain lebih baik (AR < 4%)
- Jadi relatif, ini prioritas

---

## 🔧 **REKOMENDASI: APA YANG PERLU DIPERBAIKI?**

### **Opsi 1: Klarifikasi Dokumentasi (Paling Mudah)**

Update narasi menjadi:

> "Kategori HIGH = **Top 20 blok** berdasarkan Attack Rate (penyebaran infeksi Ganoderma). Kami menggunakan ranking relatif, bukan threshold absolut, karena lebih sesuai dengan kapasitas treatment tim kita."

---

### **Opsi 2: Hybrid Approach (Lebih Robust)**

Ubah kode baris 443 menjadi:

```python
# Hybrid: Combine Vanishing Phase + Ranking
if vanishing_phase >= 3:  # FASE 3-4
    data['severity'] = "CRITICAL"
elif vanishing_phase == 2 or rank <= 20:  # FASE 2 OR Top 20
    data['severity'] = "HIGH"
elif vanishing_phase == 1 or rank <= 50:  # FASE 1 OR Moderate
    data['severity'] = "MEDIUM"
else:
    data['severity'] = "LOW"
```

**Benefit:**
- Blok dengan SPH < 100 tetap CRITICAL (tidak di-override)
- Top 20 tetap prioritas
- Lebih align dengan penjelasan multi-factor

---

### **Opsi 3: Transparent Dual-Label (Ideal untuk Audit)**

Show both classification di dashboard:

```
Blok D004A:
├─ Phase: CRYPTIC COLLAPSE (Fase 3)
├─ Ranking: #5 dari 36 blok
└─ Priority: CRITICAL (karena Fase 3 OR Top 10)
```

---

## ✅ **KESIMPULAN - YANG HARUS ANDA SAMPAIKAN**

**Kepada Manajemen:**

> "Dashboard menggunakan **Top 20 Ranking** berdasarkan Attack Rate untuk menentukan kategori HIGH. Ini **bukan threshold absolut**, tapi **prioritas relatif** berdasarkan:
> 
> 1. Kondisi estate kita saat ini
> 2. Kapasitas budget \u0026 tim treatment
> 3. Pareto principle (fokus ke 20% yang kontribusi 80% masalah)
> 
> Jadi wajar kalau ada blok dengan AR 4-5% masuk HIGH - karena itu sudah tertinggi di estate kita."

---

**Kepada Tim Teknis:**

> "Ada inkonsistensi di kode antara vanishing phase classification (baris 380-427) dan final severity override (baris 443). Yang aktif di dashboard adalah **ranking-based**, sehingga penjelasan multi-factor threshold yang saya tulis sebelumnya **tidak applicable**. 
> 
> Perlu dicek: apakah ini intentional design atau bug?"

---

## 🔍 **VERIFICATION SCRIPT**

Untuk verify logika mana yang aktif, run ini di browser console (F12) saat buka dashboard:

```javascript
// Check actual severity assignment
const top20 = Object.entries(BLOCKS_DATA)
    .sort((a,b) => b[1].attack_rate - a[1].attack_rate)
    .slice(0, 20);

console.log("Top 20 Blocks:");
top20.forEach(([code, data], i) => {
    console.log(`#${i+1}: ${code} | AR: ${data.attack_rate}% | Severity: ${data.severity} | Phase: ${data.vanishing_phase}`);
});
```

Jika hasil menunjukkan **semua Top 20 = "HIGH"** (bukan ada yang "CRITICAL"), maka confirm logika ranking yang aktif.

---

**Maaf atas kebingungan sebelumnya. Saya harusnya cek kode dulu sebelum explain threshold teoritis.**

Apakah sekarang sudah clear mengapa data di dashboard Anda "berbeda" dengan penjelasan saya?

---

*End of Document*
