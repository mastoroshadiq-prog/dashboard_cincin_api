import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def fix_balance(content, phase_id):
    # Find start of phase
    start_marker = f'id="{phase_id}"'
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Phase {phase_id} not found.")
        return content

    # Find the tag start "<div id=..."
    tag_start = content.rfind('<div', 0, start_idx)
    
    # We assume the layout is:
    # <div id="phase-X" ...>
    #    ... content ...
    # </div>
    # <div id="phase-Y" ...>
    
    # We need to find where the NEXT phase starts (or End of Container).
    # Regex for next phase or end
    next_phase_pattern = re.compile(r'<div id="phase-\d+"', re.DOTALL)
    
    # Search for next phase starting AFTER the current tag opening
    matches = list(next_phase_pattern.finditer(content, tag_start + 1))
    
    if len(matches) > 0:
        # The content of THIS phase ends right before the next phase starts.
        # But wait, there should be a closing </div> for this phase before the next div starts.
        end_idx = matches[0].start()
    else:
        # Last phase? Ends at "</div> <!-- End Overview -->"
        end_marker = "</div> <!-- End Overview -->"
        end_idx = content.find(end_marker, tag_start)
        if end_idx == -1:
             # Fallback
             end_idx = content.find("</body>")

    # Extract the block
    block = content[tag_start:end_idx]
    
    # Check div balance
    # We filter out self-closing divs if any (rare in HTML5 for div, but let's assume valid HTML)
    # Actually simple count is usually enough for generated code.
    open_count = block.count('<div')
    close_count = block.count('</div>')
    
    balance = open_count - close_count
    
    print(f"[{phase_id}] Open: {open_count}, Close: {close_count}, Balance: {balance}")
    
    if balance == 0:
        print(f"[{phase_id}] Structure is OK.")
        return content
        
    elif balance > 0:
        print(f"[{phase_id}] Missing {balance} closing divs. Appending...")
        # We assume the last </div> in the block is meant to close the phase, 
        # but we are short.
        # We insert the missing </div>s right before the end_idx.
        correction = "</div>" * balance
        new_content = content[:end_idx] + "\n" + correction + "\n" + content[end_idx:]
        return new_content
        
    elif balance < 0:
        print(f"[{phase_id}] Too many closing divs ({abs(balance)}). Removing tail...")
        # Detecting which </div> to remove is hard.
        # But usually in my extract logic, I might have grabbed an extra </div> from the source.
        # We will attempt to remove the LAST '</div>' occurrences in the block.
        
        corrected_block = block
        for _ in range(abs(balance)):
            r_idx = corrected_block.rfind('</div>')
            if r_idx != -1:
                corrected_block = corrected_block[:r_idx] + corrected_block[r_idx+6:]
        
        new_content = content[:tag_start] + corrected_block + content[end_idx:]
        return new_content

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = fix_balance(content, 'phase-1')
    content = fix_balance(content, 'phase-2')
    content = fix_balance(content, 'phase-3')
    content = fix_balance(content, 'phase-4')
    content = fix_balance(content, 'phase-5')
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ STARTUP: Phase Structure Balanced.")

if __name__ == "__main__":
    main()
