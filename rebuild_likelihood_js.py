import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the LIKELIHOOD & TREND ANALYSIS LOGIC section
    marker = '// ========================================'
    likelihood_section_start = content.find('// LIKELIHOOD & TREND ANALYSIS LOGIC')
    
    if likelihood_section_start == -1:
        print("⚠️  Likelihood script section not found - need to add it from scratch")
        
        # Find a safe injection point - before closing </body>
        body_close = content.rfind('</body>')
        
        if body_close == -1:
            print("ERROR: Could not find </body> tag")
            return
        
        # Create complete, clean JavaScript
        clean_js = '''
<script>
// ========================================
// LIKELIHOOD & TREND ANALYSIS LOGIC
// ========================================

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
    const scoreEl = document.getElementById('likelihoodScore');
    const barEl = document.getElementById('likelihoodBar');
    if (scoreEl) scoreEl.textContent = Math.round(likelihoodScore);
    if (barEl) barEl.style.width = likelihoodScore + '%';
    
    // 2. TIME TO CRITICAL (SPH < 100)
    let monthsToCritical = 0;
    
    if (sph > 100) {
        const sphDeficit = sph - 100;
        const monthlyDecline = Math.max(ar * 0.5, 0.1); // Prevent division by zero
        monthsToCritical = Math.ceil(sphDeficit / monthlyDecline);
    } else {
        monthsToCritical = 0;
    }
    
    monthsToCritical = Math.max(1, Math.min(36, monthsToCritical));
    
    const timeEl = document.getElementById('timeTocrítica');
    const timelineEl = document.getElementById('timelineBar');
    if (timeEl) timeEl.textContent = monthsToCritical;
    
    if (timelineEl) {
        const timelineProgress = Math.max(0, 100 - (monthsToCritical * 2.5));
        timelineEl.style.width = timelineProgress + '%';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 Initializing Likelihood Analysis...');
    
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
    
    // Update weight display values
    const arSlider = document.getElementById('arWeightSlider');
    if (arSlider) {
        arSlider.addEventListener('input', function() {
            const valueEl = document.getElementById('arWeightValue');
            if (valueEl) {
                valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
            }
        });
    }
    
    const sphSlider = document.getElementById('sphModifierSlider');
    if (sphSlider) {
        sphSlider.addEventListener('input', function() {
            const valueEl = document.getElementById('sphModifierValue');
            if (valueEl) {
                valueEl.textContent = parseFloat(this.value).toFixed(1) + 'x';
            }
        });
    }
    
    // Recalculate button
    const recalcBtn = document.getElementById('recalculateLikelihood');
    if (recalcBtn) {
        recalcBtn.addEventListener('click', function() {
            const selector = document.getElementById('globalSelectorLeft');
            const selectedBlock = selector?.value;
            if (selectedBlock && window.BLOCKS_DATA) {
                const blockData = window.BLOCKS_DATA[selectedBlock];
                updateLikelihoodMetrics(blockData);
            }
        });
    }
    
    // Hook into existing block selection logic
    const selector = document.getElementById('globalSelectorLeft');
    if (selector) {
        selector.addEventListener('change', function() {
            const selectedBlock = this.value;
            if (selectedBlock && window.BLOCKS_DATA) {
                const blockData = window.BLOCKS_DATA[selectedBlock];
                updateLikelihoodMetrics(blockData);
            }
        });
    }
});
</script>
'''
        
        # Inject before </body>
        content = content[:body_close] + clean_js + '\n' + content[body_close:]
        print("✅ Added clean Likelihood Analysis JavaScript")
    
    else:
        print("Likelihood script section found - checking for issues...")
        
        # Find the end of this section
        # Look for next </script> after the section start
        script_close = content.find('</script>', likelihood_section_start)
        
        if script_close != -1:
            print("✅ Script section structure looks okay")
        else:
            print("⚠️  Script section missing closing tag!")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Syntax error fix complete")
    print("Please refresh browser and check console")

if __name__ == "__main__":
    main()
