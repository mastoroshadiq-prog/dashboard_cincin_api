"""
HYBRID MULTI-FACTOR RISK SCORING SYSTEM
Mengimplementasikan severity classification berbasis:
- Attack Rate (40%)
- Financial Loss (30%)
- SPH Population Health (15%)
- Yield Gap (15%)
"""

import json
import pandas as pd
from pathlib import Path

print("=" * 80)
print("🔥 IMPLEMENTING HYBRID MULTI-FACTOR RISK SCORING")
print("=" * 80)

# Load existing data
input_file = 'data/output/all_blocks_data.json'
with open(input_file, 'r') as f:
    blocks_data = json.load(f)

print(f"\n✅ Loaded {len(blocks_data)} blocks from {input_file}")

def calculate_ar_score(ar):
    """Score Attack Rate (0-100)"""
    if ar >= 10:
        return 100
    elif ar >= 7:
        return 75
    elif ar >= 5:
        return 50
    elif ar >= 3:
        return 25
    else:
        return 0

def calculate_financial_score(loss_juta):
    """Score Financial Loss (0-100)"""
    if loss_juta >= 150:
        return 100
    elif loss_juta >= 100:
        return 75
    elif loss_juta >= 50:
        return 50
    elif loss_juta >= 25:
        return 25
    else:
        return 0

def calculate_sph_score(sph):
    """Score SPH - lower is worse (0-100)"""
    if sph is None or sph == 0:
        return 50  # Default moderate if no data
    
    if sph < 80:
        return 100  # Crisis
    elif sph < 100:
        return 75
    elif sph < 120:
        return 50
    elif sph < 130:
        return 25
    else:
        return 0  # Healthy

def calculate_gap_score(gap_pct):
    """Score Yield Gap - more negative is worse (0-100)"""
    if gap_pct <= -20:
        return 100
    elif gap_pct <= -15:
        return 75
    elif gap_pct <= -10:
        return 50
    elif gap_pct <= -5:
        return 25
    else:
        return 0  # Surplus or minimal gap

def calculate_risk_score(block_data):
    """Calculate composite risk score"""
    # Get parameters
    ar = block_data.get('attack_rate', 0)
    loss_juta = block_data.get('loss_value_juta', 0)
    sph = block_data.get('sph', 130)  # Default healthy if missing
    gap_pct = block_data.get('gap_pct', 0)
    
    # Calculate component scores
    ar_score = calculate_ar_score(ar)
    financial_score = calculate_financial_score(loss_juta)
    sph_score = calculate_sph_score(sph)
    gap_score = calculate_gap_score(gap_pct)
    
    # Weighted composite (total = 100)
    risk_score = (
        ar_score * 0.40 +
        financial_score * 0.30 +
        sph_score * 0.15 +
        gap_score * 0.15
    )
    
    return {
        'risk_score': round(risk_score, 2),
        'ar_score': ar_score,
        'financial_score': financial_score,
        'sph_score': sph_score,
        'gap_score': gap_score
    }

def classify_severity_hybrid(risk_score):
    """Classify severity based on risk score"""
    if risk_score >= 70:
        return 'CRITICAL'
    elif risk_score >= 50:
        return 'HIGH'
    elif risk_score >= 30:
        return 'MEDIUM'
    else:
        return 'LOW'

# Process all blocks
print("\n" + "=" * 80)
print("Processing blocks with Hybrid Scoring...")
print("=" * 80)

for block_code, data in blocks_data.items():
    # Store original severity
    data['severity_original'] = data.get('severity', 'UNKNOWN')
    data['rank_original'] = data.get('rank', 999)
    
    # Calculate new risk score
    score_breakdown = calculate_risk_score(data)
    
    # Add to block data
    data['risk_score'] = score_breakdown['risk_score']
    data['ar_score'] = score_breakdown['ar_score']
    data['financial_score'] = score_breakdown['financial_score']
    data['sph_score'] = score_breakdown['sph_score']
    data['gap_score'] = score_breakdown['gap_score']
    
    # Classify new severity
    data['severity_hybrid'] = classify_severity_hybrid(data['risk_score'])

# Re-rank based on risk score
sorted_by_risk = sorted(blocks_data.items(), 
                       key=lambda x: x[1]['risk_score'], 
                       reverse=True)

for rank, (block_code, data) in enumerate(sorted_by_risk, 1):
    data['rank_hybrid'] = rank
    # Final severity is hybrid
    data['severity'] = data['severity_hybrid']
    data['rank'] = rank

print(f"\n✅ Processed {len(blocks_data)} blocks")

# Generate comparison report
print("\n" + "=" * 80)
print("SEVERITY CHANGES REPORT")
print("=" * 80)

changes = []
for block_code, data in blocks_data.items():
    old_sev = data['severity_original']
    new_sev = data['severity_hybrid']
    old_rank = data['rank_original']
    new_rank = data['rank_hybrid']
    
    if old_sev != new_sev or abs(old_rank - new_rank) > 5:
        changes.append({
            'block': block_code,
            'old_severity': old_sev,
            'new_severity': new_sev,
            'old_rank': old_rank,
            'new_rank': new_rank,
            'rank_change': new_rank - old_rank,
            'risk_score': data['risk_score'],
            'ar': data.get('attack_rate', 0),
            'loss': data.get('loss_value_juta', 0),
            'sph': data.get('sph', 0),
            'gap': data.get('gap_pct', 0)
        })

