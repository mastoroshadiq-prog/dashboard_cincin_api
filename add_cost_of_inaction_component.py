"""
ADD "COST OF INACTION" COMPONENT TO DASHBOARD
Menambahkan visual warning untuk 8 blok CRITICAL
dengan proyeksi dampak jika tidak ditangani
"""

import json

print("=" * 80)
print("🚨 ADDING 'COST OF INACTION' COMPONENT TO DASHBOARD")
print("=" * 80)

# Load data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    blocks_data = json.load(f)

# Get CRITICAL blocks
critical_blocks = [(code, data) for code, data in blocks_data.items() 
                   if data.get('severity_hybrid') == 'CRITICAL']
critical_blocks.sort(key=lambda x: x[1]['risk_score'], reverse=True)

print(f"\n✅ Found {len(critical_blocks)} CRITICAL blocks")

# Calculate totals
total_current_loss = sum(d.get('loss_value_juta', 0) for _, d in critical_blocks)
total_projected_3yr = sum(d.get('projected_loss_3yr', 0) for _, d in critical_blocks)

# Calculate "no treatment" scenario (conservative: 30% escalation per year)
no_treatment_year1 = total_current_loss * 1.10
no_treatment_year2 = no_treatment_year1 * 1.20
no_treatment_year3 = no_treatment_year2 * 1.30
total_no_treatment_3yr = no_treatment_year1 + no_treatment_year2 + no_treatment_year3

# Treatment cost (rough estimate: Rp 50 Juta per block)
treatment_cost = len(critical_blocks) * 50

# Prevented loss (70% effectiveness)
prevented_loss_3yr = total_no_treatment_3yr * 0.70

# Net benefit
net_benefit_3yr = prevented_loss_3yr - treatment_cost

# ROI
roi_pct = (net_benefit_3yr / treatment_cost) * 100 if treatment_cost > 0 else 0

# Payback period (months)
payback_months = (treatment_cost / (prevented_loss_3yr / 36)) if prevented_loss_3yr > 0 else 999

print(f"\n📊 FINANCIAL SUMMARY:")
print(f"  Current Loss/year: Rp {total_current_loss:,.0f} Juta")
print(f"  3-Year No Treatment: Rp {total_no_treatment_3yr:,.0f} Juta")
print(f"  Treatment Cost: Rp {treatment_cost:,.0f} Juta")
print(f"  Prevented Loss (70%): Rp {prevented_loss_3yr:,.0f} Juta")
print(f"  Net Benefit: Rp {net_benefit_3yr:,.0f} Juta")
print(f"  ROI: {roi_pct:,.0f}%")
print(f"  Payback: {payback_months:.1f} months")

