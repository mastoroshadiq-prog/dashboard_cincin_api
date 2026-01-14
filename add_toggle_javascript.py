"""
Add JavaScript for view mode toggle and aggregate calculations
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add new functions before renderModalCharts
new_functions = '''
        let viewMode = 'per-blok'; // 'per-blok' or 'total'
        
        function populateBlockSelector() {
            const selector = document.getElementById('blockSelector');
            selector.innerHTML = '';
            Object.keys(BLOCKS_DATA).forEach(code => {
                const option = document.createElement('option');
                option.value = code;
                option.textContent = code;
                selector.appendChild(option);
            });
            selector.value = currentBlockCode || Object.keys(BLOCKS_DATA)[0];
        }
        
        function switchViewMode(mode) {
            viewMode = mode;
            
            // Update button states
            document.getElementById('viewPerBlok').className = mode === 'per-blok'
                ? 'px-4 py-2 rounded-lg text-sm font-bold bg-indigo-600 text-white border-2 border-indigo-400 transition-all'
                : 'px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600 transition-all';
            document.getElementById('viewTotal').className = mode === 'total'
                ? 'px-4 py-2 rounded-lg text-sm font-bold bg-indigo-600 text-white border-2 border-indigo-400 transition-all'
                : 'px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-slate-300 border-2 border-slate-600 transition-all';
            
            // Enable/disable dropdown
            const selector = document.getElementById('blockSelector');
            selector.disabled = (mode === 'total');
            selector.className = mode === 'total'
                ? 'px-4 py-2 rounded-lg text-sm font-bold bg-slate-600 text-slate-400 border-2 border-slate-600 cursor-not-allowed'
                : 'px-4 py-2 rounded-lg text-sm font-bold bg-slate-700 text-white border-2 border-slate-600 hover:border-indigo-400 transition-all';
            
            // Update display
            if (mode === 'total') {
                document.getElementById('modalBlockCode').textContent = 'All 8 Critical Blocks (Aggregate)';
                renderTotalAnalysis();
            } else {
                const code = selector.value;
                document.getElementById('modalBlockCode').textContent = code;
                modalData = BLOCKS_DATA[code];
                renderComparisonChart(document.querySelector('[id^="toggle"].bg-indigo-600').id.replace('toggle', '').toLowerCase());
            }
        }
        
        function switchBlock(code) {
            if (viewMode !== 'per-blok') return;
            currentBlockCode = code;
            document.getElementById('modalBlockCode').textContent = code;
            modalData = BLOCKS_DATA[code];
            const currentMetric = document.querySelector('[id^="toggle"].bg-indigo-600').id.replace('toggle', '').toLowerCase();
            renderComparisonChart(currentMetric);
            
            // Update metrics
            const data = BLOCKS_DATA[code];
            const total3Year = data.projected_loss_3yr || 0;
            const treatmentCost = data.mitigation_cost_juta || 50;
            const savings = total3Year * 0.70;
            const netBenefit = savings - treatmentCost;
            
            document.getElementById('modalNoTreatmentLoss').textContent = 'Rp ' + Math.round(total3Year) + ' Jt';
            document.getElementById('modalTreatmentCost').textContent = 'Rp ' + Math.round(treatmentCost) + ' Jt';
            document.getElementById('modalSavings').textContent = 'Rp ' + Math.round(savings) + ' Jt';
            document.getElementById('modalNetBenefit').textContent = 'Rp ' + Math.round(netBenefit) + ' Jt';
        }
        
        function renderTotalAnalysis() {
            // Calculate aggregate metrics
            let totalLoss3yr = 0, totalTreatmentCost = 0;
            let avgAR = 0, avgGap = 0, avgSPH = 0, avgLoss = 0;
            const count = Object.keys(BLOCKS_DATA).length;
            
            Object.values(BLOCKS_DATA).forEach(data => {
                totalLoss3yr += (data.projected_loss_3yr || 0);
                totalTreatmentCost += (data.mitigation_cost_juta || 50);
                avgAR += (data.attack_rate || 0);
                avgGap += Math.abs(data.gap_pct || 0);
                avgSPH += (data.sph || 0);
                avgLoss += (data.loss_value_juta || 0);
            });
            
            avgAR /= count;
            avgGap /= count;
            avgSPH /= count;
            avgLoss /= count;
            
            const totalSavings = totalLoss3yr * 0.70;
            const totalNetBenefit = totalSavings - totalTreatmentCost;
            
            // Update metrics
            document.getElementById('modalNoTreatmentLoss').textContent = 'Rp ' + Math.round(totalLoss3yr) + ' Jt';
            document.getElementById('modalTreatmentCost').textContent = 'Rp ' + Math.round(totalTreatmentCost) + ' Jt';
            document.getElementById('modalSavings').textContent = 'Rp ' + Math.round(totalSavings) + ' Jt';
            document.getElementById('modalNetBenefit').textContent = 'Rp ' + Math.round(totalNetBenefit) + ' Jt';
            
            // Create aggregate data object
            modalData = {
                attack_rate: avgAR,
                gap_pct: -avgGap,
                sph: avgSPH,
                loss_value_juta: avgLoss
            };
            
            const currentMetric = document.querySelector('[id^="toggle"].bg-indigo-600').id.replace('toggle', '').toLowerCase();
            renderComparisonChart(currentMetric);
        }

        function renderModalCharts(data) {'''

# Insert before existing renderModalCharts
content = content.replace('        function renderModalCharts(data) {', new_functions)

# Update openAnalysisModal to populate selector
old_open = '''        function openAnalysisModal() {
            if (!currentBlockCode || !BLOCKS_DATA[currentBlockCode]) return;
            
            const data = BLOCKS_DATA[currentBlockCode];
            document.getElementById('analysisModal').classList.remove('hidden');
            document.getElementById('modalBlockCode').textContent = currentBlockCode;'''

new_open = '''        function openAnalysisModal() {
            if (!currentBlockCode || !BLOCKS_DATA[currentBlockCode]) return;
            
            const data = BLOCKS_DATA[currentBlockCode];
            document.getElementById('analysisModal').classList.remove('hidden');
            
            // Populate & setup
            populateBlockSelector();
            viewMode = 'per-blok';
            switchViewMode('per-blok');
            document.getElementById('modalBlockCode').textContent = currentBlockCode;'''

content = content.replace(old_open, new_open)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added switchViewMode(mode)")
print("✅ Added switchBlock(code) for dropdown")
print("✅ Added renderTotalAnalysis() for aggregate view")
print("✅ Added populateBlockSelector()")
print("✅ Dropdown enabled/disabled based on mode")
print("✅ Total mode shows average of all 8 blocks")
