"""
Script untuk update Treatment Impact Analysis dengan FULL 3-year projection
(4 data points: Baseline 2025 + Year 1-3 projections)
"""

def add_full_3year_projection():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Adding FULL 3-year projection to Treatment Impact Analysis...")
    
    # 1. Update HTML structure to show 4 years (Baseline + 3 projections)
    old_no_treatment = '''                                <div class="space-y-3">
                                    <div class="bg-black/20 p-3 rounded-lg border border-red-500/20">
                                        <div class="text-xs text-red-200/80 font-bold mb-1 uppercase">📊 Baseline Loss (2025)</div>
                                        <div class="text-3xl font-black text-red-400" id="noTreatment_baseline">--</div>
                                        <div class="text-[9px] text-red-300/60 mt-1">Current year actual loss</div>
                                    </div>
                                    <div class="bg-black/30 p-3 rounded-lg border border-red-500/30">
                                        <div class="text-xs text-red-200/60 font-bold mb-1 uppercase">🔮 Projected Loss (2026)</div>
                                        <div class="text-4xl font-black text-red-400" id="noTreatment_projected">--</div>
                                        <div class="text-[9px] text-red-300/60 mt-1">+15% degradation rate (Year 1)</div>
                                    </div>'''
    
    new_no_treatment = '''                                <div class="space-y-2">
                                    <!-- 3-YEAR LOSS PROJECTION TABLE -->
                                    <div class="bg-black/30 rounded-lg border border-red-500/30 p-3">
                                        <div class="text-xs text-red-200/80 font-bold mb-2 uppercase">📈 3-Year Loss Projection (No Treatment)</div>
                                        
                                        <div class="grid grid-cols-4 gap-2 text-center">
                                            <!-- Year 0: Baseline 2025 -->
                                            <div class="bg-red-900/20 rounded-md p-2 border border-red-500/20">
                                                <div class="text-[9px] text-red-300/70 font-bold mb-1">2025<br/>(Baseline)</div>
                                                <div class="text-lg font-black text-red-400" id="noTreatment_year0">--</div>
                                            </div>
                                            
                                            <!-- Year 1: 2026 -->
                                            <div class="bg-red-900/30 rounded-md p-2 border border-red-500/30">
                                                <div class="text-[9px] text-red-300/70 font-bold mb-1">2026<br/>(+15%)</div>
                                                <div class="text-lg font-black text-red-400" id="noTreatment_year1">--</div>
                                            </div>
                                            
                                            <!-- Year 2: 2027 -->
                                            <div class="bg-red-900/40 rounded-md p-2 border border-red-500/40">
                                                <div class="text-[9px] text-red-300/70 font-bold mb-1">2027<br/>(+32%)</div>
                                                <div class="text-lg font-black text-red-400" id="noTreatment_year2">--</div>
                                            </div>
                                            
                                            <!-- Year 3: 2028 -->
                                            <div class="bg-red-900/50 rounded-md p-2 border-2 border-red-500/50">
                                                <div class="text-[9px] text-red-300/70 font-bold mb-1">2028<br/>(+52%)</div>
                                                <div class="text-xl font-black text-red-400" id="noTreatment_year3">--</div>
                                            </div>
                                        </div>
                                        
                                        <div class="mt-2 text-[9px] text-red-300/60 text-center">
                                            💀 Cumulative 3-Year Loss: <span class="font-bold text-red-400" id="noTreatment_cumulative">--</span>
                                        </div>
                                    </div>'''
    
    if old_no_treatment in content:
        content = content.replace(old_no_treatment, new_no_treatment)
        print("[SUCCESS] Updated NO TREATMENT section with 3-year projection table")
    else:
        print("[WARNING] Could not find NO TREATMENT section")
    
    # 2. Update JavaScript calculation
    old_calc = '''            // NO TREATMENT scenario - Show BOTH baseline and projected
            // Baseline 2025: Current year actual loss
            const baselineLoss2025 = annualLoss;
            
            // Projected 2026: Apply 15% annual degradation (consistent with 3-Year Chart)
            const degradationRate = 0.15;
            const projectedLoss2026 = baselineLoss2025 * (1 + degradationRate);
            
            document.getElementById('noTreatment_baseline').textContent = formatLossMiliar(baselineLoss2025);
            document.getElementById('noTreatment_projected').textContent = formatLossMiliar(projectedLoss2026);
            document.getElementById('noTreatment_gap').textContent = `${Math.round(totalProductionGap)} Ton`;
            document.getElementById('noTreatment_critical').textContent =
                `${metrics.criticalBlocks} / ${metrics.totalBlocks} (${metrics.criticalRate.toFixed(0)}%)`;
            
            console.log('[TREATMENT IMPACT] Baseline 2025:', baselineLoss2025, 'Jt | Projected 2026:', projectedLoss2026, 'Jt');'''
    
    new_calc = '''            // NO TREATMENT scenario - FULL 3-YEAR PROJECTION
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
            document.getElementById('noTreatment_cumulative').textContent = formatLossMiliar(cumulativeLoss);
            
            document.getElementById('noTreatment_gap').textContent = `${Math.round(totalProductionGap)} Ton`;
            document.getElementById('noTreatment_critical').textContent =
                `${metrics.criticalBlocks} / ${metrics.totalBlocks} (${metrics.criticalRate.toFixed(0)}%)`;
            
            console.log('[TREATMENT IMPACT] 3-Year Projection:', {
                year0: year0Loss,
                year1: year1Loss,
                year2: year2Loss,
                year3: year3Loss,
                cumulative: cumulativeLoss
            });'''
    
    if old_calc in content:
        content = content.replace(old_calc, new_calc)
        print("[SUCCESS] Updated calculation to full 3-year projection")
    else:
        print("[WARNING] Could not find calculation section")
    
    # 3. Update WITH TREATMENT to use Year 1 projection for comparison
    old_treatment = '''            // WITH TREATMENT scenario (70% effectiveness)
            // Compare against projected 2026 loss (not baseline)
            const reducedLoss = projectedLoss2026 * 0.30; // 70% prevented from projected loss'''
    
    new_treatment = '''            // WITH TREATMENT scenario (70% effectiveness)
            // Compare against Year 1 projected loss
            const reducedLoss = year1Loss * 0.30; // 70% prevented from Year 1 projection'''
    
    if old_treatment in content:
        content = content.replace(old_treatment, new_treatment)
        print("[SUCCESS] Updated WITH TREATMENT to use year1Loss")
    
    # 4. Fix savings percentage calculation
    old_savings = '''            const savingsPercent = Math.round((1 - reducedLoss / projectedLoss2026) * 100);'''
    new_savings = '''            const savingsPercent = Math.round((1 - reducedLoss / year1Loss) * 100);'''
    
    if old_savings in content:
        content = content.replace(old_savings, new_savings)
        print("[SUCCESS] Updated savings calculation")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ Changes Summary:")
    print("  1. Added 4-column table showing Year 0-3 projections")
    print("  2. Year 0 (2025): Baseline")
    print("  3. Year 1 (2026): Baseline × 1.15 (+15%)")
    print("  4. Year 2 (2027): Baseline × 1.15² (+32%)")
    print("  5. Year 3 (2028): Baseline × 1.15³ (+52%)")
    print("  6. Added cumulative 3-year loss total")
    print("\n📊 Now FULLY synchronized with 3-Year Degradation Model Chart!")
    print("  • Same degradation rate (15%)")
    print("  • Same calculation formula")
    print("  • Same year-by-year values")

if __name__ == '__main__':
    add_full_3year_projection()
