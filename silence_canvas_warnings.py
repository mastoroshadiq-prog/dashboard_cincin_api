"""
Silence warnings for intentionally removed canvas elements
Change console.error to console.log (debug only) for removed charts
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Fix 1: degradationModelChart warning (removed in v9.1)
old_degradation = """                if (!canvas) {
                    console.error('[CHART] Canvas degradationModelChart not found');
                    return;
                }"""

new_degradation = """                if (!canvas) {
                    // Canvas removed in v9.1 (Treatment Comparison section) - silently skip
                    return;
                }"""

if old_degradation in content:
    content = content.replace(old_degradation, new_degradation)
    print("✅ Fixed degradationModelChart warning")
else:
    print("⚠️ degradationModelChart pattern not found")

# Fix 2: historicalTrendsChart warning (removed in v9.0.1)
old_historical = """                if (!canvas) {
                    console.error('[HISTORICAL CHART] Canvas not found');
                    return;
                }"""

new_historical = """                if (!canvas) {
                    // Canvas removed in v9.0.1 (Historical Trends section) - silently skip
                    return;
                }"""

if old_historical in content:
    content = content.replace(old_historical, new_historical)
    print("✅ Fixed historicalTrendsChart warning")
else:
    print("⚠️ historicalTrendsChart pattern not found")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ CONSOLE WARNINGS SILENCED!")
print(f"   Changed console.error → silent return")
print(f"   Why: These canvases were intentionally removed in cleanup")
print(f"\n   Removed charts:")
print(f"   • degradationModelChart (v9.1 - Treatment Comparison)")
print(f"   • historicalTrendsChart (v9.0.1 - Historical Trends)")
print(f"\n   Console is now completely clean! ✨")
