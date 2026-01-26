MISI: Integrasi Data Cost Control ke Dashboard Cincin Api
​1. Validasi Algoritma (Ground Truth Check)
​Input: Ambil data Historis Pkk.csv -> Kolom STADIUM 3&4.
​Aksi: Bandingkan dengan Peta Heatmap "Cincin Api" hasil olahan dronemu.
​Pertanyaan: "Apakah blok yang di Excel tercatat sakit parah, juga terlihat Merah di peta dronemu?"
​Jika Cocok: Algoritma valid.
​Jika Drone Merah tapi Excel Hijau: TEMUAN EMAS! Ini indikasi infeksi baru yang lolos dari sensus manual lama.
​Jika Drone Hijau tapi Excel Merah: Cek algoritma, mungkin sensitivitas terlalu rendah atau pohonnya sudah dibongkar.
​2. Pembersihan Bias Umur (Tanpa Tebak-tebakan)
​Input: File Arlt Counting ulang.csv.
​Aksi: Identifikasi blok mana yang persentase tanaman sisipannya (Total SISIP / TOTAL POKOK) signifikan (misal > 20%).
​Logika Baru: Untuk blok dengan sisipan tinggi, WAJIB gunakan logika "Split-Merge" (Ranking terpisah) yang lebih ketat. Jangan sampai tanaman muda dianggap sakit hanya karena NDRE-nya beda dengan pohon tua.
​3. Audit Aset (Ghost Tree Detection)
​Input: File Arlt.csv -> Kolom JUM POKOK (Data Buku).
​Aksi: Bandingkan dengan Total Count pohon yang terdeteksi Drone di blok tersebut.
​Output: Hitung selisihnya per blok.
​Data Buku 2.500 vs Drone Detect 2.300 = 200 Pohon Hilang (Ghost Trees).
​Ini data yang sangat disukai Wk. Direktur dan Finance. Ke mana perginya 200 pohon itu? (Mati/Tumbang tak terlapor).