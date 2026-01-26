"""
INSERT COST OF INACTION COMPONENT - DIRECT METHOD
"""
import json

# Load critical blocks data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    blocks_data = json.load(f)

critical_blocks = [(code, data) for code, data in blocks_data.items() 
                   if data.get('severity_hybrid') == 'CRITICAL']
critical_blocks.sort(key=lambda x: x[1]['risk_score'], reverse=True)

# Calculate metrics
total_current_loss = sum(d.get('loss_value_juta', 0) for _, d in critical_blocks)
no_treat_3yr = total_current_loss * (1.1 + 1.32 + 1.72)  # Year 1 + 2 + 3 escalation
treatment_cost = len(critical_blocks) * 50
prevented_loss = no_treat_3yr * 0.70
net_benefit = prevented_loss - treatment_cost
roi_pct = (net_benefit / treatment_cost) * 100 if treatment_cost > 0 else 0
payback_months = (treatment_cost / (prevented_loss / 36)) if prevented_loss > 0 else 999

print(f"Critical Blocks: {len(critical_blocks)}")
print(f"Total Current Loss: Rp {total_current_loss:,.0f} Juta")
print(f"3-Year No Treatment: Rp {no_treat_3yr:,.0f} Juta")
print(f"Treatment Cost: Rp {treatment_cost:,.0f} Juta")
print(f"ROI: {roi_pct:,.0f}%")

# Create component HTML
component_html = f'''
                <!-- ============================================ -->
                <!-- COST OF INACTION WARNING PANEL -->
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
                                <p class="text-rose-300 text-sm font-semibold">{len(critical_blocks)} Critical Blocks Require Immediate Attention</p>
                            </div>
                        </div>
                        
                        <!-- Financial Impact Grid -->
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-rose-500/30">
                                <div class="text-xs text-rose-300 font-bold uppercase mb-1">Current Loss (This Year)</div>
                                <div class="text-3xl font-black text-white">Rp {total_current_loss:,.0f}</div>
                                <div class="text-xs text-rose-400 mt-1">Juta / year</div>
                            </div>
                            
                            <div class="bg-black/30 backdrop-blur-sm p-4 rounded-xl border border-orange-500/30">
                                <div class="text-xs text-orange-300 font-bold uppercase mb-1">3-Year Projected Loss</div>
                                <div class="text-3xl font-black text-white">Rp {no_treat_3yr:,.0f}</div>
                                <div class="text-xs text-orange-400 mt-1">Juta (if NO treatment)</div>
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
                        
                        <!-- Critical Blocks List -->
                        <div class="mt-6">
                            <div class="text-sm font-bold text-white uppercase mb-3">🔥 Critical Blocks:</div>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
'''

# Add critical blocks
for code, data in critical_blocks:
    loss = data.get('loss_value_juta', 0)
    component_html += f'''
                                <div class="bg-rose-900/30 border border-rose-600/50 rounded-lg p-2 hover:bg-rose-800/40 transition-all cursor-pointer">
                                    <div class="text-xs font-black text-white">{code}</div>
                                    <div class="text-[10px] text-rose-300">Rp {loss:.0f} Jt/yr</div>
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
'''

# Read original file
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point (after line 386 - closing div of riskWatchlistContainer)
insertion_line = 386  # After </div> of riskWatchlistContainer

# Insert component
lines.insert(insertion_line, component_html + '\n')

# Write back
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ Component inserted at line {insertion_line + 1}")
print(f"✅ File updated: dashboard_cincin_api_INTERACTIVE_FULL.html")
print("\n🎉 DONE! Refresh your browser to see 'Cost of Inaction' component")
