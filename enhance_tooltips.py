
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Pola lama yang ingin diganti
# <span class="text-slate-500 text-[10px]">ⓘ</span>
old_pattern = r'<span class="text-slate-500 text-\[10px\]">ⓘ</span>'

# Desain Baru: Tombol bulat modern
# Flex container, rounded full, cyan color theme, hover effects
new_icon = (
    '<div class="w-5 h-5 flex items-center justify-center rounded-full '
    'bg-slate-700/80 text-cyan-400 text-xs font-bold font-serif italic '
    'border border-cyan-500/30 hover:bg-cyan-500 hover:text-white '
    'transition-all shadow-[0_0_5px_rgba(34,211,238,0.2)] select-none">i</div>'
)

# Replace untuk metrics di grid
html_updated = re.sub(old_pattern, new_icon, html)

# Khusus untuk Heading "Analisis Gap Yield" (mungkin stylingnya beda? text-slate-500 text-xs)
# <span class="text-slate-500 text-xs">ⓘ</span>
old_pattern_xs = r'<span class="text-slate-500 text-xs">ⓘ</span>'
html_updated = re.sub(old_pattern_xs, new_icon, html_updated)

# Data Infected Breakdown (Extra Fix if needed)
# ...

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_updated)

print(f"Berhasil mempercantik ikon tooltips di {html_path}")
