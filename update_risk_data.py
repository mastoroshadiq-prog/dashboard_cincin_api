
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
json_path = r'data\output\risk_metrics_real.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    risk_data = json.load(f)

# Update variabel JS yang sudah ada
new_data_str = f"const RISK_METRICS_DATA = {json.dumps(risk_data)};"

# Regex untuk mencari deklarasi variabel yang sudah ada (termasuk isinya yang panjang)
# Hati-hati dengan karakter spesial di JSON.
# Kita cari pattern: const RISK_METRICS_DATA = \{.*?\}; (dotall)
# Tapi json dump bisa multilines atau one line.

# Cara paling aman: Cari start index dan end index dari brace penutup variabel.
start_marker = "const RISK_METRICS_DATA ="
start_idx = html_content.find(start_marker)

if start_idx != -1:
    # Cari posisi akhir variable (titik koma terdekat setelah kurung kurawal tutup??)
    # Ini riskan kalau logic parsing manual.
    # Kita asumsikan JSON valid dan balance braces? Susah.
    
    # Pendekatan string replace:
    # Kita cari string unik dari data lama? Tidak tahu data lama apa.
    
    # Pendekatan: Hapus variabel lama, insert yang baru.
    # Tapi kita harus tahu batasnya.
    
    # Kita coba regex simplifikasi: Variabel ini diinject tadi sebagai satu baris atau blok?
    # Tadi di inject_risk_fix.py:
    # risk_data_script = f"\n            const RISK_METRICS_DATA = {json.dumps(risk_data)};\n"
    
    # Jadi formatnya: newline + sapces + const ... = {...}; + newline
    # Kita replace dari "const RISK_METRICS_DATA =" sampai semicolon pertama yang ketemu di level root?
    
    # Alternatif: Replace file content menggunakan tool `replace_file_content` jika kita tahu barisnya.
    # Tapi baris bisa geser.
    
    # Regex non-greedy match sampai semicolon?
    # const RISK_METRICS_DATA = \{.*?\};
    # Tapi json bisa mengandung }; di dalam string.
    
    # Solusi Pragmatis:
    # Kita replace berdasarkan baris dimana marker ditemukan.
    # File JSON dump biasanya satu baris panjang jika tidak pakai indent=4, tapi tadi pakai indent=4.
    # "json.dump(risk_data, f, indent=4)" -> Multiline!
    
    # Jika Multiline, kita harus cari brace penutup yang balancing.
    
    count = 0
    found_start = False
    end_idx = -1
    
    # Cari kurung kurawal buka pertama setelah start_idx
    brace_start = html_content.find('{', start_idx)
    
    for i in range(brace_start, len(html_content)):
        if html_content[i] == '{':
            count += 1
        elif html_content[i] == '}':
            count -= 1
            if count == 0:
                end_idx = i + 1 # Include closing brace
                break
    
    if end_idx != -1:
        # Cek semicolon setelahnya
        if end_idx < len(html_content) and html_content[end_idx] == ';':
            end_idx += 1
            
        old_block = html_content[start_idx:end_idx]
        html_content = html_content.replace(old_block, new_data_str)
        print("Updated RISK_METRICS_DATA variable successfully.")
    else:
        print("Failed to parse existing JSON block.")

else:
    print("Variable RISK_METRICS_DATA not found. Cannot update.")
    
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
