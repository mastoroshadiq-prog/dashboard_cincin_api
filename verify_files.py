import os

files = [
    'dashboard-cincin-api/data/output/DASHBOARD_DEMO_FEATURES.html',
    'dashboard-cincin-api/data/output/DASHBOARD_CLEAN_v2.html', 
    'dashboard-cincin-api/data/output/DASHBOARD_FIXED_FINAL.html'
]

print('FILE VERIFICATION')
print('=' * 80)

for filepath in files:
    if not os.path.exists(filepath):
        print(f'MISSING: {filepath}')
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    size = len(content)
    has_breakdown = 'blockBreakdownModal' in content
    has_paparan = 'paparanRisikoModal' in content
    has_closing = content.rstrip().endswith('</html>')
    has_null_check = 'const subtitleEl = document.getElementById' in content
    
    status = 'COMPLETE' if all([has_breakdown, has_paparan, has_closing, has_null_check]) else 'INCOMPLETE'
    
    print(f'\n{os.path.basename(filepath)}:')
    print(f'  Size: {size:,} bytes')
    print(f'  Block Breakdown Modal: {"YES" if has_breakdown else "NO"}')
    print(f'  Paparan Risiko Modal: {"YES" if has_paparan else "NO"}')
    print(f'  Closing tags: {"YES" if has_closing else "NO"}')
    print(f'  Null safety: {"YES" if has_null_check else "NO"}')
    print(f'  --> {status}')

print('\n' + '=' * 80)
print('WHICH FILE ARE YOU OPENING IN BROWSER?')
print('Please verify you are opening: DASHBOARD_DEMO_FEATURES.html')
