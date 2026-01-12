"""
UPDATE COST OF INACTION COMPONENT WITH CORRECTED DATA
+ ADD MODAL POPUP FOR PER-BLOCK DETAIL
"""
import json

print("="*80)
print("UPDATING COST OF INACTION COMPONENT - CORRECTED VERSION")
print("="*80)

# Load degradation projections
with open('data/output/cost_of_inaction_projections.json', 'r') as f:
    proj_data = json.load(f)

total_current = proj_data['total_current_loss_juta']
total_3yr = proj_data['total_3yr_loss_juta']
projections = proj_data['projections_by_block']
num_blocks = proj_data['total_blocks']

# Treatment economics
treatment_cost = num_blocks * 50
prevented_loss = total_3yr * 0.70
net_benefit = prevented_loss - treatment_cost
roi_pct = (net_benefit / treatment_cost) * 100
payback_months = (treatment_cost / (prevented_loss / 36))

print(f"\n📊 DATA SUMMARY:")
print(f"Total Blocks: {num_blocks}")
print(f"Current Loss: Rp {total_current:,.0f} Juta")
print(f"3-Year Loss (degradation): Rp {total_3yr:,.0f} Juta")
print(f"Treatment Cost: Rp {treatment_cost:,.0f} Juta")
print(f"ROI: {roi_pct:,.0f}%")

# Create updated component HTML
component_html = f'''
                <!-- ============================================ -->
                <!-- COST OF INACTION WARNING PANEL (CORRECTED) -->
                <!-- ============================================ -->
                <div class="mt-8 p-6 bg-gradient-to-br from-rose-900/40 to-orange-900/40 rounded-2xl border-2 border-rose-500 shadow-2xl relative overflow-hidden">
                    <div class="absolute inset-0 opacity-5" style="background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, currentColor 10px, currentColor 20px);"></div>
                    
                    <div class="relative z-10">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 bg-rose-600 rounded-xl flex items-center justify-center shadow-lg animate-pulse">
                                <span class="text-2xl">⚠️</span>
                            </div>
                            <div>
                                <h3 class="text-xl font-black text-white uppercase tracking-wider">URGENT: Cost of Inaction</h3>
                                <p class="text-rose-300 text-sm font-semibold">{num_blocks} Critical Blocks Require Immediate Attention</p>
                            </div>
                        </div>
                        
                        <!-- Financial Impact Grid -->
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-rose-500/30">
                                <div class="text-xs text-rose-300 font-bold uppercase mb-1">Current Loss (Year 0)</div>
                                <div class="text-3xl font-black text-white">Rp {total_current:,.0f}</div>
                                <div class="text-xs text-rose-400 mt-1">Juta / year</div>
                            </div>
                            
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-orange-500/30">
                                <div class="text-xs text-orange-300 font-bold uppercase mb-1">3-Year Projected Loss</div>
                                <div class="text-3xl font-black text-white">Rp {total_3yr:,.0f}</div>
                                <div class="text-xs text-orange-400 mt-1">Juta (with degradation)</div>
                            </div>
                            
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-emerald-500/30">
                                <div class="text-xs text-emerald-300 font-bold uppercase mb-1">Treatment Investment</div>
                                <div class="text-3xl font-black text-white">Rp {treatment_cost:,.0f}</div>
                                <div class="text-xs text-emerald-400 mt-1">Juta (one-time)</div>
                            </div>
                            
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-cyan-500/30">
                                <div class="text-xs text-cyan-300 font-bold uppercase mb-1">Potential Savings</div>
                                <div class="text-3xl font-black text-white">Rp {prevented_loss:,.0f}</div>
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
                                <div class="text-xs text-red-300 mt-1">Months before irreversible</div>
                            </div>
                        </div>
                        
                        <!-- Degradation Note -->
                        <div class="mb-6 p-4 bg-yellow-900/20 border border-yellow-600/40 rounded-xl">
                            <p class="text-sm text-yellow-200">
                                <strong>📉 Degradation Model:</strong> Projected loss includes realistic deterioration - 
                                Attack Rate increases (+2.5-4% yearly), Yield Gap worsens (-5 to -10%), 
                                SPH drops (-10 to -20 trees/ha yearly) if no treatment applied.
                            </p>
                        </div>
                        
                        <!-- Critical Blocks List (Clickable) -->
                        <div class="mt-6">
                            <div class="text-sm font-bold text-white uppercase mb-3">
                                🔥 Critical Blocks (Click for Detail):
                            </div>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
'''

