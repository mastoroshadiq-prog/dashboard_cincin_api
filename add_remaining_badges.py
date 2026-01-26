import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def add_badge_after_pattern(content, search_text, badge, name):
    """Find text and add badge after the div opening"""
    idx = content.find(search_text)
    if idx == -1:
        print(f"  ⚠️  {name} - not found")
        return content, False
    
    # Find the > that closes the opening div tag after this text
    close_idx = content.find('>', idx)
    if close_idx == -1:
        print(f"  ⚠️  {name} - closing > not found")
        return content, False
    
    # Insert badge right after >
    insert_pos = close_idx + 1
    content = content[:insert_pos] + '\n            ' + badge + content[insert_pos:]
    print(f"  ✅ {name}")
    return content, True

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Adding missing ISO badges...")
    count = 0
    
    # Phase 2: Financial Simulator (find by unique text)
    if 'Harga TBS Simulasi' in content:
        content, success = add_badge_after_pattern(
            content,
            'Harga TBS Simulasi',
            '<span class="iso-badge iso-phase-2">2. ANALYSIS</span>',
            'Financial Simulator (Phase 2)'
        )
        if success: count += 1
    
    # Phase 2: Financial Impact (find by "Estimasi Kerugian")
    if 'Estimasi Kerugian (Blok' in content:
        content, success = add_badge_after_pattern(
            content,
            'Estimasi Kerugian (Blok',
            '<span class="iso-badge iso-phase-2">2. ANALYSIS</span>',
            'Financial Impact (Phase 2)'
        )
        if success: count += 1
    
    # Phase 3: Risk Matrix (find by canvas id)
    if 'id="riskMatrixCanvas"' in content:
        # Find the parent container
        idx = content.find('id="riskMatrixCanvas"')
        # Search backwards for the div with class containing "gradient"
        search_start = max(0, idx - 500)
        section = content[search_start:idx]
        div_idx = section.rfind('<div')
        if div_idx != -1:
            actual_idx = search_start + div_idx
            close_idx = content.find('>', actual_idx)
            if close_idx != -1:
                content = content[:close_idx+1] + '\n            <span class="iso-badge iso-phase-3">3. EVALUATION</span>' + content[close_idx+1:]
                print("  ✅ Risk Matrix (Phase 3)")
                count += 1
    
    # Phase 4: Standard Protocols (find by "STANDARD PROTOCOLS")
    if 'STANDARD PROTOCOLS' in content:
        content, success = add_badge_after_pattern(
            content,
            'STANDARD PROTOCOLS',
            '<span class="iso-badge iso-phase-4">4. TREATMENT</span>',
            'Standard Protocols (Phase 4)'
        )
        if success: count += 1
    
    # Phase 1: SPH Analysis (Analisis Kerapatan SPH)
    if 'Analisis Kerapatan SPH' in content or 'SPH Manual' in content:
        # This might be in a dedicated section
        content, success = add_badge_after_pattern(
            content,
            'SPH Manual',
            '<span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>',
            'SPH Density Analysis (Phase 1)'
        )
        if success: count += 1
    
    print(f"\n✅ Added {count} additional badges")
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ ISO 31000 BADGES COMPLETE!")
    print("🔄 Hard refresh browser (Ctrl + Shift + R)")

if __name__ == "__main__":
    main()
