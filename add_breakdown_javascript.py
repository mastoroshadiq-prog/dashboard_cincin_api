"""
Add JavaScript to populate breakdown section with degradation model
"""

# Read demo
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    demo = f.read()

print("Adding breakdown population logic...")

# Find loadBlockData function and enhance it
old_func_end = '''            gapPctEl.className = gapPct > 20 ? 'text-red-400 text-3xl font-black' : 'text-emerald-400 text-3xl font-black';
            
            // Update Footer Stats'''

new_func_with_breakdown = '''            gapPctEl.className = gapPct > 20 ? 'text-red-400 text-3xl font-black' : 'text-emerald-400 text-3xl font-black';
            
            // Show breakdown section
            document.getElementById('blockBreakdownSection').classList.remove('hidden');
            
            // Populate 4 Metric Boxes
            const currentLoss = data.loss_value_juta || 0;
            const total3Year = (data.projected_loss_3yr || currentLoss * 3);
            const treatmentCost = data.mitigation_cost_juta || 50;
            const roi = treatmentCost > 0 ? Math.round(((total3Year - treatmentCost) / treatmentCost) * 100) : 0;
            
            document.getElementById('breakdownCurrentLoss').textContent = 'Rp ' + Math.round(currentLoss);
            document.getElementById('breakdown3YearTotal').textContent = 'Rp ' + Math.round(total3Year);
            document.getElementById('breakdownTreatment').textContent = 'Rp ' + Math.round(treatmentCost);
            document.getElementById('breakdownROI').textContent = roi;
            
            // Build degradation table (simple model: AR increases, yield decreases)
            const ar0 = data.attack_rate || 7.5;
            const gap0 = Math.abs(data.gap_pct || 21);
            const sph0 = data.sph || 108;
            const loss0 = currentLoss;
            
            // Year 1: AR +33%, gap +23%, SPH -10
            const ar1 = ar0 * 1.33;
            const gap1 = gap0 * 1.23;
            const sph1 = sph0 - 10;
            const loss1 = loss0 * 1.12;
            
            // Year 2: AR +59%, gap +56%, SPH -25
            const ar2 = ar0 * 1.59;
            const gap2 = gap0 * 1.56;
            const sph2 = sph0 - 25;
            const loss2 = loss0 * 1.42;
            
            // Year 3: AR +127%, gap +150%, SPH -45
            const ar3 = ar0 * 2.27;
            const gap3 = gap0 * 2.50;
            const sph3 = sph0 - 45;
            const loss3 = loss0 * 2.27;
            
            const tableBody = document.getElementById('degradationTableBody');
            tableBody.innerHTML = `
                <tr class="border-b border-white/10 hover:bg-white/5">
                    <td class="p-3 font-bold">Tingkat Infeksi</td>
                    <td class="p-3 text-center">${ar0.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">${ar1.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">${ar2.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">${ar3.toFixed(1)}%</td>
                    <td class="p-3 text-center text-orange-400">+${(ar3-ar0).toFixed(1)}%</td>
                </tr>
                <tr class="border-b border-white/10 hover:bg-white/5">
                    <td class="p-3 font-bold">Gap Hasil</td>
                    <td class="p-3 text-center">-${gap0.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">-${gap1.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">-${gap2.toFixed(1)}%</td>
                    <td class="p-3 text-center text-yellow-400">-${gap3.toFixed(1)}%</td>
                    <td class="p-3 text-center text-orange-400">-${(gap3-gap0).toFixed(1)}%</td>
                </tr>
                <tr class="border-b border-white/10 hover:bg-white/5">
                    <td class="p-3 font-bold">SPH (trees/ha)</td>
                    <td class="p-3 text-center">${Math.round(sph0)}</td>
                    <td class="p-3 text-center text-yellow-400">${Math.round(sph1)}</td>
                    <td class="p-3 text-center text-yellow-400">${Math.round(sph2)}</td>
                    <td class="p-3 text-center text-yellow-400">${Math.round(sph3)}</td>
                    <td class="p-3 text-center text-orange-400">-${Math.round(sph0-sph3)} trees</td>
                </tr>
                <tr class="hover:bg-white/5">
                    <td class="p-3 font-bold">Kerugian (Juta)</td>
                    <td class="p-3 text-center">Rp ${Math.round(loss0)}</td>
                    <td class="p-3 text-center text-yellow-400">Rp ${Math.round(loss1)}</td>
                    <td class="p-3 text-center text-yellow-400">Rp ${Math.round(loss2)}</td>
                    <td class="p-3 text-center text-yellow-400">Rp ${Math.round(loss3)}</td>
                    <td class="p-3 text-center text-orange-400">+Rp ${Math.round(loss3-loss0)}</td>
                </tr>
            `;
            
            // Populate treatment impact
            const prevented = total3Year * 0.70; // 70% effective
            const netBenefit = prevented - treatmentCost;
            document.getElementById('treatmentPrevented').textContent = 'Rp ' + Math.round(prevented) + ' Juta';
            document.getElementById('treatmentNetBenefit').textContent = 'Rp ' + Math.round(netBenefit) + ' Juta';
            
            //  Update Footer Stats'''

demo = demo.replace(old_func_end, new_func_with_breakdown)
print("✅ Breakdown population logic added to loadBlockData function")

# Save
with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(demo)

print(f"\n✅ Breakdown JavaScript added!")
print(f"   File size: {len(demo)} chars")
print("\nNOW: Click block → Breakdown appears with degradation model!")
