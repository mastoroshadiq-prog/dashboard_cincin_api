"""
Verify all units are consistent in modals
"""
import re

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check modal section only (after line 3500)
lines = content.split('\n')
modal_section = '\n'.join(lines[3500:])

# Pattern: Number with comma followed by Juta
pattern = r'Rp\s+[\d,]+\s+Juta'
matches = re.findall(pattern, modal_section)

print("="*80)
print("VERIFICATION: Unit Consistency in Modals")
print("="*80)

print(f'\nRemaining "X,XXX Juta" patterns in modals: {len(matches)}')
if matches:
    unique = set(matches)
    for m in sorted(unique):
        print(f'  - {m}')
    print('\n⚠️  These might need to be Miliar if >= 1000')
else:
    print('✅ All comma-formatted numbers properly handled!')

# Check specific values
print("\nChecking critical values:")
critical_values = {
    '1.35': 'Miliar',
    '1.57': 'Miliar', 
    '1.97': 'Miliar',
    '3.13': 'Miliar',
    '6.2': 'Miliar',
    '6.67': 'Miliar',
    '4.3': 'Miliar',
    '3.94': 'Miliar',
    '1.86': 'Miliar',
}

issues = []
for val, expected_unit in critical_values.items():
    count_juta = modal_section.count(f'{val} Juta')
    count_miliar = modal_section.count(f'{val} Miliar')
    
    if count_juta > 0:
        issues.append(f'{val} Juta: {count_juta} times (should be {expected_unit})')
        print(f'  ⚠️  Rp {val} Juta: {count_juta} occurrences')
    elif count_miliar > 0:
        print(f'  ✅ Rp {val} Miliar: {count_miliar} occurrences')
    else:
        print(f'  ℹ️  Rp {val}: not found')

print("\n" + "="*80)
if issues:
    print(f"❌ FOUND {len(issues)} ISSUES - Need to fix!")
    for issue in issues:
        print(f"   - {issue}")
else:
    print("✅ ALL UNITS CONSISTENT!")
print("="*80)
