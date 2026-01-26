
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Cari blok RISK_METRICS_DATA
marker = "const RISK_METRICS_DATA ="
start = content.find(marker)

if start == -1:
    print("Variabel RISK_METRICS_DATA TIDAK DITEMUKAN!")
else:
    # Ambil snippet sekitar A012C setelah marker ini
    snippet = content[start:start+1000000] # Ambil cukup banyak
    
    # Cari A012C di snippet ini
    idx = snippet.find('"A012C": {')
    if idx == -1:
        print("A012C tidak ditemukan di dalam blok RISK_METRICS_DATA")
    else:
        # Tampilkan 5 baris data A012C
        data_block = snippet[idx:idx+200]
        print("Data A012C di HTML:")
        print(data_block)
