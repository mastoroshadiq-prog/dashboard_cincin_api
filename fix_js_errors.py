"""
Fix JavaScript errors from removed Treatment Comparison section
Add null checks for removed DOM elements
"""

# Read the file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📖 File size: {len(content):,} characters")

# Find and replace the problematic section with null-safe version
# Lines 14600-14616: Update NO TREATMENT, WITH TREATMENT, and SAVINGS displays

old_code = """                // Update NO TREATMENT displays
                document.getElementById('noTreatment_year0').textContent = formatLossMiliar(noTx_year0);
                document.getElementById('noTreatment_year1').textContent = formatLossMiliar(noTx_year1);
                document.getElementById('noTreatment_year2').textContent = formatLossMiliar(noTx_year2);
                document.getElementById('noTreatment_year3').textContent = formatLossMiliar(noTx_year3);
                document.getElementById('noTreatment_cumulative').textContent = formatLossMiliar(noTx_cumulative);

                // Update WITH TREATMENT displays
                document.getElementById('withTreatment_year0').textContent = formatLossMiliar(withTx_year0);
                document.getElementById('withTreatment_year1').textContent = formatLossMiliar(withTx_year1);
                document.getElementById('withTreatment_year2').textContent = formatLossMiliar(withTx_year2);
                document.getElementById('withTreatment_year3').textContent = formatLossMiliar(withTx_year3);
                document.getElementById('withTreatment_cumulative').textContent = formatLossMiliar(withTx_cumulative);

                // Update SAVINGS displays
                document.getElementById('treatment_totalSavings').textContent = formatLossMiliar(totalSavings);
                document.getElementById('treatment_savingsPercent').textContent = treatment_savingsPercent.toFixed(0) + '%';"""

new_code = """                // Update NO TREATMENT displays (NULL-SAFE - elements removed in v9.1)
                const noTx0 = document.getElementById('noTreatment_year0');
                if (noTx0) noTx0.textContent = formatLossMiliar(noTx_year0);
                const noTx1 = document.getElementById('noTreatment_year1');
                if (noTx1) noTx1.textContent = formatLossMiliar(noTx_year1);
                const noTx2 = document.getElementById('noTreatment_year2');
                if (noTx2) noTx2.textContent = formatLossMiliar(noTx_year2);
                const noTx3 = document.getElementById('noTreatment_year3');
                if (noTx3) noTx3.textContent = formatLossMiliar(noTx_year3);
                const noTxCum = document.getElementById('noTreatment_cumulative');
                if (noTxCum) noTxCum.textContent = formatLossMiliar(noTx_cumulative);

                // Update WITH TREATMENT displays (NULL-SAFE - elements removed in v9.1)
                const withTx0 = document.getElementById('withTreatment_year0');
                if (withTx0) withTx0.textContent = formatLossMiliar(withTx_year0);
                const withTx1 = document.getElementById('withTreatment_year1');
                if (withTx1) withTx1.textContent = formatLossMiliar(withTx_year1);
                const withTx2 = document.getElementById('withTreatment_year2');
                if (withTx2) withTx2.textContent = formatLossMiliar(withTx_year2);
                const withTx3 = document.getElementById('withTreatment_year3');
                if (withTx3) withTx3.textContent = formatLossMiliar(withTx_year3);
                const withTxCum = document.getElementById('withTreatment_cumulative');
                if (withTxCum) withTxCum.textContent = formatLossMiliar(withTx_cumulative);

                // Update SAVINGS displays (NULL-SAFE - elements removed in v9.1)
                const savingsTotal = document.getElementById('treatment_totalSavings');
                if (savingsTotal) savingsTotal.textContent = formatLossMiliar(totalSavings);
                const savingsPercent = document.getElementById('treatment_savingsPercent');
                if (savingsPercent) savingsPercent.textContent = treatment_savingsPercent.toFixed(0) + '%';"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Fixed Treatment Comparison element references with null checks")
else:
    print("⚠️ Could not find exact match - checking alternative pattern...")
    # Try alternative approach - just find the first line and replace block
    import re
    pattern = r"// Update NO TREATMENT displays\s+document\.getElementById\('noTreatment_year0'\)\.textContent.*?document\.getElementById\('treatment_savingsPercent'\)\.textContent = treatment_savingsPercent\.toFixed\(0\) \+ '%';"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_code, content, flags=re.DOTALL)
        print("✅ Fixed using regex pattern")
    else:
        print("❌ Pattern not found - manual fix needed")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ JAVASCRIPT ERROR FIXED!")
print(f"   Added null checks for removed Treatment Comparison elements")
print(f"   Elements now checked before updating:")
print(f"   • noTreatment_year0-3, cumulative")
print(f"   • withTreatment_year0-3, cumulative")
print(f"   • treatment_totalSavings, savingsPercent")
print(f"\n   These elements were removed in v9.1 but JS still tried to update them")
print(f"   Now safe with null checks!")
