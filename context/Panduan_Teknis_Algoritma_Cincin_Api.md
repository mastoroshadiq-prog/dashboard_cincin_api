# **PANDUAN TEKNIS: ALGORITMA "CINCIN API" & AUTO-TUNING SENSITIVITAS**

**Untuk:** Sdr. Toro (Lead Developer & Data Analyst) **Dari:** Project Owner **Tujuan:** Implementasi SQL untuk deteksi kluster Ganoderma menggunakan data NDRE tanpa kalibrasi papan.

## **1\. LATAR BELAKANG MASALAH & SOLUSI**

Kita memiliki data NDRE dari drone, namun karena belum menggunakan papan kalibrasi, nilai absolutnya bias (tergantung cuaca/jam terbang). Kita tidak bisa sekadar bilang "NDRE \< 0.4 \= Sakit".  
**Solusi Kita:** Menggunakan pendekatan **Statistik Relatif** dan **Analisis Spasial (Tetangga)**.

1. **Ranking Relatif:** Mencari pohon-pohon dengan nilai terendah *di dalam bloknya sendiri* (Normalisasi per Blok).  
2. **Klasterisasi:** Membedakan antara pohon sakit (membentuk pola/kluster) vs *noise* (error/kentosan yang sendirian).

## **2\. FILOSOFI DETEKSI POLA: 3 SKENARIO SIGNAL VS NOISE**

Dalam menentukan apakah sekumpulan pohon adalah "Sarang Ganoderma" (Signal) atau hanya kebetulan (Noise), kita menggunakan logika tetangga (Grid 3x3).  
**Pertanyaan:** Berapa jumlah tetangga sakit yang diperlukan untuk memvonis sebuah titik sebagai Kluster Merah?

### **Skenario A: Minimal 2 Tetangga Sakit (Threshold \> 1\)**

* **Kondisi:** Pusat \+ 2 Tetangga.  
* **Analisis:** Terlalu Sensitif. Dalam kebun yang kurang subur, probabilitas 2 pohon berdekatan memiliki nilai rendah secara acak cukup tinggi.  
* **Hasil:** Banyak **Positif Palsu (Noise)**. Kita akan membuang tenaga memvalidasi area yang sebenarnya bukan serangan aktif.

### **Skenario B: Minimal 4 Tetangga Sakit (Threshold \> 3\)**

* **Kondisi:** Pusat \+ 4 Tetangga (50% area sekitar).  
* **Analisis:** Terlalu Ketat. Ini hanya akan mendeteksi infeksi yang sudah sangat parah dan meluas melingkar.  
* **Hasil:** Banyak **Negatif Palsu (Lost Signal)**. Kita melewatkan kluster awal yang baru merambat ke satu arah (misal: sepanjang baris).

### **Skenario C: Minimal 3 Tetangga Sakit (Threshold \> 2\) \- PILIHAN KITA**

* **Kondisi:** Pusat \+ 3 Tetangga.  
* **Analisis:** Titik Keseimbangan (*Goldilocks Zone*). Secara statistik, probabilitas 3 tetangga sakit secara acak sangat kecil. Ini indikator kuat adanya faktor penularan lokal (akar).  
* **Hasil:** **Optimal**. Menangkap pola infeksi dini tanpa terlalu banyak *noise*.

## **3\. METODOLOGI "ELBOW METHOD" (AUTO-TUNING)**

Kita tidak tahu persis berapa % pohon yang sakit di sebuah blok. Apakah kita ambil 10% terbawah? Atau 20%?  
Kita gunakan **Elbow Method (Metode Siku)** otomatis:

1. **Simulasi:** Algoritma akan mencoba memotong data dari 5% terbawah hingga 30% terbawah (kelipatan 1%).  
2. **Ukur Efisiensi:** Di setiap level, kita hitung: *"Dari semua pohon yang kita curigai, berapa persen yang benar-benar membentuk Kluster Cincin Api?"*  
3. **Pilih Pemenang:** Titik di mana **Rasio Efisiensi Kluster** mencapai puncaknya adalah batas (threshold) terbaik untuk blok tersebut.

