import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if slider event handlers exist in the updateLikelihoodMetrics function
    if 'arWeightSlider' not in content and 'sphModifierSlider' not in content:
        print("⚠️  Slider JavaScript handlers NOT found - need to add")
        
        # Find the integration script we added
        integration_marker = '// LIKELIHOOD INTEGRATION FIX'
        idx_integration = content.find(integration_marker)
        
        if idx_integration != -1:
            # Find the end of this script block
            script_end = content.find('</script>', idx_integration)
            
            # Add slider handlers before the closing script tag
            slider_js = '''
    
    // ========================================
    // SLIDER EVENT HANDLERS
    // ========================================
    
    // Update AR Weight display
    document.addEventListener('DOMContentLoaded', function() {
        const arSlider = document.getElementById('arWeightSlider');
        if (arSlider) {
            arSlider.addEventListener('input', function() {
                const valueEl = document.getElementById('arWeightValue');
                if (valueEl) {
                    valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
                }
            });
        }
        
        // Update SPH Modifier display
        const sphSlider = document.getElementById('sphModifierSlider');
        if (sphSlider) {
            sphSlider.addEventListener('input', function() {
                const valueEl = document.getElementById('sphModifierValue');
                if (valueEl) {
                    valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
                }
            });
        }
        
        // Toggle formula explanation
        const toggleBtn = document.getElementById('toggleFormulaInfo');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                const explanation = document.getElementById('formulaExplanation');
                if (explanation) {
                    explanation.classList.toggle('hidden');
                }
            });
        }
        
        // Recalculate button
        const recalcBtn = document.getElementById('recalculateLikelihood');
        if (recalcBtn) {
            recalcBtn.addEventListener('click', function() {
                console.log('🔄 Manual recalculate triggered');
                const selector = document.getElementById('globalSelectorLeft');
                const selectedBlock = selector?.value;
                
                if (!selectedBlock) {
                    console.warn('⚠️  No block selected for recalculation');
                    return;
                }
                
                const DATA = window.BLOCKS_DATA || BLOCKS_DATA;
                const blockData = DATA?.[selectedBlock];
                
                if (blockData && typeof updateLikelihoodMetrics === 'function') {
                    updateLikelihoodMetrics(blockData);
                    console.log('✅ Likelihood recalculated with adjusted parameters');
                } else {
                    console.error('❌ Cannot recalculate - data or function missing');
                }
            });
        }
    });
'''
            
            # Insert before </script>
            content = content[:script_end] + slider_js + '\n' + content[script_end:]
            print("✅ Added slider event handlers")
        else:
            print("ERROR: Integration script not found")
            return
    else:
        print("✅ Slider handlers already exist")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Slider functionality complete")
    print("Please refresh browser and test sliders")

if __name__ == "__main__":
    main()