# Sort blocks by total 3yr loss descending
sorted_blocks = sorted(projections.items(), 
                       key=lambda x: x[1]['total_3yr_loss'], 
                       reverse=True)

# Add clickable blocks
for code, data in sorted_blocks:
    current_loss = data['current']['loss_juta']
    total_3yr = data['total_3yr_loss']
    
    component_html += f'''
                                <div onclick="showBlockDetail('{code}')" 
                                     class="bg-rose-900/30 border border-rose-600/50 rounded-lg p-2 hover:bg-rose-800/50 hover:border-rose-500 hover:scale-105 transition-all cursor-pointer">
                                    <div class="text-xs font-black text-white">{code}</div>
                                    <div class="text-[10px] text-rose-300">Now: Rp {current_loss:.0f} Jt</div>
                                    <div class="text-[10px] text-orange-300">3yr: Rp {total_3yr:.0f} Jt</div>
                                </div>
'''

component_html += '''
                            </div>
                        </div>
                        
                        <!-- Action CTA -->
                        <div class="mt-6 p-4 bg-gradient-to-r from-rose-600 to-orange-600 rounded-xl text-center">
                            <p class="text-white font-black text-lg mb-2">⏰ Immediate Action Required</p>
                            <p class="text-white/90 text-sm">Treatment decision must be made within 30 days to prevent exponential loss escalation</p>
                        </div>
                    </div>
                </div>

                <!-- ============================================ -->
                <!-- MODAL: BLOCK DETAIL POPUP -->
                <!-- ============================================ -->
                <div id="blockDetailModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border-2 border-rose-500 max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                        <!-- Modal Header -->
                        <div class="sticky top-0 bg-gradient-to-r from-rose-600 to-orange-600 p-6 border-b border-white/10">
                            <div class="flex items-center justify-between">
                                <div>
                                    <h2 class="text-2xl font-black text-white" id="modalBlockCode">BLOK XXX</h2>
                                    <p class="text-white/80 text-sm">Cost of Inaction Detail Analysis</p>
                                </div>
                                <button onclick="closeBlockDetail()" class="text-white hover:text-rose-200 text-3xl font-bold">×</button>
                            </div>
                        </div>
                        
                        <!-- Modal Body -->
                        <div class="p-6 space-y-6">
                            <!-- Financial Summary -->
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div class="bg-black/40 p-4 rounded-xl border border-rose-500/30">
                                    <div class="text-xs text-rose-300 font-bold uppercase mb-1">Current Loss</div>
                                    <div class="text-2xl font-black text-white" id="modalCurrentLoss">--</div>
                                    <div class="text-xs text-rose-400">Juta/year</div>
                                </div>
                                <div class="bg-black/40 p-4 rounded-xl border border-orange-500/30">
                                    <div class="text-xs text-orange-300 font-bold uppercase mb-1">3-Year Total</div>
                                    <div class="text-2xl font-black text-white" id="modal3YrLoss">--</div>
                                    <div class="text-xs text-orange-400">Juta</div>
                                </div>
                                <div class="bg-black/40 p-4 rounded-xl border border-emerald-500/30">
                                    <div class="text-xs text-emerald-300 font-bold uppercase mb-1">Treatment</div>
                                    <div class="text-2xl font-black text-white">Rp 50</div>
                                    <div class="text-xs text-emerald-400">Juta</div>
                                </div>
                                <div class="bg-black/40 p-4 rounded-xl border border-cyan-500/30">
                                    <div class="text-xs text-cyan-300 font-bold uppercase mb-1">ROI</div>
                                    <div class="text-2xl font-black text-white" id="modalROI">--</div>
                                    <div class="text-xs text-cyan-400">%</div>
                                </div>
                            </div>
                            
                            <!-- Degradation Timeline Table -->
                            <div class="bg-black/30 p-5 rounded-xl border border-white/10">
                                <h3 class="text-lg font-black text-white mb-4">📉 Degradation Timeline (No Treatment)</h3>
                                <div class="overflow-x-auto">
                                    <table class="w-full text-sm">
                                        <thead>
                                            <tr class="border-b border-white/20">
                                                <th class="text-left text-rose-300 font-bold p-2">Parameter</th>
                                                <th class="text-center text-white font-bold p-2">Year 0<br/><span class="text-xs text-gray-400">(Current)</span></th>
                                                <th class="text-center text-orange-300 font-bold p-2">Year 1</th>
                                                <th class="text-center text-yellow-300 font-bold p-2">Year 2</th>
                                                <th class="text-center text-red-300 font-bold p-2">Year 3</th>
                                                <th class="text-center text-cyan-300 font-bold p-2">Change</th>
                                            </tr>
                                        </thead>
                                        <tbody id="modalDegradationTable">
                                            <!-- Will be populated by JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            
                            <!-- Treatment Impact -->
                            <div class="bg-gradient-to-r from-emerald-900/30 to-green-900/30 p-5 rounded-xl border border-emerald-500/50">
                                <h3 class="text-lg font-black text-white mb-3">✅ Impact of Treatment</h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <p class="text-sm text-emerald-200 mb-2"><strong>Prevented Loss (70% eff):</strong></p>
                                        <p class="text-2xl font-black text-emerald-400" id="modalPreventedLoss">--</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-green-200 mb-2"><strong>Net Benefit:</strong></p>
                                        <p class="text-2xl font-black text-green-400" id="modalNetBenefit">--</p>
                                    </div>
                                </div>
                                <p class="text-xs text-emerald-300 mt-3 italic">
                                    Treatment includes: Isolation trenching (4×4m), systemic fungicide, sanitation, and drainage improvement.
                                </p>
                            </div>
                        </div>
                        
                        <!-- Modal Footer -->
                        <div class="bg-slate-800/50 p-4 border-t border-white/10 text-center">
                            <button onclick="closeBlockDetail()" class="px-6 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-lg transition-all">
                                Close
                            </button>
                        </div>
                    </div>
                </div>
'''

