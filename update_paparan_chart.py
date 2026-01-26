"""
Script untuk update PAPARAN RISIKO chart menjadi double bar chart
menampilkan Attack Rate (%) dan Loss (Miliar Rp) per block
"""

def update_paparan_chart_to_double_bar():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Updating PAPARAN RISIKO chart to double bar...")
    
    # Find the chart creation code dalam renderPaparanRisk
    # Look for "new Chart" for riskBarChart
    search_pattern = "new Chart(document.getElementById('riskBarChart')"
    
    idx = content.find(search_pattern)
    if idx == -1:
        print("[ERROR] Chart initialization not found")
        return
    
    print(f"[FOUND] Chart initialization at position {idx}")
    
    # The chart config should be right after this
    # Find the full chart config (from "new Chart" to the closing });
    
    # Strategy: Replace entire chart configuration with dual-axis bar chart
    # OLD pattern to find:
    old_chart_pattern = '''            riskChartInstance = new Chart(document.getElementById('riskBarChart'), {
                type: 'bar',
                data: {'''
    
    if old_chart_pattern not in content:
        print("[WARNING] Exact pattern not found, searching for alternative...")
        
        # Try to find by looking for riskChartInstance assignment
        alt_pattern = "riskChartInstance = new Chart"
        idx = content.find(alt_pattern)
        if idx != -1:
            print(f"[FOUND] Alternative pattern at {idx}")
            # Get surrounding context
            start = max(0, idx - 100)
            end = min(len(content), idx + 2000)
            print("Context:")
            print(content[start:end][:500])
    
    # For now, let me create a Python script that will:
    # 1. Find renderPaparanRisk function
    # 2. Locate the chart creation
    # 3. Replace with dual-axis configuration
    
    # Since the exact structure varies, let's use a more robust approach:
    # Find and replace the entire chart datasets configuration
    
    # Look for the chart config more broadly
    chart_start = content.find("riskChartInstance = new Chart")
    if chart_start == -1:
        print("[ERROR] riskChartInstance not found")
        return
    
    # Find the end of this chart config (look for the closing }) of new Chart()
    # This is tricky, need to count braces
    config_start = chart_start
    brace_count = 0
    in_chart_config = False
    config_end = config_start
    
    for i in range(config_start, min(len(content), config_start + 5000)):
        char = content[i]
        if char == '{':
            brace_count += 1
            in_chart_config = True
        elif char == '}':
            brace_count -= 1
            if in_chart_config and brace_count == 0:
                config_end = i + 1
                # Look for the closing );
                if content[i+1:i+3] == ');':
                    config_end = i + 3
                break
    
    if config_end == config_start:
        print("[ERROR] Could not find chart config end")
        return
    
    old_chart_config = content[config_start:config_end]
    print(f"[FOUND] Chart config: {len(old_chart_config)} chars")
    print(f"First 200 chars: {old_chart_config[:200]}")
    
    # Create new dual-axis bar chart configuration
    new_chart_config = '''riskChartInstance = new Chart(document.getElementById('riskBarChart'), {
                type: 'bar',
                data: {
                    labels: blockLabels,
                    datasets: [
                        {
                            label: 'Attack Rate (%)',
                            data: attackRates,
                            backgroundColor: 'rgba(239, 68, 68, 0.8)',
                            borderColor: 'rgb(239, 68, 68)',
                            borderWidth: 2,
                            yAxisID: 'y',
                            barThickness: 'flex',
                            maxBarThickness: 40
                        },
                        {
                            label: 'Loss (Miliar Rp)',
                            data: lossValues,
                            backgroundColor: 'rgba(251, 191, 36, 0.8)',
                            borderColor: 'rgb(251, 191, 36)',
                            borderWidth: 2,
                            yAxisID: 'y1',
                            barThickness: 'flex',
                            maxBarThickness: 40
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#fff',
                                font: { size: 11, weight: 'bold' },
                                padding: 15,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.9)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: 'rgba(239, 68, 68, 0.5)',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: true,
                            callbacks: {
                                label: function(context) {
                                    const label = context.dataset.label || '';
                                    const value = context.parsed.y;
                                    if (label.includes('Attack Rate')) {
                                        return `${label}: ${value.toFixed(1)}%`;
                                    } else {
                                        return `${label}: Rp ${value.toFixed(2)} M`;
                                    }
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { 
                                color: '#fff',
                                font: { size: 9, weight: 'bold' },
                                maxRotation: 45,
                                minRotation: 0
                            },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        y: {
                            type: 'linear',
                            position: 'left',
                            beginAtZero: true,
                            ticks: { 
                                color: 'rgb(239, 68, 68)',
                                font: { size: 10, weight: 'bold' },
                                callback: function(value) {
                                    return value.toFixed(0) + '%';
                                }
                            },
                            grid: { color: 'rgba(239, 68, 68, 0.2)' },
                            title: {
                                display: true,
                                text: 'Attack Rate (%)',
                                color: 'rgb(239, 68, 68)',
                                font: { size: 12, weight: 'bold' }
                            }
                        },
                        y1: {
                            type: 'linear',
                            position: 'right',
                            beginAtZero: true,
                            ticks: { 
                                color: 'rgb(251, 191, 36)',
                                font: { size: 10, weight: 'bold' },
                                callback: function(value) {
                                    return 'Rp ' + value.toFixed(1) + ' M';
                                }
                            },
                            grid: { drawOnChartArea: false },
                            title: {
                                display: true,
                                text: 'Loss (Miliar Rp)',
                                color: 'rgb(251, 191, 36)',
                                font: { size: 12, weight: 'bold' }
                            }
                        }
                    }
                }
            })'''
    
    # Replace
    content = content.replace(old_chart_config, new_chart_config)
    print("[SUCCESS] Replaced chart configuration with dual-axis bar chart")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ PAPARAN RISIKO Chart Updated to Double Bar:")
    print("  • Left Y-axis: Attack Rate (%) - Red bars")
    print("  • Right Y-axis: Loss (Miliar Rp) - Yellow/Orange bars")
    print("  • Interactive tooltips")
    print("  • Legend at top")
    print("  • Responsive design")

if __name__ == '__main__':
    update_paparan_chart_to_double_bar()
