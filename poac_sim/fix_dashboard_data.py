import pandas as pd
import json

print('='*80)
print('🔧 FIXING DATA ISSUES')
print('='*80)

# Load data
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)
df_ranked = pd.read_csv('data/output/all_blocks_ranked_by_severity.csv')

# Get F008A and D001A data
f008a = df[df['Unnamed: 0'] == 'F008A'].iloc[0]
d001a = df[df['Unnamed: 0'] == 'D001A'].iloc[0]

f008a_ndre = df_ranked[df_ranked['blok'] == 'F08'].iloc[0]
d001a_ndre = df_ranked[df_ranked['blok'] == 'D01'].iloc[0]

print('\n1️⃣ Checking TT for D001A:')
print(f'   D001A TT from Excel: {d001a["TT"]}')
print(f'   ✅ Correct: 2009')

print('\n2️⃣ Calculating loss for F008A:')
print(f'   Real: {f008a.iloc[170] / f008a["HA STATEMENT"]:.2f} Ton/Ha')
print(f'   Potensi: {f008a.iloc[173] / f008a["HA STATEMENT"]:.2f} Ton/Ha')
print(f'   Gap: {(f008a.iloc[170] - f008a.iloc[173]) / f008a["HA STATEMENT"]:.2f} Ton/Ha')

gap_f008a = (f008a.iloc[170] - f008a.iloc[173]) / f008a["HA STATEMENT"]

if gap_f008a > 0:
    # Surplus - no loss, actually gain
    loss_f008a_million = 0
    print(f'   ✅ F008A has SURPLUS (+{gap_f008a:.2f} Ton/Ha)')
    print(f'   Loss: Rp 0 (No loss, production exceeds potential)')
else:
    # Deficit - calculate loss
    loss_f008a_million = abs(gap_f008a) * f008a["HA STATEMENT"] * 1.5 / 1000
    print(f'   Loss: Rp {loss_f008a_million:.3f} Miliar')

print('\n3️⃣ Calculating loss for D001A:')
gap_d001a = (d001a.iloc[170] - d001a.iloc[173]) / d001a["HA STATEMENT"]
loss_d001a_million = abs(gap_d001a) * d001a["HA STATEMENT"] * 1.5 / 1000
print(f'   Gap: {gap_d001a:.2f} Ton/Ha')
print(f'   Loss: Rp {loss_d001a_million:.3f} Miliar')