# Embed projection data as JavaScript
js_data = f'''
                <script>
                // Cost of Inaction Projection Data (Embedded)
                const COST_PROJECTIONS = {json.dumps(projections, indent=4)};
                
                // Show block detail modal
                function showBlockDetail(blockCode) {{
                    const data = COST_PROJECTIONS[blockCode];
                    if (!data) {{
                        alert('Data not found for block: ' + blockCode);
                        return;
                    }}
                    
                    // Update modal content
                    document.getElementById('modalBlockCode').textContent = 'BLOK ' + blockCode;
                    document.getElementById('modalCurrentLoss').textContent =  'Rp ' + data.current.loss_juta.toFixed(0);
                    document.getElementById('modal3YrLoss').textContent = 'Rp ' + data.total_3yr_loss.toFixed(0);
                    
                    // Calculate ROI for this block
                    const treatment = 50;
                    const prevented = data.total_3yr_loss * 0.70;
                    const netBenefit = prevented - treatment;
                    const roi = (netBenefit / treatment * 100).toFixed(0);
                    
                    document.getElementById('modalROI').textContent = roi;
                    document.getElementById('modalPreventedLoss').textContent = 'Rp ' + prevented.toFixed(0) + ' Juta';
                    document.getElementById('modalNetBenefit').textContent = 'Rp ' + netBenefit.toFixed(0) + ' Juta';
                    
                    // Build degradation table
                    const tableHTML = `
                        <tr class="border-b border-white/10">
                            <td class="p-2 text-rose-200 font-semibold">Attack Rate</td>
                            <td class="p-2 text-center text-white">${{data.current.ar.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-orange-200">${{data.year1.ar.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-yellow-200">${{data.year2.ar.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-red-200">${{data.year3.ar.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-cyan-200 font-bold">+${{(data.year3.ar - data.current.ar).toFixed(1)}}%</td>
                        </tr>
                        <tr class="border-b border-white/10">
                            <td class="p-2 text-rose-200 font-semibold">Yield Gap</td>
                            <td class="p-2 text-center text-white">${{data.current.gap_pct.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-orange-200">${{data.year1.gap_pct.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-yellow-200">${{data.year2.gap_pct.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-red-200">${{data.year3.gap_pct.toFixed(1)}}%</td>
                            <td class="p-2 text-center text-cyan-200 font-bold">${{(data.year3.gap_pct - data.current.gap_pct).toFixed(1)}}%</td>
                        </tr>
                        <tr class="border-b border-white/10">
                            <td class="p-2 text-rose-200 font-semibold">SPH (trees/ha)</td>
                            <td class="p-2 text-center text-white">${{data.current.sph.toFixed(0)}}</td>
                            <td class="p-2 text-center text-orange-200">${{data.year1.sph.toFixed(0)}}</td>
                            <td class="p-2 text-center text-yellow-200">${{data.year2.sph.toFixed(0)}}</td>
                            <td class="p-2 text-center text-red-200">${{data.year3.sph.toFixed(0)}}</td>
                            <td class="p-2 text-center text-cyan-200 font-bold">${{(data.year3.sph - data.current.sph).toFixed(0)}} trees</td>
                        </tr>
                        <tr>
                            <td class="p-2 text-rose-200 font-semibold">Loss (Juta)</td>
                            <td class="p-2 text-center text-white font-bold">Rp ${{data.current.loss_juta.toFixed(0)}}</td>
                            <td class="p-2 text-center text-orange-200 font-bold">Rp ${{data.year1.loss_juta.toFixed(0)}}</td>
                            <td class="p-2 text-center text-yellow-200 font-bold">Rp ${{data.year2.loss_juta.toFixed(0)}}</td>
                            <td class="p-2 text-center text-red-200 font-bold">Rp ${{data.year3.loss_juta.toFixed(0)}}</td>
                            <td class="p-2 text-center text-cyan-200 font-bold">+Rp ${{(data.year3.loss_juta - data.current.loss_juta).toFixed(0)}}</td>
                        </tr>
                    `;
                    
                    document.getElementById('modalDegradationTable').innerHTML = tableHTML;
                    
                    // Show modal
                    document.getElementById('blockDetailModal').classList.remove('hidden');
                }}
                
                // Close modal
                function closeBlockDetail() {{
                    document.getElementById('blockDetailModal').classList.add('hidden');
                }}
                
                // Close on Escape key
                document.addEventListener('keydown', function(e) {{
                    if (e.key === 'Escape') closeBlockDetail();
                }});
                
                // Close on background click
                document.getElementById('blockDetailModal').addEventListener('click', function(e) {{
                    if (e.target === this) closeBlockDetail();
                }});
                </script>
'''

