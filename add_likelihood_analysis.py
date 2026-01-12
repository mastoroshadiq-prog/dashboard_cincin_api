import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CHANGE GRID FROM 2 COLS TO 3 COLS
    # Find: <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
    # This is the current grid container for Financial + Vanishing
    old_grid = '<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">'
    
    if old_grid not in content:
        print("Error: Could not find grid container")
        return
    
    # Grid is already 3 cols, we just need to insert a new middle component
    # Find the closing of first column (Financial Metrics)
    # Then insert Likelihood component before Vanishing column
    
    # 2. CREATE LIKELIHOOD COMPONENT HTML
    likelihood_html = '''
<div class="lg:col-span-1 h-full">
    <!-- LIKELIHOOD & TREND ANALYSIS -->
    <div class="bg-gradient-to-br from-blue-900 to-blue-950 text-white p-6 rounded-3xl shadow-xl relative overflow-hidden group border border-blue-500/30 h-full flex flex-col">
        <span class="iso-badge iso-phase-2">2. ANALYSIS</span>
        
        <!-- Decorative Background -->
        <div class="absolute top-0 right-0 w-48 h-48 bg-blue-400/10 rounded-bl-[100px] transition-transform group-hover:scale-110 pointer-events-none"></div>
        
        <!-- Header -->
        <div class="mb-6 relative z-10 border-b border-blue-500/30 pb-4">
            <h3 class="text-lg font-black text-blue-200 uppercase tracking-tight mb-1">Likelihood & Trend</h3>
            <p class="text-blue-300 text-xs font-bold">Analisis Probabilitas & Proyeksi</p>
        </div>
        
        <div class="space-y-6 relative z-10 flex-grow">
            <!-- 1. LIKELIHOOD SCORE (Gauge) -->
            <div class="bg-black/30 rounded-2xl p-5 border border-blue-500/20">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest">Probability Score</span>
                    <span class="text-xs bg-blue-800 text-blue-200 px-2 py-0.5 rounded font-bold">12 Months</span>
                </div>
                <div class="flex items-baseline gap-2">
                    <span class="text-5xl font-black text-white" id="likelihoodScore">--</span>
                    <span class="text-xl font-bold text-blue-400">%</span>
                </div>
                <p class="text-xs text-blue-300 mt-2 italic">Probabilitas mencapai Critical State</p>
                
                <!-- Visual Progress Bar -->
                <div class="mt-4 h-3 bg-slate-800 rounded-full overflow-hidden">
                    <div id="likelihoodBar" class="h-full bg-gradient-to-r from-blue-500 to-red-500 transition-all duration-1000" style="width: 0%"></div>
                </div>
            </div>
            
            <!-- 2. ATTACK RATE TREND (Mini Chart Placeholder) -->
            <div class="bg-black/30 rounded-2xl p-5 border border-blue-500/20">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-black text-blue-300 uppercase tracking-widest">Attack Rate Trend</span>
                    <span class="text-xs bg-blue-800 text-blue-200 px-2 py-0.5 rounded font-bold">6 Months</span>
                </div>
                
                <!-- Mini Chart Container -->
                <div class="h-24 relative bg-slate-900/50 rounded-xl p-2 border border-white/5">
                    <canvas id="trendMiniChart" class="w-full h-full"></canvas>
                </div>
                
                <!-- Trend Summary -->
                <div class="mt-3 flex items-center justify-between">
                    <div>
                        <p class="text-xs text-blue-300">Change Rate</p>
                        <p class="text-lg font-black text-white" id="trendVelocity">--</p>
                    </div>
                    <div id="trendBadge" class="px-3 py-1 rounded-full text-xs font-black bg-red-900/50 text-red-300">
                        🚀 ACCELERATING
                    </div>
                </div>
            </div>
            
            <!-- 3. TIME TO CRITICAL PROJECTION -->
            <div class="bg-black/30 rounded-2xl p-5 border border-blue-500/20">
                <span class="text-xs font-black text-blue-300 uppercase tracking-widest block mb-3">Time to Critical (SPH <100)</span>
                <div class="flex items-baseline gap-2 mb-2">
                    <span class="text-4xl font-black text-white" id="timeTocrítica">--</span>
                    <span class="text-lg font-bold text-blue-400">Bulan</span>
                </div>
                <p class="text-xs text-blue-300 italic">Proyeksi jika trend continues</p>
                
                <!-- Timeline Visual -->
                <div class="mt-4 flex items-center gap-2">
                    <div class="flex-grow h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div id="timelineBar" class="h-full bg-gradient-to-r from-emerald-500 via-yellow-500 to-red-500" style="width: 60%"></div>
                    </div>
                    <span class="text-xs font-bold text-slate-400">⚠️</span>
                </div>
            </div>
        </div>
    </div>
</div>
'''

    # 3. FIND INSERTION POINT
    # We need to insert AFTER Financial Metrics column closes, BEFORE Vanishing Yield starts
    # Financial column ends with: </div></div>
    # Then immediately: <div class="lg:col-span-2 h-full"> (Vanishing starts)
    
    vanishing_start_marker = '<div class="lg:col-span-2 h-full"><div'
    idx_vanishing = content.find(vanishing_start_marker)
    
    if idx_vanishing == -1:
        print("Error: Could not find Vanishing Yield start marker")
        return
    
    # Insert Likelihood component BEFORE Vanishing
    content_new = content[:idx_vanishing] + likelihood_html + '\n' + content[idx_vanishing:]
    
    # 4. ADJUST VANISHING YIELD COLUMN SPAN (from 2 to 1)
    # Change: lg:col-span-2 → lg:col-span-1
    content_new = content_new.replace(
        '<div class="lg:col-span-2 h-full"><div',
        '<div class="lg:col-span-1 h-full"><div'
    )
    
    print("✅ Injected Likelihood & Trend Analysis component")
    print("✅ Adjusted Vanishing Yield column span (2→1)")

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content_new)
        
    print("✅ Phase 2 enhancement complete - Dashboard now has 3-column analysis!")

if __name__ == "__main__":
    main()
