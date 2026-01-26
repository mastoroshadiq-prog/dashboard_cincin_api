"""
Script untuk menambahkan function updatePaparanRisiko() yang sinkron dengan Treatment Impact Analysis
"""

def add_paparan_risiko_update():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert new function (after render3YearDegradationChart and before renderDivisionComparison)
    insertion_marker = "        /**\n         * Render Division Comparison Table"
    
    if insertion_marker not in content:
        print("[ERROR] Could not find insertion point")
        return
    
    # Create new function to update Paparan Risiko
    new_function = '''        /**
         * Update Paparan Risiko Section (synchronized with Division metrics)
         * @param {Object} metrics - Division metrics object
         */
        function updatePaparanRisiko(metrics) {
            console.log('[PAPARAN RISIKO] Updating with metrics:', metrics);
            
            // Calculate total loss from critical blocks only (Stadium 3+)
            // Use same source as Treatment Impact Analysis for consistency
            const totalLoss = metrics.totalGanodermaLoss; // in Juta
            const criticalCount = metrics.criticalBlocks;
            
            // Convert to Miliar for display
            const lossInMiliar = totalLoss / 1000;
            
            // Update main loss display
            document.getElementById('summaryTotalLoss').textContent = lossInMiliar.toFixed(2);
            
            // Update critical count
            document.getElementById('summaryCriticalCount').textContent = criticalCount;
            
            // Calculate risk area (area of critical blocks only)
            // Assuming critical blocks have proportional area
            const riskArea = metrics.totalArea * (criticalCount / metrics.totalBlocks);
            document.getElementById('summaryRiskArea').textContent = riskArea.toFixed(1);
            
            // Update title and badge
            const currentDivision = window.currentDivision || 'ALL';
            document.getElementById('paparanRiskTitle').textContent = 
                currentDivision === 'ALL' ? 'PAPARAN RISIKO ESTATE' : `PAPARAN RISIKO - ${currentDivision}`;
            
            document.getElementById('paparanRiskBadge').textContent = 
                `📍 Showing: ${currentDivision} Division (${criticalCount} Stadium 3+ critical blocks)`;
            
            console.log(`[PAPARAN RISIKO] Updated: Rp ${lossInMiliar.toFixed(2)} M from ${criticalCount} critical blocks`);
        }

        '''
    
    # Insert new function
    content = content.replace(insertion_marker, new_function + insertion_marker)
    
    # Now update updateDivisionSummary to call this function
    # Find where 3-year chart is rendered
    chart_call_marker = "            // FIX #3: Render 3-Year Degradation Model Chart\n            renderDegradationModelChart(metrics);"
    
    if chart_call_marker in content:
        new_marker = chart_call_marker + "\n\n            // Update Paparan Risiko section\n            updatePaparanRisiko(metrics);"
        content = content.replace(chart_call_marker, new_marker)
        print("[SUCCESS] Added updatePaparanRisiko() call to updateDivisionSummary()")
    else:
        print("[WARNING] Could not find chart call marker - manual update needed")
    
    # Update hardcoded text "(8 Blok Kritis)" to dynamic
    # Line 427-429
    old_label_1 = '''                        <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Total Potensi Kerugian
                            (8
                            Blok Kritis)</span>'''
    
    new_label_1 = '''                        <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1" id="paparanRiskLabel">Total Potensi Kerugian
                            (-- Blok Kritis)</span>'''
    
    if old_label_1 in content:
        content = content.replace(old_label_1, new_label_1)
        print("[SUCCESS] Made label 1 dynamic with ID 'paparanRiskLabel'")
    
    # Line 436-437
    old_label_2 = '''                        <p class="text-[10px] text-rose-300/80 mt-1 italic">*Akumulasi kerugian dari 8 blok berstatus
                            KRITIS
                        </p>'''
    
    new_label_2 = '''                        <p class="text-[10px] text-rose-300/80 mt-1 italic" id="paparanRiskDisclaimer">*Akumulasi kerugian dari blok berstatus KRITIS
                        </p>'''
    
    if old_label_2 in content:
        content = content.replace(old_label_2, new_label_2)
        print("[SUCCESS] Made label 2 dynamic with ID 'paparanRiskDisclaimer'")
    
    # Add label updates to updatePaparanRisiko function
    label_update_code = '''            
            // Update dynamic labels
            const labelEl = document.getElementById('paparanRiskLabel');
            if (labelEl) {
                labelEl.innerHTML = `Total Potensi Kerugian<br/>(${criticalCount} Blok Kritis)`;
            }
            
            const disclaimerEl = document.getElementById('paparanRiskDisclaimer');
            if (disclaimerEl) {
                disclaimerEl.textContent = `*Akumulasi kerugian dari ${criticalCount} blok berstatus KRITIS`;
            }
'''
    
    # Insert before console.log in updatePaparanRisiko
    function_end_marker = "            console.log(`[PAPARAN RISIKO]"
    if function_end_marker in content:
        content = content.replace(function_end_marker, label_update_code + "            console.log(`[PAPARAN RISIKO]")
        print("[SUCCESS] Added label update code to function")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ Changes made:")
    print("  1. Added updatePaparanRisiko() function")
    print("  2. Integrated with updateDivisionSummary()")
    print("  3. Made hardcoded labels dynamic")
    print("  4. Now uses same data source as Treatment Impact Analysis (metrics.totalGanodermaLoss)")
    print("\n💡 Result: Paparan Risiko will now show SAME loss as Treatment Impact Analysis")

if __name__ == '__main__':
    add_paparan_risiko_update()
