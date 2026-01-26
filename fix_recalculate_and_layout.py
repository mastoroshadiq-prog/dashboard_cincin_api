import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # ============================================
    # FIX 1: Update updateLikelihoodMetrics to use slider values
    # ============================================
    
    # Find the function
    func_marker = 'function updateLikelihoodMetrics(blockData) {'
    idx_func = content.find(func_marker)
    
    if idx_func != -1:
        # Find the end of the function
        # Look for the closing brace
        brace_count = 1
        idx = idx_func + len(func_marker)
        while idx < len(content) and brace_count > 0:
            if content[idx] == '{':
                brace_count += 1
            elif content[idx] == '}':
                brace_count -= 1
            idx += 1
        
        idx_func_end = idx
        
        # Replace entire function with corrected version
        new_function = '''function updateLikelihoodMetrics(blockData) {
    if (!blockData) return;
    
    console.log('📊 updateLikelihoodMetrics called with:', blockData);
    
    const ar = blockData.arNdre || 0;
    const sph = blockData.sph || 0;
    
    // Get user-adjusted weights from sliders
    const arSlider = document.getElementById('arWeightSlider');
    const sphSlider = document.getElementById('sphModifierSlider');
    
    const arWeight = arSlider ? parseFloat(arSlider.value) : 1.0;
    const sphModifier = sphSlider ? parseFloat(sphSlider.value) : 1.0;
    
    console.log('🎛️  Using weights - AR:', arWeight, 'SPH:', sphModifier);
    
    // 1. CALCULATE LIKELIHOOD SCORE (with adjustable weights)
    let likelihoodScore = 0;
    
    if (ar >= 5) {
        likelihoodScore = 75 + (ar - 5) * 5;
    } else if (ar >= 2) {
        likelihoodScore = 40 + (ar - 2) * 10;
    } else {
        likelihoodScore = ar * 20;
    }
    
    console.log('📈 Base likelihood score:', likelihoodScore);
    
    // Apply AR weight adjustment
    likelihoodScore = likelihoodScore * arWeight;
    console.log('📈 After AR weight adjustment:', likelihoodScore);
    
    // SPH modifier (adjustable)
    let sphBonus = 0;
    if (sph > 130) {
        sphBonus = 10;
    } else if (sph > 120) {
        sphBonus = 5;
    }
    sphBonus = sphBonus * sphModifier;
    likelihoodScore += sphBonus;
    
    console.log('📈 SPH bonus:', sphBonus, '→ Final score:', likelihoodScore);
    
    likelihoodScore = Math.min(95, Math.max(0, likelihoodScore));
    
    // Update UI
    const scoreEl = document.getElementById('likelihoodScore');
    const barEl = document.getElementById('likelihoodBar');
    if (scoreEl) {
        scoreEl.textContent = Math.round(likelihoodScore);
        console.log('✅ Updated score display:', Math.round(likelihoodScore));
    }
    if (barEl) {
        barEl.style.width = likelihoodScore + '%';
    }
    
    // 2. TIME TO CRITICAL (SPH < 100)
    let monthsToCritical = 0;
    
    if (sph > 100) {
        const sphDeficit = sph - 100;
        const monthlyDecline = Math.max(ar * 0.5, 0.1);
        monthsToCritical = Math.ceil(sphDeficit / monthlyDecline);
    } else {
        monthsToCritical = 0;
    }
    
    monthsToCritical = Math.max(1, Math.min(36, monthsToCritical));
    
    const timeEl = document.getElementById('timeTocrítica');
    const timelineEl = document.getElementById('timelineBar');
    if (timeEl) {
        timeEl.textContent = monthsToCritical;
        console.log('✅ Updated time-to-critical:', monthsToCritical, 'months');
    }
    
    if (timelineEl) {
        const timelineProgress = Math.max(0, 100 - (monthsToCritical * 2.5));
        timelineEl.style.width = timelineProgress + '%';
    }
}
'''
        
        content = content[:idx_func] + new_function + content[idx_func_end:]
        print("✅ Fixed updateLikelihoodMetrics to read slider values")
    
    # ============================================
    # FIX 2: Verify Vanishing Yield layout
    # ============================================
    
    # Check if Vanishing Yield is in correct position (after grid closing)
    # Look for the pattern: grid closing → vanishing component
    
    vanishing_marker = '>VANISHING YIELD ANALYSIS<'
    idx_vanishing = content.find(vanishing_marker)
    
    if idx_vanishing != -1:
        # Check if it's inside a lg:col-span-1 (wrong) or standalone (correct)
        search_back = content[max(0, idx_vanishing-500):idx_vanishing]
        
        if 'lg:col-span-1' in search_back:
            print("⚠️  Vanishing Yield is still in column layout - needs repositioning")
            print("   (This was supposed to be fixed in previous script)")
            # The earlier script should have moved it - if not, that's the issue
        else:
            print("✅ Vanishing Yield appears to be in standalone position")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Recalculate fix applied")
    print("\nPlease refresh and test:")
    print("  1. Select a block")
    print("  2. Note the initial Likelihood Score")
    print("  3. Move AR Weight slider to 0.5x")
    print("  4. Click Recalculate")
    print("  5. Score should DECREASE")
    print("  6. Check console for debug logs")

if __name__ == "__main__":
    main()
