"""
Replace openPaparanRisikoModal with version that uses calculateDivisionMetrics()
"""

input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the function start and end
start_marker = "function openPaparanRisikoModal(divisionCode) {"
end_marker = "// Show modal"

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find function start")
    exit(1)

# Find end - look for the line after "// Render chart"
temp_idx = content.find("// Render chart", start_idx)
end_idx = content.find(end_marker, temp_idx)

if end_idx == -1:
    print("ERROR: Could not find end marker")
    exit(1)

# Extract before and after
before = content[:start_idx]
after = content[end_idx:]

# New function body
new_function = """function openPaparanRisikoModal(divisionCode) {
                console.log('[MODAL] Opening for division (raw):', divisionCode);
                
                // MAP: AME_II -> AME02, AME_IV -> AME04  
                const divisionMap = { 'AME_II': 'AME02', 'AME_IV': 'AME04', 'ALL': 'ALL' };
                const mappedCode = divisionMap[divisionCode] || divisionCode;
                console.log('[MODAL] Mapped to:', mappedCode);
                
                currentModalDivision = mappedCode;
                
                // USE EXISTING calculateDivisionMetrics() - IT WORKS!
                const metrics = calculateDivisionMetrics(mappedCode);
                
                if (!metrics) {
                    console.error('[MODAL] No metrics found for division:', mappedCode);
                    alert(`Tidak ada data untuk division: ${mappedCode}`);
                    return;
                }
                
                console.log('[MODAL] Division metrics:', metrics);
                console.log('[MODAL] Critical blocks count:', metrics.criticalBlocks);
                console.log('[MODAL] Total loss (Juta):', metrics.totalGanodermaLoss);
                
                // Get critical blocks array for chart
                const allBlocks = Object.values(BLOCKS_DATA);
                const divisionBlocks = allBlocks.filter(block => block.division === mappedCode);
                
                // Filter critical blocks (Stadium 3+) using SAME logic as getGanodermaStadium
                const criticalBlocksArray = divisionBlocks.filter(block => {
                    const attackRate = parseFloat(block.attack_rate) || 0;
                    const gapPct = parseFloat(block.gap_pct) || 0;
                    return attackRate >= 15 || gapPct >= 20;  // Stadium 3+
                });
                
                console.log('[MODAL] Critical blocks array:', criticalBlocksArray.length);
                
                // Update modal content using metrics
                document.getElementById('modalDivisionSubtitle').textContent =
                    `${mappedCode} Division - ${metrics.criticalBlocks} blok kritis (Stadium 3+)`;
                
                document.getElementById('modalTotalLoss').textContent =
                    `Rp ${(metrics.totalGanodermaLoss / 1000).toFixed(1)} M`;
                
                document.getElementById('modalCriticalCount').textContent =
                    `${metrics.criticalBlocks} Blok`;
                
                // Calculate critical area
                const criticalArea = metrics.totalArea * (metrics.criticalBlocks / metrics.totalBlocks);
                document.getElementById('modalRiskArea').textContent =
                    `${criticalArea.toFixed(1)} Ha`;
                
                // Render chart with critical blocks array
                renderModalChart(criticalBlocksArray, currentModalSort);

                """

new_content = before + new_function + after

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Successfully replaced openPaparanRisikoModal function")
print(f"   Now uses calculateDivisionMetrics() from working code")
