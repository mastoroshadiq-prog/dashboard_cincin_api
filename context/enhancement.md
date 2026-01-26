QUERY 1 (Cari Merah):Filter pohon yang NDRE_Rendah DAN Jumlah_Tetangga_Sakit >= 3.$\rightarrow$ Output: 500 Pohon. (Kirim ke Tim Sanitasi / Butuh Asap Cair).

QUERY 2 (Cari Oranye):Cari pohon yang Bukan Merah TAPI Jaraknya = 1 dari pohon Merah.$\rightarrow$ Output: 3.000 Pohon. (Kirim ke Tim APH / Butuh Trichoderma).

Kesimpulan:

1. Merah didapat dari Analisis Pola Data.
2. Oranye didapat dari Posisi Fisik terhadap Merah.

Tujuan: Mengambil data pohon sehat/ringan yang "sial" karena bertetangga dengan pohon Merah, untuk target prioritas APH.

Penjelasan :
1. CTE Daftar_Merah: Ini mengunci target untuk Tim Sanitasi (Opsi B).

2. CTE Daftar_Oranye: Ini adalah logika kuncinya.

Ia mencari semua pohon yang menempel pada Daftar_Merah.
PENTING: Ia memfilter keluar pohon yang sudah Merah (NOT IN Daftar_Merah). Jadi kita tidak menyiram APH ke pohon yang mau ditebang.

Output Akhir: Sebuah tabel ringkas yang langsung memberi angka liter untuk proposal Bapak.

Dengan tambahan skrip ini "Berapa liter Asap Cair dan berapa liter Trichoderma yang harus saya setujui hari ini?" dengan data presisi, bukan kira-kira.

/*
   BAGIAN 2: EKSTRAKSI TARGET LOGISTIK (MEMISAHKAN MERAH & ORANYE)
   Prasyarat: Jalankan dulu Query 'Analisis_Kluster' (dari file sebelumnya)
   dan simpan hasilnya dalam tabel sementara atau CTE bernama 'Hasil_Deteksi'.
*/

-- LANGKAH 1: ISOLASI DULU SIAPA 'SI MERAH' (SUMBER MASALAH)
WITH Daftar_Merah AS (
    SELECT id_pohon, kode_blok, no_baris, no_pokok
    FROM Hasil_Deteksi
    -- Definisi Merah: Pohon Suspect yang punya >= 3 tetangga sakit
    WHERE status_risiko_final LIKE '%MERAH%' 
),

-- LANGKAH 2: CARI TETANGGANYA (CINCIN API)
Daftar_Oranye AS (
    SELECT DISTINCT
        T.id_pohon,
        T.kode_blok,
        T.no_baris,
        T.no_pokok
    FROM Tabel_Data_Drone AS T
    JOIN Daftar_Merah AS M
        ON T.kode_blok = M.kode_blok
        -- Logika Jarak: Tetangga adalah yang selisih baris/pokok maks 1
        AND T.no_baris BETWEEN M.no_baris - 1 AND M.no_baris + 1
        AND T.no_pokok BETWEEN M.no_pokok - 1 AND M.no_pokok + 1
    WHERE 
        T.id_pohon <> M.id_pohon -- Bukan si Merah itu sendiri
        AND T.id_pohon NOT IN (SELECT id_pohon FROM Daftar_Merah) -- Dan bukan pohon Merah lain
)

-- LANGKAH 3: LAPORAN AKHIR UNTUK PROPOSAL LOGISTIK
-- A. KEBUTUHAN SANITASI (ASAP CAIR)
SELECT 
    'PAKET SANITASI (MERAH)' as kategori,
    COUNT(*) as jumlah_pohon,
    COUNT(*) * 3 as estimasi_liter_asap_cair -- Asumsi 3 Liter/Pohon
FROM Daftar_Merah

UNION ALL

-- B. KEBUTUHAN PROTEKSI (APH/TRICHODERMA)
SELECT 
    'PAKET PROTEKSI (ORANYE)',
    COUNT(*),
    COUNT(*) * 2 as estimasi_liter_aph -- Asumsi 2 Liter/Pohon
FROM Daftar_Oranye;