"""
Replace 2 charts with single chart + toggle buttons
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the side-by-side charts section with single chart + toggles
old_charts = '''                    <!-- Side-by-Side Charts -->
                    <div class="grid grid-cols-2 gap-6">
                        
                        <!-- NO TREATMENT -->
                        <div class="bg-red-900/10 p-6 rounded-xl border-2 border-red-500/30">
                            <h3 class="text-lg font-bold text-red-400 mb-4">❌ No Treatment</h3>
                            <div style="height: 400px;">
                                <canvas id="modalNoTreatmentChart"></canvas>
                            </div>
                        </div>

                        <!-- WITH TREATMENT -->
                        <div class="bg-emerald-900/10 p-6 rounded-xl border-2 border-emerald-500/30">
                            <h3 class="text-lg font-bold text-emerald-400 mb-4">✅ With Treatment</h3>
                            <div style="height: 400px;">
                                <canvas id="modalWithTreatmentChart"></canvas>
                            </div>
                        </div>

                    </div>'''

new_chart = '''                    <!-- Single Comparison Chart with Toggle -->
                    <div class="bg-slate-900/50 p-6 rounded-xl border-2 border-indigo-500/30">
                        
                        <!-- Toggle Buttons -->
                        <div class="flex items-center gap-3 mb-6">
                            <span class="text-sm text-slate-400 font-bold uppercase">Compare Factor:</span>
                            <button onclick="renderComparisonChart('ar')" id="toggleAR" 
                                class="px-4 py-2 rounded-lg text-sm font-bold bg-indigo-600 text-white border-2 border-indigo-400">
                                📈 Attack Rate (%)
                            </button>
                            <button onclick="renderComparisonChart('gap')" id="toggleGap"
                                class="px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">
                                📉 Gap Hasil (%)
                            </button>
                            <button onclick="renderComparisonChart('sph')" id="toggleSPH"
                                class="px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">
                                🌴 SPH (trees/ha)
                            </button>
                            <button onclick="renderComparisonChart('loss')" id="toggleLoss"
                                class="px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600">
                                💰 Loss (Juta)
                            </button>
                        </div>

                        <!-- Comparison Chart -->
                        <div class="bg-slate-800/50 p-4 rounded-xl">
                            <div style="height: 450px;">
                                <canvas id="modalComparisonChart"></canvas>
                            </div>
                        </div>

                        <!-- Legend Info -->
                        <div class="mt-4 flex justify-center gap-6">
                            <div class="flex items-center gap-2">
                                <div class="w-4 h-4 bg-red-500 rounded"></div>
                                <span class="text-sm text-white font-bold">No Treatment (Degradation)</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <div class="w-4 h-4 bg-emerald-500 rounded"></div>
                                <span class="text-sm text-white font-bold">With Treatment (70% Effective)</span>
                            </div>
                        </div>

                    </div>'''

content = content.replace(old_charts, new_chart)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Replaced 2 charts with single comparison chart")
print("✅ Added 4 toggle buttons (AR, Gap, SPH, Loss)")
print("✅ Added legend for red vs green lines")
print("\nNEXT: Update JavaScript to render single comparison chart")