## **4\. IMPLEMENTASI KODE SQL (COMPLETE)**

Berikut adalah kode SQL lengkap. Kode ini dirancang untuk berjalan di database modern (PostgreSQL/SQL Server/MySQL 8.0+) yang mendukung *Window Functions* dan *CTE*.

### **A. Struktur Input (Asumsi Tabel raw\_drone\_data)**

* blok\_id (VARCHAR)  
* baris\_no (INT)  
* pokok\_no (INT)  
* ndre\_value (FLOAT)

### **B. Script Algoritma Utama (Auto-Elbow & Classification)**

`/* ALGORITMA CINCIN API v1.0`   
   `Fitur: Normalisasi Blok, Simulasi Sensitivitas, Auto-Elbow Detection`  
`*/`

`-- LANGKAH 1: NORMALISASI DATA (RANKING RELATIF)`  
`-- Memberikan nilai persentil (0.0 - 1.0) untuk setiap pohon relatif terhadap bloknya.`  
`WITH Data_Teranking AS (`  
    `SELECT`   
        `*,`  
        `-- Pohon NDRE terendah di blok dapat nilai 0.0, tertinggi 1.0`  
        `PERCENT_RANK() OVER (PARTITION BY blok_id ORDER BY ndre_value ASC) as ranking_persentil`  
    `FROM raw_drone_data`  
`),`

`-- LANGKAH 2: SKENARIO UJI COBA (SIMULASI 5% s/d 30%)`  
`-- Membuat daftar threshold yang akan diuji (0.05, 0.06, ... 0.30)`  
`Skenario_Uji AS (`  
    `-- Contoh sintaks PostgreSQL (Ganti dengan tabel bantu jika pakai MySQL lama)`  
    `SELECT generate_series(0.05, 0.30, 0.01) as batas_ambang`  
`),`

`-- LANGKAH 3: CEK TETANGGA MASSAL (INTI ALGORITMA)`  
`-- Menghitung jumlah tetangga sakit untuk setiap pohon di setiap skenario`  
`Analisis_Simulasi AS (`  
    `SELECT`   
        `S.batas_ambang,`  
        `Pusat.blok_id,`  
        `Pusat.baris_no,`  
        `Pusat.pokok_no,`  
        `-- Subquery untuk menghitung tetangga yang juga 'kuning' di level ambang ini`  
        `(`  
            `SELECT COUNT(*)`  
            `FROM Data_Teranking AS Tetangga`  
            `WHERE Tetangga.blok_id = Pusat.blok_id`  
              `-- Logika Spasial (Grid 3x3)`  
              `AND Tetangga.baris_no BETWEEN Pusat.baris_no - 1 AND Pusat.baris_no + 1`  
              `AND Tetangga.pokok_no BETWEEN Pusat.pokok_no - 1 AND Pusat.pokok_no + 1`  
              `AND NOT (Tetangga.baris_no = Pusat.baris_no AND Tetangga.pokok_no = Pusat.pokok_no)`  
              `-- Syarat Sakit: Tetangga juga harus masuk threshold ini`  
              `AND Tetangga.ranking_persentil <= S.batas_ambang`  
        `) as jumlah_tetangga_sakit`  
    `FROM Data_Teranking AS Pusat`  
    `CROSS JOIN Skenario_Uji AS S`  
    `WHERE Pusat.ranking_persentil <= S.batas_ambang -- Hanya analisis pohon suspect`  
`),`

