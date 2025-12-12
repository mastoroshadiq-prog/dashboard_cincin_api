import pandas as pd

print("\n" + "="*70)
print("HASIL VALIDASI METODE ADAPTIF vs DATA SENSUS")
print("="*70)

for divisi, file in [('AME II', 'metrics_AME_II.csv'), ('AME IV', 'metrics_AME_IV.csv')]:
    df = pd.read_csv(f'data/output/validation_adaptive/{file}')
    print(f'\n{divisi} (Avg Sensus: {df.iloc[0]["avg_sensus_pct"]:.1f}%):')
    print("-"*70)
    print(f"{'Metode':<28} {'r':>7} {'MAE':>8} {'Match':>7} {'OD':>7} {'Sig':>5}")
    print("-"*70)
    for _, row in df.iterrows():
        sig = "Ya" if row['significant'] == 'Ya' else "-"
        print(f"{row['method_display']:<28} {row['pearson_r']:>7.3f} {row['mae']:>7.1f}% {row['match_rate_5pct']:>6.0f}% {row['over_detection']:>6.2f}x {sig:>5}")
    
    # Find best
    best_r = df.loc[df['pearson_r'].idxmax()]
    best_mae = df.loc[df['mae'].idxmin()]
    print(f"\n  * Best Korelasi: {best_r['method_display']} (r={best_r['pearson_r']:.3f})")
    print(f"  * Lowest Error: {best_mae['method_display']} (MAE={best_mae['mae']:.1f}%)")

