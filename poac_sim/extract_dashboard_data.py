import pandas as pd
import json

print('='*80)
print('📊 EKSTRAKSI DATA LENGKAP UNTUK DASHBOARD')
print('='*80)

# Load data
df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx', header=3)
df_ranked = pd.read_csv('data/output/all_blocks_ranked_by_severity.csv')

# Get F008A and D001A data
f008a = df[df['Unnamed: 0'] == 'F008A'].iloc[0]
d001a = df[df['Unnamed: 0'] == 'D001A'].iloc[0]

f008a_ndre = df_ranked[df_ranked['blok'] == 'F08'].iloc[0]
d001a_ndre = df_ranked[df_ranked['blok'] == 'D01'].iloc[0]

# Extract all data
dashboard_data = {
    'F008A': {
        # Basic Info
        'code_full': 'F008A',
        'code_short': 'F 08',
        'blok_display': 'F008A',
        'tt': str(f008a['TT']),
        'age': 2026 - int(f008a['TT']),
        'luas': float(f008a['HA STATEMENT']),
        
        # Cincin Api Data
        'total_trees': int(f008a_ndre['total_trees']),
        'merah': int(f008a_ndre['merah']),
        'oranye': int(f008a_ndre['oranye']),
        'kuning': int(f008a_ndre['kuning']),
        'hijau': int(f008a_ndre['hijau']),
        'spread_ratio': float(f008a_ndre['spread_ratio']),
        'infection_pct': float(f008a_ndre['infection_pct']),
        'severity_score': float(f008a_ndre['severity_score']),
        
        # Production Data
        'real_ton': float(f008a.iloc[170]),
        'potensi_ton': float(f008a.iloc[173]),
        'real_ton_ha': float(f008a.iloc[170] / f008a['HA STATEMENT']),
        'potensi_ton_ha': float(f008a.iloc[173] / f008a['HA STATEMENT']),
        'gap_ton_ha': float((f008a.iloc[170] - f008a.iloc[173]) / f008a['HA STATEMENT']),
        'gap_pct': float(((f008a.iloc[170] - f008a.iloc[173]) / f008a.iloc[173]) * 100),
        
        # PKK Data
        'pkk_stadium_12': int(f008a.iloc[55]),
        'pkk_stadium_34': int(f008a.iloc[56]),
        'pkk_total': int(f008a.iloc[57]),
        'pkk_pct': float((f008a.iloc[57] / f008a_ndre['total_trees']) * 100),
        
        # Financial (assuming Rp 1.5 juta/ton)
        'loss_per_year_million': float(abs((f008a.iloc[170] - f008a.iloc[173]) / f008a['HA STATEMENT']) * f008a['HA STATEMENT'] * 1.5 / 1000) if (f008a.iloc[170] - f008a.iloc[173]) < 0 else 0,
        
        # SPH
        'sph': int(f008a_ndre['total_trees'] / f008a['HA STATEMENT'])
    },
    'D001A': {
        # Basic Info
        'code_full': 'D001A',
        'code_short': 'D 01',
        'blok_display': 'D001A',
        'tt': str(d001a['TT']),
        'age': 2026 - int(d001a['TT']),
        'luas': float(d001a['HA STATEMENT']),
        
        # Cincin Api Data
        'total_trees': int(d001a_ndre['total_trees']),
        'merah': int(d001a_ndre['merah']),
        'oranye': int(d001a_ndre['oranye']),
        'kuning': int(d001a_ndre['kuning']),
        'hijau': int(d001a_ndre['hijau']),
        'spread_ratio': float(d001a_ndre['spread_ratio']),
        'infection_pct': float(d001a_ndre['infection_pct']),
        'severity_score': float(d001a_ndre['severity_score']),
        
        # Production Data
        'real_ton': float(d001a.iloc[170]),
        'potensi_ton': float(d001a.iloc[173]),
        'real_ton_ha': float(d001a.iloc[170] / d001a['HA STATEMENT']),
        'potensi_ton_ha': float(d001a.iloc[173] / d001a['HA STATEMENT']),
        'gap_ton_ha': float((d001a.iloc[170] - d001a.iloc[173]) / d001a['HA STATEMENT']),
        'gap_pct': float(((d001a.iloc[170] - d001a.iloc[173]) / d001a.iloc[173]) * 100),
        
        # PKK Data
        'pkk_stadium_12': int(d001a.iloc[55]),
        'pkk_stadium_34': int(d001a.iloc[56]),
        'pkk_total': int(d001a.iloc[57]),
        'pkk_pct': float((d001a.iloc[57] / d001a_ndre['total_trees']) * 100),
        
        # Financial
        'loss_per_year_million': float(abs((d001a.iloc[170] - d001a.iloc[173]) / d001a['HA STATEMENT']) * d001a['HA STATEMENT'] * 1.5 / 1000),
        
        # SPH
        'sph': int(d001a_ndre['total_trees'] / d001a['HA STATEMENT'])
    }
}

# Calculate combined stats
total_luas = dashboard_data['F008A']['luas'] + dashboard_data['D001A']['luas']
total_loss = dashboard_data['F008A']['loss_per_year_million'] + dashboard_data['D001A']['loss_per_year_million']

dashboard_data['combined'] = {
    'total_luas': total_luas,
    'total_loss_million': total_loss,
    'total_trees': dashboard_data['F008A']['total_trees'] + dashboard_data['D001A']['total_trees'],
    'total_infected': (dashboard_data['F008A']['merah'] + dashboard_data['F008A']['oranye'] + 
                      dashboard_data['D001A']['merah'] + dashboard_data['D001A']['oranye']),
    'avg_infection_pct': (dashboard_data['F008A']['infection_pct'] + dashboard_data['D001A']['infection_pct']) / 2
}

# Save to JSON
with open('data/output/dashboard_data_f008a_d001a.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print('\n✅ Data extracted successfully!')
print('\n📊 SUMMARY:')
print(f"\nF008A:")
print(f"  Luas: {dashboard_data['F008A']['luas']} Ha")
print(f"  Spread Ratio: {dashboard_data['F008A']['spread_ratio']:.0f}x")
print(f"  Infection: {dashboard_data['F008A']['infection_pct']:.1f}%")
print(f"  Real: {dashboard_data['F008A']['real_ton_ha']:.2f} Ton/Ha")
print(f"  Potensi: {dashboard_data['F008A']['potensi_ton_ha']:.2f} Ton/Ha")
print(f"  Gap: {dashboard_data['F008A']['gap_pct']:.1f}%")

print(f"\nD001A:")
print(f"  Luas: {dashboard_data['D001A']['luas']} Ha")
print(f"  Spread Ratio: {dashboard_data['D001A']['spread_ratio']:.0f}x")
print(f"  Infection: {dashboard_data['D001A']['infection_pct']:.1f}%")
print(f"  Real: {dashboard_data['D001A']['real_ton_ha']:.2f} Ton/Ha")
print(f"  Potensi: {dashboard_data['D001A']['potensi_ton_ha']:.2f} Ton/Ha")
print(f"  Gap: {dashboard_data['D001A']['gap_pct']:.1f}%")

print(f"\nCombined:")
print(f"  Total Luas: {total_luas} Ha")
print(f"  Total Loss: Rp {total_loss:.3f} Miliar/Tahun")

print('\n📁 Saved to: data/output/dashboard_data_f008a_d001a.json')
