import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the integration script and add slider/button handlers INSIDE it
    integration_marker = "console.log('✅ Likelihood integration complete');"
    idx_integration_log = content.find(integration_marker)
    
    if idx_integration_log == -1:
        print("ERROR: Integration script not found")
        return
    
    # Add handlers BEFORE the final console.log
    handlers_script = '''
        
        // ========================================
        // SLIDER & BUTTON HANDLERS
        // ========================================
        
        // AR Weight Slider - Update display value
        const arSlider = document.getElementById('arWeightSlider');
        if (arSlider) {
            arSlider.addEventListener('input', function() {
                const valueEl = document.getElementById('arWeightValue');
                if (valueEl) {
                    valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
                }
            });
            console.log('✅ AR Weight slider handler attached');
        } else {
            console.warn('⚠️  arWeightSlider not found');
        }
        
        // SPH Modifier Slider - Update display value
        const sphSlider = document.getElementById('sphModifierSlider');
        if (sphSlider) {
            sphSlider.addEventListener('input', function() {
                const valueEl = document.getElementById('sphModifierValue');
                if (valueEl) {
                    valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
                }
            });
            console.log('✅ SPH Modifier slider handler attached');
        } else {
            console.warn('⚠️  sphModifierSlider not found');
        }
        
        // Toggle Formula Info button
        const toggleBtn = document.getElementById('toggleFormulaInfo');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                const explanation = document.getElementById('formulaExplanation');
                if (explanation) {
                    explanation.classList.toggle('hidden');
                    console.log('ℹ️  Formula explanation toggled');
                }
            });
            console.log('✅ Formula info toggle handler attached');
        } else {
            console.warn('⚠️  toggleFormulaInfo button not found');
        }
        
        // Recalculate Button - Manual recalculation
        const recalcBtn = document.getElementById('recalculateLikelihood');
        if (recalcBtn) {
            recalcBtn.addEventListener('click', function() {
                console.log('🔄 RECALCULATE BUTTON CLICKED');
                
                const selector = document.getElementById('globalSelectorLeft');
                if (!selector) {
                    console.error('❌ Selector not found');
                    return;
                }
                
                const selectedBlock = selector.value;
                if (!selectedBlock) {
                    console.warn('⚠️  No block selected - please select a block first');
                    alert('Please select a block first!');
                    return;
                }
                
                // Get data
                const DATA = window.BLOCKS_DATA || BLOCKS_DATA;
                if (!DATA) {
                    console.error('❌ BLOCKS_DATA not found');
                    return;
                }
                
                const blockData = DATA[selectedBlock];
                if (!blockData) {
                    console.error('❌ Block data not found for:', selectedBlock);
                    return;
                }
                
                // Call update function
                if (typeof updateLikelihoodMetrics === 'function') {
                    updateLikelihoodMetrics(blockData);
                    console.log('✅ Recalculated with adjusted parameters');
                } else {
                    console.error('❌ updateLikelihoodMetrics function not found');
                }
            });
            console.log('✅ Recalculate button handler attached');
        } else {
            console.warn('⚠️  recalculateLikelihood button not found');
        }
        
'''
    
    # Insert handlers before final log
    content = content[:idx_integration_log] + handlers_script + '\n        ' + content[idx_integration_log:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Added all slider and button event handlers")
    print("\nEvent handlers added:")
    print("  • AR Weight Slider → Updates display value")
    print("  • SPH Modifier Slider → Updates display value")
    print("  • Toggle Formula Info → Toggles explanation visibility")
    print("  • Recalculate Button → Triggers updateLikelihoodMetrics()")
    print("\nPlease refresh browser and:")
    print("  1. Open Console (F12)")
    print("  2. Check for handler attachment logs")
    print("  3. Select a block")
    print("  4. Adjust sliders")
    print("  5. Click Recalculate - should see '🔄 RECALCULATE BUTTON CLICKED'")

if __name__ == "__main__":
    main()
