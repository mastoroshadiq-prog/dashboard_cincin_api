"""Add Yield 2024 element to block detail panel"""
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the Yield 2023 div and add 2024 after it
# Look for pattern around Yield 2023
search = 'Yield 2023</div>'
i = c.find(search)
if i > 0:
    # Find the closing </div> of the whole section (after detailYield2023)
    j = c.find('</div>', i + len(search) + 50)  # After detailYield2023 div
    k = c.find('</div>', j + 6)  # The container div
    
    # Insert Yield 2024 after the Yield 2023 container
    yield_2024_html = '''
                        <div class="bg-black/30 rounded-lg p-3 border border-slate-700">
                            <div class="text-xs text-slate-400">Yield 2024</div>
                            <div class="text-xl font-bold text-blue-400" id="detailYield2024">- T/Ha</div>
                        </div>'''
    
    c = c[:k+6] + yield_2024_html + c[k+6:]
    print("✅ Added Yield 2024 HTML element")
else:
    print("⚠️ Yield 2023 not found")

# Write back
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f"File saved: {len(c)} bytes")