`-- LANGKAH 4: MENGHITUNG EFISIENSI (MENCARI ELBOW)`  
`Statistik_Per_Level AS (`  
    `SELECT`   
        `batas_ambang,`  
        `COUNT(*) as total_suspect,`  
        `-- Berapa yang membentuk kluster (>2 tetangga)?`  
        `SUM(CASE WHEN jumlah_tetangga_sakit >= 3 THEN 1 ELSE 0 END) as kluster_valid,`  
        `-- Rasio Efisiensi = (Kluster Valid / Total Suspect) * 100`  
        `(CAST(SUM(CASE WHEN jumlah_tetangga_sakit >= 3 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 as rasio_efisiensi`  
    `FROM Analisis_Simulasi`  
    `GROUP BY batas_ambang`  
`),`

`-- LANGKAH 5: MEMILIH THRESHOLD PEMENANG (AUTO-TUNING)`  
`Threshold_Pemenang AS (`  
    `SELECT batas_ambang`  
    `FROM Statistik_Per_Level`  
    `-- Syarat: Minimal menemukan 10 pohon kluster (agar tidak bias data sedikit)`  
    `WHERE kluster_valid > 10`   
    `ORDER BY rasio_efisiensi DESC, batas_ambang ASC`  
    `LIMIT 1`  
`)`

`-- LANGKAH 6: HASIL FINAL (OUTPUT DASHBOARD)`  
`-- Menggunakan threshold pemenang untuk mengklasifikasikan data akhir`  
`SELECT`   
    `D.blok_id,`  
    `D.baris_no,`  
    `D.pokok_no,`  
    `D.ndre_value,`  
    `-- Hitung tetangga real-time berdasarkan threshold pemenang`  
    `(`  
        `SELECT COUNT(*)`  
        `FROM Data_Teranking T2`  
        `WHERE T2.blok_id = D.blok_id`  
          `AND T2.baris_no BETWEEN D.baris_no - 1 AND D.baris_no + 1`  
          `AND T2.pokok_no BETWEEN D.pokok_no - 1 AND D.pokok_no + 1`  
          `AND T2.ranking_persentil <= (SELECT batas_ambang FROM Threshold_Pemenang)`  
          `AND NOT (T2.baris_no = D.baris_no AND T2.pokok_no = D.pokok_no)`  
    `) as skor_kepadatan_kluster,`  
      
    `-- LABEL STATUS FINAL`  
    `CASE`   
        `-- Jika tidak masuk threshold pemenang = HIJAU`  
        `WHEN D.ranking_persentil > (SELECT batas_ambang FROM Threshold_Pemenang) THEN 'HIJAU (SEHAT)'`  
        `-- Jika masuk threshold, cek tetangganya`  
        `-- Skenario C: >2 Tetangga = MERAH`  
        `WHEN (SELECT COUNT(*) FROM Data_Teranking T2 WHERE ... ) >= 3 THEN 'MERAH (KLUSTER AKTIF)'`  
        `-- Noise: 0 Tetangga = ORANYE`  
        `WHEN (SELECT COUNT(*) FROM Data_Teranking T2 WHERE ... ) = 0 THEN 'ORANYE (NOISE/KENTOSAN)'`  
        `-- Sisanya = KUNING`  
        `ELSE 'KUNING (RISIKO TINGGI)'`  
    `END as status_risiko`  
      
`FROM Data_Teranking D;`

## **5\. INSTRUKSI VISUALISASI DASHBOARD**

Mas Toro, gunakan hasil query di atas untuk mengisi Dashboard:

1. **Peta Panas (Heatmap):** Tampilkan blok-blok kebun. Warna blok ditentukan oleh COUNT(Status \= 'MERAH').  
2. **Daftar Target (List):** Filter hasil query: WHERE status\_risiko \= 'MERAH'. Urutkan berdasarkan skor\_kepadatan\_kluster tertinggi (maks 8). Ini yang dikirim ke Mandor.  
3. **Filter Noise:** Jangan kirim status ORANYE (Noise/Kentosan) sebagai prioritas utama. Fokus pada MERAH dan KUNING.