c = open('data/output/DASHBOARD_DEMO_FEATURES.html','r',encoding='utf-8').read()

# Find where attack rate is set in showBlockDetail
lines = c.split('\n')
for idx, line in enumerate(lines):
    if 'detailAttackRate' in line:
        print(f'Line {idx+1}: {line[:100]}')
        # Show context
        for j in range(max(0, idx-2), min(len(lines), idx+5)):
            print(f'  {j+1}: {lines[j][:90]}')
        print()
