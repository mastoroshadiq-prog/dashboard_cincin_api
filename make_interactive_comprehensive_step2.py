"""
Step 2: Add comprehensive JavaScript controller to INTERACTIVE_FULL
"""

with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🔧 Adding comprehensive JavaScript...")
print("="*70)

# Add embedded data script and controller before </body>
comprehensive_js = '''
    <!-- Embedded Block Data -->
    <script src="blocks_data_embed.js"></script>

    <!-- Comprehensive Interactive Controller -->
    <script>
        let currentBlockData = null;

        // Initialize on page load
        window.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Interactive Dashboard Loading...');
            
            if (typeof BLOCKS_DATA === 'undefined') {
                console.error('❌ BLOCKS_DATA not loaded');
                alert('Error: Block data not loaded. Ensure blocks_data_embed.js is in same folder.');
                return;
            }
            
            console.log('✅ Loaded', Object.keys(BLOCKS_DATA).length, 'blocks');
            
            populateDropdown();
            
            // Attach event listener
            const selector = document.getElementById('blockSelector');
            if (selector) {
                selector.addEventListener('change', function() {
                    updateDashboard(this.value);
                });
                
                // Auto-select first block (highest attack rate)
                const firstBlock = Object.keys(BLOCKS_DATA)[0];
                if (firstBlock) {
                    selector.value = firstBlock;
                    updateDashboard(firstBlock);
                }
            }
        });

        // Populate dropdown
        function populateDropdown() {
            const selector = document.getElementById('blockSelector');
            if (!selector) return;
            
            const sorted = Object.entries(BLOCKS_DATA).sort((a,b) => a[1].rank - b[1].rank);
            
            selector.innerHTML = sorted.map(([code, data]) => 
                `<option value="${code}">#${data.rank} - ${code} | ${data.attack_rate}% | ${data.severity}</option>`
            ).join('');
            
            const totalEl = document.getElementById('totalBlocks');
            if (totalEl) totalEl.textContent = sorted.length;
            
            console.log('✅ Populated dropdown with', sorted.length, 'blocks');
        }

        // Update dashboard comprehensively
        function updateDashboard(blockCode) {
            if (!blockCode || !BLOCKS_DATA[blockCode]) {
                console.warn('Invalid block code:', blockCode);
                return;
            }
            
            const data = BLOCKS_DATA[blockCode];
            currentBlockData = data;
            
            console.log('📊 Updating dashboard for:', blockCode, data);
            
            // Comprehensive updates array
            const updates = [
                // Headers
                ['headerBlockCode', blockCode],
                ['blockDetailHeader', `Detail Blok ${blockCode} (${((data.total_pohon * 64) / 10000).toFixed(1)} Ha)`],
                
                // Status
                ['statusText', data.severity === 'HIGH' ? 'Darurat' : 'Perhatian'],
                
                // Basic stats
                ['blockTT', `${data.tt || 'N/A'} (${data.age || 'N/A'} Tahun)`],
                ['blockSPH', `${data.sph || 'N/A'} Pokok/Ha`],
                ['blockTotalPohon', data.total_pohon.toLocaleString()],
                ['blockSisip', data.sisip ? data.sisip.toLocaleString() : 'N/A'],
                
                // Counts
                ['blockMerahCount', data.merah],
                ['blockOranyeCount', data.oranye],
                ['blockKuningCount', data.kuning]
            ];
            
            let successCount = 0;
            updates.forEach(([id, value]) => {
                const el = document.getElementById(id);
                if (el) {
                    el.textContent = value;
                    el.classList.add('flash-update');
                    setTimeout(() => el.classList.remove('flash-update'), 600);
                    successCount++;
                }
            });
            
            console.log(`✅ Updated ${successCount}/${updates.length} elements`);
            
            // Update page title
            document.title = `Dashboard Cincin Api - ${blockCode} (${data.attack_rate}%)`;
            
            // Update cluster map if it exists
            updateClusterMap(blockCode, data);
        }

        // Update cluster map
        function updateClusterMap(blockCode, data) {
            const mapImages = document.querySelectorAll('img[src*="cincin_api_map"]');
            
            if (mapImages.length > 0) {
                mapImages.forEach(img => {
                    if (blockCode === 'F008A' || blockCode === 'D001A') {
                        img.src = data.map_filename;
                        img.alt = `Peta Kluster ${blockCode}`;
                        img.style.display = 'block';
                    } else {
                        // Hide map, show placeholder message
                        img.style.display = 'none';
                        const parent = img.parentElement;
                        if (parent && !parent.querySelector('.map-placeholder')) {
                            const placeholder = document.createElement('div');
                            placeholder.className = 'map-placeholder bg-gray-100 rounded p-12 text-center text-gray-500';
                            placeholder.innerHTML = `
                                <svg class="mx-auto h-24 w-24 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                                <p class="font-bold">Peta cluster belum tersedia untuk ${blockCode}</p>
                                <p class="text-sm mt-2">Hanya F008A dan D001A yang memiliki peta cluster saat ini</p>
                            `;
                            parent.appendChild(placeholder);
                        }
                    }
                });
                console.log('✅ Updated cluster map display');
            }
        }

        // Tab switching function (from original dashboard)
        function showTab(tabName) {
            // Hide all tabs
            const tabs = document.querySelectorAll('[id^="tab-"]');
            tabs.forEach(tab => tab.style.display = 'none');
            
            // Remove active styling from all buttons
            const buttons = document.querySelectorAll('[id^="btn-"]');
            buttons.forEach(btn => {
                btn.classList.remove('bg-indigo-600', 'text-white', 'shadow-md');
                btn.classList.add('text-black', 'hover:bg-slate-50');
            });
            
            // Show selected tab
            const selectedTab = document.getElementById('tab-' + tabName);
            if (selectedTab) {
                selectedTab.style.display = 'block';
            }
            
            // Add active styling to selected button
            const activeBtn = document.getElementById('btn-' + tabName);
            if (activeBtn) {
                activeBtn.classList.add('bg-indigo-600', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-black', 'hover:bg-slate-50');
            }
        }
    </script>
'''

# Insert before </body>
body_close = '</body>'
if body_close in html:
    html = html.replace(body_close, comprehensive_js + '\n</body>')
    print("✅ Added comprehensive JavaScript controller")
else:
    print("⚠️  </body> tag not found")

# Save final
with open('data/output/dashboard_cincin_api_INTERACTIVE_FULL.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*70)
print("✅ INTERACTIVE_FULL IS NOW COMPREHENSIVE!")
print("="*70)
print("\nFeatures:")
print("  ✅ Full dashboard structure from FINAL_CORRECTED")
print("  ✅ Interactive dropdown selector")
print("  ✅ 10+ dynamic elements with flash animation")
print("  ✅ Smart cluster map display")
print("  ✅ Tab switching support")
print("\nDynamic elements:")
print("  • Block headers and codes")
print("  • Status badge")
print("  • TT, SPH, Total Pohon, Sisip")
print("  • Merah, Oranye, Kuning counts")
print("  • Page title")
print("  • Cluster maps (with placeholder)")
print("\nTest: Open dashboard_cincin_api_INTERACTIVE_FULL.html")
