"""Find modal HTML with avgChange_declining"""
c = open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8').read()

# Check if elements exist
elements = ['avgChange_declining', 'avgProd2023_declining', 'avgProd2025_declining', 'totalArea_declining',
            'avgAR_critical', 'avgSPH_critical', 'avgGap_critical', 'totalAreaRisk']

for el in elements:
    if f'id="{el}"' in c:
        print(f"✅ {el} found")
    else:
        print(f"❌ {el} NOT FOUND")

# Find modal HTML position
i = c.find('id="blockBreakdownModal"')
print(f"\nModal HTML at: {i}")
if i > 0:
    print(c[i:i+500])