# Sort by absolute rank change
changes.sort(key=lambda x: abs(x['rank_change']), reverse=True)

print("\n🔄 TOP 15 BLOCKS WITH BIGGEST CHANGES:")
print("-" * 80)
print(f"{'Block':<10} {'Old→New Sev':<20} {'Rank Δ':<10} {'Risk':<8} {'AR':<7} {'Loss':<10} {'SPH':<6}")
print("-" * 80)

for change in changes[:15]:
    severity_change = f"{change['old_severity']}→{change['new_severity']}"
    rank_delta = f"{change['rank_change']:+d}"
    
    print(f"{change['block']:<10} {severity_change:<20} {rank_delta:<10} "
          f"{change['risk_score']:<8.1f} {change['ar']:<7.1f} "
          f"{change['loss']:<10.1f} {change['sph']:<6}")

# Count severity distribution
print("\n" + "=" * 80)
print("SEVERITY DISTRIBUTION COMPARISON")
print("=" * 80)

old_dist = {}
new_dist = {}

for data in blocks_data.values():
    old_sev = data['severity_original']
    new_sev = data['severity_hybrid']
    
    old_dist[old_sev] = old_dist.get(old_sev, 0) + 1
    new_dist[new_sev] = new_dist.get(new_sev, 0) + 1

print(f"\n{'Severity':<12} {'OLD System':<15} {'NEW System':<15} {'Change':<10}")
print("-" * 80)
for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    old_count = old_dist.get(sev, 0)
    new_count = new_dist.get(sev, 0)
    change = new_count - old_count
    print(f"{sev:<12} {old_count:<15} {new_count:<15} {change:+d}")

# Calculate total loss coverage
print("\n" + "=" * 80)
print("FINANCIAL IMPACT COMPARISON")
print("=" * 80)

# Top 20 by old system
old_top20 = sorted(blocks_data.items(), 
                   key=lambda x: x[1]['rank_original'])[:20]
old_top20_loss = sum(data.get('loss_value_juta', 0) for _, data in old_top20)

# Top 20 by new system
new_top20 = sorted(blocks_data.items(), 
                   key=lambda x: x[1]['rank_hybrid'])[:20]
new_top20_loss = sum(data.get('loss_value_juta', 0) for _, data in new_top20)

print(f"\nTotal Loss in TOP 20 (OLD System): Rp {old_top20_loss:,.1f} Juta")
print(f"Total Loss in TOP 20 (NEW System): Rp {new_top20_loss:,.1f} Juta")
print(f"Improvement: Rp {(new_top20_loss - old_top20_loss):+,.1f} Juta ({((new_top20_loss/old_top20_loss - 1) * 100):+.1f}%)")

# Save updated data
output_file = 'data/output/all_blocks_data_hybrid.json'
with open(output_file, 'w') as f:
    json.dump(blocks_data, f, indent=2)

print(f"\n✅ Saved hybrid scoring data to: {output_file}")

# Also update the original file (backup first)
import shutil
backup_file = 'data/output/all_blocks_data_original_backup.json'
shutil.copy(input_file, backup_file)
print(f"✅ Backed up original to: {backup_file}")

with open(input_file, 'w') as f:
    json.dump(blocks_data, f, indent=2)

print(f"✅ Updated original file: {input_file}")

# Generate detailed Excel report
print("\n" + "=" * 80)
print("Generating Excel Comparison Report...")
print("=" * 80)

report_data = []
for block_code, data in sorted_by_risk:
    report_data.append({
        'Block': block_code,
        'Risk_Score': data['risk_score'],
        'Rank_New': data['rank_hybrid'],
        'Rank_Old': data['rank_original'],
        'Rank_Change': data['rank_hybrid'] - data['rank_original'],
        'Severity_New': data['severity_hybrid'],
        'Severity_Old': data['severity_original'],
        'Attack_Rate': data.get('attack_rate', 0),
        'AR_Score': data['ar_score'],
        'Financial_Loss_Juta': data.get('loss_value_juta', 0),
        'Financial_Score': data['financial_score'],
        'SPH': data.get('sph', 0),
        'SPH_Score': data['sph_score'],
        'Yield_Gap_Pct': data.get('gap_pct', 0),
        'Gap_Score': data['gap_score'],
        'Vanishing_Phase': data.get('vanishing_phase', 0),
        'Status_Narrative': data.get('status_narrative', ''),
        'Luas_Ha': data.get('luas_ha', 0)
    })

df_report = pd.DataFrame(report_data)
excel_file = 'data/output/hybrid_severity_comparison_report.xlsx'
df_report.to_excel(excel_file, index=False, sheet_name='Hybrid Scoring')

print(f"✅ Excel report saved: {excel_file}")

# Update JS embed file
js_output_file = 'data/output/blocks_data_embed.js'
with open(js_output_file, 'w') as f:
    f.write("const BLOCKS_DATA = ")
    json.dump(blocks_data, f, indent=2)
    f.write(";")

print(f"✅ Updated JS embed: {js_output_file}")

print("\n" + "=" * 80)
print("✅ HYBRID SCORING IMPLEMENTATION COMPLETE!")
print("=" * 80)
print("\nNext Steps:")
print("1. Review Excel report: hybrid_severity_comparison_report.xlsx")
print("2. Refresh dashboard to see new severity classifications")
print("3. Validate changes with field team")
print("=" * 80)
