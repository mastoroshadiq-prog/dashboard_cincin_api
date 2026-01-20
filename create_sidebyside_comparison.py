"""
Script untuk membuat side-by-side 3-year comparison:
NO TREATMENT vs WITH TREATMENT + SAVINGS highlight
"""

def create_sidebyside_comparison():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Creating side-by-side 3-year comparison...")
    
    # Find and replace the entire NO TREATMENT section with side-by-side layout
    # Look for the section starting from the NO TREATMENT box
    start_marker = '''                            <!-- NO TREATMENT -->
                            <div class="bg-red-900/30 rounded-xl border-2 border-red-500/50 p-6">
                                <div class="flex items-center gap-2 mb-4">
                                    <div class="text-3xl">❌</div>
                                    <h4 class="text-lg font-black text-red-300">NO TREATMENT<br />(Continue as-is)</h4>
                                </div>

                                <div class="space-y-2">'''
    
    # New side-by-side layout
    new_layout = '''                            <!-- 3-YEAR PROJECTION COMPARISON -->
                            <div class="col-span-2 bg-gradient-to-br from-slate-900/90 to-black/90 rounded-2xl border-2 border-purple-500/30 p-6">
                                <h3 class="text-xl font-black text-white mb-4 flex items-center gap-2">
                                    📊 3-YEAR FINANCIAL IMPACT ANALYSIS
                                </h3>
                                
                                <div class="grid grid-cols-2 gap-6 mb-6">
                                    <!-- LEFT: NO TREATMENT -->
                                    <div class="bg-red-900/20 rounded-xl border-2 border-red-500/30 p-4">
                                        <div class="flex items-center gap-2 mb-3">
                                            <div class="text-2xl">❌</div>
                                            <h4 class="text-sm font-black text-red-300 uppercase">No Treatment<br/><span class="text-xs opacity-70">(Continue as-is)</span></h4>
                                        </div>
                                        
                                        <!-- 3-Year Table -->
                                        <div class="grid grid-cols-4 gap-1 mb-3">
                                            <div class="bg-red-900/20 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-red-300/70 font-bold mb-0.5">2025</div>
                                                <div class="text-sm font-black text-red-400" id="noTreatment_year0">--</div>
                                            </div>
                                            <div class="bg-red-900/30 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-red-300/70 font-bold mb-0.5">2026</div>
                                                <div class="text-sm font-black text-red-400" id="noTreatment_year1">--</div>
                                            </div>
                                            <div class="bg-red-900/40 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-red-300/70 font-bold mb-0.5">2027</div>
                                                <div class="text-sm font-black text-red-400" id="noTreatment_year2">--</div>
                                            </div>
                                            <div class="bg-red-900/50 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-red-300/70 font-bold mb-0.5">2028</div>
                                                <div class="text-sm font-black text-red-400" id="noTreatment_year3">--</div>
                                            </div>
                                        </div>
                                        
                                        <!-- Total Loss -->
                                        <div class="bg-red-950/50 rounded-lg border border-red-500/50 p-3 text-center">
                                            <div class="text-[10px] text-red-300/80 font-bold mb-1 uppercase">Total 3-Year Loss</div>
                                            <div class="text-3xl font-black text-red-400" id="noTreatment_cumulative">--</div>
                                        </div>
                                    </div>
                                    
                                    <!-- RIGHT: WITH TREATMENT -->
                                    <div class="bg-emerald-900/20 rounded-xl border-2 border-emerald-500/30 p-4">
                                        <div class="flex items-center gap-2 mb-3">
                                            <div class="text-2xl">✅</div>
                                            <h4 class="text-sm font-black text-emerald-300 uppercase">With Treatment<br/><span class="text-xs opacity-70">(70% Effective)</span></h4>
                                        </div>
                                        
                                        <!-- 3-Year Table -->
                                        <div class="grid grid-cols-4 gap-1 mb-3">
                                            <div class="bg-emerald-900/20 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-emerald-300/70 font-bold mb-0.5">2025</div>
                                                <div class="text-sm font-black text-emerald-400" id="withTreatment_year0">--</div>
                                            </div>
                                            <div class="bg-emerald-900/30 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-emerald-300/70 font-bold mb-0.5">2026</div>
                                                <div class="text-sm font-black text-emerald-400" id="withTreatment_year1">--</div>
                                            </div>
                                            <div class="bg-emerald-900/40 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-emerald-300/70 font-bold mb-0.5">2027</div>
                                                <div class="text-sm font-black text-emerald-400" id="withTreatment_year2">--</div>
                                            </div>
                                            <div class="bg-emerald-900/50 rounded p-1.5 text-center">
                                                <div class="text-[8px] text-emerald-300/70 font-bold mb-0.5">2028</div>
                                                <div class="text-sm font-black text-emerald-400" id="withTreatment_year3">--</div>
                                            </div>
                                        </div>
                                        
                                        <!-- Total Loss -->
                                        <div class="bg-emerald-950/50 rounded-lg border border-emerald-500/50 p-3 text-center">
                                            <div class="text-[10px] text-emerald-300/80 font-bold mb-1 uppercase">Total 3-Year Loss</div>
                                            <div class="text-3xl font-black text-emerald-400" id="withTreatment_cumulative">--</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- SAVINGS HIGHLIGHT -->
                                <div class="bg-gradient-to-r from-yellow-900/30 to-orange-900/30 rounded-xl border-2 border-yellow-500/50 p-4">
                                    <div class="flex items-center justify-between">
                                        <div class="flex items-center gap-3">
                                            <div class="text-4xl">💰</div>
                                            <div>
                                                <div class="text-xs text-yellow-300/80 font-bold uppercase mb-1">3-Year Savings with Treatment</div>
                                                <div class="text-5xl font-black text-yellow-400" id="treatment_totalSavings">--</div>
                                            </div>
                                        </div>
                                        <div class="text-right">
                                            <div class="text-xs text-yellow-300/80 font-bold uppercase mb-1">Savings Rate</div>
                                            <div class="text-4xl font-black text-yellow-400" id="treatment_savingsPercent">--%</div>
                                        </div>
                                    </div>
                                    <div class="mt-3 text-xs text-yellow-200/70 text-center">
                                        ⚡ Cost of Treatment vs. Cost of Inaction - <span class="font-bold text-yellow-300">Treatment ROI is clear</span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Other metrics (Production Gap, Critical Blocks) -->
                            <div class="bg-slate-800/50 rounded-xl border border-slate-600/30 p-4">
                                <div class="space-y-2">'''
    
    # Find the start marker and replace section
    if start_marker in content:
        # Find the end of the old section (we'll replace up to Production Gap section)
        end_marker = '''                                    <div>
                                        <div class="text-xs text-red-200/60 font-bold mb-1">PRODUCTION GAP</div>'''
        
        if end_marker in content:
            # Extract before and after
            before = content.split(start_marker)[0]
            after_temp = content.split(start_marker)[1]
            after = after_temp.split(end_marker)[1]
            
            # Reconstruct with new layout
            content = before + new_layout + end_marker + after
            print("[SUCCESS] Replaced with side-by-side comparison layout")
        else:
            print("[ERROR] Could not find end marker")
            return
    else:
        print("[ERROR] Could not find start marker")
        return
    
    # Now update JavaScript to calculate WITH TREATMENT 3-year projection
    old_js = '''            // NO TREATMENT scenario - FULL 3-YEAR PROJECTION
            // Same calculation as 3-Year Degradation Chart
            const baselineLoss = annualLoss; // Year 0 (2025)
            const degradationRate = 0.15; // 15% annual increase
            
            // Calculate all 4 years (synchronized with chart)
            const year0Loss = baselineLoss;
            const year1Loss = baselineLoss * (1 + degradationRate);
            const year2Loss = baselineLoss * Math.pow(1 + degradationRate, 2);
            const year3Loss = baselineLoss * Math.pow(1 + degradationRate, 3);
            
            // Calculate cumulative 3-year loss
            const cumulativeLoss = year0Loss + year1Loss + year2Loss + year3Loss;
            
            // Update each year display
            document.getElementById('noTreatment_year0').textContent = formatLossMiliar(year0Loss);
            document.getElementById('noTreatment_year1').textContent = formatLossMiliar(year1Loss);
            document.getElementById('noTreatment_year2').textContent = formatLossMiliar(year2Loss);
            document.getElementById('noTreatment_year3').textContent = formatLossMiliar(year3Loss);
            document.getElementById('noTreatment_cumulative').textContent = formatLossMiliar(cumulativeLoss);'''
    
    new_js = '''            // 3-YEAR PROJECTION - NO TREATMENT vs WITH TREATMENT
            const baselineLoss = annualLoss;
            const degradationRate = 0.15;
            const treatmentEffectiveness = 0.70;
            
            // NO TREATMENT: Losses increase by 15% annually
            const noTx_year0 = baselineLoss;
            const noTx_year1 = baselineLoss * (1 + degradationRate);
            const noTx_year2 = baselineLoss * Math.pow(1 + degradationRate, 2);
            const noTx_year3 = baselineLoss * Math.pow(1 + degradationRate, 3);
            const noTx_cumulative = noTx_year0 + noTx_year1 + noTx_year2 + noTx_year3;
            
            // WITH TREATMENT: Progressive reduction (synchronized with chart)
            const withTx_year0 = baselineLoss; // Same starting point
            const withTx_year1 = baselineLoss * (1 - treatmentEffectiveness * 0.5); // 50% reduction in Y1
            const withTx_year2 = baselineLoss * (1 - treatmentEffectiveness * 0.8); // 80% reduction in Y2
            const withTx_year3 = baselineLoss * (1 - treatmentEffectiveness); // Full 70% reduction in Y3
            const withTx_cumulative = withTx_year0 + withTx_year1 + withTx_year2 + withTx_year3;
            
            // SAVINGS CALCULATION
            const totalSavings = noTx_cumulative - withTx_cumulative;
            const savingsPercent = ((totalSavings / noTx_cumulative) * 100);
            
            // Update NO TREATMENT displays
            document.getElementById('noTreatment_year0').textContent = formatLossMiliar(noTx_year0);
            document.getElementById('noTreatment_year1').textContent = formatLossMiliar(noTx_year1);
            document.getElementById('noTreatment_year2').textContent = formatLossMiliar(noTx_year2);
            document.getElementById('noTreatment_year3').textContent = formatLossMiliar(noTx_year3);
            document.getElementById('noTreatment_cumulative').textContent = formatLossMiliar(noTx_cumulative);
            
            // Update WITH TREATMENT displays
            document.getElementById('withTreatment_year0').textContent = formatLossMiliar(withTx_year0);
            document.getElementById('withTreatment_year1').textContent = formatLossMiliar(withTx_year1);
            document.getElementById('withTreatment_year2').textContent = formatLossMiliar(withTx_year2);
            document.getElementById('withTreatment_year3').textContent = formatLossMiliar(withTx_year3);
            document.getElementById('withTreatment_cumulative').textContent = formatLossMiliar(withTx_cumulative);
            
            // Update SAVINGS displays
            document.getElementById('treatment_totalSavings').textContent = formatLossMiliar(totalSavings);
            document.getElementById('treatment_savingsPercent').textContent = savingsPercent.toFixed(0) + '%';'''
    
    if old_js in content:
        content = content.replace(old_js, new_js)
        print("[SUCCESS] Updated JavaScript with WITH TREATMENT calculations")
    else:
        print("[WARNING] Could not find JS section to update")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ Enhancements:")
    print("  1. Side-by-side comparison: NO TREATMENT vs WITH TREATMENT")
    print("  2. Both show full 3-year projections")
    print("  3. Larger cumulative totals (text-3xl)")
    print("  4. Savings highlight panel showing:")
    print("     - Total 3-year savings (text-5xl!)")
    print("     - Savings percentage")
    print("  5. Visual differentiation (red vs green)")

if __name__ == '__main__':
    create_sidebyside_comparison()
