# RINGKASAN UPDATE: ESTATE RISK EXPOSURE
## Konsistensi 8 Blok CRITICAL & Bahasa Indonesia

---

## ✅ **YANG PERLU DIUPDATE**

### **1. Filter Watchlist: Hanya 8 Blok CRITICAL**

**Lokasi:** Function `renderRiskWatchlist()` di line 2085

**OLD (Tampilkan semua blok HIGH+CRITICAL):**
```javascript
const sorted = Object.entries(BLOCKS_DATA).sort((a, b) => a[1].rank - b[1].rank);
// ...
if (['CRITICAL', 'HIGH'].includes(data.severity)) {
    totalLoss += currentLoss;
    criticalCount++;
}
```

**NEW (Hanya CRITICAL):**
```javascript
const sorted = Object.entries(BLOCKS_DATA)
    .filter(([code, data]) => data.severity_hybrid === 'CRITICAL')
    .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));
// ...
// Semua di loop langsung dihitung (karena sudah filtered)
totalLoss += currentLoss;
criticalCount++;
```

---

### **2. Update Labels ke Bahasa Indonesia**

**Watchlist Labels:**
- "Est. Loss" → **"Est. Kerugian"**
- "Infection" → **"Infeksi"**
- "CRITICAL" badge → **"KRITIS"**

**Summary Labels:**
- "Critical Blocks" → **"Blok Kritis"**
- "Area at Risk" → **"Area Berisiko"**
- "Est. Total Loss" → **"Est. Total Kerugian"**

**Cost of Inaction Labels:**
- "Cost of Inaction" → **"Biaya Tidak Bertindak"**
- "Current Loss (Year 0)" → **"Kerugian Saat Ini (Tahun 0)"**
- "3-Year Projected Loss" → **"Proyeksi Kerugian 3 Tahun"**
- "Treatment Investment" → **"Investasi Treatment"**
- "Potential Savings" → **"Potensi Penghematan"**
- "Return on Investment" → **"Return on Investment (ROI)"**
- "Payback Period" → **"Periode Balik Modal"**
- "Action Window" → **"Jendela Aksi"**
- "Months before irreversible" → **"Bulan sebelum irreversible"**
- "Critical Blocks Require Immediate Attention" → **"Blok Kritis Memerlukan Perhatian Segera"**
- "Immediate Action Required" → **"Tindakan Segera Diperlukan"**
- "Treatment decision must be made within 30 days..." → **"Keputusan treatment harus diambil dalam 30 hari..."**

**Modal Popup Labels:**
- "Cost of Inaction Detail Analysis" → **"Analisis Detail Biaya Tidak Bertindak"**
- "Current Loss" → **"Kerugian Saat Ini"**
- "3-Year Total" → **"Total 3 Tahun"**
- "DEGRADATION TIMELINE (NO TREATMENT)" → **"TIMELINE DEGRADASI (TANPA TREATMENT)"**
- "Year 0 (Current)" → **"Tahun 0 (Saat Ini)"**
- "Year 1/2/3" → **"Tahun 1/2/3"**
- "Change" → **"Perubahan"**
- "Attack Rate" → **"Tingkat Infeksi"**
- "Yield Gap" → **"Gap Hasil"**
- "SPH (trees/ha)" → **"SPH (pohon/ha)"**
- "Loss (Juta)" → **"Kerugian (Juta)"**
- "IMPACT OF TREATMENT" → **"DAMPAK TREATMENT"**
- "Prevented Loss (70% eff)" → **"Kerugian yang Dicegah (70% efektif)"**
- "Net Benefit" → **"Manfaat Bersih"**

---

## 📊 **EXPECTED RESULT**

### **ESTATE RISK EXPOSURE - Watchlist:**
```
╔═══════════════════════════════════════════════════════════╗
║  PAPARAN RISIKO ESTATE                                   ║
╠═══════════════════════════════════════════════════════════╣
║  Blok Kritis: 8                                          ║
║  Est. Total Kerugian: Rp 1.4 Miliar                      ║
║  Area Berisiko: ~175 Ha                                  ║
╠═══════════════════════════════════════════════════════════╣
║  📋 Daftar Blok (8 KRITIS):                             ║
║                                                           ║
║  ┌─ Blok D003A ──────────────────── [KRITIS] ─┐         ║
║  │ Est. Kerugian: Rp 177 Jt   Infeksi: 7.2%  │         ║
║  └──────────────────────────────────────────────┘         ║
║                                                           ║
║  ┌─ Blok D004A ──────────────────── [KRITIS] ─┐         ║
║  │ Est. Kerugian: Rp 146 Jt   Infeksi: 10.7% │         ║
║  └──────────────────────────────────────────────┘         ║
║                                                           ║
║  ... (6 more CRITICAL blocks)                            ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🔧 **MANUAL UPDATE INSTRUCTIONS**

Karena automated script gagal (whitespace issues), berikut manual steps:

### **Step 1: Buka File**
```
File: dashboard_cincin_api_INTERACTIVE_FULL.html
Lokasi: Line 2085-2151
```

### **Step 2: Find Function**
Search for: `function renderRiskWatchlist()`

### **Step 3: Replace Line 2087**
**OLD:**
```javascript
const sorted = Object.entries(BLOCKS_DATA).sort((a, b) => a[1].rank - b[1].rank);
```

**NEW:**
```javascript
const sorted = Object.entries(BLOCKS_DATA)
    .filter(([code, data]) => data.severity_hybrid === 'CRITICAL')
    .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));
