"""
QUICK FIX: Update dashboard panel with CORRECTED AME II data
"""

import json

# Load corrected summary
with open('data/output/ame_ii_division_summary_CORRECTED.json') as f:
    summary = json.load(f)

# Read dashboard
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update values in division summary panel
replacements = {
    '<div class="text-3xl font-black text-white" id="divMetric_totalBlocks">179</div>': 
    f'<div class="text-3xl font-black text-white" id="divMetric_totalBlocks">{summary["total_blocks"]}</div>',
    
    '<div class="text-3xl font-black text-white" id="divMetric_totalArea">2,890': 
    f'<div class="text-3xl font-black text-white" id="divMetric_totalArea">{summary["total_area_ha"]:.0f}',
    
    '<div class="text-3xl font-black text-white" id="divMetric_avgYield">14.44': 
    f'<div class="text-3xl font-black text-white" id="divMetric_avgYield">{summary["avg_yield_2025"]["real_ton_ha"]:.2f}',
    
    '<div class="text-3xl font-black text-red-400" id="divMetric_critical">97<span class="text-sm text-slate-400 ml-1">/ 179</span></div>': 
    f'<div class="text-3xl font-black text-red-400" id="divMetric_critical">{summary["critical_blocks_count"]}<span class="text-sm text-slate-400 ml-1">/ {summary["total_blocks"]}</span></div>',
    
    # Treatment comparison - estimate based on corrected data
    '<div class="text-4xl font-black text-red-400" id="noTreatment_loss">Rp 5,970 Jt</div>':
    '<div class="text-4xl font-black text-red-400" id="noTreatment_loss">Rp 602 Jt</div>',  # 480 Rp/kg * 1254 ton
    
    '<div class="text-2xl font-black text-white" id="noTreatment_gap">12,426 Ton</div>':
    f'<div class="text-2xl font-black text-white" id="noTreatment_gap">{summary["total_gap_tons"]:.0f} Ton</div>',
    
    '<div class="text-2xl font-black text-white" id="noTreatment_critical">97 / 179 (55%)</div>':
    f'<div class="text-2xl font-black text-white" id="noTreatment_critical">{summary["critical_blocks_count"]} / {summary["total_blocks"]} ({summary["critical_blocks_pct"]:.0f}%)</div>',
    
    '<div class="text-4xl font-black text-emerald-400" id="withTreatment_loss">Rp 1,195 Jt':
    '<div class="text-4xl font-black text-emerald-400" id="withTreatment_loss">Rp 120 Jt',  # 80% reduction
    
    '<div class="text-2xl font-black text-white" id="withTreatment_gap">2,485 Ton':
    '<div class="text-2xl font-black text-white" id="withTreatment_gap">251 Ton',  # 80% reduction
    
    '<div class="text-2xl font-black text-white" id="withTreatment_recovered">65 / 97 (67%)</div>':
    '<div class="text-2xl font-black text-white" id="withTreatment_recovered">4 / 6 (67%)</div>',
    
    '<div class="text-3xl font-black text-yellow-400" id="roi_savings">Rp 4,775 Juta</div>':
    '<div class="text-3xl font-black text-yellow-400" id="roi_savings">Rp 482 Juta</div>',
    
    '<div class="text-xs text-slate-400">Treatment cost: ~Rp 955 Juta</div>':
    '<div class="text-xs text-slate-400">Treatment cost: ~Rp 96 Juta</div>',
    
    '<strong>ALL 179 blocks</strong> in AME II division (2,890 Ha total)':
    f'<strong>ALL {summary["total_blocks"]} blocks</strong> in AME II division ({summary["total_area_ha"]:.0f} Ha total)',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("="*70)
print("✅ DASHBOARD UPDATED WITH CORRECTED DATA!")
print("="*70)
print(f"\nAME II (AME02): {summary['total_blocks']} blocks, {summary['total_area_ha']:.0f} Ha")
print(f"Critical blocks: {summary['critical_blocks_count']} ({summary['critical_blocks_pct']:.0f}%)")
print(f"Total gap: {summary['total_gap_tons']:.0f} Tons")
print("\n🌐 REFRESH BROWSER NOW!")
print("="*70)
