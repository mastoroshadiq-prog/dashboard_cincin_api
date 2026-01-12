import os

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    print("Reading file...")
    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    
    # Target Range to Delete:
    # From line ~3440 (empty line/start of script)
    # To line ~3578 (end of style block)
    
    # Identification markers:
    # Start: <script> followed by // ISO 31000 TAB MANAGER
    # End: </style> followed by </body> (inside the template string context)
    
    skip = False
    
    for i, line in enumerate(lines):
        # DETECT START
        # We look for the inserted chunk's signature
        if '<script>' in line and i+1 < len(lines) and '// ISO 31000 TAB MANAGER' in lines[i+1]:
            print(f"Detected START of misplaced script block at line {i+1}")
            skip = True
            
        if skip:
            # We are skipping.
            # Check for END
            # The block ends with </style>
            if '</style>' in line:
                print(f"Detected END of misplaced script block at line {i+1}")
                skip = False
                continue # Skip the </style> line too
            continue # Skip current line
            
        new_lines.append(line)
        
    with open(FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ SURGICAL FIX COMPLETE: Function leakage resolved.")

if __name__ == "__main__":
    main()
