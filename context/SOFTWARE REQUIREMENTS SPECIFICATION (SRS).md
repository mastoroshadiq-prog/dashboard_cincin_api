# **SOFTWARE REQUIREMENTS SPECIFICATION (SRS)**

Project: POAC v3.3 \- Simulation Engine (Ring of Fire & Adaptive NDRE)  
Target: Python Developer Team  
Version: 1.0  
Status: DRAFT FOR EXECUTION

## **1\. PENDAHULUAN**

### **1.1 Tujuan**

Dokumen ini mendefinisikan spesifikasi teknis untuk **Engine Simulasi POAC**. Engine ini berfungsi sebagai alat bantu keputusan (*Decision Support Tool*) untuk mengkalibrasi parameter sensitivitas deteksi Ganoderma sebelum diterapkan ke sistem produksi (Backend utama).

### **1.2 Lingkup Masalah**

Sistem produksi saat ini menggunakan nilai NDRE absolut yang rentan terhadap bias lingkungan (cuaca/umur tanaman). Engine simulasi ini harus menerapkan pendekatan **Statistik Lokal (Z-Score)** dan **Geometri Heksagonal** untuk mensimulasikan dampak dari berbagai skenario kebijakan (Hemat vs Agresif).

### **1.3 Referensi Dokumen**

* technical\_blueprint\_poac\_v3.2.md (Arsitektur Umum)  
* BACKEND\_TUNABLE\_PARAMS\_V3.3.md (Parameter Variabel)  
* poac\_simulation\_tool.py (Prototipe Kode)

## **2\. SPESIFIKASI ALGORITMA (CORE LOGIC)**

Tim Python wajib mengimplementasikan 3 logika inti berikut dalam Engine Simulasi.

### **2.1 Logika A: Normalisasi Statistik (Adaptive Thresholding)**

Sistem tidak boleh menggunakan nilai mentah NDRE (Absolute Float).

* **Input:** Data Frame CSV (NDRE125, Blok).  
* **Proses:**  
  1. Grouping data per Blok.  
  2. Hitung Rata-rata ($\\mu$) dan Standar Deviasi ($\\sigma$) untuk blok tersebut.  
  3. Hitung Z-Score untuk setiap pohon:  
     $$Z \= \\frac{(NDRE\_{pohon} \- \\mu)}{\\sigma}$$  
* **Output:** Kolom baru Z\_Score (Float).

### **2.2 Logika B: Geometri Tetangga Heksagonal**

Perkebunan sawit menggunakan pola mata lima (segitiga). Logika grid kotak (Cartesian) **DILARANG** digunakan.

* **Aturan Offset Baris:**  
  * **Baris Ganjil (**$R\\%2 \\neq 0$**):** Tetangga berada di diagonal kiri/kanan normal.  
  * **Baris Genap (**$R\\%2 \== 0$**):** Tetangga bergeser (offset).  
* **Implementasi Referensi:** Lihat fungsi get\_hex\_neighbors(r, p).

### **2.3 Logika C: Pembentukan Cincin Api (Ring Detection)**

* **Trigger:** Pohon dengan status **G3** (berdasarkan ambang batas Z-Score).  
* **Proses:**  
  1. Ambil koordinat $(r, p)$ dari semua G3.  
  2. Cari 6 tetangga heksagonalnya.  
  3. Validasi Tetangga:  
     * Harus ada di database (bukan lahan kosong).  
     * Bukan pohon G3 itu sendiri.  
* **Output:** List unik pohon sehat yang menjadi kandidat "Cincin Api".

## **3\. PERSYARATAN FUNGSIONAL (FUNCTIONAL REQUIREMENTS \- FR)**

### **FR-01: Data Ingestion & Cleaning**

* **FR-01.1:** Sistem harus mampu membaca file format .csv.  
* **FR-01.2:** Sistem harus memvalidasi keberadaan kolom wajib: Blok, N\_BARIS, N\_POKOK, NDRE125.  
* **FR-01.3:** Data dengan koordinat null atau NDRE non-numerik harus dibuang (*dropped*) secara otomatis dengan logging peringatan.

### **FR-02: Scenario Runner (Multi-Scenario Simulation)**

Sistem harus mampu menjalankan simulasi berulang dengan parameter berbeda dalam satu kali eksekusi.

* **Parameter Input:** List of Dictionary berisi:  
  * Scenario Name (String)  
  * Z\_Threshold\_G3 (Float, misal: \-2.0)  
  * Z\_Threshold\_G2 (Float, misal: \-1.0)  
* **Proses:** Loop algoritma klasifikasi & deteksi cincin untuk setiap set parameter.

### **FR-03: Reporting & Visualization**

* **FR-03.1:** Output harus berupa Tabel Ringkasan (Pandas DataFrame) yang membandingkan setiap skenario.  
* **FR-03.2:** Metrik wajib dalam laporan:  
  * Jumlah G3 (Target Sanitasi).  
  * Jumlah Cincin Api (Target Proteksi).  
  * Total Intervensi (Beban Kerja Mandor).

## **4\. STRUKTUR KODE & IMPLEMENTASI**

Gunakan struktur modul Python berikut agar rapi dan *maintainable*.

poac\_sim/  
├── data/  
│   └── input/ (Tempat file tableNDRE.csv)  
├── src/  
│   ├── \_\_init\_\_.py  
│   ├── ingestion.py      \# FR-01: Load & Clean CSV  
│   ├── statistics.py     \# Logika A: Z-Score calc  
│   ├── spatial.py        \# Logika B: Hexagonal Neighbors  
│   └── engine.py         \# FR-02: Main Simulation Loop  
├── main.py               \# Entry point  
└── config.py             \# Definisi Skenario (Hemat, Seimbang, Perang)

## **5\. PARAMETER KONFIGURASI (TUNABLE VARIABLES)**

Berikut adalah nilai standar yang harus digunakan sebagai *default* dalam config.py.

| Parameter | Tipe | Default | Deskripsi |
| :---- | :---- | :---- | :---- |
| **Skenario 1 (Hemat)** | Dict | G3: \-2.5, G2: \-1.5 | Hanya deteksi outlier ekstrem. |
| **Skenario 2 (Seimbang)** | Dict | G3: \-2.0, G2: \-1.0 | **Rekomendasi Baseline**. Sesuai standar statistik (2.5% tail). |
| **Skenario 3 (Perang)** | Dict | G3: \-1.5, G2: \-0.5 | Sangat sensitif. Proteksi maksimum. |

## **6\. ACCEPTANCE CRITERIA (Definisi Selesai)**

Pekerjaan Tim Python dianggap selesai jika:

1. Script dapat berjalan tanpa error membaca tableNDRE.csv.  
2. Hasil output konsisten (deterministik) untuk input data yang sama.  
3. Perubahan nilai Z\_Threshold pada config langsung mengubah jumlah output "Cincin Api" secara logis (makin rendah threshold, makin banyak cincin).