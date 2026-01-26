"""Find and add Yield 2024 HTML"""
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the yield section
i = c.find('id="detailYield2023"')
if i > 0:
    print("Found detailYield2023 at:", i)
    print(c[i-400:i+300])
else:
    print("detailYield2023 not found")
    # Search for any detail element
    i2 = c.find('detailYield')
    print("detailYield at:", i2)