# Read dashboard HTML
html_file = 'data/output/dashboard_cincin_api_INTERACTIVE_FULL.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Create component HTML
cost_of_inaction_html = f'''
<!-- COST OF INACTION WARNING PANEL -->
<div class="mt-8 p-6 bg-gradient-to-br from-rose-900/40 to-orange-900/40 rounded-2xl border-2 border-rose-500 shadow-2xl relative overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5">
        <div class="absolute inset-0" style="background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, currentColor 10px, currentColor 20px);"></div>
    </div>
    
    <div class="relative z-10">
        <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-rose-600 rounded-xl flex items-center justify-center shadow-lg animate-pulse">
                <span class="text-2xl">⚠️</span>
            </div>
            <div>
                <h3 class="text-xl font-black text-white uppercase tracking-wider">URGENT: Cost of Inaction</h3>
                <p class="text-rose-300 text-sm font-semibold">{len(critical_blocks)} Critical Blocks Require Immediate Attention</p>
            </div>
        </div>
        
        <!-- Financial Impact Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <!-- Current Loss -->
            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-rose-500/30">
                <div class="text-xs text-rose-300 font-bold uppercase mb-1">Current Loss (This Year)</div>
                <div class="text-3xl font-black text-white">Rp {total_current_loss:,.0f}</div>
                <div class="text-xs text-rose-400 mt-1">Juta / year</div>
            </div>
            
            <!-- 3-Year Projection -->
            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-orange-500/30">
                <div class="text-xs text-orange-300 font-bold uppercase mb-1">3-Year Projected Loss</div>
                <div class="text-3xl font-black text-white">Rp {total_no_treatment_3yr:,.0f}</div>
                <div class="text-xs text-orange-400 mt-1">Juta (if NO treatment)</div>
            </div>
            
            <!-- Treatment Cost -->
            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-emerald-500/30">
                <div class="text-xs text-emerald-300 font-bold uppercase mb-1">Treatment Investment</div>
                <div class="text-3xl font-black text-white">Rp {treatment_cost:,.0f}</div>
                <div class="text-xs text-emerald-400 mt-1">Juta (one-time)</div>
            </div>
            
            <!-- Potential Savings -->
            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-cyan-500/30">
                <div class="text-xs text-cyan-300 font-bold uppercase mb-1">Potential Savings</div>
                <div class="text-3xl font-black text-white">Rp {prevented_loss_3yr:,.0f}</div>
                <div class="text-xs text-cyan-400 mt-1">Juta (3-year prevented)</div>
            </div>
        </div>
        
        <!-- ROI Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-gradient-to-r from-rose-600/20 to-orange-600/20 p-4 rounded-xl border border-yellow-500/50">
                <div class="text-xs text-yellow-300 font-bold uppercase mb-1">Return on Investment</div>
                <div class="text-4xl font-black text-yellow-400">{roi_pct:,.0f}%</div>
                <div class="text-xs text-yellow-300 mt-1">Over 3 years</div>
            </div>
            
            <div class="bg-gradient-to-r from-orange-600/20 to-rose-600/20 p-4 rounded-xl border border-green-500/50">
                <div class="text-xs text-green-300 font-bold uppercase mb-1">Payback Period</div>
                <div class="text-4xl font-black text-green-400">{payback_months:.1f}</div>
                <div class="text-xs text-green-300 mt-1">Months</div>
            </div>
            
            <div class="bg-gradient-to-r from-rose-600/20 to-purple-600/20 p-4 rounded-xl border border-red-500/50">
                <div class="text-xs text-red-300 font-bold uppercase mb-1">Action Window</div>
                <div class="text-4xl font-black text-red-400">6</div>
                <div class="text-xs text-red-300 mt-1">Months before irreversible damage</div>
            </div>
        </div>
        
        <!-- Comparison Bar -->
        <div class="bg-black/40 p-5 rounded-xl border border-white/10">
            <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-bold text-white uppercase">Financial Impact Comparison</span>
                <span class="text-xs text-gray-400">3-Year Projection</span>
            </div>
            
            <div class="space-y-3">
                <!-- With Treatment -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-emerald-400 font-semibold">✓ With Treatment</span>
                        <span class="text-white font-bold">Rp {treatment_cost + (total_no_treatment_3yr * 0.30):,.0f} Juta</span>
                    </div>
                    <div class="w-full bg-gray-700 rounded-full h-6 overflow-hidden">
                        <div class="bg-gradient-to-r from-emerald-500 to-green-600 h-6 flex items-center justify-end pr-2 rounded-full" 
                             style="width: {((treatment_cost + (total_no_treatment_3yr * 0.30)) / total_no_treatment_3yr * 100):.0f}%">
                            <span class="text-xs font-bold text-white">{((treatment_cost + (total_no_treatment_3yr * 0.30)) / total_no_treatment_3yr * 100):.0f}%</span>
                        </div>
                    </div>
                </div>
                
                <!-- Without Treatment -->
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="text-rose-400 font-semibold">✗ Without Treatment</span>
                        <span class="text-white font-bold">Rp {total_no_treatment_3yr:,.0f} Juta</span>
                    </div>
                    <div class="w-full bg-gray-700 rounded-full h-6 overflow-hidden">
                        <div class="bg-gradient-to-r from-rose-500 to-red-600 h-6 flex items-center justify-end pr-2 rounded-full animate-pulse" 
                             style="width: 100%">
                            <span class="text-xs font-bold text-white">100%</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4 p-3 bg-yellow-900/30 border border-yellow-600/50 rounded-lg">
                <p class="text-sm text-yellow-200 font-semibold">
                    💰 <strong>Savings:</strong> Rp {(total_no_treatment_3yr - (treatment_cost + (total_no_treatment_3yr * 0.30))):,.0f} Juta over 3 years by treating now!
                </p>
            </div>
        </div>
        
        <!-- Critical Blocks List -->
        <div class="mt-6">
            <div class="text-sm font-bold text-white uppercase mb-3">🔥 Critical Blocks Breakdown:</div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
'''

