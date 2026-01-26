import json

# Load hybrid data
with open('data/output/all_blocks_data_hybrid.json', 'r') as f:
    data = json.load(f)

# Sort by risk score
sorted_blocks = sorted(data.items(), key=lambda x: x[1]['risk_score'], reverse=True)

print("\n" + "=" * 120)
print("TOP 20 BLOCKS - HYBRID MULTI-FACTOR SCORING")
print("=" * 120)
print(f"{'Rank':<6} {'Block':<10} {'Risk':<8} {'Severity':<12} {'AR%':<7} {'Loss(Jt)':<12} {'SPH':<6} {'Gap%':<8} {'Old Rank':<10} {'Change':<8}")
print("=" * 120)

for i, (code, d) in enumerate(sorted_blocks[:20], 1):
    rank_change = i - d['rank_original']
    change_str = f"{rank_change:+d}"
    
    print(f"{i:<6} {code:<10} {d['risk_score']:<8.1f} {d['severity_hybrid']:<12} "
          f"{d.get('attack_rate',0):<7.1f} {d.get('loss_value_juta',0):<12.1f} "
          f"{d.get('sph',0):<6} {d.get('gap_pct',0):<8.1f} {d['rank_original']:<10} {change_str:<8}")

print("\n" + "=" * 120)
print("SEVERITY DISTRIBUTION")
print("=" * 120)

severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
for d in data.values():
    sev = d.get('severity_hybrid', 'LOW')
    severity_counts[sev] = severity_counts.get(sev, 0) + 1

for sev, count in severity_counts.items():
    print(f"{sev:<12}: {count} blocks")

# Total loss comparison
old_top20 = sorted(data.items(), key=lambda x: x[1]['rank_original'])[:20]
old_top20_loss = sum(d.get('loss_value_juta', 0) for _, d in old_top20)

new_top20_loss = sum(d.get('loss_value_juta', 0) for _, d in sorted_blocks[:20])

print("\n" + "=" * 120)
print("FINANCIAL IMPACT")
print("=" * 120)
print(f"Total Loss - OLD Top 20: Rp {old_top20_loss:,.1f} Juta")
print(f"Total Loss - NEW Top 20: Rp {new_top20_loss:,.1f} Juta")
print(f"Improvement: Rp {(new_top20_loss - old_top20_loss):+,.1f} Juta ({((new_top20_loss/old_top20_loss - 1) * 100):+.1f}%)")
print("=" * 120)
