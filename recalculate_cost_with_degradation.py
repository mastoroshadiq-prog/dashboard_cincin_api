"""
RECALCULATE COST OF INACTION WITH DEGRADATION MODEL
Dan buat komponen detail per-block
"""
import json

print("="*80)
print("RECALCULATING COST OF INACTION - WITH DEGRADATION")
print("="*80)

# Load data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    blocks_data = json.load(f)

# Get CRITICAL blocks
critical_blocks = [(code, data) for code, data in blocks_data.items() 
                   if data.get('severity_hybrid') == 'CRITICAL']
critical_blocks.sort(key=lambda x: x[1]['risk_score'], reverse=True)

print(f"\n✅ Found {len(critical_blocks)} CRITICAL blocks")

# DEGRADATION MODEL (realistic projections)
def calculate_degradation_projection(block_code, block_data):
    """
    Calculate realistic 3-year projection WITH degradation if no treatment
    """
    current_ar = block_data.get('attack_rate', 0)
    current_gap_pct = block_data.get('gap_pct', 0)
    current_sph = block_data.get('sph', 130)
    current_loss_juta = block_data.get('loss_value_juta', 0)
    luas_ha = block_data.get('luas_ha', 0)
    
    # TBS Price (estimate - bisa di-adjust)
    TBS_PRICE_PER_TON = 1_500_000  # Rp 1.5 Juta per ton
    
    # YEAR 1 (No Treatment)
    # AR increase: +2-3% per year (Ganoderma spread radial)
    ar_y1 = min(current_ar + 2.5, 25)  # Cap at 25%
    
    # Gap worsens: -5% additional decline (root degradation)
    gap_y1 = current_gap_pct - 5  # e.g., -20% becomes -25%
    
    # SPH decline: lose ~10 trees/ha per year (death from infection)
    sph_y1 = max(current_sph - 10, 50)  # Minimum 50
    
    # Loss calculation Year 1
    gap_ton_ha_y1 = abs(gap_y1) / 100 * 20  # Assume baseline 20 ton/ha potential
    loss_y1 = gap_ton_ha_y1 * luas_ha * (TBS_PRICE_PER_TON / 1_000_000)  # Juta
    
    # YEAR 2 (No Treatment - Accelerated)
    ar_y2 = min(ar_y1 + 3, 30)  # Spread accelerates
    gap_y2 = gap_y1 - 7  # Faster decline
    sph_y2 = max(sph_y1 - 15, 40)  # More deaths
    gap_ton_ha_y2 = abs(gap_y2) / 100 * 20
    loss_y2 = gap_ton_ha_y2 * luas_ha * (TBS_PRICE_PER_TON / 1_000_000)
    
    # YEAR 3 (No Treatment - Critical Phase)
    ar_y3 = min(ar_y2 + 4, 35)
    gap_y3 = gap_y2 - 10  # Severe decline
    sph_y3 = max(sph_y2 - 20, 30)  # Massive die-off
    
    # If SPH < 100, add "insolvency penalty"
    if sph_y3 < 100:
        gap_y3 = gap_y3 - 10  # Operational inefficiency
    
    gap_ton_ha_y3 = abs(gap_y3) / 100 * 20
    loss_y3 = gap_ton_ha_y3 * luas_ha * (TBS_PRICE_PER_TON / 1_000_000)
    
    # Cumulative 3-year loss
    total_3yr_loss = loss_y1 + loss_y2 + loss_y3
    
    return {
        'current': {
            'ar': current_ar,
            'gap_pct': current_gap_pct,
            'sph': current_sph,
            'loss_juta': current_loss_juta
        },
        'year1': {
            'ar': ar_y1,
            'gap_pct': gap_y1,
            'sph': sph_y1,
            'loss_juta': loss_y1
        },
        'year2': {
            'ar': ar_y2,
            'gap_pct': gap_y2,
            'sph': sph_y2,
            'loss_juta': loss_y2
        },
        'year3': {
            'ar': ar_y3,
            'gap_pct': gap_y3,
            'sph': sph_y3,
            'loss_juta': loss_y3
        },
        'total_3yr_loss': total_3yr_loss,
        'avg_annual_loss': total_3yr_loss / 3
    }

# Calculate for all CRITICAL blocks
projection_results = {}
total_current_loss = 0
total_3yr_loss = 0

print("\n" + "="*80)
print("DEGRADATION PROJECTION BY BLOCK")
print("="*80)
print(f"{'Block':<10} {'Current':<12} {'Year 1':<12} {'Year 2':<12} {'Year 3':<12} {'3-Yr Total':<12}")
print("-"*80)

