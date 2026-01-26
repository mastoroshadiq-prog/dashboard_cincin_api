"""Find modal structure in Dashboard"""
content = open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8').read()

# Find various patterns
patterns = [
    'TREN PRODUKSI PER BLOK',
    'Block Breakdown',
    'categoryDistributionChart',
    'Blok dengan Penurunan',
    'DECLINING',
]

for p in patterns:
    idx = content.find(p)
    print(f"\n'{p}' at: {idx}")
    if idx > 0:
        print(content[max(0, idx-100):idx+200])
        print("---")