# Recreate dashboard data with corrections
dashboard_data = {
    'F008A': {
        'code_full': 'F008A',
        'code_short': 'F 08',
        'blok_display': 'F008A',
        'tt': str(f008a['TT']),
        'age': 2026 - int(f008a['TT']),
        'luas': float(f008a['HA STATEMENT']),
        'total_trees': int(f008a_ndre['total_trees']),
        'merah': int(f008a_ndre['merah']),
        'oranye': int(f008a_ndre['oranye']),
        'kuning': int(f008a_ndre['kuning']),
        'hijau': int(f008a_ndre['hijau']),
        'spread_ratio': float(f008a_ndre['spread_ratio']),
        'infection_pct': float(f008a_ndre['infection_pct']),
        'severity_score': float(f008a_ndre['severity_score']),
        'real_ton': float(f008a.iloc[170]),
        'potensi_ton': float(f008a.iloc[173]),
        'real_ton_ha': float(f008a.iloc[170] / f008a['HA STATEMENT']),
        'potensi_ton_ha': float(f008a.iloc[173] / f008a['HA STATEMENT']),
        'gap_ton_ha': float(gap_f008a),
        'gap_pct': float((gap_f008a / (f008a.iloc[173] / f008a['HA STATEMENT'])) * 100),
        'pkk_stadium_12': int(f008a.iloc[55]),
        'pkk_stadium_34': int(f008a.iloc[56]),
        'pkk_total': int(f008a.iloc[57]),
        'pkk_pct': float((f008a.iloc[57] / f008a_ndre['total_trees']) * 100),
        'loss_per_year_million': float(loss_f008a_million),
        'loss_per_year_juta': float(loss_f008a_million * 1000),
        'sph': int(f008a_ndre['total_trees'] / f008a['HA STATEMENT'])
    },
    'D001A': {
        'code_full': 'D001A',
        'code_short': 'D 01',
        'blok_display': 'D001A',
        'tt': str(d001a['TT']),  # This should be 2009
        'age': 2026 - int(d001a['TT']),  # This should be 17
        'luas': float(d001a['HA STATEMENT']),
        'total_trees': int(d001a_ndre['total_trees']),
        'merah': int(d001a_ndre['merah']),
        'oranye': int(d001a_ndre['oranye']),
        'kuning': int(d001a_ndre['kuning']),
        'hijau': int(d001a_ndre['hijau']),
        'spread_ratio': float(d001a_ndre['spread_ratio']),
        'infection_pct': float(d001a_ndre['infection_pct']),
        'severity_score': float(d001a_ndre['severity_score']),
        'real_ton': float(d001a.iloc[170]),
        'potensi_ton': float(d001a.iloc[173]),
        'real_ton_ha': float(d001a.iloc[170] / d001a['HA STATEMENT']),
        'potensi_ton_ha': float(d001a.iloc[173] / d001a['HA STATEMENT']),
        'gap_ton_ha': float(gap_d001a),
        'gap_pct': float((gap_d001a / (d001a.iloc[173] / d001a['HA STATEMENT'])) * 100),
        'pkk_stadium_12': int(d001a.iloc[55]),
        'pkk_stadium_34': int(d001a.iloc[56]),
        'pkk_total': int(d001a.iloc[57]),
        'pkk_pct': float((d001a.iloc[57] / d001a_ndre['total_trees']) * 100),
        'loss_per_year_million': float(loss_d001a_million),
        'loss_per_year_juta': float(loss_d001a_million * 1000),
        'sph': int(d001a_ndre['total_trees'] / d001a['HA STATEMENT'])
    }
}

# Calculate combined
total_loss = dashboard_data['F008A']['loss_per_year_million'] + dashboard_data['D001A']['loss_per_year_million']

dashboard_data['combined'] = {
    'total_luas': dashboard_data['F008A']['luas'] + dashboard_data['D001A']['luas'],
    'total_loss_million': total_loss,
    'total_loss_juta': total_loss * 1000,
    'total_trees': dashboard_data['F008A']['total_trees'] + dashboard_data['D001A']['total_trees'],
    'total_infected': (dashboard_data['F008A']['merah'] + dashboard_data['F008A']['oranye'] + 
                      dashboard_data['D001A']['merah'] + dashboard_data['D001A']['oranye']),
    'avg_infection_pct': (dashboard_data['F008A']['infection_pct'] + dashboard_data['D001A']['infection_pct']) / 2
}

# Save corrected data
with open('data/output/dashboard_data_f008a_d001a_CORRECTED.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print('\n' + '='*80)
print('✅ CORRECTED DATA SUMMARY')
print('='*80)

print(f'\nF008A:')
print(f'  TT: {dashboard_data["F008A"]["tt"]} (Age: {dashboard_data["F008A"]["age"]} years)')
print(f'  Gap: {dashboard_data["F008A"]["gap_pct"]:.1f}% (SURPLUS)')
print(f'  Loss: Rp {dashboard_data["F008A"]["loss_per_year_juta"]:.1f} Juta/Tahun')

print(f'\nD001A:')
print(f'  TT: {dashboard_data["D001A"]["tt"]} (Age: {dashboard_data["D001A"]["age"]} years)')
print(f'  Gap: {dashboard_data["D001A"]["gap_pct"]:.1f}% (DEFICIT)')
print(f'  Loss: Rp {dashboard_data["D001A"]["loss_per_year_juta"]:.1f} Juta/Tahun')

print(f'\nCombined:')
print(f'  Total Loss: Rp {dashboard_data["combined"]["total_loss_juta"]:.1f} Juta/Tahun')
print(f'  Total Loss: Rp {dashboard_data["combined"]["total_loss_million"]:.3f} Miliar/Tahun')

print('\n📁 Saved to: data/output/dashboard_data_f008a_d001a_CORRECTED.json')
