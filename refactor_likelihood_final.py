import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================
    # STEP 1: REMOVE TREND CHART SECTION
    # ============================================
    
    # Find and remove the entire trend chart div block
    trend_chart_start = '<!-- 2. ATTACK RATE TREND (Mini Chart Placeholder) -->'
    trend_chart_end = '</div>\n                \n            <!-- 3. TIME TO CRITICAL PROJECTION -->'
    
    idx_start = content.find(trend_chart_start)
    if idx_start != -1:
        idx_end = content.find(trend_chart_end, idx_start)
        if idx_end != -1:
            # Remove the entire trend chart block
            content = content[:idx_start] + content[idx_end:]
            print("✅ Removed historical trend chart section")
    
    # ============================================
    # STEP 2: ADD FORMULA DISCLAIMER & PARAMETER ADJUSTER
    # ============================================
    
    # Find the Likelihood Score section
    likelihood_score_marker = '<!-- 1. LIKELIHOOD SCORE (Gauge) -->'
    idx_likelihood = content.find(likelihood_score_marker)
    
    if idx_likelihood != -1:
        # Find the end of likelihood score div (before Time to Critical)
        time_critical_marker = '<!-- 3. TIME TO CRITICAL PROJECTION -->'
        idx_time_critical = content.find(time_critical_marker, idx_likelihood)
        
        # Insert Formula Disclaimer & Parameter Adjuster BEFORE Time to Critical
        adjuster_html = '''
            
            <!-- FORMULA DISCLAIMER & PARAMETERS -->
            <div class="bg-black/20 rounded-2xl p-4 border border-blue-500/10">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest">Formula Parameters</span>
                    <button id="toggleFormulaInfo" class="text-xs text-blue-400 hover:text-blue-200 underline">
                        ℹ️ Info
                    </button>
                </div>
                
                <!-- Collapsible Formula Explanation -->
                <div id="formulaExplanation" class="hidden mb-4 p-3 bg-slate-900/50 rounded-lg border border-blue-500/20">
                    <p class="text-xs text-blue-200 leading-relaxed mb-2">
                        <strong>Formula Basis:</strong> Likelihood score dihitung berdasarkan:
                    </p>
                    <ul class="text-xs text-blue-300 space-y-1 ml-4">
                        <li>• <strong>Attack Rate (AR):</strong> Primary indicator (40-95% range)</li>
                        <li>• <strong>SPH Density:</strong> Spread risk modifier (+5-10%)</li>
                    </ul>
                    <p class="text-xs text-yellow-300 mt-2 italic">
                        ⚠️ <strong>Note:</strong> Formula ini adalah estimasi empiris. 
                        Nilai aktual bergantung pada validasi <strong>domain expert</strong> dan kondisi lapangan spesifik.
                    </p>
                </div>
                
                <!-- Adjustable Weight Sliders -->
                <div class="space-y-3">
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">AR Weight</span>
                            <span class="text-white font-black" id="arWeightValue">1.0x</span>
                        </div>
                        <input type="range" id="arWeightSlider" min="0.5" max="2.0" step="0.1" value="1.0"
                            class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">SPH Modifier</span>
                            <span class="text-white font-black" id="sphModifierValue">1.0x</span>
                        </div>
                        <input type="range" id="sphModifierSlider" min="0" max="2.0" step="0.1" value="1.0"
                            class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    
                    <button id="recalculateLikelihood" 
                        class="w-full mt-2 px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black uppercase rounded-lg transition-colors">
                        🔄 Recalculate
                    </button>
                </div>
            </div>
            
            '''
        
        content = content[:idx_time_critical] + adjuster_html + content[idx_time_critical:]
        print("✅ Added formula disclaimer & parameter adjuster")
    
    # ============================================
    # STEP 3: CHANGE LAYOUT - MOVE VANISHING YIELD TO BOTTOM
    # ============================================
    
    # Current structure:
    # <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
    #    [Financial - col-span-1]
    #    [Likelihood - col-span-1]
    #    [Vanishing - col-span-1]
    # </div>
    
    # Target structure:
    # <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
    #    [Financial - col-span-1]
    #    [Likelihood - col-span-1]
    # </div>
    # [Vanishing - full width below]
    
    # Find the grid container
    grid_marker = '<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">'
    idx_grid = content.find(grid_marker)
    
    if idx_grid != -1:
        # Change grid from 3 cols to 2 cols
        content = content.replace(
            '<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">',
            '<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">',
            1  # Only first occurrence
        )
        print("✅ Changed grid from 3 columns to 2 columns")
        
        # Find Vanishing Yield component start
        vanishing_marker = '<div class="lg:col-span-1 h-full"><div'
        # Need to find the THIRD occurrence (after Financial and Likelihood)
        
        # Strategy: Find all col-span-1 divs, extract the 3rd one (Vanishing)
        # Then move it outside the grid
        
        # Find closing of grid </div> (the one that closes grid container)
        # Count div balance to find correct closing
        
        # Simpler approach: Find Vanishing component by unique marker inside it
        vanishing_content_marker = '>VANISHING YIELD ANALYSIS<'
        idx_vanishing_h2 = content.find(vanishing_content_marker)
        
        if idx_vanishing_h2 != -1:
            # Backtrack to find the opening <div class="lg:col-span-1 h-full">
            # Search backwards for the nearest col-span-1
            search_start = max(0, idx_vanishing_h2 - 500)
            vanishing_col_start_marker = '<div class="lg:col-span-1 h-full">'
            idx_vanishing_col = content.rfind(vanishing_col_start_marker, search_start, idx_vanishing_h2)
            
            if idx_vanishing_col != -1:
                # Find the closing of this column div
                # Use div balance counter
                def find_closing_div(text, start_pos):
                    balance = 0
                    pos = start_pos
                    while pos < len(text):
                        if text[pos:pos+4] == '<div':
                            balance += 1
                            pos += 4
                        elif text[pos:pos+6] == '</div>':
                            balance -= 1
                            if balance == 0:
                                return pos + 6
                            pos += 6
                        else:
                            pos += 1
                    return -1
                
                idx_vanishing_end = find_closing_div(content, idx_vanishing_col)
                
                if idx_vanishing_end != -1:
                    # Extract Vanishing component
                    vanishing_html = content[idx_vanishing_col:idx_vanishing_end]
                    
                    # Remove from grid (leave empty space for now)
                    content = content[:idx_vanishing_col] + content[idx_vanishing_end:]
                    
                    # Find grid closing div (after Financial + Likelihood)
                    # Search for </div></div> pattern that closes grid and its parent
                    grid_close_marker = '</div>\n</div></div>'
                    idx_after_grid = content.find(grid_close_marker, idx_grid)
                    
                    if idx_after_grid != -1:
                        # Insert Vanishing AFTER grid (with spacing)
                        vanishing_full_width = f'\n\n<!-- Vanishing Yield - Full Width Below -->\n{vanishing_html}\n'
                        insert_pos = idx_after_grid + len(grid_close_marker)
                        content = content[:insert_pos] + vanishing_full_width + content[insert_pos:]
                        print("✅ Moved Vanishing Yield to bottom (full width)")
    
    # ============================================
    # STEP 4: UPDATE JAVASCRIPT FOR PARAMETER ADJUSTERS
    # ============================================
    
    # Find the existing updateLikelihoodMetrics function
    js_func_marker = 'function updateLikelihoodMetrics(blockData) {'
    idx_js_func = content.find(js_func_marker)
    
    if idx_js_func != -1:
        # Find end of function (closing brace)
        idx_func_end = content.find('\n    }', idx_js_func + 100)
        
        # Replace the function with enhanced version
        new_js_function = '''
    function updateLikelihoodMetrics(blockData) {
        if (!blockData) return;
        
        const ar = blockData.arNdre || 0;
        const sph = blockData.sph || 0;
        
        // Get user-adjusted weights
        const arWeight = parseFloat(document.getElementById('arWeightSlider')?.value || 1.0);
        const sphModifier = parseFloat(document.getElementById('sphModifierSlider')?.value || 1.0);
        
        // 1. CALCULATE LIKELIHOOD SCORE (with adjustable weights)
        let likelihoodScore = 0;
        
        if (ar >= 5) {
            likelihoodScore = 75 + (ar - 5) * 5;
        } else if (ar >= 2) {
            likelihoodScore = 40 + (ar - 2) * 10;
        } else {
            likelihoodScore = ar * 20;
        }
        
        // Apply AR weight adjustment
        likelihoodScore = likelihoodScore * arWeight;
        
        // SPH modifier (adjustable)
        let sphBonus = 0;
        if (sph > 130) {
            sphBonus = 10;
        } else if (sph > 120) {
            sphBonus = 5;
        }
        sphBonus = sphBonus * sphModifier;
        likelihoodScore += sphBonus;
        
        likelihoodScore = Math.min(95, Math.max(0, likelihoodScore));
        
        // Update UI
        document.getElementById('likelihoodScore').textContent = Math.round(likelihoodScore);
        document.getElementById('likelihoodBar').style.width = likelihoodScore + '%';
        
        // 2. TIME TO CRITICAL (SPH < 100)
        let monthsToCritical = 0;
        
        if (sph > 100) {
            const sphDeficit = sph - 100;
            const monthlyDecline = ar * 0.5;
            monthsToCritical = Math.ceil(sphDeficit / monthlyDecline);
        } else {
            monthsToCritical = 0;
        }
        
        monthsToCritical = Math.max(1, Math.min(36, monthsToCritical));
        
        document.getElementById('timeTocrítica').textContent = monthsToCritical;
        
        const timelineProgress = Math.max(0, 100 - (monthsToCritical * 2.5));
        document.getElementById('timelineBar').style.width = timelineProgress + '%';
    }
    
    // Toggle formula explanation
    document.getElementById('toggleFormulaInfo')?.addEventListener('click', function() {
        const explanation = document.getElementById('formulaExplanation');
        explanation.classList.toggle('hidden');
    });
    
    // Update weight display values
    document.getElementById('arWeightSlider')?.addEventListener('input', function() {
        document.getElementById('arWeightValue').textContent = parseFloat(this.value).toFixed(1) + 'x';
    });
    
    document.getElementById('sphModifierSlider')?.addEventListener('input', function() {
        document.getElementById('sphModifierValue').textContent = parseFloat(this.value).toFixed(1) + 'x';
    });
    
    // Recalculate button
    document.getElementById('recalculateLikelihood')?.addEventListener('click', function() {
        const selector = document.getElementById('globalSelectorLeft');
        const selectedBlock = selector?.value;
        if (selectedBlock && window.BLOCKS_DATA) {
            const blockData = window.BLOCKS_DATA[selectedBlock];
            updateLikelihoodMetrics(blockData);
        }
    });
    '''
        
        content = content[:idx_js_func] + new_js_function + content[idx_func_end+5:]
        print("✅ Updated JavaScript with parameter adjustment logic")
    
    # Remove trend chart initialization from JS
    trend_init_marker = 'function initializeLikelihoodAnalysis() {'
    idx_trend_init = content.find(trend_init_marker)
    if idx_trend_init != -1:
        # Find end of this function
        idx_init_end = content.find('\n    }\n    \n    function updateLikelihoodMetrics', idx_trend_init)
        if idx_init_end != -1:
            # Remove the entire initializeLikelihoodAnalysis function
            content = content[:idx_trend_init] + content[idx_init_end+9:]
            print("✅ Removed trend chart initialization JS")
            
            # Also remove the call to initializeLikelihoodAnalysis
            init_call = 'initializeLikelihoodAnalysis();'
            content = content.replace(init_call, '// Trend chart removed - no historical data available')
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n" + "="*60)
    print("✅ ALL CHANGES APPLIED SUCCESSFULLY!")
    print("="*60)
    print("\nSummary:")
    print("  1. ✅ Removed historical trend chart")
    print("  2. ✅ Added formula disclaimer with expert note")
    print("  3. ✅ Added adjustable parameter sliders (AR Weight, SPH Modifier)")
    print("  4. ✅ Repositioned layout:")
    print("      - Top: Financial + Likelihood (side-by-side)")
    print("      - Bottom: Vanishing Yield (full width)")

if __name__ == "__main__":
    main()
