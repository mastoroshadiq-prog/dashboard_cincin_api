"""
Manually update the degradation chart with REAL historical data
"""

# Read dashboard
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the chart data calculation
# The mini chart should be using HISTORICAL_YIELDS data just like the modal

# OLD pattern - calculated/simulated data
old_pattern = '''            // REAL HISTORICAL YIELD DATA from Excel (2023-2025)
            const blockCode = currentBlockCode;
            const historicalData = HISTORICAL_YIELDS[blockCode];
            
            if (!historicalData) {
                console.error('No historical data for block:', blockCode);
                return;
            }
            
            // Real data from Excel
            const year3ago = historicalData.yields[2023]?.real_ton_ha || 0;  // 2023
            const year2ago = historicalData.yields[2024]?.real_ton_ha || 0;  // 2024
            const year1ago = historicalData.yields[2025]?.real_ton_ha || 0;  // 2025
            
            const potentialYield = historicalData.yields[2025]?.poten_ton_ha || 0;'''

# Check if this pattern exists (from modal)
if old_pattern in content:
    print("Modal chart already uses HISTORICAL_YIELDS - GOOD")
    
    # Now find the MAIN degradation chart and check if it also uses HISTORICAL_YIELDS
    # Search for 'window.degradationChart'
    import re
    
    # Find the degradation chart rendering
    degradation_pattern = re.search(r'(window\.degradationChart = new Chart.*?)\}\);', content, re.DOTALL)
    
    if degradation_pattern:
        chart_code = degradation_pattern.group(0)
        
        if 'HISTORICAL_YIELDS' in chart_code:
            print("Main degradation chart ALREADY uses HISTORICAL_YIELDS!")
        else:
            print("Main degradation chart NOT using HISTORICAL_YIELDS - needs update")
    else:
        print("Could not find window.degradationChart rendering")
else:
    print("HISTORICAL_YIELDS pattern not found - integration didn't work!") 
    print("Need to run full integration again")

# Let me check simpler - does HISTORICAL_YIELDS object exist?
if 'const HISTORICAL_YIELDS' in content:
    print("\nHISTORICAL_YIELDS object EXISTS in file")
else:
    print("\nHISTORICAL_YIELDS object NOT FOUND - need to add it!")

print("\nDone checking")
