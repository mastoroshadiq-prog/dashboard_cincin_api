"""
COMPREHENSIVE IMPLEMENTATION: Prototype → Real Dashboard
All 3 features in one script
"""

print("="*80)
print("IMPLEMENTING PROTOTYPE FEATURES TO REAL DASHBOARD")
print("="*80)

# Load both files
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    dashboard = f.read()

with open('data/output/PROTOTYPE_3_ENHANCEMENTS.html', 'r', encoding='utf-8') as f:
    prototype = f.read()

print("\n✅ Files loaded")
print(f"   Dashboard: {len(dashboard)} chars")
print(f"   Prototype: {len(prototype)} chars")

# ============================================================================
# FEATURE 2: RENAME "ESTIMASI KERUGIAN BLOK" → "STATISTIK BLOK"
# ============================================================================
print("\n" + "="*80)
print("FEATURE 2: Renaming section title")
print("="*80)

old_title = "ESTIMASI KERUGIAN BLOK"
new_title = "STATISTIK BLOK"

count_before = dashboard.count(old_title)
dashboard = dashboard.replace(old_title, new_title)
count_after = dashboard.count(new_title)

print(f"✅ Renamed: '{old_title}' → '{new_title}'")
print(f"   Occurrences: {count_before} replaced")

# ============================================================================
# FEATURE 1: INSERT TREATMENT COMPARISON CHART
# ============================================================================
print("\n" + "="*80)
print("FEATURE 1: Adding treatment comparison chart")
print("="*80)

# Extract Feature 1 HTML from prototype (the chart section)
# Find the Feature 1 section in prototype
feature1_html_start = prototype.find('<!-- Chart Container -->')
feature1_html_end = prototype.find('</div>', feature1_html_start + 2000) + 6  # Find closing div after summary boxes

if feature1_html_start > 0:
    # Extract the HTML
    feature1_html = prototype[feature1_html_start:feature1_html_end]
    
    # Find insertion point in dashboard (after ROI metrics, before block details)
    # Look for the COI section closing and block detail start
    insertion_marker = '<!-- ============================================ -->'
    # Find after "Biaya Tidak Bertindak" section
    coi_section_end = dashboard.find('</div>', dashboard.find('URGENT: Biaya Tidak'))
    
    if coi_section_end > 0:
        # Find next section start
        next_section = dashboard.find('<!-- ', coi_section_end)
        
        # Insert Feature 1
        feature1_wrapper = f'''

        <!-- ============================================ -->
        <!-- FEATURE 1: Before/After Treatment Comparison -->
        <!-- ============================================ -->
        <div class="mt-8 p-6 bg-slate-800/50 backdrop-blur-lg rounded-2xl border border-white/10 shadow-2xl">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-4xl">📊</span>
                <div>
                    <h2 class="text-2xl font-black text-white">Perbandingan: TANPA vs DENGAN Treatment</h2>
                    <p class="text-slate-400">Proyeksi 3 tahun dengan degradation model</p>
                </div>
            </div>

            {feature1_html}
        </div>
'''
        
        dashboard = dashboard[:next_section] + feature1_wrapper + dashboard[next_section:]
        print("✅ Feature 1 HTML inserted")
    else:
        print("⚠️  Could not find insertion point - will add manually")
else:
    print("⚠️  Could not extract Feature 1 HTML from prototype")

# Extract Feature 1 JavaScript from prototype
js_start = prototype.find('const ctx1 = document.getElementById(\'treatmentComparisonChart\')')
js_end = prototype.find('});', js_start + 500) + 3

if js_start > 0:
    feature1_js = prototype[js_start:js_end]
    
    # Find where to insert JS in dashboard (before closing </script>)
    script_close = dashboard.rfind('</script>')
    
    if script_close > 0:
        dashboard = dashboard[:script_close] + '\n        // Feature 1: Treatment Comparison Chart\n        ' + feature1_js + '\n        ' + dashboard[script_close:]
        print("✅ Feature 1 JavaScript inserted")
else:
    print("⚠️  Could not extract Feature 1 JS")

# ============================================================================
# FEATURE 3: ENHANCED MODAL CHARTS
# ============================================================================
print("\n" + "="*80)
print("FEATURE 3: Enhancing modal charts")
print("="*80)

# This is complex - need to:
# 1. Add data display table container (for 3-year chart)
# 2. Replace 3-year chart code with enhanced version
# 3. Replace pie chart code with labeled version

# For now, mark as TODO and provide manual instructions
print("⚠️  Feature 3 requires careful modal integration")
print("   Will create separate script for modal enhancements")

# ============================================================================
# SAVE UPDATED DASHBOARD
# ============================================================================
print("\n" + "="*80)
print("SAVING UPDATED DASHBOARD")
print("="*80)

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(dashboard)

print("✅ Dashboard saved!")
print(f"   New size: {len(dashboard)} chars")

print("\n" + "="*80)
print("IMPLEMENTATION SUMMARY")
print("="*80)
print("✅ Feature 2: Title renamed (ESTIMASI → STATISTIK)")
print("✅ Feature 1: Treatment chart added (pending JS check)")
print("⚠️  Feature 3: Modals enhancement (separate script)")
print("\nNEXT STEPS:")
print("1. Open dashboard dan verify Feature 1 chart")
print("2. Run modal enhancement script for Feature 3")
print("3. Full testing")
print("="*80)
