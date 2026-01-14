"""
Make block lists clickable
"""

# Read sections
with open('paparan_section.html', 'r', encoding='utf-8') as f:
    paparan = f.read()

with open('statistik_section.html', 'r', encoding='utf-8') as f:
    statistik = f.read()

# Block codes
codes = ['D003A', 'D004A', 'D001A', 'E003A', 'E001A', 'E002A', 'F002A', 'F004A']

# Add onclick to each block in PAPARAN
for code in codes:
    # Find the div for this block
    old_pattern = f'''<div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>'''
    
    new_pattern = f'''<div class="bg-rose-900/40 p-3 rounded-xl border border-rose-500/30 hover:border-rose-400 transition-all cursor-pointer" onclick="openBlockModal('{code}')">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>'''
    
    paparan = paparan.replace(old_pattern, new_pattern)

# Add onclick to each block in STATISTIK
for code in codes:
    old_pattern = f'''<div class="bg-blue-900/40 p-3 rounded-xl border border-blue-500/30 hover:border-blue-400 transition-all cursor-pointer">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>'''
    
    new_pattern = f'''<div class="bg-blue-900/40 p-3 rounded-xl border border-blue-500/30 hover:border-blue-400 transition-all cursor-pointer" onclick="openBlockModal('{code}')">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-white font-bold">{code}</span>'''
    
    statistik = statistik.replace(old_pattern, new_pattern)

# Save
with open('paparan_section_clickable.html', 'w', encoding='utf-8') as f:
    f.write(paparan)

with open('statistik_section_clickable.html', 'w', encoding='utf-8') as f:
    f.write(statistik)

print("✅ Clickable block lists created!")
print("   - paparan_section_clickable.html")
print("   - statistik_section_clickable.html")
