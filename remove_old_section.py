"""
Script untuk mencari dan menghapus section lama (Production Gap, WITH TREATMENT old box, ROI box)
yang ditunjukkan di screenshot
"""

def remove_old_treatment_section():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Searching for old treatment section elements...")
    
    # Search for the section containing these old elements
    # Pattern 1: Look for "Other metrics (Production Gap, Critical Blocks)" comment
    if "Other metrics (Production Gap, Critical Blocks)" in content:
        print("[FOUND] Old 'Other metrics' section exists")
        
        # This section should be after the side-by-side comparison
        # Let's find and remove it
        start_marker = '''            <!-- Other metrics (Production Gap, Critical Blocks) -->
            <div class="bg-slate-800/50 rounded-xl border border-slate-600/30 p-4">
                <div class="space-y-2">'''
        
        if start_marker in content:
            print("[FOUND] Start marker for old metrics section")
            
            # Find the end of this section (look for closing divs)
            # This section should end before the next major section or before renderDegradationModelChart
            
            # Strategy: Find the section and remove up to the closing divs
            # We need to find where this section ends - likely before ROI highlight or script tag
            
            # Let's find the whole block by looking for the ROI section that follows
            end_marker = '''            <!-- ROI Highlight (below production gap section) -->'''
            
            if end_marker in content:
                print("[FOUND] End marker (ROI section)")
                # Extract and remove the section between markers
                before = content.split(start_marker)[0]
                after_temp = content.split(start_marker)[1]
                
                if end_marker in after_temp:
                    after = end_marker + after_temp.split(end_marker)[1]
                    content = before + after
                    print("[SUCCESS] Removed old metrics section")
                else:
                    print("[WARNING] End marker not found in expected location")
            else:
                # Try alternative: remove from start_marker to next </div> that closes this section
                # Count divs to find the matching closing tag
                print("[INFO] Using alternative removal method...")
                
                before = content.split(start_marker)[0]
                after_temp = content.split(start_marker)[1]
                
                # Find where this div block ends (we need to count opening and closing divs)
                div_count = 1  # We have one opening div from start_marker
                pos = 0
                
                while div_count > 0 and pos < len(after_temp):
                    if after_temp[pos:pos+5] == '<div ':
                        div_count += 1
                    elif after_temp[pos:pos+6] == '</div>':
                        div_count -= 1
                        if div_count == 0:
                            # Found the closing div
                            pos += 6
                            break
                    pos += 1
                
                if div_count == 0:
                    after = after_temp[pos:]
                    content = before + after
                    print(f"[SUCCESS] Removed {pos} characters of old section")
                else:
                    print("[ERROR] Could not find matching closing div")
        else:
            print("[INFO] Start marker not found - section may have been removed already")
    
    # Also remove any standalone ROI boxes that show "POTENTIAL SAVINGS" and "ROI RATIO"
    if "POTENTIAL SAVINGS" in content or "💰" in content:
        print("[INFO] Checking for standalone ROI boxes...")
        
        # Look for the ROI highlight section
        roi_pattern = '''            <!-- ROI Highlight'''
        if roi_pattern in content:
            print("[FOUND] ROI Highlight section")
            # This might be after our side-by-side, we may want to keep it or remove it
            # Let me check context
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    
    # Show summary
    if "Other metrics (Production Gap, Critical Blocks)" not in content:
        print("✅ Old metrics section removed")
    else:
        print("⚠️ Old metrics section may still exist")

if __name__ == '__main__':
    remove_old_treatment_section()
