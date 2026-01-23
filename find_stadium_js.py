c = open('data/output/DASHBOARD_DEMO_FEATURES.html','r',encoding='utf-8').read()
i = c.find("getElementById('detailStadium')")
print('detailStadium JS found at:', i if i > 0 else 'Not found')

# Also search for stadium in JS
lines = c.split('\n')
for idx, line in enumerate(lines):
    if 'detailStadium' in line and 'getElementById' in line:
        print(f'Line {idx+1}: {line[:100]}')
