import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")
    
    # Find the escaped Formula Parameters section and move it back inside Likelihood column
    # Look for line "<!-- FORMULA DISCLAIMER & PARAMETERS -->"
    
    formula_start_idx = None
    for i, line in enumerate(lines):
        if '<!-- FORMULA DISCLAIMER & PARAMETERS -->' in line:
            formula_start_idx = i
            break
    
    if formula_start_idx is None:
        print("ERROR: Formula Parameters section not found")
        return
    
    print(f"Found Formula section at line {formula_start_idx + 1}")
    
    # Find the end of Formula Parameters section
    # It ends before "<!-- 3. TIME TO CRITICAL PROJECTION -->"
    formula_end_idx = None
    for i in range(formula_start_idx, len(lines)):
        if '<!-- 3. TIME TO CRITICAL PROJECTION -->' in line[i]:
            formula_end_idx = i - 1  # Line before TIME TO CRITICAL
            break
    
    if formula_end_idx is None:
        print("ERROR: Cannot find end of Formula section")
        return
    
    print(f"Formula section ends at line {formula_end_idx + 1}")
    
    # Extract the Formula section (including closing divs before it)
    # Need to trim excessive whitespace/closing divs that escaped
    
    # Find where Formula section should be inserted
    # It should be INSIDE the Likelihood column, after Probability Score
    # Look for the closing of Probability Score section
    
    prob_score_end = None
    for i in range(formula_start_idx - 1, max(0, formula_start_idx - 20), -1):
        if '</div>' in lines[i] and '</div>' in lines[i+1]:
            # Found double closing divs - likely end of Probability Score
            prob_score_end = i + 2  # Insert after the closing divs
            break
    
    if prob_score_end is None:
        print("WARNING: Cannot find Probability Score end, using fallback")
        prob_score_end = formula_start_idx
    
    # Extract Formula content (lines from formula_start_idx to formula_end_idx)
    formula_content = lines[formula_start_idx:formula_end_idx+1]
    
    # Remove Formula from current position
    del lines[formula_start_idx:formula_end_idx+1]
    
    # Clean up excess blank lines left behind
    while formula_start_idx < len(lines) and lines[formula_start_idx].strip() == '':
        del lines[formula_start_idx]
    
    # INSERT Formula back inside Likelihood column
    # Since we deleted content, indices shifted - need to recalculate
    # The prob_score_end was BEFORE formula section, so it's still valid
    
    # Add proper indentation to formula content
    indented_formula = []
    for line in formula_content:
        # Add extra 4 spaces to nest it properly inside Likelihood card
        indented_formula.append('    ' + line)
    
    # Insert at prob_score_end
    for i, line in enumerate(indented_formula):
        lines.insert(prob_score_end + i, line)
    
    print(f"✅ Moved Formula Parameters inside Likelihood column")
    
    # Write back
    with open(FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print("\n✅ Structure fixed")
    print("\nChanges:")
    print("  • Formula Parameters moved inside Likelihood column")
    print("  • Likelihood width should now be 50% (lg:col-span-1)")
    print("  • Info toggle should work (formulaExplanation inside proper container)")
    print("\nPlease refresh browser and verify:")
    print("  1. Likelihood card is 50% width (next to Financial)")
    print("  2. Click ℹ️ Info → Formula explanation appears")
    print("  3. Click again → Formula explanation collapses")

if __name__ == "__main__":
    main()
