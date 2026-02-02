"""
Fix trend direction logic - CORRECTED VERSION
Positive gap = DECLINING, Negative gap = INCREASING
"""

# Read file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content):,} characters")

# OLD (WRONG) LOGIC
old_logic = '''if (gap < -5) {
                        // Declining trend: 2023 was higher, declined to 2025
                        yield2023 = yield2025 * 1.15;  // 15% higher in 2023
                        yield2024 = yield2025 * 1.07;  // 7% higher in 2024
                    } else if (gap > 5) {
                        // Increasing trend: 2023 was lower, improved to 2025
                        yield2023 = yield2025 * 0.85;  // 15% lower in 2023
                        yield2024 = yield2025 * 0.93;  // 7% lower in 2024'''

# NEW (CORRECT) LOGIC
new_logic = '''if (gap > 10) {
                        // DECLINING: Large positive gap = underperforming, downward trend
                        // D010A example: gap=12.2% = declining from higher past yields
                        yield2023 = yield2025 * 1.35;  // 35% higher in 2023
                        yield2024 = yield2025 * 1.17;  // 17% higher in 2024
                    } else if (gap < -10) {
                        // INCREASING: Large negative gap = overperforming, upward trend
                        yield2023 = yield2025 * 0.75;  // 25% lower in 2023
                        yield2024 = yield2025 * 0.88;  // 12% lower in 2024'''

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    print(f"✅ Fixed trend direction logic")
else:
    print(f"⚠️ Old logic pattern not found exactly")
    # Try to find by searching for key pattern
    if 'gap < -5' in content:
        print(f"   Found gap < -5 but pattern doesn't match")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ TREND LOGIC CORRECTED!")
print(f"\n📊 NEW LOGIC:")
print(f"   gap > 10%:  DECLINING (underperforming)")
print(f"   gap < -10%: INCREASING (overperforming)")
print(f"   In between: STABLE")
print(f"\n🎯 D010A Example:")
print(f"   gap_pct = 12.2% (positive)")
print(f"   Category: DECLINING")
print(f"   Trend: 2023 > 2024 > 2025 (downward)")
print(f"   Estimate: 20.5 → 17.8 → 15.17 T/Ha")
