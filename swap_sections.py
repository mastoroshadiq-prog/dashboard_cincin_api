"""
Script untuk memindahkan section "Analisis Dampak Finansial" 
ke ATAS "Division Comparison" di DASHBOARD_DEMO_FEATURES.html
"""

def swap_sections():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"[INFO] Total lines: {len(lines)}")
    
    # Define section boundaries (0-indexed)
    # Division Comparison: lines 384-486 (inclusive)
    div_comp_start = 384  # Line 385 (1-indexed) - 1
    div_comp_end = 486    # Line 487 (1-indexed) - 1
    
    # Analisis Dampak Finansial: lines 488-901 (inclusive)
    anal_fin_start = 488  # Line 489 (1-indexed) - 1  
    anal_fin_end = 901    # Line 902 (1-indexed) - 1
    
    print(f"[INFO] Division Comparison: lines {div_comp_start+1}-{div_comp_end+1}")
    print(f"[INFO] Analisis Dampak Finansial: lines {anal_fin_start+1}-{anal_fin_end+1}")
    
    # Extract sections
    division_comparison = lines[div_comp_start:div_comp_end+1]
    analisis_finansial = lines[anal_fin_start:anal_fin_end+1]
    
    print(f"[INFO] Division Comparison: {len(division_comparison)} lines")
    print(f"[INFO] Analisis Finansial: {len(analisis_finansial)} lines")
    
    # Rebuild file:
    # 1. Lines before Division Comparison (0 to div_comp_start-1)
    # 2. Analisis Finansial section
    # 3. Division Comparison section  
    # 4. Lines after Analisis Finansial (anal_fin_end+1 to end)
    
    new_lines = (
        lines[:div_comp_start] +          # Before Division Comparison
        analisis_finansial +               # Analisis Finansial (now first)
        ['\n'] +                           # Add spacing
        division_comparison +              # Division Comparison (now second)
        lines[anal_fin_end+1:]            # After Analisis Finansial
    )
    
    print(f"[INFO] New total lines: {len(new_lines)}")
    
    # Write output
    output_file = input_file  # Overwrite the same file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"[SUCCESS] Sections swapped successfully!")
    print(f"[OUTPUT] File saved: {output_file}")
    
    # Verify
    print("\n[VERIFICATION]")
    print(f"Line {div_comp_start+1} preview (should be Analisis Finansial now):")
    print(new_lines[div_comp_start][:100])
    
if __name__ == '__main__':
    swap_sections()
