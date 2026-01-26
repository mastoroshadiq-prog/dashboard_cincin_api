FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start_viz = -1
    end_p2 = -1
    start_p3 = -1
    
    for i, line in enumerate(lines):
        if 'VANISHING YIELD' in line:
            start_viz = i
        if '<div id="phase-2"' in line:
            start_p2 = i # Just to know start
        if '<div id="phase-3"' in line:
            start_p3 = i
            
    # Locate CLOSE of P2?
    # We can't easily track close divs line by line without a stack.
    # But usually my rebuild script puts </div> right before <div id="phase-3">
    
    # Check lines around start_p3
    print(f"Vanishing Yield at line: {start_viz}")
    print(f"Phase 3 Starts at line: {start_p3}")
    
    # Print content between them
    if start_viz != -1 and start_p3 != -1:
        print("--- CONTENT BETWEEN YIELD AND P3 ---")
        for j in range(start_viz, start_p3 + 1):
             print(f"{j}: {lines[j].strip()}")

if __name__ == "__main__":
    main()
