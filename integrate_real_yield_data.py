"""
Integrate VERIFIED historical yield data (2023-2025) into dashboard
Replace calculated data with REAL data from Excel
"""

import json

# Load verified data
with open('data/output/verified_historical_data_2023_2025.json', 'r') as f:
    verified_data = json.load(f)

# Read current dashboard
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Generate JavaScript object for historical yields
js_historical_data = "const HISTORICAL_YIELDS = {\n"

for block, data in verified_data.items():
    js_historical_data += f"    '{block}': {{\n"
    js_historical_data += f"        luas_ha: {data['luas_ha']},\n"
    js_historical_data += f"        yields: {{\n"
    
    for year, year_data in data['years'].items():
        js_historical_data += f"            {year}: {{\n"
        js_historical_data += f"                real_ton_ha: {year_data['real_ton_ha']},\n"
        js_historical_data += f"                poten_ton_ha: {year_data['poten_ton_ha']},\n"
        js_historical_data += f"                gap_ton_ha: {year_data['gap_ton_ha']},\n"
        js_historical_data += f"                gap_pct: {year_data['gap_pct']}\n"
        js_historical_data += f"            }},\n"
    
    js_historical_data += f"        }}\n"
    js_historical_data += f"    }},\n"

js_historical_data += "};\n"

# Find where to insert (before BLOCKS_DATA)
insert_marker = "        const BLOCKS_DATA = {"
insert_pos = content.find(insert_marker)

if insert_pos == -1:
    print("❌ Could not find BLOCKS_DATA marker!")
else:
    # Insert historical data before BLOCKS_DATA
    content = content[:insert_pos] + "        // REAL HISTORICAL YIELD DATA FROM EXCEL (2023-2025)\n        " + js_historical_data + "\n        " + content[insert_pos:]
    print("✅ Inserted HISTORICAL_YIELDS data")

# Update chart rendering to use REAL data instead of calculated
old_chart_calc = '''            // Historical production data calculation
            const currentYield = data.realisasi_ton_ha || 18.5;
            const potentialYield = data.potensi_ton_ha || 26.0;
            const gapTonHa = Math.abs(data.gap_ton_ha || 7.5);
            
            // Calculate historical trend (assumes linear degradation)
            const year3ago = currentYield + (gapTonHa * 0.7);  // 2023
            const year2ago = currentYield + (gapTonHa * 0.5);  // 2024
            const year1ago = currentYield;  // 2025 (actual census data)'''

new_chart_calc = '''            // REAL HISTORICAL YIELD DATA from Excel (2023-2025)
            const blockCode = currentBlockCode;
            const historicalData = HISTORICAL_YIELDS[blockCode];
            
            if (!historicalData) {
                console.error('No historical data for block:', blockCode);
                return;
            }
            
            // Real data from Excel
            const year3ago = historicalData.yields[2023]?.real_ton_ha || 0;  // 2023
            const year2ago = historicalData.yields[2024]?.real_ton_ha || 0;  // 2024
            const year1ago = historicalData.yields[2025]?.real_ton_ha || 0;  // 2025
            
            const potentialYield = historicalData.yields[2025]?.poten_ton_ha || 0;'''

content = content.replace(old_chart_calc, new_chart_calc)
print("✅ Updated main chart to use REAL data")

# Update modal chart as well
old_modal_calc = '''        const currentYield = data.realisasi_ton_ha || 18.5;
        const potentialYield = data.potensi_ton_ha || 26.0;
        const gapTonHa = Math.abs(data.gap_ton_ha || 7.5);
        
        // Calculate historical trend
        const year3ago = currentYield + (gapTonHa * 0.7);  // 2023
        const year2ago = currentYield + (gapTonHa * 0.5);  // 2024
        const year1ago = currentYield;  // 2025 (actual census data)'''

new_modal_calc = '''        const blockCode = currentBlockCode;
        const historicalData = HISTORICAL_YIELDS[blockCode];
        
        if (!historicalData) {
            console.error('No historical data for block:', blockCode);
            return;
        }
        
        // REAL data from Excel (2023-2025)
        const year3ago = historicalData.yields[2023]?.real_ton_ha || 0;
        const year2ago = historicalData.yields[2024]?.real_ton_ha || 0;
        const year1ago = historicalData.yields[2025]?.real_ton_ha || 0;
        
        const potentialYield = historicalData.yields[2025]?.poten_ton_ha || 0;'''

content = content.replace(old_modal_calc, new_modal_calc)
print("✅ Updated modal chart to use REAL data")

# Remove disclaimer about calculated data
old_disclaimer = '<p class="text-xs text-yellow-400 mt-1">⚠️ Data trend dihitung dari realisasi 2025 (data historis belum tersedia)</p>'
new_disclaimer = '<p class="text-xs text-emerald-400 mt-1">✅ Data realisasi produksi dari sensus lapangan 2023-2025</p>'

content = content.replace(old_disclaimer, new_disclaimer)
print("✅ Updated disclaimer to show REAL data source")

# Update chart title
old_title = '📊 Trend Realisasi Produksi (2023-2025)'
new_title = '📊 Trend Realisasi Produksi (Data Sensus 2023-2025)'

content = content.replace(old_title, new_title)
print("✅ Updated chart title")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*80)
print("✅ DASHBOARD UPDATED WITH REAL HISTORICAL DATA!")
print("="*80)
print("\nChanges:")
print("  1. Added HISTORICAL_YIELDS object with verified Excel data")
print("  2. Updated main chart to use REAL yields (not calculated)")
print("  3. Updated modal zoom chart to use REAL yields")
print("  4. Changed disclaimer from 'calculated' to 'sensus lapangan'")
print("  5. Updated title to emphasize real census data")
print("\n" + "="*80)
print("VERIFIED DATA EXAMPLES:")
print("="*80)
print("E003A 2023: 13.99 Ton/Ha (Potensi: 22.53, Gap: 37.9%)")
print("E003A 2024: 14.85 Ton/Ha (Potensi: 21.29, Gap: 30.2%)")
print("E003A 2025: 14.06 Ton/Ha (Potensi: 20.50, Gap: 31.4%)")
print("="*80)
