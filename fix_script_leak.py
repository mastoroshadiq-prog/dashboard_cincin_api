import os

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    
    # We want to remove the accidental injection of main dashboard scripts into the print report string.
    # The print report string starts around line 3407: printWin.document.write(`
    # PROPER content is <html>...window.print()<\/script></html>
    # BAD content starts after line 3439.
    
    # Markers (based on line numbers seen in view_file)
    # Line 3438: setTimeout(() => { window.print(); }, 1000);
    # Line 3439: <\/script>  (escaped properly)
    
    # We need to KEEP line 3439.
    # We need to DELETE lines 3440 all the way to 3580 (where </body> and </html> are).
    # wait, the </body> and </html> at 3580/3581 are needed for the report.
    
    # So we delete:
    # <script>
    # // Likelihood Analysis Logic...
    # ...
    # </style>
    
    # This block spans roughly 3440 to 3578.
    
    skip_mode = False
    
    for i, line in enumerate(lines):
        # Detect start of accidental injection
        if '<script>' in line and '// Likelihood Analysis Logic' in lines[i+1]:
            print(f"Detected START of injected garbage at line {i+1}")
            skip_mode = True
            
        # Detect end of accidental injection
        # The bad block ends with </style> around line 3578
        # And next line is </body>
        if skip_mode and '</body>' in line:
            print(f"Detected END of injected garbage at line {i+1}")
            skip_mode = False
            # We keep the </body> line!
            new_lines.append(line)
            continue
            
        if not skip_mode:
            # Also, check for unescaped </script> tags inside the big string?
            # The only unescaped one was the one causing the leak, but we are deleting it now!
            # So simple deletion should fix the leak too.
            new_lines.append(line)
            
    with open(FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print("✅ FIXED: Removed injected script block from Printable Report logic.")

if __name__ == "__main__":
    main()
