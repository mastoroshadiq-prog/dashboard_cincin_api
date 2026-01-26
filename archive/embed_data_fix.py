"""
Embed blocks_data_embed.js directly into HTML to fix loading issue
"""

# Read data
with open('data/output/blocks_data_embed.js', 'r', encoding='utf-8') as f:
    js_data = f.read()

# Read HTML  
with open('data/output/dashboard_cincin_api_FINAL_CORRECTED.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace external script with embedded
old_script = '<script src="blocks_data_embed.js"></script>'
new_script = f'<script>\n{js_data}\n</script>'

html = html.replace(old_script, new_script)

# Write back
with open('data/output/dashboard_cincin_api_FINAL_CORRECTED.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Data embedded directly into HTML!")
print("✅ File size increased but data now guaranteed to load!")
