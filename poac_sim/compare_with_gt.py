"""Compare Consensus Voting result with Ground Truth"""
import pandas as pd

# Load GT
df_gt = pd.read_excel('data/input/areal_inti_serangan_gano_AMEII_AMEIV.xlsx', sheet_name='Sheet1', header=[0, 1])
df_gt.columns = ['DIVISI', 'BLOK', 'TAHUN_TANAM', 'LUAS_SD_2024', 'PENAMBAHAN', 
                 'LUAS_SD_2025', 'TANAM', 'SISIP', 'SISIP_KENTOSAN', 'TOTAL_PKK',
                 'SPH', 'STADIUM_12', 'STADIUM_34', 'TOTAL_GANO', 'SERANGAN_PCT']

# Filter AME II only
df_ame2 = df_gt[df_gt['DIVISI'].str.contains('II|2', na=False, case=False)]
df_ame2 = df_ame2[~df_ame2['DIVISI'].str.contains('IV|4', na=False, case=False)]

print('GROUND TRUTH - AME II')
print('=' * 50)
print('Total Blok:', len(df_ame2))
total_pkk = df_ame2['TOTAL_PKK'].sum()
print('Total Pohon (TOTAL_PKK):', f'{total_pkk:,.0f}')
print()
print('GANODERMA DETECTION (Ground Truth):')
stadium_12 = df_ame2['STADIUM_12'].sum()
stadium_34 = df_ame2['STADIUM_34'].sum()
total_gano = df_ame2['TOTAL_GANO'].sum()
print(f'  Stadium 1-2:  {stadium_12:,.0f}')
print(f'  Stadium 3-4:  {stadium_34:,.0f}')
print(f'  TOTAL GANO:   {total_gano:,.0f}')
print()
avg_serangan = df_ame2['SERANGAN_PCT'].mean()
print(f'Avg Serangan %: {avg_serangan:.2f}%')
print()
print('=' * 50)
print('COMPARISON: Consensus Voting vs Ground Truth')
print('=' * 50)
print()
print(f'GT TOTAL_GANO (sensus):       {total_gano:,.0f}')
print(f'Consensus Voting (algorithm): 1,022')
print()
diff = 1022 - total_gano
diff_pct = diff / total_gano * 100 if total_gano > 0 else 0
print(f'Difference: {diff:+,.0f} ({diff_pct:+.1f}%)')
print()
if diff < 0:
    print('STATUS: Consensus Voting UNDER-DETECT dibanding GT')
else:
    print('STATUS: Consensus Voting OVER-DETECT dibanding GT')
