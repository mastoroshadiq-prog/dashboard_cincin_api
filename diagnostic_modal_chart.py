"""
COMPREHENSIVE DIAGNOSTIC - Check ALL issues in modal rendering
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*80)
print("DIAGNOSTIC 1: Check if canvas element exists in HTML")
print("="*80)

# Find modal HTML
modal_start = content.find('id="paparanRisikoModal"')
if modal_start != -1:
    modal_section = content[modal_start:modal_start+5000]
    
    # Check for canvas
    if 'id="modalRiskChart"' in modal_section:
        print("✅ Canvas #modalRiskChart EXISTS in HTML")
        # Extract the canvas tag
        canvas_idx = modal_section.find('id="modalRiskChart"')
        canvas_snippet = modal_section[max(0, canvas_idx-100):canvas_idx+200]
        print("\nCanvas element:")
        print(canvas_snippet)
    else:
        print("❌ Canvas #modalRiskChart NOT FOUND in modal!")
else:
    print("❌ Modal #paparanRisikoModal not found!")

print("\n" + "="*80)
print("DIAGNOSTIC 2: Check renderModalChart function")
print("="*80)

func_start = content.find('function renderModalChart(blocks, sortBy)')
if func_start != -1:
    func_section = content[func_start:func_start+2000]
    
    # Check for getElementById
    if "getElementById('modalRiskChart')" in func_section:
        print("✅ Function calls getElementById('modalRiskChart')")
    else:
        print("❌ Function doesn't call getElementById('modalRiskChart')")
    
    # Check for Chart.js instantiation
    if "new Chart(" in func_section:
        print("✅ Function creates new Chart()")
    else:
        print("❌ Function doesn't create Chart object")
        
    # Check field names
    if "loss_value_juta" in func_section:
        print("✅ Uses correct field: loss_value_juta")
    else:
        print("❌ Still using wrong field name")

print("\n" + "="*80)
print("DIAGNOSTIC 3: Check if Chart.js library is loaded")
print("="*80)

if 'chart.js' in content.lower() or 'chartjs' in content.lower():
    # Find script tag
    import re
    chart_scripts = re.findall(r'<script[^>]*chart[^>]*>.*?</script>|<script[^>]*src=["\']([^"\']*chart[^"\']*)["\']', content, re.IGNORECASE | re.DOTALL)
    if chart_scripts:
        print("✅ Chart.js library found:")
        for script in chart_scripts[:3]:
            print(f"   {script[:150]}")
    else:
        print("⚠️  Chart.js referenced but script tag unclear")
else:
    print("❌ Chart.js library NOT FOUND!")

print("\n" + "="*80)
print("DIAGNOSTIC 4: Sample first critical block data")
print("="*80)

# Find BLOCKS_DATA
blocks_start = content.find('const BLOCKS_DATA = {')
if blocks_start != -1:
    blocks_section = content[blocks_start:blocks_start+10000]
    
    # Extract first block
    import re
    block_code_match = re.search(r'"block_code":\s*"([^"]+)"', blocks_section)
    attack_rate_match = re.search(r'"attack_rate":\s*([0-9.]+)', blocks_section)
    loss_match = re.search(r'"loss_value_juta":\s*([0-9.]+)', blocks_section)
    
    if block_code_match and attack_rate_match and loss_match:
        print(f"✅ Sample block data:")
        print(f"   block_code: {block_code_match.group(1)}")
        print(f"   attack_rate: {attack_rate_match.group(1)}")
        print(f"   loss_value_juta: {loss_match.group(1)}")
    else:
        print("❌ Could not extract block data")

print("\n" + "="*80)
print("DIAGNOSTIC 5: Check if modalRiskChart variable is declared")
print("="*80)

if 'let modalRiskChart' in content or 'var modalRiskChart' in content:
    print("✅ modalRiskChart variable declared")
else:
    print("❌ modalRiskChart variable NOT declared!")

print("\n" + "="*80)
print("RECOMMENDATION:")
print("="*80)
print("Please run this in browser console when modal is open:")
print("  1. console.log(document.getElementById('modalRiskChart'))")
print("  2. console.log('Critical blocks array:', criticalBlocksArray)")
print("  3. Check for any JavaScript errors in Console tab")
print("\nThen share the console output!")
