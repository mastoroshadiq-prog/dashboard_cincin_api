"""
STEP 2: Build Division Summary Panel with Treatment Comparison
Add visual panel below division selector
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find insertion point - after division selector (after divisionStats closing div)
marker = '</div>\n    </div>\n\n    <div class="max-w-7xl mx-auto space-y-8">'

if marker not in content:
    print("❌ Marker not found! Searching for alternative...")
    # Try simpler marker
    marker = '<div class="max-w-7xl mx-auto space-y-8">'
    if marker not in content:
        print("❌ Alternative marker also not found!")
        exit(1)

division_summary_panel = '''
    <!-- ================================================ -->
    <!--  STEP 2: DIVISION SUMMARY PANEL (NEW)           -->
    <!-- ================================================ -->
    <div class="max-w-7xl mx-auto mb-8" id="divisionSummaryPanel">
        <div class="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl rounded-3xl border-2 border-emerald-500/30 shadow-2xl p-8">
            
            <!-- Header -->
            <div class="flex items-center gap-4 mb-6">
                <div class="text-5xl">🌍</div>
                <div>
                    <h2 class="text-3xl font-black text-emerald-400 mb-1">AME II DIVISION OVERVIEW</h2>
                    <p class="text-slate-300 text-sm">Complete aggregated metrics from all blocks</p>
                </div>
            </div>

            <!-- Quick Metrics Grid -->
            <div class="grid grid-cols-4 gap-4 mb-6">
                <div class="bg-black/30 rounded-xl p-4 border border-cyan-500/20">
                    <div class="text-xs text-cyan-300 font-bold uppercase mb-1">Total Blocks</div>
                    <div class="text-3xl font-black text-white" id="divMetric_totalBlocks">179</div>
                </div>
                <div class="bg-black/30 rounded-xl p-4 border border-blue-500/20">
                    <div class="text-xs text-blue-300 font-bold uppercase mb-1">Total Area</div>
                    <div class="text-3xl font-black text-white" id="divMetric_totalArea">2,890<span class="text-sm text-slate-400 ml-1">Ha</span></div>
                </div>
                <div class="bg-black/30 rounded-xl p-4 border border-yellow-500/20">
                    <div class="text-xs text-yellow-300 font-bold uppercase mb-1">Avg Yield 2025</div>
                    <div class="text-3xl font-black text-white" id="divMetric_avgYield">14.44<span class="text-sm text-slate-400 ml-1">T/Ha</span></div>
                </div>
                <div class="bg-black/30 rounded-xl p-4 border border-red-500/20">
                    <div class="text-xs text-red-300 font-bold uppercase mb-1">Critical Blocks</div>
                    <div class="text-3xl font-black text-red-400" id="divMetric_critical">97<span class="text-sm text-slate-400 ml-1">/ 179</span></div>
                </div>
            </div>

            <!-- Treatment Comparison Panel -->
            <div class="bg-gradient-to-r from-red-900/20 to-emerald-900/20 rounded-2xl border-2 border-white/10 p-6">
                <h3 class="text-xl font-black text-white mb-4 flex items-center gap-2">
                    💰 TREATMENT IMPACT ANALYSIS (DIVISION LEVEL)
                </h3>

                <div class="grid grid-cols-2 gap-6">
                    <!-- NO TREATMENT -->
                    <div class="bg-red-900/30 rounded-xl border-2 border-red-500/50 p-6">
                        <div class="flex items-center gap-2 mb-4">
                            <div class="text-3xl">❌</div>
                            <h4 class="text-lg font-black text-red-300">NO TREATMENT<br/>(Continue as-is)</h4>
                        </div>
                        
                        <div class="space-y-3">
                            <div>
                                <div class="text-xs text-red-200/60 font-bold mb-1">ANNUAL LOSS (2026)</div>
                                <div class="text-4xl font-black text-red-400" id="noTreatment_loss">Rp 5,970 Jt</div>
                            </div>
                            <div>
                                <div class="text-xs text-red-200/60 font-bold mb-1">PRODUCTION GAP</div>
                                <div class="text-2xl font-black text-white" id="noTreatment_gap">12,426 Ton</div>
                            </div>
                            <div>
                                <div class="text-xs text-red-200/60 font-bold mb-1">CRITICAL BLOCKS</div>
                                <div class="text-2xl font-black text-white" id="noTreatment_critical">97 / 179 (55%)</div>
                            </div>
                        </div>
                    </div>

                    <!-- WITH TREATMENT -->
                    <div class="bg-emerald-900/30 rounded-xl border-2 border-emerald-500/50 p-6">
                        <div class="flex items-center gap-2 mb-4">
                            <div class="text-3xl">✅</div>
                            <h4 class="text-lg font-black text-emerald-300">WITH TREATMENT<br/>(Immediate Action)</h4>
                        </div>
                        
                        <div class="space-y-3">
                            <div>
                                <div class="text-xs text-emerald-200/60 font-bold mb-1">REDUCED LOSS (2026)</div>
                                <div class="text-4xl font-black text-emerald-400" id="withTreatment_loss">Rp 1,195 Jt<span class="text-lg ml-2 text-emerald-300">↓80%</span></div>
                            </div>
                            <div>
                                <div class="text-xs text-emerald-200/60 font-bold mb-1">RECOVERED GAP</div>
                                <div class="text-2xl font-black text-white" id="withTreatment_gap">2,485 Ton<span class="text-sm text-emerald-300 ml-2">↓80%</span></div>
                            </div>
                            <div>
                                <div class="text-xs text-emerald-200/60 font-bold mb-1">BLOCKS RECOVERED</div>
                                <div class="text-2xl font-black text-white" id="withTreatment_recovered">65 / 97 (67%)</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ROI Highlight -->
                <div class="mt-6 bg-yellow-500/10 border-2 border-yellow-500/50 rounded-xl p-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="text-4xl">💡</div>
                            <div>
                                <div class="text-sm text-yellow-300 font-bold uppercase">POTENTIAL SAVINGS</div>
                                <div class="text-3xl font-black text-yellow-400" id="roi_savings">Rp 4,775 Juta</div>
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-sm text-emerald-300 font-bold uppercase">ROI RATIO</div>
                            <div class="text-3xl font-black text-emerald-400" id="roi_ratio">5.0x</div>
                            <div class="text-xs text-slate-400">Treatment cost: ~Rp 955 Juta</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Disclaimer / Showing Blocks Info -->
            <div class="mt-6 bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
                <div class="flex items-start gap-2">
                    <div class="text-xl">ℹ️</div>
                    <div class="text-sm text-blue-200">
                        <strong>Data Coverage:</strong> Above metrics calculated from <strong>ALL 179 blocks</strong> in AME II division (2,890 Ha total). 
                        Critical block details below show <strong>top 8 highest-risk blocks</strong> requiring immediate attention.
                    </div>
                </div>
            </div>
        </div>
    </div>

'''

# Insert panel
content = content.replace(marker, division_summary_panel + '\n    ' + marker)

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("="*70)
print("✅ STEP 2 COMPLETE: DIVISION SUMMARY PANEL ADDED!")
print("="*70)
print("\nPanel includes:")
print("  ✅ Division metrics (179 blocks, 2,890 Ha)")
print("  ✅ Treatment comparison (NO vs WITH)")
print("  ✅ ROI highlight (5.0x ratio)")
print("  ✅ Visual side-by-side layout")
print("\n🌐 REFRESH BROWSER TO SEE!")
print("="*70)
