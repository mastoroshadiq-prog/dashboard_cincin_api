import os

FILE = r'data/output/dashboard_cincin_api_ISO_LINEAR_v9.html'

def main():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # ADD JAVASCRIPT FOR LIKELIHOOD ANALYSIS
    # We'll inject this BEFORE the closing </body> tag
    
    js_code = '''
    <script>
    // ========================================
    // LIKELIHOOD & TREND ANALYSIS LOGIC
    // ========================================
    
    let trendChart = null;
    
    function initializeLikelihoodAnalysis() {
        // Initialize mini trend chart
        const ctx = document.getElementById('trendMiniChart');
        if (!ctx) return;
        
        // Dummy historical data (6 months) - Replace with real data
        const trendData = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Attack Rate',
                data: [2.1, 2.5, 3.2, 3.8, 4.5, 5.2],
                borderColor: 'rgba(59, 130, 246, 1)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                pointRadius: 3,
                tension: 0.3,
                fill: true
            }]
        };
        
        trendChart = new Chart(ctx, {
            type: 'line',
            data: trendData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'AR: ' + context.parsed.y.toFixed(1) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 9 } }
                    },
                    y: {
                        display: true,
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 9 } }
                    }
                }
            }
        });
    }
    
    function updateLikelihoodMetrics(blockData) {
        if (!blockData) return;
        
        const ar = blockData.arNdre || 0;
        const sph = blockData.sph || 0;
        
        // 1. CALCULATE LIKELIHOOD SCORE
        // Formula: Base on AR + SPH factors
        // Higher AR + Higher SPH (>120) = Higher likelihood of critical state
        let likelihoodScore = 0;
        
        if (ar >= 5) {
            likelihoodScore = 75 + (ar - 5) * 5; // 5%+ AR = 75%+ likelihood
        } else if (ar >= 2) {
            likelihoodScore = 40 + (ar - 2) * 10; // 2-5% AR = 40-75%
        } else {
            likelihoodScore = ar * 20; // <2% AR = <40%
        }
        
        // SPH modifier (high density = higher spread risk)
        if (sph > 130) {
            likelihoodScore += 10;
        } else if (sph > 120) {
            likelihoodScore += 5;
        }
        
        likelihoodScore = Math.min(95, likelihoodScore); // Cap at 95%
        
        // Update UI
        document.getElementById('likelihoodScore').textContent = Math.round(likelihoodScore);
        document.getElementById('likelihoodBar').style.width = likelihoodScore + '%';
        
        // 2. CALCULATE TREND VELOCITY
        // Dummy calculation - in real app, compare current AR with 3-month-ago AR
        const trendVelocity = '+' + (ar / 3).toFixed(1) + '% /bulan';
        document.getElementById('trendVelocity').textContent = trendVelocity;
        
        // Update trend badge
        const badge = document.getElementById('trendBadge');
        if (ar > 4) {
            badge.textContent = '🚀 ACCELERATING';
            badge.className = 'px-3 py-1 rounded-full text-xs font-black bg-red-900/50 text-red-300';
        } else if (ar > 2) {
            badge.textContent = '⚠️ INCREASING';
            badge.className = 'px-3 py-1 rounded-full text-xs font-black bg-orange-900/50 text-orange-300';
        } else {
            badge.textContent = '✓ STABLE';
            badge.className = 'px-3 py-1 rounded-full text-xs font-black bg-emerald-900/50 text-emerald-300';
        }
        
        // 3. TIME TO CRITICAL (SPH < 100)
        // Simplified projection based on AR
        let monthsToCritical = 0;
        
        if (sph > 100) {
            const sphDeficit = sph - 100;
            const monthlyDecline = ar * 0.5; // Estimate: AR% translates to 0.5 SPH loss per month
            monthsToCritical = Math.ceil(sphDeficit / monthlyDecline);
        } else {
            monthsToCritical = 0; // Already critical
        }
        
        monthsToCritical = Math.max(1, Math.min(36, monthsToCritical)); // Cap between 1-36 months
        
        document.getElementById('timeTocrítica').textContent = monthsToCritical;
        
        // Timeline bar progress (inverse - closer to critical = more progress)
        const timelineProgress = Math.max(0, 100 - (monthsToCritical * 2.5));
        document.getElementById('timelineBar').style.width = timelineProgress + '%';
        
        // 4. UPDATE MINI TREND CHART (if needed)
        // In production, update with real historical data
        // For now, we just ensure chart is initialized
    }
    
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        initializeLikelihoodAnalysis();
        
        // Hook into existing block selection logic
        // When globalSelectorLeft changes, update likelihood metrics
        const selector = document.getElementById('globalSelectorLeft');
        if (selector) {
            selector.addEventListener('change', function() {
                const selectedBlock = this.value;
                if (selectedBlock && window.BLOCKS_DATA) {
                    const blockData = window.BLOCKS_DATA[selectedBlock];
                    updateLikelihoodMetrics(blockData);
                }
            });
        }
    });
    </script>
    '''
    
    # Find closing </body> tag
    body_close = content.rfind('</body>')
    
    if body_close == -1:
        print("Error: Could not find </body> tag")
        return
    
    # Inject JS before </body>
    content_new = content[:body_close] + js_code + '\n' + content[body_close:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content_new)
        
    print("✅ Added JavaScript logic for Likelihood Analysis")
    print("✅ Mini trend chart initialized")
    print("✅ Likelihood score calculation implemented")
    print("✅ Time-to-critical projection logic added")

if __name__ == "__main__":
    main()
