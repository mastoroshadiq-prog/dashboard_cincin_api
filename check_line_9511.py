"""
Quick HTML/JS syntax checker for line 9511 area
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check around line 9511
target_line = 9511 - 1  # 0-indexed

print("="*70)
print(f"Checking lines {target_line-5} to {target_line+5}")
print("="*70)

for i in range(max(0, target_line-10), min(len(lines), target_line+10)):
    line_num = i + 1
    line = lines[i].rstrip()
    marker = " ← LINE 9511" if line_num == 9511 else ""
    print(f"{line_num:5d}: {line}{marker}")

print("\n" + "="*70)
print("CHECKING FOR COMMON ISSUES:")
print("="*70)

# Check for unclosed template literals
template_start = 0
for i in range(max(0, target_line-50), min(len(lines), target_line+50)):
    line = lines[i]
    if '`' in line:
        count = line.count('`')
        print(f"Line {i+1}: Found {count} backtick(s): {line.strip()[:80]}")

# Check for script tag balance
script_opens = 0
script_closes = 0
for i in range(len(lines)):
    if '<script' in lines[i]:
        script_opens += 1
    if '</script>' in lines[i]:
        script_closes += 1

print(f"\n<script> tags: {script_opens} open, {script_closes} close")
if script_opens != script_closes:
    print("⚠️ WARNING: Unbalanced script tags!")

print("="*70)
