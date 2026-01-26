
import html

target_file = r'data\output\DASHBOARD_DEMO_FEATURES.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Marker: Awal fungsi showBlockDetail
marker = "function showBlockDetail(blockCode) {"
log_marker = "console.log('[BLOCK DETAIL] Opening for:', blockCode);"

if marker in content:
    # Kita cari posisi setelah log marker agar aman
    idx = content.find(log_marker)
    if idx != -1:
        # Posisikan insertion point setelah baris log
        insertion_point = idx + len(log_marker)
        
        interceptor_code = """
                
                // --- TBM INTERCEPTOR V8 (AUTOMATIC REDIRECT) ---
                // Jika blok terdaftar di TBM Database, buka Popup TBM (Hijau)
                // alih-alih Popup Standar (Biru)
                if (typeof TBM_REAL_STATS !== 'undefined' && TBM_REAL_STATS[blockCode]) {
                     console.log('[TBM INTERCEPTOR] Redirecting to TBM Stats Modal for:', blockCode);
                     openTbmStatsModal(blockCode);
                     return;
                }
                // -----------------------------------------------
        """
        
        # Cek apakah interceptor sudah ada (untuk menghindari duplikasi)
        if "[TBM INTERCEPTOR]" in content:
            print("Interceptor TBM sepertinya sudah ada. Membatalkan injeksi untuk mencegah duplikasi.")
        else:
            new_content = content[:insertion_point] + interceptor_code + content[insertion_point:]
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Sukses menyisipkan TBM Interceptor ke showBlockDetail.")
    else:
        print("Marker console.log tidak ditemukan di dalam showBlockDetail.")
else:
    print("Fungsi showBlockDetail tidak ditemukan.")