for code, data in critical_blocks:
    proj = calculate_degradation_projection(code, data)
    projection_results[code] = proj
    
    total_current_loss += proj['current']['loss_juta']
    total_3yr_loss += proj['total_3yr_loss']
    
    print(f"{code:<10} "
          f"Rp {proj['current']['loss_juta']:<10,.0f} "
          f"Rp {proj['year1']['loss_juta']:<10,.0f} "
          f"Rp {proj['year2']['loss_juta']:<10,.0f} "
          f"Rp {proj['year3']['loss_juta']:<10,.0f} "
          f"Rp {proj['total_3yr_loss']:<10,.0f}")

print("-"*80)
print(f"{'TOTAL':<10} "
      f"Rp {total_current_loss:<10,.0f} "
      f"{'':<12} {'':<12} {'':<12} "
      f"Rp {total_3yr_loss:<10,.0f}")

# Save projections to file
output_data = {
    'total_blocks': len(critical_blocks),
    'total_current_loss_juta': total_current_loss,
    'total_3yr_loss_juta': total_3yr_loss,
    'projections_by_block': projection_results
}

with open('data/output/cost_of_inaction_projections.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"\n✅ Projections saved to: cost_of_inaction_projections.json")

# Calculate treatment economics
treatment_cost_per_block = 50  # Juta
total_treatment_cost = len(critical_blocks) * treatment_cost_per_block
prevented_loss = total_3yr_loss * 0.70  # 70% effectiveness
net_benefit = prevented_loss - total_treatment_cost
roi_pct = (net_benefit / total_treatment_cost) * 100 if total_treatment_cost > 0 else 0
payback_months = (total_treatment_cost / (prevented_loss / 36)) if prevented_loss > 0 else 999

print("\n" + "="*80)
print("FINANCIAL SUMMARY (WITH REALISTIC DEGRADATION)")
print("="*80)
print(f"Total Current Loss (Year 0):     Rp {total_current_loss:,.0f} Juta")
print(f"Total 3-Year Loss (No Treat):    Rp {total_3yr_loss:,.0f} Juta")
print(f"Treatment Cost ({len(critical_blocks)} blocks):      Rp {total_treatment_cost:,.0f} Juta")
print(f"Prevented Loss (70% eff):        Rp {prevented_loss:,.0f} Juta")
print(f"Net Benefit:                      Rp {net_benefit:,.0f} Juta")
print(f"ROI:                              {roi_pct:,.0f}%")
print(f"Payback Period:                   {payback_months:.1f} months")
print("="*80)

# Show example degradation detail for one block
example_block = critical_blocks[0]
example_code = example_block[0]
example_proj = projection_results[example_code]

print(f"\n📊 EXAMPLE DEGRADATION: {example_code}")
print("-"*80)
print("Parameter         Current    Year 1    Year 2    Year 3    Change")
print("-"*80)
print(f"Attack Rate       {example_proj['current']['ar']:.1f}%      "
      f"{example_proj['year1']['ar']:.1f}%     "
      f"{example_proj['year2']['ar']:.1f}%     "
      f"{example_proj['year3']['ar']:.1f}%     "
      f"+{example_proj['year3']['ar'] - example_proj['current']['ar']:.1f}%")

print(f"Yield Gap         {example_proj['current']['gap_pct']:.1f}%     "
      f"{example_proj['year1']['gap_pct']:.1f}%    "
      f"{example_proj['year2']['gap_pct']:.1f}%    "
      f"{example_proj['year3']['gap_pct']:.1f}%    "
      f"{example_proj['year3']['gap_pct'] - example_proj['current']['gap_pct']:.1f}%")

print(f"SPH               {example_proj['current']['sph']:.0f}        "
      f"{example_proj['year1']['sph']:.0f}       "
      f"{example_proj['year2']['sph']:.0f}       "
      f"{example_proj['year3']['sph']:.0f}       "
      f"{example_proj['year3']['sph'] - example_proj['current']['sph']:.0f}")

print(f"Loss (Juta)       {example_proj['current']['loss_juta']:.0f}        "
      f"{example_proj['year1']['loss_juta']:.0f}       "
      f"{example_proj['year2']['loss_juta']:.0f}       "
      f"{example_proj['year3']['loss_juta']:.0f}       "
      f"+{example_proj['year3']['loss_juta'] - example_proj['current']['loss_juta']:.0f}")

print("\n✅ DONE!")
