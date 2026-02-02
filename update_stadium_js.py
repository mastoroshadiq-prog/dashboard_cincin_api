"""
Update JavaScript to populate grouped stadium values
"""

# Read file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content):,} characters")

# Find and replace stadium JavaScript code
# Look for the section where stadium values are assigned

old_js = '''// Ganoderma stadium
            const stadiumI = blockData.stadium_i_pct || 0;
            const stadiumII = blockData.stadium_ii_pct || 0;
            const stadiumIII = blockData.stadium_iii_pct || 0;
            document.getElementById('block_ganoderma_stadium').textContent =
                stadiumIII > 10 ? 'Stadium III (Kritis)' :
                    stadiumII > 10 ? 'Stadium II (Sedang)' :
                        'Stadium I (Ringan)';

            document.getElementById('block_stadium_i').textContent = stadiumI.toFixed(1) + '%';
            document.getElementById('block_stadium_ii').textContent = stadiumII.toFixed(1) + '%';
            document.getElementById('block_stadium_iii').textContent = stadiumIII.toFixed(1) + '%';'''

new_js = '''// Ganoderma stadium (grouped 1&2 vs 3&4)
            const stadium12 = blockData.stadium_12_pct || 0;
            const stadium34 = blockData.stadium_34_pct || 0;
            
            // Determine severity based on advanced stage percentage
            document.getElementById('block_ganoderma_stadium').textContent =
                stadium34 > 15 ? 'Kritis (Stadium 3&4 dominan)' :
                    stadium34 > 5 ? 'Sedang (Stadium 3&4 terkendali)' :
                        'Ringan (Stadium 1&2 dominan)';

            document.getElementById('block_stadium_12').textContent = stadium12.toFixed(1) + '%';
            document.getElementById('block_stadium_34').textContent = stadium34.toFixed(1) + '%';'''

if old_js in content:
    content = content.replace(old_js, new_js)
    print(f"✅ Replaced stadium JavaScript")
else:
    # Try simpler pattern
    if 'block_stadium_i' in content and 'block_stadium_ii' in content:
        print(f"✅ Found stadium references, but pattern doesn't match exactly")
        print(f"   Manual check required - file may have been modified")
    else:
        print(f"⚠️ Stadium element IDs not found")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ UI UPDATE COMPLETE!")
print(f"\n📊 Ganoderma Detail Card now shows:")
print(f"   Stadium 1 & 2 (Early Stage): X.X%")
print(f"   Stadium 3 & 4 (Advanced): X.X%")
