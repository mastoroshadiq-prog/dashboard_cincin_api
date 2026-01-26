"""
Script untuk menemukan dan fix duplikasi variable 'savingsPercent'
"""

def fix_duplicate_variable():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Analyzing file for duplicate variable declarations...")
    
    # Find all occurrences of savingsPercent declaration
    lines = content.split('\n')
    savings_percent_lines = []
    
    for i, line in enumerate(lines, 1):
        if 'savingsPercent' in line and ('const ' in line or 'let ' in line or 'var ' in line):
            savings_percent_lines.append((i, line.strip()))
            print(f"  Line {i}: {line.strip()[:100]}")
    
    if len(savings_percent_lines) > 1:
        print(f"\n[FOUND] {len(savings_percent_lines)} declarations of savingsPercent")
        print("[FIX] Will rename duplicates...")
        
        # Strategy: Keep the first one, rename others
        # First occurrence stays as 'savingsPercent'
        # Second becomes 'treatment_savingsPercent' (already in our new code)
        # Others get unique names
        
        # Find and replace the OLD duplicate (likely from WITH TREATMENT old code)
        old_pattern1 = '''const savingsPercent = Math.round((1 - reducedLoss / year1Loss) * 100);
            document.getElementById('withTreatment_loss').innerHTML =
                `${formatLossMiliar(reducedLoss)}<span class="text-lg ml-2 text-emerald-300">↓${savingsPercent}%</span>`;'''
        
        new_pattern1 = '''const oldSavingsPercent = Math.round((1 - reducedLoss / year1Loss) * 100);
            document.getElementById('withTreatment_loss').innerHTML =
                `${formatLossMiliar(reducedLoss)}<span class="text-lg ml-2 text-emerald-300">↓${oldSavingsPercent}%</span>`;'''
        
        if old_pattern1 in content:
            content = content.replace(old_pattern1, new_pattern1)
            print("[SUCCESS] Renamed first duplicate to 'oldSavingsPercent'")
        
        # Also check for this pattern
        old_pattern2 = '''const savingsPercent = ((totalSavings / noTx_cumulative) * 100);'''
        new_pattern2 = '''const treatment_savingsPercent = ((totalSavings / noTx_cumulative) * 100);'''
        
        if old_pattern2 in content:
            content = content.replace(old_pattern2, new_pattern2)
            print("[SUCCESS] Renamed second to 'treatment_savingsPercent'")
            
            # Also update the usage
            old_usage = '''document.getElementById('treatment_savingsPercent').textContent = savingsPercent.toFixed(0) + '%';'''
            new_usage = '''document.getElementById('treatment_savingsPercent').textContent = treatment_savingsPercent.toFixed(0) + '%';'''
            
            if old_usage in content:
                content = content.replace(old_usage, new_usage)
                print("[SUCCESS] Updated usage of renamed variable")
    else:
        print("[INFO] No duplicate declarations found - checking for other issues...")
        
        # Check if variable exists at all
        if 'savingsPercent' in content:
            print("[INFO] savingsPercent exists in file")
            # Count occurrences
            count = content.count('savingsPercent')
            print(f"[INFO] Found {count} occurrences of 'savingsPercent'")
        else:
            print("[WARNING] No 'savingsPercent' found in file!")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")

if __name__ == '__main__':
    fix_duplicate_variable()