# Read HTML file
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find and replace old component (between line 387-500 approximately)
# Look for the old component marker
old_marker_start = '<!-- COST OF INACTION WARNING PANEL -->'
old_marker_end = '</div>\n                </div>'  # End of cost component

if old_marker_start in html_content:
    # Find positions
    start_pos = html_content.find(old_marker_start)
    
    # Find the end (look for the action CTA closing)
    search_from = start_pos
    cta_marker = 'Treatment decision must be made within 30 days'
    cta_pos = html_content.find(cta_marker, search_from)
    
    if cta_pos > 0:
        # Find closing divs after CTA
        end_search = cta_pos
        div_count = 0
        for i in range(cta_pos, len(html_content)):
            if html_content[i:i+6] == '</div>':
                div_count += 1
                if div_count == 3:  # Third closing div after CTA
                    end_pos = i + 6
                    break
        
        # Replace old component with new
        html_updated = (html_content[:start_pos] + 
                       component_html +
                       js_data +
                       html_content[end_pos:])
        
        # Save
        with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
            f.write(html_updated)
        
        print("\n✅ Component UPDATED with corrected data!")
        print("✅ Modal popup for per-block detail ADDED!")
        print(f"✅ File: dashboard_cincin_api_INTERACTIVE_FULL.html")
    else:
        print("\n⚠️  Could not find CTA marker for precise replacement")
        print("   Saving component separately...")
        with open('data/output/updated_cost_component.html', 'w') as f:
            f.write(component_html + js_data)
        print("   Saved to: updated_cost_component.html")
else:
    print("\n⚠️  Old component not found")
    print("   Saving new component separately...")
    with open('data/output/updated_cost_component.html', 'w') as f:
        f.write(component_html + js_data)
    print("   Saved to: updated_cost_component.html")

print("\n" + "="*80)
print("IMPLEMENTATION COMPLETE!")
print("="*80)
print("\n📊 Updated Metrics:")
print(f"  - Current Loss: Rp {total_current:,.0f} Juta")
print(f"  - 3-Year Projection: Rp {total_3yr:,.0f} Juta (WITH degradation)")
print(f"  - ROI: {roi_pct:,.0f}%")
print(f"  - Payback: {payback_months:.1f} months")
print("\n✨ New Features:")
print("  - Clickable block badges")
print("  - Modal popup with degradation timeline")
print("  - Per-block ROI calculation")
print("  - Detailed degradation table (AR, Gap, SPH, Loss)")
print("\n🎉 Refresh dashboard to see changes!")
print("="*80)
