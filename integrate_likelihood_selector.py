import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where updateLikelihoodMetrics is called/hooked
    # We need to integrate it with existing block selection logic
    
    # Strategy: Find the main data population function and add our call there
    # Look for patterns like "selector.addEventListener" or "onChange"
    
    # Let's inject a GLOBAL event listener that hooks AFTER DOMContentLoaded
    # And make sure it calls updateLikelihoodMetrics whenever block changes
    
    # Find the closing </body> tag to inject our integration script
    body_close = content.rfind('</body>')
    
    if body_close == -1:
        print("ERROR: </body> not found")
        return
    
    # Create integration script
    integration_script = '''
<script>
// ========================================
// LIKELIHOOD INTEGRATION FIX
// ========================================
(function() {
    console.log('🔧 Integrating Likelihood Analysis with Block Selection...');
    
    // Wait for DOM and other scripts to load
    window.addEventListener('load', function() {
        const selector = document.getElementById('globalSelectorLeft');
        
        if (!selector) {
            console.warn('⚠️  globalSelectorLeft not found');
            return;
        }
        
        console.log('✅ Selector found, attaching listener...');
        
        // Add change event listener
        selector.addEventListener('change', function() {
            const selectedBlock = this.value;
            console.log('📊 Block changed to:', selectedBlock);
            
            if (!selectedBlock) {
                console.log('⚠️  No block selected');
                return;
            }
            
            // Check if BLOCKS_DATA exists
            if (typeof BLOCKS_DATA === 'undefined' && typeof window.BLOCKS_DATA === 'undefined') {
                console.warn('⚠️  BLOCKS_DATA not found');
                return;
            }
            
            const DATA = window.BLOCKS_DATA || BLOCKS_DATA;
            const blockData = DATA[selectedBlock];
            
            if (!blockData) {
                console.warn('⚠️  Block data not found for:', selectedBlock);
                return;
            }
            
            console.log('📈 Updating Likelihood Metrics with data:', blockData);
            
            // Call updateLikelihoodMetrics if it exists
            if (typeof updateLikelihoodMetrics === 'function') {
                updateLikelihoodMetrics(blockData);
                console.log('✅ Likelihood metrics updated successfully');
            } else {
                console.error('❌ updateLikelihoodMetrics function not found!');
            }
        });
        
        console.log('✅ Likelihood integration complete');
    });
})();
</script>
'''
    
    # Inject before </body>
    content = content[:body_close] + integration_script + '\n' + content[body_close:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Integration script added")
    print("✅ Likelihood Analysis will now update on block selection change")
    print("\nPlease refresh browser and:")
    print("  1. Open Console (F12)")
    print("  2. Select a block from dropdown")
    print("  3. Check console logs for debug info")
    print("  4. Verify Likelihood Score & Time-to-Critical update")

if __name__ == "__main__":
    main()
