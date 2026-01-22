"""Fix script tags properly"""
with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    c = f.read()

lines = c.split('\n')
print(f"Total lines: {len(lines)}")

# Keep lines 1-7 (index 0-6: DOCTYPE, html, head, meta, meta, title, (before script))
new_lines = lines[:7]

# Add clean script tags  
new_lines.append('    <script src="https://cdn.tailwindcss.com"></script>')
new_lines.append('    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>')

# Skip lines 8-81 (index 7-80) which are the bad script content
# Add from line 82 onward (index 81+)
new_lines.extend(lines[81:])

c = '\n'.join(new_lines)

with open(r'data\output\DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"Fixed! New size: {len(c)} bytes")
print(f"Removed {len(lines) - len(new_lines)} lines")
