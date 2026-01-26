
import json
import re

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
tbm_path = r'data\output\tbm_stats_real.json'
output_json = r'data\output\block_breakdown_v2.json'

try:
    print("=== KATEGORISASI BLOK V3.1 (SOURCE: HTML HISTORICAL DATA - MANUAL PARSING) ===")
    
    # 1. PARSE HTML LINE BY LINE
    with open(html_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    extracted_data = {}
    current_block = None
    
    # Flag to know we are inside HISTORICAL_YIELDS var
    in_historical_var = False
    
    # Simple regexes
    re_var_start = re.compile(r'const HISTORICAL_YIELDS = \{')
    re_block_start = re.compile(r'"([A-Z0-9]+)":\s*\{')
    re_luas = re.compile(r'luas_ha:\s*([\d\.]+)')
    re_yield_23 = re.compile(r'2023:\s*\{\s*real_ton_ha:\s*([\d\.]+)')
    re_yield_25 = re.compile(r'2025:\s*\{\s*real_ton_ha:\s*([\d\.]+)')
    re_is_tbm = re.compile(r'is_tbm:\s*(true|false)')
    
    # Temp vars
    temp_luas = 0
    temp_y23 = 0
    temp_y25 = 0
    temp_is_tbm = False
    
    for line in lines:
        line = line.strip()
        
        if not in_historical_var:
            if re_var_start.search(line):
                in_historical_var = True
                print("Found HISTORICAL_YIELDS start.")
            continue
            
        # We are inside the variable
        # Check block start
        m_block = re_block_start.search(line)
        if m_block:
            # Save previous if any (should have been saved at closure, but just in case)
            current_block = m_block.group(1)
            temp_luas = 0
            temp_y23 = 0
            temp_y25 = 0
            temp_is_tbm = False
            continue
            
        if current_block:
            # Parse properties
            m_luas = re_luas.search(line)
            if m_luas: temp_luas = float(m_luas.group(1))
            
            m_y23 = re_yield_23.search(line)
            if m_y23: temp_y23 = float(m_y23.group(1))
            
            m_y25 = re_yield_25.search(line)
            if m_y25: temp_y25 = float(m_y25.group(1))

            m_tbm = re_is_tbm.search(line)
            if m_tbm: temp_is_tbm = (m_tbm.group(1) == 'true')
            
            # Check block end (simplified logic: keys are usually "XXXX", so if we see "},", we define it as end of block IF indent suggests it)
            # Or just save whatever we have collected so far to the dictionary, overwriting is fine.
            # Efficient way: update dict continuously
            
            extracted_data[current_block] = {
                "luas": temp_luas,
                "y23": temp_y23,
                "y25": temp_y25,
                "is_tbm": temp_is_tbm,
                "total_yield": temp_y23 + temp_y25 # Simplifikasi indikator
            }
            
        # Stop condition: End of variable? "};"
        if line == '};':
            in_historical_var = False
            break

    print(f"Sukses Extract Historical Data: {len(extracted_data)} blok.")
    
    # Debug Blocks
    for dbg_code in ["B003A", "F025E", "B006D", "C003A"]:
        if dbg_code in extracted_data:
            print(f"[DEBUG] {dbg_code} Extracted: {extracted_data[dbg_code]}")
        else:
            print(f"[DEBUG] {dbg_code} NOT FOUND in Extraction!")

    # 2. READ TBM DATA (Filtered)
    with open(tbm_path, 'r') as f:
        tbm_data = json.load(f)

    # 3. KATEGORISASI
    categories = {
        "declining": [],
        "stable": [],
        "increasing": [],
        "tbm": [],
        "empty": []
    }
    
    summary_stats = {
        "declining": {"count": 0, "avg_change": 0, "total_area": 0, "avg_prod_2023": 0, "avg_prod_2025": 0},
        "stable": {"count": 0},
        "increasing": {"count": 0},
        "tbm": {"count": 0},
        "empty": {"count": 0, "total_area": 0}
    }
    
    all_blocks = set(extracted_data.keys()) | set(tbm_data.keys())
    
    for block_code in all_blocks:
        yd = extracted_data.get(block_code)
        
        y23 = yd['y23'] if yd else 0
        y25 = yd['y25'] if yd else 0
        is_tbm_html = yd['is_tbm'] if yd else False

        # total yield approximation (jika salah satu tahun ada, anggap produktif)
        has_production = (y23 > 0 or y25 > 0)
        
        luas = yd['luas'] if yd else 0
        
        # LOGIC 1: PRODUCTIVE
        if has_production:
            change_pct = 0
            if y23 > 0:
                change_pct = ((y25 - y23) / y23) * 100
            else:
                change_pct = 100
                
            item = {
                "block_code": block_code,
                "val": round(change_pct, 1),
                "desc": f"{y23:.1f} ➝ {y25:.1f} T/Ha"
            }
            
            if change_pct < -5:
                categories["declining"].append(item)
                summary_stats["declining"]["avg_change"] += change_pct
                summary_stats["declining"]["total_area"] += luas
            elif change_pct > 5:
                categories["increasing"].append(item)
            else:
                categories["stable"].append(item)
                
        # LOGIC 2: TBM
        else:
            # Check TBM Stats
            has_tbm_stats = (block_code in tbm_data and tbm_data[block_code].get('total_tbm_3th', 0) > 0)
            
            if has_tbm_stats:
                 categories["tbm"].append({
                    "block_code": block_code, 
                    "val": 0, 
                    "desc": "Tahun Tanam: " + str(tbm_data[block_code].get('year', '-'))
                })
            elif is_tbm_html:
                 # Fallback: Marked as TBM in HTML but no stats
                 year = tbm_data[block_code].get('year', '?') if block_code in tbm_data else '?'
                 categories["tbm"].append({
                    "block_code": block_code, 
                    "val": 0, 
                    "desc": f"Tahun Tanam: {year}" # (No Data) implisit
                })
            else:
                # LOGIC 3: EMPTY
                categories["empty"].append({
                    "block_code": block_code,
                    "val": 0,
                    "desc": f"Luas: {luas} Ha (Tanpa Tanaman)"
                })
                summary_stats["empty"]["total_area"] += luas

    # Finalize Stats
    decl_count = len(categories["declining"])
    if decl_count > 0:
        summary_stats["declining"]["avg_change"] = round(summary_stats["declining"]["avg_change"] / decl_count, 1)
        summary_stats["declining"]["total_area"] = round(summary_stats["declining"]["total_area"], 1)
    
    summary_stats["declining"]["count"] = decl_count
    summary_stats["stable"]["count"] = len(categories["stable"])
    summary_stats["increasing"]["count"] = len(categories["increasing"])
    summary_stats["tbm"]["count"] = len(categories["tbm"])
    summary_stats["empty"]["count"] = len(categories["empty"])
    summary_stats["empty"]["total_area"] = round(summary_stats["empty"]["total_area"], 1)

    print(f"Categorized: Declining={decl_count}, Stable={summary_stats['stable']['count']}, Increasing={summary_stats['increasing']['count']}, TBM={summary_stats['tbm']['count']}, Empty={summary_stats['empty']['count']}")

    # Save output
    output_data = {
        "categories": categories,
        "summary": summary_stats
    }
    
    with open(output_json, 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print("Done. Saved accurate breakdown to block_breakdown_v2.json")

except Exception as e:
    print(f"Error: {e}")
