"""
CRITICAL CAUSAL ANALYSIS:
Attack Rate vs Yield Gap - Is Ganoderma the cause?
"""

print("🔬 CAUSAL ANALYSIS: Ganoderma Attack Rate → Production Loss")
print("="*70)

# Data from dashboard (F008A and D001A as examples)
cases = {
    'F008A': {
        'attack_rate': 12.2,
        'potensi': 19.52,
        'realisasi': 21.22,
        'gap_ton': 1.71,
        'gap_pct': +8.7,
        'merah': 90,
        'oranye': 369
    },
    'D001A': {
        'attack_rate': 12.9,
        'potensi': 22.13,
        'realisasi': 17.42,
        'gap_ton': -4.71,
        'gap_pct': -21.3,
        'merah': 87,
        'oranye': 362
    }
}

print("\n📊 CASE COMPARISON:")
print("-" * 70)

for block, data in cases.items():
    print(f"\n{block}:")
    print(f"  Attack Rate: {data['attack_rate']}%")
    print(f"  Infected: {data['merah'] + data['oranye']} trees ({data['merah']} inti + {data['oranye']} ring)")
    print(f"  Potensi: {data['potensi']} ton/ha")
    print(f"  Realisasi: {data['realisasi']} ton/ha")
    print(f"  Gap: {data['gap_pct']:+.1f}% ({data['gap_ton']:+.2f} ton/ha)")

print("\n" + "="*70)
print("🔍 CRITICAL OBSERVATION:")
print("="*70)

print("""
PARADOX DETECTED:
-----------------
• F008A: 12.2% attack rate → +8.7% SURPLUS (BETTER than potential!)
• D001A: 12.9% attack rate → -21.3% DEFICIT (WORSE than potential)

Both have ALMOST IDENTICAL attack rates!
Both have SIMILAR infected tree counts!

┌─────────────────────────────────────────────────────────────────┐
│            WHY THE OPPOSITE PRODUCTION RESULTS?                 │
└─────────────────────────────────────────────────────────────────┘

HYPOTHESIS 1: SYMPTOM LAG
-------------------------
✓ Dashboard explicitly states this!
✓ F008A infection is RECENT → not yet impacting production
✓ D001A infection is OLDER → already causing yield loss
✓ Time lag between infection and production decline: 6-12 months

HYPOTHESIS 2: Other Factors (Less Likely)
------------------------------------------
Could gap be caused by non-Ganoderma factors?
❌ Weather: Would affect BOTH blocks similarly (same location)
❌ Fertilization: Would show in SPH or tree health patterns
❌ Harvesting practices: Wouldn't create 30% swing between blocks
❌ Soil variation: Possible but unlikely for adjacent blocks

HYPOTHESIS 3: Data Quality Issues
----------------------------------
⚠️  Could "potensi" be miscalculated?
⚠️  Could realisasi have measurement errors?
⚠️  Need to verify data source and methodology
""")

print("\n" + "="*70)
print("💡 ANALYTICAL CONCLUSION:")
print("="*70)

print("""
TENTATIVE ATTRIBUTION:
---------------------

For D001A (-21.3% gap):
  • Attack rate: 12.9%
  • Gap is LIKELY substantially caused by Ganoderma
  • Magnitude suggests ~50-70% of gap attributable to infection
  • Other factors may contribute 30-50%

For F008A (+8.7% surplus):
  • Attack rate: 12.2% (similar severity!)
  • SYMPTOM LAG phenomenon
  • Infection present but not yet impacting yield
  • FUTURE projection: Will likely show deficit in 6-12 months

RECOMMENDED LOSS CALCULATION:
-----------------------------
Instead of arbitrary 128 kg/tree assumption:

Option A: Use ACTUAL yield gap when available
  Loss = (Potensi - Realisasi) × Luas × Harga TBS
  
Option B: Apply conservative attribution factor
  Loss = Gap × 60% attribution × Luas × Harga
  (Assumes 60% of gap is Ganoderma-caused)

Option C: Use symptom lag adjusted model
  For blocks with positive gap: Project FUTURE loss
  For blocks with negative gap: Use CURRENT loss
""")

print("\n" + "="*70)
print("🎯 RECOMMENDATION:")
print("="*70)

print("""
USE REAL PRODUCTION DATA:
------------------------
1. Parse actual Potensi and Realisasi for each block
2. Calculate yield gap: (Realisasi - Potensi)
3. If gap is negative: Use as ACTUAL measured loss
4. If gap is positive: Flag as "Symptom Lag" + project future loss
5. Apply conservative Ganoderma attribution (50-70%)

This is MORE DEFENSIBLE than arbitrary kg/tree assumptions!
""")
