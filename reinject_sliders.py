import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Likelihood component - search for unique marker
    likelihood_marker = '<!-- 3. TIME TO CRITICAL PROJECTION -->'
    idx_time_critical = content.find(likelihood_marker)
    
    if idx_time_critical == -1:
        print("ERROR: Time to Critical section not found")
        return
    
    # Inject Formula Parameters HTML BEFORE Time to Critical
    slider_html = '''
            
            <!-- FORMULA DISCLAIMER & PARAMETERS -->
            <div class="bg-black/30 rounded-2xl p-4 border border-blue-500/20">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest">Formula Parameters</span>
                    <button id="toggleFormulaInfo" class="text-xs text-blue-400 hover:text-blue-200 underline transition-colors">
                        ℹ️ Info
                    </button>
                </div>
                
                <!-- Collapsible Formula Explanation -->
                <div id="formulaExplanation" class="hidden mb-4 p-3 bg-slate-900/50 rounded-lg border border-blue-500/20">
                    <p class="text-xs text-blue-200 leading-relaxed mb-2">
                        <strong>Formula Basis:</strong> Likelihood score dihitung berdasarkan:
                    </p>
                    <ul class="text-xs text-blue-300 space-y-1 ml-4">
                        <li>• <strong>Attack Rate (AR):</strong> Primary indicator (40-95% range)</li>
                        <li>• <strong>SPH Density:</strong> Spread risk modifier (+5-10%)</li>
                    </ul>
                    <p class="text-xs text-yellow-300 mt-2 italic">
                        ⚠️ <strong>Note:</strong> Formula ini adalah estimasi empiris. 
                        Nilai aktual bergantung pada validasi <strong>domain expert</strong> dan kondisi lapangan spesifik.
                    </p>
                </div>
                
                <!-- Adjustable Weight Sliders -->
                <div class="space-y-3">
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">AR Weight</span>
                            <span class="text-white font-black" id="arWeightValue">1.0x</span>
                        </div>
                        <input type="range" id="arWeightSlider" min="0.5" max="2.0" step="0.1" value="1.0"
                            class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    
                    <div>
                        <div class="flex justify-between text-xs mb-1">
                            <span class="text-blue-300 font-bold">SPH Modifier</span>
                            <span class="text-white font-black" id="sphModifierValue">1.0x</span>
                        </div>
                        <input type="range" id="sphModifierSlider" min="0" max="2.0" step="0.1" value="1.0"
                            class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                    </div>
                    
                    <button id="recalculateLikelihood" 
                        class="w-full mt-2 px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black uppercase rounded-lg transition-colors shadow-lg hover:shadow-xl">
                        🔄 Recalculate
                    </button>
                </div>
            </div>
            
            '''
    
    # Insert before Time to Critical section
    content = content[:idx_time_critical] + slider_html + content[idx_time_critical:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ Formula Parameters & Sliders re-injected")
    print("✅ Sliders should now be visible in Likelihood component")
    print("\nPlease refresh browser and verify:")
    print("  • Formula Parameters section visible")
    print("  • AR Weight slider (0.5x - 2.0x)")
    print("  • SPH Modifier slider (0x - 2.0x)")
    print("  • ℹ️ Info button (click to expand explanation)")
    print("  • 🔄 Recalculate button")

if __name__ == "__main__":
    main()
