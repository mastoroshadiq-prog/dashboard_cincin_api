"""
SIMPLE COPY-PASTE: Just copy exact sections from dashboard to demo
NO popups, NO reinvention, just SWAP positions
"""

print("="*80)
print("COPYING EXACT SECTIONS FROM ORIGINAL DASHBOARD")
print("="*80)

# Read original dashboard
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    dashboard = f.read()

# Extract lines 217-338: "ESTIMASI KERUGIAN BLOK A" (LEFT panel - Indigo)
left_start = dashboard.find('<!-- Left Financial (Blok A) -->')
left_end = dashboard.find('<!-- Risk Control Tower (Summary) -->')
left_panel = dashboard[left_start:left_end].strip()

print(f"✅ Extracted LEFT panel (ESTIMASI KERUGIAN BLOK A): {len(left_panel)} chars")

# Extract lines 341-387: "PAPARAN RISIKO ESTATE" (RIGHT panel - Red/Rose)
right_start = dashboard.find('<!-- Risk Control Tower (Summary) -->')
right_end = dashboard.find('<!-- ============================================ -->', right_start + 100)
right_panel = dashboard[right_start:right_end].strip()

print(f"✅ Extracted RIGHT panel (PAPARAN RISIKO ESTATE): {len(right_panel)} chars")

# Now prepare for demo - these will REPLACE Feature 2
# Feature 2 currently at lines ~53-110 in DASHBOARD_DEMO_FEATURES.html

# Create NEW Feature 2 HTML with SWAPPED positions (PAPARAN LEFT, STATISTIK/ESTIMASI RIGHT)
new_feature2 = f'''        <!-- ============================================ -->
        <!-- FEATURE 2: Section Layout (COPIED FROM ORIGINAL) -->
        <!-- ============================================ -->
        <div class="bg-slate-800/50 backdrop-blur-lg p-8 rounded-2xl border border-white/10 shadow-2xl">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-4xl">🔄</span>
                <div>
                    <h2 class="text-2xl font-black text-white">Analisis Dampak Finansial</h2>
                    <p class="text-slate-400">PAPARAN RISK (Kiri) + STATISTIK BLOK (Kanan)</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <!-- LEFT: PAPARAN RISIKO ESTATE (Red) -->
                {right_panel}

                <!-- RIGHT: STATISTIK BLOK / ESTIMASI KERUGIAN (Blue) -->
                {left_panel}

            </div>
        </div>
'''

# Save this
with open('exact_feature2_from_original.html', 'w', encoding='utf-8') as f:
    f.write(new_feature2)

print("\n✅ Feature 2 HTML generated with EXACT original sections!")
print("   LEFT: PAPARAN RISIKO ESTATE")
print("   RIGHT: ESTIMASI KERUGIAN BLOK")
print("\nFile: exact_feature2_from_original.html")
print("="*80)