```

### **Step 4: Remove Conditional Accumulation (Line 2106-2110)**
**DELETE:**
```javascript
if (['CRITICAL', 'HIGH'].includes(data.severity)) {
    totalLoss += currentLoss;
    criticalCount++;
    riskArea += data.luas_ha;
}
```

**REPLACE WITH:**
```javascript
// Accumulate (all items already filtered as CRITICAL)
totalLoss += currentLoss;
criticalCount++;
riskArea += data.luas_ha;
```

### **Step 5: Simplify Badge Color (Line 2113-2116)**
**DELETE:**
```javascript
let badgeColor = 'bg-slate-700 text-slate-300';
if (data.severity === 'CRITICAL') badgeColor = 'bg-rose-600 text-white animate-pulse';
if (data.severity === 'HIGH') badgeColor = 'bg-orange-600 text-white';
if (data.severity === 'MEDIUM') badgeColor = 'bg-yellow-500 text-black';
```

**REPLACE WITH:**
```javascript
// All items are CRITICAL (already filtered)
let badgeColor = 'bg-rose-600 text-white animate-pulse';
```

### **Step 6: Update Labels (Line 2123, 2127, 2131)**
**Line 2123:** `${data.severity}` → `KRITIS`
**Line 2127:** `Est. Loss` → `Est. Kerugian`
**Line 2131:** `Infection` → `Infeksi`

---

## ✅ **VERIFICATION CHECKLIST**

Setelah update, verify:

- [ ] ESTATE RISK EXPOSURE watchlist menampilkan **8 blok** (bukan 14)
- [ ] Semua badge menampilkan **"KRITIS"** (merah, animasi pulse)
- [ ] Total Loss Summary = **Rp ~1.4 Miliar** (dari 8 blok saja)
- [ ] Critical Count = **8**
- [ ] Labels: **"Est. Kerugian"**, **"Infeksi"**, **"Blok Kritis"**
- [ ] Konsisten dengan "Biaya Tidak Bertindak" component (juga 8 blok)

---

## 💡 **ALTERNATIVE: Quick Fix via Browser Console**

Jika tidak ingin edit HTML manual, bisa test via browser console:

```javascript
// Paste this in browser console (F12) saat dashboard terbuka
function renderRiskWatchlist() {
    const sorted = Object.entries(BLOCKS_DATA)
        .filter(([code, data]) => data.severity_hybrid === 'CRITICAL')
        .sort((a, b) => (b[1].risk_score || 0) - (a[1].risk_score || 0));

    let totalLoss = 0, criticalCount = 0, riskArea = 0, html = '';

    sorted.forEach(([code, data]) => {
        let currentLoss = data.loss_value_juta || 0;
        totalLoss += currentLoss;
        criticalCount++;
        riskArea += data.luas_ha;

        html += `<div onclick="updateBlockData('Left', '${code}')" class="bg-slate-800/40 p-3 rounded-lg border border-slate-700 hover:border-rose-500 cursor-pointer transition-all hover:bg-slate-800 group mb-2">
            <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-black text-white group-hover:text-rose-400 opacity-90">Blok ${code}</span>
                <span class="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-rose-600 text-white animate-pulse shadow-lg shadow-black/50">KRITIS</span>
            </div>
            <div class="flex justify-between items-end">
                <div>
                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Est. Kerugian</span>
                    <span class="text-sm font-bold text-rose-400">Rp ${Math.round(currentLoss).toLocaleString('id-ID')} Jt</span>
                </div>
                <div class="text-right">
                    <span class="text-[9px] text-slate-500 block uppercase font-bold">Infeksi</span>
                    <span class="text-xs font-bold text-white bg-white/10 px-1.5 rounded">${data.attack_rate}%</span>
                </div>
            </div>
        </div>`;
    });

    document.getElementById('riskWatchlistContainer').innerHTML = html;
    document.getElementById('summaryTotalLoss').textContent = (totalLoss / 1000).toFixed(1);
    document.getElementById('summaryCriticalCount').textContent = criticalCount;
    document.getElementById('summaryRiskArea').textContent = riskArea.toFixed(1);
}

// Run it
renderRiskWatchlist();
```

Ini akan instantly update watchlist tanpa perlu edit HTML!

---

**End of Document**
