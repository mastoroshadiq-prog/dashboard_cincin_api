"""
Script untuk:
1. Perbesar angka-angka di 3-year comparison
2. Buat popup modal untuk PAPARAN RISIKO yang triggered dari CRITICAL BLOCKS
"""

def enhance_ui_and_add_modal():
    input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Enhancing UI...")
    
    # 1. PERBESAR ANGKA di 3-year tables
    # Find year values in NO TREATMENT table
    old_year_size = 'class="text-sm font-black text-red-400"'
    new_year_size = 'class="text-xl font-black text-red-400"'  # sm -> xl
    
    content = content.replace(old_year_size, new_year_size)
    print("[SUCCESS] Increased NO TREATMENT year numbers from text-sm to text-xl")
    
    # Find year values in WITH TREATMENT table
    old_year_size_green = 'class="text-sm font-black text-emerald-400"'
    new_year_size_green = 'class="text-xl font-black text-emerald-400"'
    
    content = content.replace(old_year_size_green, new_year_size_green)
    print("[SUCCESS] Increased WITH TREATMENT year numbers from text-sm to text-xl")
    
    # Total 3-year loss is already text-3xl, but we can make it even bigger
    old_total_size = 'class="text-3xl font-black text-red-400"'
    new_total_size = 'class="text-4xl font-black text-red-400"'
    
    content = content.replace(old_total_size, new_total_size)
    print("[SUCCESS] Increased total loss from text-3xl to text-4xl")
    
    old_total_size_green = 'class="text-3xl font-black text-emerald-400"'
    new_total_size_green = 'class="text-4xl font-black text-emerald-400"'
    
    content = content.replace(old_total_size_green, new_total_size_green)
    print("[SUCCESS] Increased total WITH TREATMENT from text-3xl to text-4xl")
    
    # 2. ADD MODAL HTML (before closing </body>)
    modal_html = '''
    <!-- PAPARAN RISIKO MODAL -->
    <div id="paparanRisikoModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
        <div class="bg-gradient-to-br from-slate-900 via-rose-950 to-slate-900 rounded-3xl border-2 border-rose-500/50 max-w-6xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
            <!-- Modal Header -->
            <div class="sticky top-0 bg-gradient-to-r from-rose-900/90 to-slate-900/90 backdrop-blur-md p-6 border-b border-rose-500/30 flex justify-between items-center">
                <div>
                    <h2 class="text-3xl font-black text-white flex items-center gap-3">
                        🚨 PAPARAN RISIKO KRITIS
                    </h2>
                    <p class="text-rose-300/80 text-sm mt-1" id="modalDivisionSubtitle">Detail analisis blok berisiko tinggi</p>
                </div>
                <button onclick="closePaparanRisikoModal()" class="text-white/80 hover:text-white hover:bg-white/10 rounded-full p-2 transition-all">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <!-- Modal Content -->
            <div class="p-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-3 gap-4 mb-6">
                    <div class="bg-black/30 rounded-xl border border-rose-500/30 p-4">
                        <div class="text-xs text-rose-300/80 font-bold uppercase mb-2">Total Potensi Kerugian</div>
                        <div class="text-4xl font-black text-rose-400" id="modalTotalLoss">--</div>
                    </div>
                    <div class="bg-black/30 rounded-xl border border-rose-500/30 p-4">
                        <div class="text-xs text-rose-300/80 font-bold uppercase mb-2">Blok Kritis</div>
                        <div class="text-4xl font-black text-white" id="modalCriticalCount">--</div>
                    </div>
                    <div class="bg-black/30 rounded-xl border border-rose-500/30 p-4">
                        <div class="text-xs text-rose-300/80 font-bold uppercase mb-2">Area Berisiko</div>
                        <div class="text-4xl font-black text-white" id="modalRiskArea">--</div>
                    </div>
                </div>
                
                <!-- Chart Container -->
                <div class="bg-black/20 rounded-xl border border-rose-500/20 p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-bold text-white">Distribusi Risiko per Blok</h3>
                        <div class="flex gap-2">
                            <button onclick="sortModalChart('ar')" id="modalSortByAR" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400">
                                AR %
                            </button>
                            <button onclick="sortModalChart('loss')" id="modalSortByLoss" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30">
                                Loss (Rp)
                            </button>
                        </div>
                    </div>
                    <div style="height: 500px;">
                        <canvas id="modalRiskChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # Insert modal before </body>
    if '</body>' in content:
        content = content.replace('</body>', modal_html + '\n</body>')
        print("[SUCCESS] Added PAPARAN RISIKO modal HTML")
    
    # 3. ADD MODAL JAVASCRIPT (before closing </script>)
    modal_js = '''
        // ========================================
        // PAPARAN RISIKO MODAL FUNCTIONS
        // ========================================
        
        let modalRiskChart = null;
        let currentModalDivision = null;
        let currentModalSort = 'ar';
        
        function openPaparanRisikoModal(divisionCode) {
            console.log('[MODAL] Opening for division:', divisionCode);
            currentModalDivision = divisionCode;
            
            // Get division data
            const divisionBlocks = window.blocksData.filter(block => block.division === divisionCode);
            const criticalBlocks = divisionBlocks.filter(block => {
                const stadium = parseInt(block.stadium_kritis) || 0;
                return stadium >= 3;
            });
            
            // Calculate totals
            const totalLoss = criticalBlocks.reduce((sum, block) => {
                const loss = parseFloat(block.ganoderma_loss_juta) || 0;
                return sum + loss;
            }, 0);
            
            const totalArea = criticalBlocks.reduce((sum, block) => {
                const area = parseFloat(block.luas_ha) || 0;
                return sum + area;
            }, 0);
            
            // Update modal content
            document.getElementById('modalDivisionSubtitle').textContent = 
                `${divisionCode} Division - ${criticalBlocks.length} blok dengan status Stadium 3+`;
            
            document.getElementById('modalTotalLoss').textContent = 
                `Rp ${(totalLoss / 1000).toFixed(1)} M`;
            
            document.getElementById('modalCriticalCount').textContent = 
                `${criticalBlocks.length} Blok`;
            
            document.getElementById('modalRiskArea').textContent = 
                `${totalArea.toFixed(1)} Ha`;
            
            // Render chart
            renderModalChart(criticalBlocks, currentModalSort);
            
            // Show modal
            const modal = document.getElementById('paparanRisikoModal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
        
        function closePaparanRisikoModal() {
            const modal = document.getElementById('paparanRisikoModal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            
            // Destroy chart
            if (modalRiskChart) {
                modalRiskChart.destroy();
                modalRiskChart = null;
            }
        }
        
        function sortModalChart(sortBy) {
            currentModalSort = sortBy;
            
            // Update button styles
            document.getElementById('modalSortByAR').className = 
                sortBy === 'ar' 
                    ? 'px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                    : 'px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';
            
            document.getElementById('modalSortByLoss').className = 
                sortBy === 'loss'
                    ? 'px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                    : 'px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';
            
            // Re-render chart
            if (currentModalDivision) {
                const divisionBlocks = window.blocksData.filter(block => block.division === currentModalDivision);
                const criticalBlocks = divisionBlocks.filter(block => {
                    const stadium = parseInt(block.stadium_kritis) || 0;
                    return stadium >= 3;
                });
                renderModalChart(criticalBlocks, sortBy);
            }
        }
        
        function renderModalChart(blocks, sortBy) {
            const ctx = document.getElementById('modalRiskChart');
            if (!ctx) return;
            
            // Destroy existing chart
            if (modalRiskChart) {
                modalRiskChart.destroy();
            }
            
            // Sort blocks
            const sortedBlocks = [...blocks].sort((a, b) => {
                if (sortBy === 'ar') {
                    return (parseFloat(b.attack_rate) || 0) - (parseFloat(a.attack_rate) || 0);
                } else {
                    return (parseFloat(b.ganoderma_loss_juta) || 0) - (parseFloat(a.ganoderma_loss_juta) || 0);
                }
            });
            
            // Prepare data
            const labels = sortedBlocks.map(block => block.block_code);
            const arData = sortedBlocks.map(block => parseFloat(block.attack_rate) || 0);
            const lossData = sortedBlocks.map(block => (parseFloat(block.ganoderma_loss_juta) || 0) / 1000); // Convert to Miliar
            
            // Create chart
            modalRiskChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Attack Rate (%)',
                            data: arData,
                            backgroundColor: 'rgba(239, 68, 68, 0.7)',
                            borderColor: 'rgb(239, 68, 68)',
                            borderWidth: 2,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Loss (Miliar Rp)',
                            data: lossData,
                            backgroundColor: 'rgba(251, 191, 36, 0.7)',
                            borderColor: 'rgb(251, 191, 36)',
                            borderWidth: 2,
                            yAxisID: 'y1'
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
                            labels: {
                                color: '#fff',
                                font: { size: 12, weight: 'bold' }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.9)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: 'rgba(239, 68, 68, 0.5)',
                            borderWidth: 1,
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
                            ticks: { color: '#fff', font: { size: 10 } },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        y: {
                            type: 'linear',
                            position: 'left',
                            ticks: { 
                                color: 'rgb(239, 68, 68)',
                                callback: function(value) {
                                    return value.toFixed(0) + '%';
                                }
                            },
                            grid: { color: 'rgba(239, 68, 68, 0.2)' },
                            title: {
                                display: true,
                                text: 'Attack Rate (%)',
                                color: 'rgb(239, 68, 68)',
                                font: { weight: 'bold' }
                            }
                        },
                        y1: {
                            type: 'linear',
                            position: 'right',
                            ticks: { 
                                color: 'rgb(251, 191, 36)',
                                callback: function(value) {
                                    return 'Rp ' + value.toFixed(1) + ' M';
                                }
                            },
                            grid: { drawOnChartArea: false },
                            title: {
                                display: true,
                                text: 'Loss (Miliar Rp)',
                                color: 'rgb(251, 191, 36)',
                                font: { weight: 'bold' }
                            }
                        }
                    }
                }
            });
        }
        
        // Close modal when clicking outside
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('paparanRisikoModal');
            if (modal) {
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        closePaparanRisikoModal();
                    }
                });
            }
        });
    '''
    
    # Find closing </script> and insert before it
    script_end = content.rfind('</script>')
    if script_end != -1:
        content = content[:script_end] + modal_js + '\n        ' + content[script_end:]
        print("[SUCCESS] Added modal JavaScript functions")
    
    # 4. MAKE CRITICAL BLOCKS CLICKABLE
    # Find the CRITICAL BLOCKS card in Division Overview
    old_critical_card = '''                    <div class="bg-gradient-to-br from-orange-900/30 to-red-900/30 rounded-xl border-2 border-orange-500/50 p-4">
                        <div class="text-xs text-orange-300/80 font-bold uppercase mb-2 tracking-wider">Critical Blocks</div>
                        <div class="text-5xl font-black text-white" id="divCriticalBlocks">--</div>'''
    
    new_critical_card = '''                    <div onclick="openPaparanRisikoModal(window.currentDivision || 'AME02')" class="bg-gradient-to-br from-orange-900/30 to-red-900/30 rounded-xl border-2 border-orange-500/50 p-4 cursor-pointer hover:border-orange-400 hover:scale-105 transition-all duration-200 group">
                        <div class="text-xs text-orange-300/80 font-bold uppercase mb-2 tracking-wider flex items-center gap-2">
                            Critical Blocks
                            <span class="text-orange-400 opacity-0 group-hover:opacity-100 transition-opacity">🔍</span>
                        </div>
                        <div class="text-5xl font-black text-white" id="divCriticalBlocks">--</div>
                        <div class="text-xs text-orange-300/60 mt-2">Klik untuk detail analisis risiko</div>'''
    
    if old_critical_card in content:
        content = content.replace(old_critical_card, new_critical_card)
        print("[SUCCESS] Made CRITICAL BLOCKS card clickable")
    
    # Write output
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[DONE] File updated: {input_file}")
    print("\n✅ Enhancements:")
    print("  1. Increased year numbers: text-sm → text-xl")
    print("  2. Increased total loss: text-3xl → text-4xl")
    print("  3. Added PAPARAN RISIKO modal")
    print("  4. Made CRITICAL BLOCKS clickable")
    print("  5. Modal shows: Total Loss, Critical Count, Risk Area, Chart")

if __name__ == '__main__':
    enhance_ui_and_add_modal()
