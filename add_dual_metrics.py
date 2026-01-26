"""
Script untuk update Treatment Impact Analysis dengan 2 metrik:
1. Baseline 2025 (current loss)
2. Projected 2026-2028 (dengan degradation rate yang sama dengan chart)
"""

def update_treatment_metrics():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Updating Treatment Impact Analysis metrics...")
    
    # 1. Update HTML structure to show both metrics
    old_no_treatment = '''                                <div class="space-y-3">
                                    <div>
                                        <div class="text-xs text-red-200/60 font-bold mb-1">ANNUAL LOSS (2026)</div>
                                        <div class="text-4xl font-black text-red-400" id="noTreatment_loss">Rp 602 Jt
                                        </div>
                                    </div>'''
    
    new_no_treatment = '''                                <div class="space-y-3">
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
    
    if old_no_treatment in content:
        content = content.replace(old_no_treatment, new_no_treatment)
        print("[SUCCESS] Updated NO TREATMENT section HTML")
    else:
        print("[WARNING] Could not find NO TREATMENT section - may need manual update")
    
    # 2. Update JavaScript calculation in updateDivisionSummary
    old_calc = '''            // NO TREATMENT scenario
            document.getElementById('noTreatment_loss').textContent = formatLossMiliar(annualLoss);
            document.getElementById('noTreatment_gap').textContent = `${Math.round(totalProductionGap)} Ton`;
            document.getElementById('noTreatment_critical').textContent =
                `${metrics.criticalBlocks} / ${metrics.totalBlocks} (${metrics.criticalRate.toFixed(0)}%)`;'''
    
    new_calc = '''            // NO TREATMENT scenario - Show BOTH baseline and projected
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
    
    if old_calc in content:
        content = content.replace(old_calc, new_calc)
        print("[SUCCESS] Updated NO TREATMENT calculation logic")
    else:
        print("[WARNING] Could not find calculation section")
    
    # 3. Also update WITH TREATMENT to use baseline for comparison
    old_treatment_calc = '''            // WITH TREATMENT scenario (70% effectiveness)
            const reducedLoss = annualLoss * 0.30; // 70% prevented'''
    
    new_treatment_calc = '''            // WITH TREATMENT scenario (70% effectiveness)
            // Compare against projected 2026 loss (not baseline)
            const reducedLoss = projectedLoss2026 * 0.30; // 70% prevented from projected loss'''
    
    if old_treatment_calc in content:
        content = content.replace(old_treatment_calc, new_treatment_calc)
        print("[SUCCESS] Updated WITH TREATMENT calculation to use projected loss")
    
    # 4. Update WITH TREATMENT savings calculation
    old_savings = '''            document.getElementById('withTreatment_loss').innerHTML =
                `${formatLossMiliar(reducedLoss)}<span class="text-lg ml-2 text-emerald-300">↓${Math.round((1 - reducedLoss / annualLoss) * 100)}%</span>`;'''
    
    new_savings = '''            const savingsPercent = Math.round((1 - reducedLoss / projectedLoss2026) * 100);
            document.getElementById('withTreatment_loss').innerHTML =
                `${formatLossMiliar(reducedLoss)}<span class="text-lg ml-2 text-emerald-300">↓${savingsPercent}%</span>`;'''
    
    if old_savings in content:
        content = content.replace(old_savings, new_savings)
        print("[SUCCESS] Updated savings percentage to use projected base")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ Changes Summary:")
    print("  1. Added 'Baseline Loss (2025)' metric - shows current year actual")
    print("  2. Added 'Projected Loss (2026)' metric - shows Year 1 projection (+15%)")
    print("  3. Updated WITH TREATMENT to compare against projected (not baseline)")
    print("  4. Now fully synchronized with 3-Year Degradation Model chart")
    print("\n📊 Calculation Logic:")
    print("  • Baseline 2025 = metrics.totalGanodermaLoss")
    print("  • Projected 2026 = Baseline × 1.15 (15% degradation)")
    print("  • Treatment reduces projected loss by 70%")
    print("\n💡 This matches the 3-Year Degradation Model chart exactly!")

if __name__ == '__main__':
    update_treatment_metrics()
