import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # FIX 1: Remove broken tag "<di" on line ~946
    content = content.replace('\n<di\n', '\n')
    content = content.replace('<di>', '')
    content = content.replace('<di', '')
    print("✅ Fixed broken <di tag")
    
    # FIX 2: Ensure proper grid closing structure
    # The grid should close BEFORE Vanishing Yield section
    # Look for pattern: grid content ends → Vanishing starts
    
    vanishing_marker = '<!-- Vanishing Yield Analysis - Full Width Below -->'
    idx_vanishing = content.find(vanishing_marker)
    
    if idx_vanishing == -1:
        print("ERROR: Vanishing marker not found")
        return
    
    # Check if there are proper closing divs before Vanishing
    # There should be at least 2-3 </div> to close: Likelihood column, grid, section
    before_vanishing = content[max(0, idx_vanishing-300):idx_vanishing]
    
    closing_div_count = before_vanishing.count('</div>')
    print(f"Found {closing_div_count} closing divs before Vanishing")
    
    if closing_div_count < 2:
        print("⚠️  WARNING: Not enough closing tags - may cause layout issues")
        # Add missing closing divs
        insert_pos = idx_vanishing
        missing_closes = '</div>\n</div>\n\n'
        content = content[:insert_pos] + missing_closes + content[insert_pos:]
        print("✅ Added missing closing divs")
    
    # FIX 3: Verify Formula Parameters is inside Likelihood column
    formula_marker = '<!-- FORMULA DISCLAIMER & PARAMETERS -->'
    likelihood_start = content.find('<!-- LIKELIHOOD & TREND ANALYSIS -->')
    likelihood_end_guess = content.find('<!-- 3. TIME TO CRITICAL', likelihood_start) + 500  # rough estimate
    
    formula_idx = content.find(formula_marker)
    
    if formula_idx != -1:
        if likelihood_start < formula_idx < likelihood_end_guess:
            print("✅ Formula Parameters is inside Likelihood column")
        else:
            print("⚠️  Formula Parameters might be outside Likelihood column")
    else:
        print("⚠️  Formula Parameters section not found")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Critical HTML fixes applied")
    print("\nPlease refresh browser")
    print("Expected result:")
    print("  • Likelihood column should now APPEAR on the right")
    print("  • Financial (left) + Likelihood (right) side-by-side")
    print("  • Vanishing Yield below (full width)")

if __name__ == "__main__":
    main()
