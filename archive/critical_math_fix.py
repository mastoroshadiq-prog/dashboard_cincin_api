import re

file_path = r'd:\PythonProjects\simulasi_poac\data\output\dashboard_cincin_api_INTERACTIVE_FULL.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FIX THE SCALE DATA (Convert MILIAR to JUTA by multiplying by 1000)
# Old: block: { area: '55.4', loss: '1.208', mitigation: '0.1', ... }
# New: block: { area: '55.4', loss: '1,208', mitigation: '100', ... }
content = re.sub(r"loss: '1\.208', mitigation: '0\.1'", "loss: '1,208', mitigation: '100'", content)
content = re.sub(r"loss: '19\.1', mitigation: '1\.57'", "loss: '19,100', mitigation: '1,570'", content)
content = re.sub(r"loss: '56\.1', mitigation: '4\.6'", "loss: '56,100', mitigation: '4,600'", content)

# 2. FIX THE DYNAMIC CALCULATION MATH
# Correct JUTA factor: (Ton * Ha * 1000 kg/ton * 1500 rp/kg) / 1,000,000 = Ton * Ha * 1.5
# Old: Math.abs(data.gap_ton_ha) * data.luas_ha * 1500 / 1000000
# New: Math.abs(data.gap_ton_ha) * data.luas_ha * 1.5
content = content.replace("Math.abs(data.gap_ton_ha) * data.luas_ha * 1500 / 1000000", "Math.abs(data.gap_ton_ha) * data.luas_ha * 1.5")

# 3. FIX MITIGATION COST MATH (also needed factor correction if it was divided by 1,000,000 but intended JUTA)
# Perimeter in meters * 15000 Rp/m. To get JUTA, divide by 1,000,000.
# Let's keep / 1000000 for mitigation because it's already in IDR.
# But let's check the unit cost. Rp 15.000 / meter.
# sqrt(N) * 32 * 15000 / 1000000 = sqrt(N) * 0.48
# For D001A: 16.2 * 0.48 = 7.7 JUTA. This is correct.

# Wait, let me check the existing mitigation lines in the file
content = content.replace("* 35000) / 1000000", "* 15000) / 1000000") # Ensure lower cost
content = content.replace("* 20000) / 1000000", "* 15000) / 1000000")

# 4. FIX HTML LABELS - ensure everything says JUTA
content = content.replace("MILAR/THN", "JUTA/THN")
content = content.replace(">MILAR<", ">JUTA<")

# 5. FIX ASSET VALUATION MATH
# Old: (healthyTrees * 150 * 1500 / 1000000)
# (Pohon * 150 kg * 1500 rp) / 1,000,000 = Pohon * 0.225
# For 3400 trees: 3400 * 0.225 = 765 Juta. Correct.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ FIXED: Math factor corrected (1000x increase to proper JUTA scale).")
print("✅ FIXED: scaleData updated to JUTA.")
print("✅ FIXED: Mitigation unit cost set to Rp 15,000/m.")
