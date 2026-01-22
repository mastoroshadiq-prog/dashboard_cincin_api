"""Find blockBreakdownModal HTML structure"""
content = open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8').read()
lines = content.split('\n')

# Find line with blockBreakdownModal
for i, line in enumerate(lines):
    if 'blockBreakdownModal' in line and 'id=' in line:
        print(f"Line {i+1}: {line[:200]}")
        # Print surrounding context
        for j in range(max(0, i-2), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j][:150]}")
        break
else:
    print("Modal HTML ID not found")
    # Check if it's referenced in JS
    for i, line in enumerate(lines):
        if 'blockBreakdownModal' in line:
            print(f"Line {i+1} (JS ref): {line[:150]}")
            break
