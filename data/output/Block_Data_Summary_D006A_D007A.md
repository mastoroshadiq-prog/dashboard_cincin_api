# Profil Detil Blok D006A & D007A
*Generated based on Consolidated POAC Simulation Data*

## 1. Ringkasan Agronomi (Agronomic Profile)

Data berikut diekstraksi dari laporan produktivitas (`Realisasi vs Potensi PT SR.xlsx`) dan analisis spasial NDRE terbaru.

### **BLOCK D006A**
| Parameter | Detail | Keterangan |
| :--- | :--- | :--- |
| **Tahun Tanam** | **2009** | Usia Tanaman: 16 Tahun (Mature) |
| **Luas Area** | **23.00 Ha** | Area Produktif |
| **Jumlah Pokok** | **2,382** | Total tanaman terdata |
| **Kerapatan (SPH)**| **104** | Stand Per Hectare (Low Density) |
| **Tanaman Pokok** | 2,382 | (Estimasi dari total populasi) |
| **Tanaman Sisip** | - | *Data spesifik sisip memerlukan verifikasi lapangan* |

### **BLOCK D007A**
| Parameter | Detail | Keterangan |
| :--- | :--- | :--- |
| **Tahun Tanam** | **2009** | Usia Tanaman: 16 Tahun (Mature) |
| **Luas Area** | **24.70 Ha** | Area Produktif |
| **Jumlah Pokok** | **2,586** | Total tanaman terdata |
| **Kerapatan (SPH)**| **105** | Stand Per Hectare (Low Density) |
| **Tanaman Pokok** | 2,586 | (Estimasi dari total populasi) |
| **Tanaman Sisip** | - | *Data spesifik sisip memerlukan verifikasi lapangan* |

---

## 2. Status Kesehatan & Cincin Api (Health Status)

Analisis menggunakan algoritma Cincin Api (Spatial Neighbors Analysis) pada data NDRE.

### **Distribusi Kesehatan**

| Kategori | D006A (Trees) | D006A (%) | D007A (Trees) | D007A (%) | Definisi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 **Core Infection** | **37** | 1.6% | **57** | 2.2% | Sumber infeksi utama (NDRE sangat rendah) |
| 🟠 **Ring of Fire** | **80** | 3.4% | **107** | 4.1% | Area penyebaran aktif di sekitar Core |
| 🟡 **At-Risk** | **244** | 10.2% | **200** | 7.7% | Pohon suspect di zona luar |
| 🟢 **Healthy** | **2,021** | 84.8% | **2,222** | 86.0% | Pohon sehat (NDRE normal) |
| **TOTAL** | **2,382** | 100% | **2,586** | 100% | |

---

## 3. Analisis Kesenjangan Produksi (Production Gap)

Dampak kesehatan tanaman terhadap realisasi panen dibandingkan potensi genetik.

### **BLOCK D006A**
*   **Current Yield**: 0.79 Ton/Ha
*   **Potential Yield**: 17.30 Ton/Ha
*   **GAP (Loss)**: **16.51 Ton/Ha** (-95.4%)
*   **Estimasi Kerugian**: Rp 24.8 Juta/Ha/Tahun

### **BLOCK D007A**
*   **Current Yield**: 0.30 Ton/Ha
*   **Potential Yield**: 17.53 Ton/Ha
*   **GAP (Loss)**: **17.23 Ton/Ha** (-98.3%)
*   **Estimasi Kerugian**: Rp 25.8 Juta/Ha/Tahun

---

## 4. Rekomendasi Tindakan (Action Plan)

Berdasarkan SPH rendah (~104-105) dan tingkat infeksi yang signifikan:

1.  **Isolation Trenching (Parit Isolasi)**:
    *   Prioritas uatama pada 37 titik Core (D006A) dan 57 titik Core (D007A).
    *   Isolasi harus mencakup zona "Ring of Fire" (Oranye) untuk mencegah penyebaran akar ke pohon sehat.

2.  **Sensus Pokok & Sisip**:
    *   Lakukan sensus fisik untuk memvalidasi data *Replanting/Sisip* yang saat ini belum terdata secara spesifik di sistem.
    *   SPH 104-105 mengindikasikan banyak ruang kosong (*blank spots*) atau kematian tanaman sebelumnya yang mungkin belum disisip.

3.  **Sanitasi**:
    *   Penebangan (chipping) pohon Core Infection untuk menghilangkan inokulum Ganoderma.
