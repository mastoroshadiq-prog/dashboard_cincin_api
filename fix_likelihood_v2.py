import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue: Formula Parameters section is OUTSIDE the Likelihood column div
    # We need to move it INSIDE
    
    # Strategy: Find the Formula section, cut it, and paste it in the right place
    
    # Find Formula section start
    formula_start_marker = '<!-- FORMULA DISCLAIMER & PARAMETERS -->'
    idx_formula_start = content.find(formula_start_marker)
    
    if idx_formula_start == -1:
        print("ERROR: Formula section not found")
        return
    
    print(f"✅ Found Formula section")
    
    # Find Formula section end (before TIME TO CRITICAL)
    time_critical_marker = '<!-- 3. TIME TO CRITICAL PROJECTION -->'
    idx_time_critical = content.find(time_critical_marker, idx_formula_start)
    
    if idx_time_critical == -1:
        print("ERROR: TIME TO CRITICAL not found")
        return
    
    # Extract everything from a bit before Formula start (to catch any stray divs/whitespace)
    # Look backwards for proper cut point
    search_back = content[max(0, idx_formula_start-200):idx_formula_start]
    # Find last closing </div> before Formula section
    last_close_div = search_back.rfind('</div>')
    if last_close_div != -1:
        actual_start = max(0, idx_formula_start-200) + last_close_div + 6  # After </div>
    else:
        actual_start = idx_formula_start
    
    # Extract Formula content
    formula_content = content[actual_start:idx_time_critical].strip()
    
    print(f"✅ Extracted Formula section ({len(formula_content)} chars)")
    
    # Remove from current position
    content = content[:actual_start] + '\n\n' + content[idx_time_critical:]
    
    # Now find WHERE to insert it - inside Likelihood card, after Probability Score
    # Look for the closing of Probability Score section
    # Search pattern: look for "<!-- 1. LIKELIHOOD SCORE" and find its closing divs
    
    likelihood_score_marker = '<!-- 1. LIKELIHOOD SCORE (Gauge) -->'
    idx_likelihood_score = content.find(likelihood_score_marker)
    
    if idx_likelihood_score == -1:
        print("ERROR: Likelihood Score section not found")
        return
    
    # Find the closing of Probability Score section
    # Look for "</div>\n                                </div>" pattern after Likelihood Score
    # This is the end of the Probability Score card
    search_area = content[idx_likelihood_score:idx_likelihood_score+3000]
    prob_close_pattern = '</div>\n                                </div>\n\n'
    idx_prob_close_relative = search_area.find(prob_close_pattern)
    
    if idx_prob_close_relative == -1:
        # Try alternative pattern
        prob_close_pattern = '</div>\n                            </div>\n\n'
        idx_prob_close_relative = search_area.find(prob_close_pattern)
    
    if idx_prob_close_relative != -1:
        insertion_point = idx_likelihood_score + idx_prob_close_relative + len(prob_close_pattern)
        print(f"✅ Found insertion point after Probability Score")
    else:
        print("⚠️  Using fallback insertion point")
        # Fallback: just insert before TIME TO CRITICAL
        insertion_point = content.find(time_critical_marker)
    
    # Insert Formula content with proper indentation
    indented_formula = '\n' + formula_content.replace('\n', '\n                            ') + '\n                            \n'
    
    content = content[:insertion_point] + indented_formula + content[insertion_point:]
    
    print("✅ Inserted Formula section inside Likelihood column")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("\n✅ Structure fixed!")
    print("\nPlease refresh browser and check:")
    print("  • Likelihood card is NOW 50% width (side-by-side with Financial)")
    print("  • Click ℹ️ Info button → Formula explanation should appear")
    print("  • Sliders and Recalculate still work")

if __name__ == "__main__":
    main()
