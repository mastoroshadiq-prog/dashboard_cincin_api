
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Pola yang dicari:
# text-[10px] text-slate-300
original_text_class = r'text-\[10px\] text-slate-300'

# Pengganti:
# text-xs (12px) text-slate-200 (lebih terang sedikit) + leading-relaxed untuk spasi baris
new_text_class = 'text-xs text-slate-200 leading-relaxed font-medium'

updated_html = re.sub(original_text_class, new_text_class, html)

# Juga perlebar kotak tooltip dari w-48/w-56 menjadi w-64 (lebih lebar)
# class="... w-48 p-2 ..." -> w-64 p-3
updated_html = re.sub(r'w-48 p-2', 'w-64 p-3 shadow-2xl', updated_html)
updated_html = re.sub(r'w-56 p-2', 'w-72 p-3 shadow-2xl', updated_html) # w-56 jadi w-72
updated_html = re.sub(r'w-60 p-2', 'w-72 p-3 shadow-2xl', updated_html) # w-60 jadi w-72

# Khusus Gap Yield yang text-xs tapi mungkin mau dibuat sm?
# Biarkan dulu xs, karena xs sudah 20% lebih besar dari 10px.

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Berhasil memperbesar teks dan ukuran kotak tooltips.")
