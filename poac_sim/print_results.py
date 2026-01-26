import pandas as pd
from pathlib import Path

def analyze_file(path):
    try:
        if not path.exists():
            return "File not found"
        df = pd.read_csv(path)
        if len(df) == 0:
            return "Empty data"
            
        over = len(df[df.Gap_Trees > 0]) / len(df) * 100
        under = len(df[df.Gap_Trees < 0]) / len(df) * 100
        mae = df['Gap_%'].abs().mean()
        avg_gap = df['Gap_%'].mean()
        
        return f"{over:6.1f}% | {under:7.1f}% | {mae:5.2f}% | {avg_gap:9.2f}%"
    except Exception as e:
        return f"Error: {e}"

base_dir = Path('data/output/validation_analysis')
print(f"{'PRESET':<15} | {'OVER %':<7} | {'UNDER %':<7} | {'MAE %':<6} | {'AVG GAP %':<9}")
print("-" * 65)

print("=== AME II ===")
for p in ['konservatif', 'standar', 'agresif']:
    path = base_dir / f'ameii_{p}_validation.csv'
    print(f"{p.title():<15} | {analyze_file(path)}")

print("\n=== AME IV ===")
for p in ['konservatif', 'standar', 'agresif']:
    path = base_dir / f'ameiv_{p}_validation.csv'
    print(f"{p.title():<15} | {analyze_file(path)}")
