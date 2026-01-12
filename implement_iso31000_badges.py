import os
import re

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

# CSS untuk ISO badges
ISO_CSS = '''
        /* ISO 31000 Badges */
        .iso-badge {
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.6rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            z-index: 50;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            pointer-events: none;
        }
        .iso-phase-1 { background: rgba(99, 102, 241, 0.85); color: white; }
        .iso-phase-2 { background: rgba(59, 130, 246, 0.85); color: white; }
        .iso-phase-3 { background: rgba(245, 158, 11, 0.85); color: white; }
        .iso-phase-4 { background: rgba(16, 185, 129, 0.85); color: white; }
        .iso-phase-5 { background: rgba(100, 116, 139, 0.85); color: white; }
'''

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Implementing ISO 31000 Badging System...")
    
    # STEP 1: Add CSS
    style_close = content.find('</style>')
    if style_close != -1:
        content = content[:style_close] + ISO_CSS + '\n    ' + content[style_close:]
        print("✅ Added ISO badge CSS")
    
    # STEP 2: Add badges to components
    # Define injection points with their badges
    injections = [
        # Phase 1: Risk Identification
        {
            'marker': 'class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-[2rem] p-8 text-white shadow-2xl border border-white/10 relative">',
            'badge': '<span class="iso-badge iso-phase-1">1. IDENTIFICATION</span>',
            'name': 'Map Container (Phase 1)'
        },
        
        # Phase 2: Risk Analysis - Financial Simulator
        {
            'marker': 'class="bg-white rounded-3xl shadow-2xl border-2 border-slate-200 p-8 relative overflow-hidden">',
            'badge': '<span class="iso-badge iso-phase-2">2. ANALYSIS</span>',
            'name': 'Financial Simulator (Phase 2)'
        },
        
        # Phase 2: Risk Analysis - Likelihood (already has badge from build script)
        # Phase 2: Risk Analysis - Financial Impact
        {
            'marker': 'class="bg-gradient-to-br from-indigo-900 to-indigo-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden border border-indigo-500/30">',
            'badge': '<span class="iso-badge iso-phase-2">2. ANALYSIS</span>',
            'name': 'Financial Impact (Phase 2)'
        },
        
        # Phase 2: Vanishing Yield
        {
            'marker': 'class="bg-gradient-to-r from-slate-900 to-slate-950 rounded-[3rem] p-10 border border-slate-800 relative overflow-hidden mb-12 shadow-2xl">',
            'badge': '<span class="iso-badge iso-phase-2">2. ANALYSIS</span>',
            'name': 'Vanishing Yield (Phase 2)'
        },
        
        # Phase 3: Risk Evaluation - Risk Matrix
        {
            'marker': 'class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6 rounded-3xl shadow-2xl border border-white/10 relative overflow-hidden">',
            'badge': '<span class="iso-badge iso-phase-3">3. EVALUATION</span>',
            'name': 'Risk Matrix (Phase 3)'
        },
        
        # Phase 3: Risk Control Tower
        {
            'marker': 'class="bg-gradient-to-br from-slate-900 via-rose-950 to-slate-900 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden group border border-rose-500/30">',
            'badge': '<span class="iso-badge iso-phase-3">3. EVALUATION</span>',
            'name': 'Risk Control Tower (Phase 3)'
        },
        
        # Phase 4: Risk Treatment - Standard Protocols  
        {
            'marker': 'class="bg-gradient-to-br from-slate-900 to-emerald-950 text-white p-8 rounded-3xl shadow-2xl relative overflow-hidden border border-emerald-500/30">',
            'badge': '<span class="iso-badge iso-phase-4">4. TREATMENT</span>',
            'name': 'Standard Protocols (Phase 4)'
        },
    ]
    
    badge_count = 0
    for injection in injections:
        marker = injection['marker']
        badge = injection['badge']
        name = injection['name']
        
        # Find first occurrence
        idx = content.find(marker)
        if idx != -1:
            # Insert badge right after the opening tag
            insert_pos = idx + len(marker)
            # Add newline and indentation for readability
            badge_html = '\n            ' + badge + '\n'
            content = content[:insert_pos] + badge_html + content[insert_pos:]
            badge_count += 1
            print(f"  ✅ {name}")
        else:
            print(f"  ⚠️  {name} - marker not found")
    
    print(f"\n✅ Added {badge_count} ISO badges")
    
    # STEP 3: Write
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ ISO 31000 BADGING COMPLETE!")
    print("\n🔄 Refresh browser to see:")
    print("  • Phase 1 badges (Indigo) on Map")
    print("  • Phase 2 badges (Blue) on Financial, Likelihood, Vanishing Yield")
    print("  • Phase 3 badges (Amber) on Risk Matrix, Control Tower")
    print("  • Phase 4 badges (Emerald) on Standard Protocols")

if __name__ == "__main__":
    main()
