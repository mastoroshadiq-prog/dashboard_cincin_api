"""
Make INTERACTIVE_FULL truly comprehensive by:
1. Adding dropdown selector
2. Adding IDs to ALL key dynamic elements
3. Adding comprehensive JavaScript
"""

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🔧 Making INTERACTIVE_FULL comprehensive...")
print("="*70)

# Step 1: Add dropdown after header (before main content)
# Find the header section end
header_end = '<div class="max-w-7xl mx-auto space-y-6">'

if header_end in html:
    dropdown_html = '''
    <!-- INTERACTIVE BLOCK SELECTOR -->
    <div class="max-w-7xl mx-auto mb-6">
        <div class="bg-gradient-to-br from-indigo-900 to-blue-900 rounded-2xl p-6 border-2 border-indigo-500 shadow-2xl">
            <label for="blockSelector" class="block text-lg font-black uppercase mb-3 text-white">
                🎯 Interactive Block Selector - AME II Division
            </label>
            <select id="blockSelector" 
                    class="w-full bg-slate-800 border-2 border-indigo-400 rounded-xl p-4 text-white font-bold text-lg focus:outline-none focus:ring-4 focus:ring-indigo-500 transition-all">
                <option value="">-- Loading blocks data --</option>
            </select>
            <p class="text-xs text-white/60 mt-2 italic">
                Total: <span id="totalBlocks">36</span> blocks | Auto-selected highest attack rate
            </p>
        </div>
    </div>

    '''
    
    html = html.replace(header_end, dropdown_html + header_end)
    print("✅ Added dropdown selector")
else:
    print("⚠️  Header end not found")

# Step 2: Add flash animation CSS
css_insert_point = '</style>'
flash_css = '''
        @keyframes flashGreen {
            0%, 100% { background-color: transparent; }
            50% { background-color: #10b981; color: white; }
        }
        .flash-update {
            animation: flashGreen 0.6s ease-in-out;
        }
    </style>'''

html = html.replace(css_insert_point, flash_css)
print("✅ Added flash animation CSS")

# Step 3: Add comprehensive IDs to key elements
# We'll add IDs to the most important sections

id_replacements = [
    # Header updates
    ('Blok F008A & D001A<', 'Blok <span id="headerBlockCode">F008A & D001A</span><'),
    
    # Detail Blok F008A header
    ('Detail Blok F008A (29.6 Ha)<', '<span id="blockDetailHeader">Detail Blok F008A (29.6 Ha)</span><'),
    
    # Status badge
    ('Darurat</', '<span id="statusText">Darurat</span></'),
    
    # TT and Age  
    ('>2008 (18 Tahun)<', ' id="blockTT">2008 (18 Tahun)<'),
    
    # SPH
    ('>127 Pokok/Ha<', ' id="blockSPH">127 Pokok/Ha<'),
    
    # Total Pohon
    ('>3,745 <span', ' id="blockTotalPohon">3,745 <span'),
    
    # Sisip
    ('>142 <span class="text-xs uppercase">PKK<', ' id="blockSisip">142 <span class="text-xs uppercase">PKK<'),
    
    # Merah count
    ('>90 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockMerahCount">90 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
    
    # Oranye count
    ('>369 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockOranyeCount">369 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
    
    # Kuning count  
    ('>141 <span\n                                            class="text-[10px] uppercase text-black">PKK<', ' id="blockKuningCount">141 <span\n                                            class="text-[10px] uppercase text-black">PKK<'),
]

count = 0
for old, new in id_replacements:
    if old in html:
        html = html.replace(old, new, 1)  # Only first occurrence
        count += 1

print(f"✅ Added {count} IDs to key elements")

# Save intermediate
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Step 1 complete - Structure ready")
print("Next: Will add comprehensive JavaScript...")
