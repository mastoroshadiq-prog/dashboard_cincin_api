# 🧠 Metodologi Ilmiah: Algoritma Cincin Api V8 (Hybrid Z-Score + Spatial)

Dokumen ini menjelaskan mengapa pendekatan **Hibrida (Hybrid Approach)** dipilih dibandingkan metode ambang batas statis (Konservatif/Standar/Agresif) untuk deteksi dini Ganoderma.

---

## 1. Mengapa Hibrida Lebih Realistis?

Pendekatan Tradisional (Konservatif/Standar/Agresif) menggunakan **Nilai Ambang Batas Tetap (Fixed Threshold)**. Contoh: *NDRE < 0.5 = Sakit*.

### ❌ Kelemahan Fatal Metode Tradisional:
1.  **Variabilitas Lahan:** Nilai NDRE 0.5 di tanah pasir mungkin "Sehat", tapi di tanah gambut "Sakit". Ambang batas kaku tidak bisa mengakomodasi perbedaan kesuburan tanah antar blok.
2.  **False Positives (Positif Palsu):** Gulma, pelepah kering, atau bayangan awan sering memiliki nilai NDRE rendah. Jika hanya melihat nilai pixel, ini dianggap sakit.
3.  **Gagal Deteksi Dini:** Jika ambang batas terlalu rendah (Konservatif), kita hanya mendeteksi pohon yang sudah mati (telat). Jika terlalu tinggi (Agresif), kita panik karena terlalu banyak "alarm palsu".

### ✅ Keunggulan Algoritma V8 (Hibrida):
1.  **Adaptif (Relatif):** Tidak peduli tanahnya subur atau tandus, algoritma mencari pohon yang **"Jauh Lebih Buruk dari Tetangganya"**. Ini membatalkan efek beda kesuburan tanah.
2.  **Biologis:** Ganoderma menular melalui kontak akar. Algoritma menolak "titik merah sendirian" (noise) dan hanya menerima **"Gerombolan Merah"** (Cluster) sebagai infeksi valid.

---

## 2. Bedah Komponen V8

### A. Z-Score (Statistical Anomaly Detection)
**"Seberapa aneh pohon ini dibanding rata-rata bloknya?"**

Rumus: `Z = (Nilai Pohon - Rata2 Blok) / Standar Deviasi`

*   **Z = 0**: Kondisi pohon sama persis dengan rata-rata kebun (Normal).
*   **Z = -1.5**: Pohon ini dalam kondisi **drop signifikan** dibanding lingkungannya.

**Insight:**
Dengan Z-Score, kita tidak perlu menebak angka NDRE "standar". Kita membiarkan data berbicara: *"Pohon ini nilainya anjlok drastis dibanding teman-temannya di blok yang sama."*

### B. Spatial Clustering (Biological Validation)
**"Apakah tetangganya juga sakit?"**

Penyakit Ganoderma bersifat **Soil-Borne** (tular tanah/akar). Polanya pasti **menggerombol (Clustered)**. Algoritma V8 menerapkan aturan ketat:

1.  **Rule 1 (The Core):** Cari pohon dengan Z-Score sangat rendah (< -1.5). Ini calon "Inti".
2.  **Rule 2 (The Neighborhood):** Cek 8 tetangga terdekatnya (Mata Lima). Apakah minimal 3 tetangga juga memiliki Z-Score rendah (< -1.0)?
    *   **YA:** Validasi! Ini adalah **Kluster Infeksi Aktif**.
    *   **TIDAK:** Abaikan. Ini hanya "Noise" (mungkin pohon kerdil, genangan air, atau kesalahan sensor).
3.  **Rule 3 (Ring of Fire):** Setelah Inti ditemukan, tandai pohon di sekeliling luarnya sebagai **Cincin Api (Oranye)**. Ini adalah zona di mana akar sehat sedang berkontak dengan akar sakit (Symptom Lag).

---

## 3. Kesimpulan: The "Symptom Lag" Insight

Kombinasi Z-Score + Spatial Clustering memungkinkan kita mendeteksi **Symptom Lag**:

*   **Z-Score** menangkap penurunan klorofil *mikro* yang belum terlihat mata manusia (daun masih hijau, tapi fotosintesis drop karena akar mulai busuk).
*   **Spatial** memastikan penurunan itu bukan eror, melainkan pola serangan sistematis.

Hasilnya:
> **Realistis & Actionable.** Kita tidak membuang biaya mitigasi untuk satu pohon yang sakit sendirian (mungkin tersambar petir), tapi kita fokus membendung **zona yang terbukti menular**.
