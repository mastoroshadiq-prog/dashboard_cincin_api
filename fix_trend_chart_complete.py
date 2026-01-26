import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Starting diagnostic & fix...")
    print("="*60)
    
    # ============================================
    # DIAGNOSTIC: Check if trend chart still exists
    # ============================================
    
    if 'trendMiniChart' in content:
        print("⚠️  FOUND: trendMiniChart canvas still exists")
        
        # Find and remove all references to trend chart
        # 1. Remove canvas element
        canvas_pattern = '<canvas id="trendMiniChart" class="w-full h-full"></canvas>'
        if canvas_pattern in content:
            content = content.replace(canvas_pattern, '<!-- Trend chart removed - no historical data -->')
            print("✅ Removed canvas element")
        
        # 2. Remove the entire container div for trend chart
        # Find by unique text content
        trend_section_start = '<!-- 2. ATTACK RATE TREND'
        trend_section_marker = 'Attack Rate Trend'
        
        if trend_section_marker in content:
            # Find the start of this section
            idx_start = content.find(trend_section_start)
            if idx_start != -1:
                # Find the end - look for next major section or closing div
                # Search for the next "<!-- 3." comment
                idx_end = content.find('<!-- 3. TIME TO CRITICAL', idx_start)
                
                if idx_end != -1:
                    # Remove everything between
                    content = content[:idx_start] + '\n' + content[idx_end:]
                    print("✅ Removed trend chart section HTML")
    else:
        print("✅ Trend chart canvas not found (already removed)")
    
    # ============================================
    # FIX: Remove ALL JavaScript references to trend chart
    # ============================================
    
    # Remove trend chart variable
    if 'let trendChart = null;' in content:
        content = content.replace('let trendChart = null;', '// Trend chart removed - no historical data')
        print("✅ Removed trendChart variable")
    
    # Remove Chart.js initialization for trend
    if 'trendChart = new Chart(ctx' in content:
        print("⚠️  FOUND: Chart.js initialization still exists")
        
        # Find and remove the entire Chart initialization block
        chart_init_start = 'trendChart = new Chart(ctx'
        idx_chart_start = content.find(chart_init_start)
        
        if idx_chart_start != -1:
            # Find the closing of this Chart() call - look for matching });
            # Search for the end of Chart options object
            idx_chart_end = content.find('});', idx_chart_start)
            if idx_chart_end != -1:
                idx_chart_end_full = content.find('\n', idx_chart_end) + 1
                content = content[:idx_chart_start] + '// Chart removed\n' + content[idx_chart_end_full:]
                print("✅ Removed Chart.js initialization")
    
    # Remove initializeLikelihoodAnalysis function completely
    func_start = 'function initializeLikelihoodAnalysis() {'
    if func_start in content:
        print("⚠️  FOUND: initializeLikelihoodAnalysis function still exists")
        
        idx_func_start = content.find(func_start)
        if idx_func_start != -1:
            # Find the end of this function - look for closing brace
            # Count braces to find matching close
            brace_count = 0
            idx = idx_func_start + len(func_start)
            while idx < len(content):
                if content[idx] == '{':
                    brace_count += 1
                elif content[idx] == '}':
                    if brace_count == 0:
                        # Found the closing brace
                        idx_func_end = idx + 1
                        break
                    brace_count -= 1
                idx += 1
            
            # Remove the entire function
            content = content[:idx_func_start] + '// initializeLikelihoodAnalysis removed\n' + content[idx_func_end:]
            print("✅ Removed initializeLikelihoodAnalysis function")
    
    # Remove call to initializeLikelihoodAnalysis
    init_call = 'initializeLikelihoodAnalysis();'
    if init_call in content:
        content = content.replace(init_call, '// Trend chart initialization removed')
        print("✅ Removed function call")
    
    # Remove trend data object
    if 'const trendData = {' in content:
        print("⚠️  FOUND: trendData object still exists")
        
        idx_data_start = content.find('const trendData = {')
        if idx_data_start != -1:
            # Find closing of this object - look for };
            idx_data_end = content.find('};', idx_data_start)
            if idx_data_end != -1:
                idx_data_end_full = content.find('\n', idx_data_end) + 1
                content = content[:idx_data_start] + '// Trend data removed\n' + content[idx_data_end_full:]
                print("✅ Removed trendData object")
    
    # ============================================
    # FIX: Clean up any console errors
    # ============================================
    
    # Remove any getElementById calls for removed elements
    problematic_selectors = [
        "document.getElementById('trendMiniChart')",
        "getElementById('trendVelocity')",
        "getElementById('trendBadge')"
    ]
    
    for selector in problematic_selectors:
        if selector in content:
            print(f"⚠️  FOUND problematic selector: {selector}")
    
    # ============================================
    # VERIFY: Final check
    # ============================================
    
    print("\n" + "="*60)
    print("VERIFICATION:")
    print("="*60)
    
    if 'trendMiniChart' in content:
        print("❌ WARNING: trendMiniChart still found in content!")
        print("   Manual inspection needed")
    else:
        print("✅ trendMiniChart completely removed")
    
    if 'Attack Rate Trend' in content:
        print("❌ WARNING: 'Attack Rate Trend' text still found!")
    else:
        print("✅ Attack Rate Trend section removed")
    
    if 'new Chart(ctx' in content:
        print("❌ WARNING: Chart initialization still found!")
    else:
        print("✅ No Chart.js initialization found")
    
    # Write the fixed content
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ File updated successfully")
    print("Please refresh browser and check console for errors")

if __name__ == "__main__":
    main()
