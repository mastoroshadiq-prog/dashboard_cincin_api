"""
Update DASHBOARD_DEMO_FEATURES.html with ALL 8 blocks content
"""

# Read sections
with open('paparan_section.html', 'r', encoding='utf-8') as f:
    paparan = f.read().strip()

with open('statistik_section.html', 'r', encoding='utf-8') as f:
    statistik = f.read().strip()

# Read current demo
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("Updating DASHBOARD_DEMO_FEATURES.html...")
print(f"Paparan HTML: {len(paparan)} chars")
print(f"Statistik HTML: {len(statistik)} chars")

# Replace PAPARAN section - add blocks list after summary
paparan_marker = '<div class="text-sm text-slate-400">Miliar</div>'
if paparan_marker in demo:
    # Insert blocks after the Miliar text
    insertion = f'''                    </div>
                    <div class="space-y-2 max-h-96 overflow-y-auto custom-scrollbar">
{paparan}
'''
    
    demo = demo.replace(
        paparan_marker + '\n                    </div>',
        paparan_marker + '\n' + insertion
    )
    print("✅ PAPARAN section updated")
else:
    print("⚠️  PAPARAN marker not found")

# Replace STATISTIK section - replace sample 2 blocks with all 8
old_stat = '''                    <div class="space-y-2">
                        <div class="bg-blue-900/40 p-3 rounded-xl border border-blue-500/30">
                            <div class="flex justify-between items-center">
                                <span class="text-white font-bold">Blok D003A</span>
                                <span class="text-blue-300">Rp 177 Jt</span>
                            </div>
                        </div>
                        <div class="bg-blue-900/40 p-3 rounded-xl border border-blue-500/30">
                            <div class="flex justify-between items-center">
                                <span class="text-white font-bold">Blok E002A</span>
                                <span class="text-blue-300">Rp 189 Jt</span>
                            </div>
                        </div>
                    </div>'''

new_stat = f'''                    <div class="space-y-2 max-h-96 overflow-y-auto custom-scrollbar">
{statistik}
                    </div>'''

if old_stat in demo:
    demo = demo.replace(old_stat, new_stat)
    print("✅ STATISTIK section updated")
else:
    print("⚠️  STATISTIK old pattern not found - trying alternative")
    # Try finding just the first block
    if 'Blok D003A' in demo:
        print("   Found sample blocks, manual replacement needed")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print("\n✅ File updated!")
print(f"   New size: {len(demo)} chars")
