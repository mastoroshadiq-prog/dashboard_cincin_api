"""
Add BREAKDOWN section below ESTIMASI panel
Shows: 4 metrics + Degradation table + Treatment impact
"""

# Read demo
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("Adding BREAKDOWN section...")

# Create breakdown HTML
breakdown_html = '''
                <!-- BREAKDOWN SECTION (hidden by default, shown after block click) -->
                <div id="blockBreakdownSection" class="hidden mt-6 space-y-6">
                    
                    <!-- 4 Metric Boxes -->
                    <div class="grid grid-cols-4 gap-4">
                        <div class="bg-red-900/30 p-4 rounded-xl border border-red-500/30">
                            <div class="text-xs text-red-300 uppercase mb-1">Kerugian Saat Ini</div>
                            <div class="text-3xl font-black text-white" id="breakdownCurrentLoss">Rp 182</div>
                            <div class="text-xs text-red-400">Juta/year</div>
                        </div>
                        <div class="bg-orange-900/30 p-4 rounded-xl border border-orange-500/30">
                            <div class="text-xs text-orange-300 uppercase mb-1">Total 3 Tahun</div>
                            <div class="text-3xl font-black text-white" id="breakdown3YearTotal">Rp 874</div>
                            <div class="text-xs text-orange-400">Juta</div>
                        </div>
                        <div class="bg-emerald-900/30 p-4 rounded-xl border border-emerald-500/30">
                            <div class="text-xs text-emerald-300 uppercase mb-1">Treatment</div>
                            <div class="text-3xl font-black text-white" id="breakdownTreatment">Rp 50</div>
                            <div class="text-xs text-emerald-400">Juta</div>
                        </div>
                        <div class="bg-cyan-900/30 p-4 rounded-xl border border-cyan-500/30">
                            <div class="text-xs text-cyan-300 uppercase mb-1">ROI</div>
                            <div class="text-3xl font-black text-white" id="breakdownROI">1123</div>
                            <div class="text-xs text-cyan-400">%</div>
                        </div>
                    </div>

                    <!-- Degradation Timeline Table -->
                    <div class="bg-slate-900/50 p-6 rounded-xl border border-white/10">
                        <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            📉 Degradation Timeline (No Treatment)
                        </h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-sm">
                                <thead>
                                    <tr class="border-b-2 border-white/20">
                                        <th class="text-left p-3 text-slate-300 font-bold">Parameter</th>
                                        <th class="text-center p-3 text-slate-400 font-bold">Tahun 0<br><span class="text-xs">(Saat Ini)</span></th>
                                        <th class="text-center p-3 text-yellow-400 font-bold">Tahun 1</th>
                                        <th class="text-center p-3 text-yellow-400 font-bold">Tahun 2</th>
                                        <th class="text-center p-3 text-yellow-400 font-bold">Tahun 3</th>
                                        <th class="text-center p-3 text-orange-400 font-bold">Perubahan</th>
                                    </tr>
                                </thead>
                                <tbody id="degradationTableBody" class="text-white">
                                    <!-- Populated by JavaScript -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Impact of Treatment -->
                    <div class="bg-emerald-900/20 p-6 rounded-xl border-2 border-emerald-500/50">
                        <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            ✅ Impact of Treatment
                        </h3>
                        <div class="grid grid-cols-2 gap-6">
                            <div>
                                <div class="text-sm text-emerald-300 mb-2">Kerugian yang Dicegah (70% efektif):</div>
                                <div class="text-4xl font-black text-emerald-400" id="treatmentPrevented">Rp 612 Juta</div>
                            </div>
                            <div>
                                <div class="text-sm text-emerald-300 mb-2">Manfaat Bersih:</div>
                                <div class="text-4xl font-black text-emerald-400" id="treatmentNetBenefit">Rp 562 Juta</div>
                            </div>
                        </div>
                        <div class="mt-4 text-xs text-emerald-200/70 italic">
                            Treatment mencakup: Parit isolasi (4x4m), fungisida sistemik, sanitasi, dan perbaikan drainage.
                        </div>
                    </div>

                </div>
'''

# Find where to insert (after ESTIMASI panel closes, before grid closes)
insertion_point = demo.find('            </div>\r\n\r\n            </div>\r\n        </div>')

if insertion_point > 0:
    # Insert before the closing divs
    demo = demo[:insertion_point] + breakdown_html + '\r\n' + demo[insertion_point:]
    print("✅ Breakdown section HTML added")
else:
    print("⚠️  Could not find insertion point")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print(f"\n✅ Breakdown section added!")
print(f"   File size: {len(demo)} chars")
print("\nNEXT: Need to add JavaScript to populate this when block clicked")