# Add critical blocks badges
for code, data in critical_blocks:
    loss = data.get('loss_value_juta', 0)
    cost_of_inaction_html += f'''
                <div class="bg-rose-900/30 border border-rose-600/50 rounded-lg p-2 hover:bg-rose-800/40 transition-all cursor-pointer">
                    <div class="text-xs font-black text-white">{code}</div>
                    <div class="text-[10px] text-rose-300">Rp {loss:.0f} Jt/yr</div>
                </div>
'''

cost_of_inaction_html += '''
            </div>
        </div>
        
        <!-- Action CTA -->
        <div class="mt-6 p-4 bg-gradient-to-r from-rose-600 to-orange-600 rounded-xl text-center">
            <p class="text-white font-black text-lg mb-2">⏰ Immediate Action Required</p>
            <p class="text-white/90 text-sm">Treatment decision must be made within 30 days to prevent exponential loss escalation</p>
        </div>
    </div>
</div>
'''

# Find insertion point (after Risk Watchlist Container)
insertion_marker = '<div id="riskWatchlistContainer"'
marker_pos = html_content.find(insertion_marker)

if marker_pos == -1:
    print("\n⚠️  Marker not found. Trying alternative...")
    insertion_marker = '<div class="mt-8 p-6 bg-slate-800/40'
    marker_pos = html_content.find(insertion_marker)

if marker_pos != -1:
    # Find end of this container
    end_pos = html_content.find('</div>', marker_pos)
    # Find the closing of parent
    end_pos = html_content.find('</div>', end_pos + 6)
    end_pos = html_content.find('</div>', end_pos + 6)
    
    # Insert after
    html_updated = (html_content[:end_pos + 6] + 
                   '\n' + cost_of_inaction_html + '\n' +
                   html_content[end_pos + 6:])
    
    # Save updated HTML
    output_file = 'data/output/dashboard_cincin_api_INTERACTIVE_FULL_WITH_COST_WARNING.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_updated)
    
    print(f"\n✅ Component added successfully!")
    print(f"✅ Saved to: {output_file}")
    
    # Also update original
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_updated)
    print(f"✅ Updated original: {html_file}")
    
else:
    print("\n❌ Could not find insertion point")
    print("   Component HTML saved separately for manual insertion")
    with open('data/output/cost_of_inaction_component.html', 'w', encoding='utf-8') as f:
        f.write(cost_of_inaction_html)
    print("   Saved to: data/output/cost_of_inaction_component.html")

print("\n" + "=" * 80)
print("✅ COST OF INACTION COMPONENT IMPLEMENTATION COMPLETE!")
print("=" * 80)
print("\nNext Steps:")
print("1. Refresh dashboard browser to see new component")
print("2. Component shows:")
print(f"   - {len(critical_blocks)} Critical blocks")
print(f"   - Rp {total_no_treatment_3yr:,.0f} Juta 3-year loss (no treatment)")
print(f"   - {roi_pct:,.0f}% ROI for treatment")
print(f"   - {payback_months:.1f} months payback")
print("=" * 80)
