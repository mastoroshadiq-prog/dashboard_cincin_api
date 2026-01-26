// ═══════════════════════════════════════════════════════════════
// 🔍 BLOCK SEARCH FEATURE - CODE SNIPPETS REFERENCE
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// 1. SEARCH INPUT HTML (Add to modal header section)
// ───────────────────────────────────────────────────────────────
const searchInputHTML = `
<!-- Search Block Input -->
<div class="mb-6">
    <div class="relative">
        <input 
            type="text" 
            id="blockSearchInput" 
            placeholder="Cari kode blok..." 
            oninput="filterBlockLists(this.value)"
            class="w-full bg-slate-800/50 backdrop-blur-sm border border-slate-600 rounded-lg px-4 py-3 pl-11 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
        />
        <div class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl pointer-events-none">
            🔍
        </div>
    </div>
</div>
`;

// ───────────────────────────────────────────────────────────────
// 2. FILTER FUNCTION (Add after closeBlockBreakdownModal)
// ───────────────────────────────────────────────────────────────
function filterBlockLists(searchTerm) {
    const term = searchTerm.toLowerCase().trim();
    
    // Filter all three categories
    const categories = [
        { selector: '.block-item-declining', listId: 'decliningBlocksList' },
        { selector: '.block-item-stable', listId: 'stableBlocksList' },
        { selector: '.block-item-increasing', listId: 'increasingBlocksList' }
    ];

    categories.forEach(category => {
        const items = document.querySelectorAll(category.selector);
        let visibleCount = 0;

        items.forEach(item => {
            const blockCode = item.getAttribute('data-block-code').toLowerCase();
            if (term === '' || blockCode.includes(term)) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Show "no results" message if no items visible
        const listElement = document.getElementById(category.listId);
        if (listElement) {
            const noResultMsg = listElement.querySelector('.no-results-message');
            if (visibleCount === 0 && items.length > 0) {
                if (!noResultMsg) {
                    const msg = document.createElement('div');
                    msg.className = 'no-results-message text-slate-400 text-center py-4 text-sm';
                    msg.textContent = '🔍 Tidak ada blok yang cocok dengan pencarian "' + searchTerm + '"';
                    listElement.appendChild(msg);
                }
            } else if (noResultMsg) {
                noResultMsg.remove();
            }
        }
    });
}

// ───────────────────────────────────────────────────────────────
// 3. AUTO-RESET ON MODAL OPEN (Add before showing modal)
// ───────────────────────────────────────────────────────────────
// Reset search input
const searchInput = document.getElementById('blockSearchInput');
if (searchInput) {
    searchInput.value = '';
}

// ───────────────────────────────────────────────────────────────
// 4. BLOCK ITEM TEMPLATE (with data-block-code attribute)
// ───────────────────────────────────────────────────────────────

// DECLINING BLOCKS:
const decliningBlockHTML = blocks.map(b =>
    '<div class="block-item-declining flex justify-between items-center py-2 px-3 bg-red-900/20 rounded mb-1 border border-transparent hover:border-red-500/50" data-block-code="' + b.block_code + '">' +
    '<span class="text-white font-medium">' + b.block_code + '</span>' +
    '<span class="text-red-400 font-bold">' + b.prodChangePct.toFixed(1) + '%</span>' +
    '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
    '</div>'
).join('');

// STABLE BLOCKS:
const stableBlockHTML = blocks.map(b =>
    '<div class="block-item-stable flex justify-between items-center py-2 px-3 bg-orange-900/20 rounded mb-1 border border-transparent hover:border-orange-500/50" data-block-code="' + b.block_code + '">' +
    '<span class="text-white font-medium">' + b.block_code + '</span>' +
    '<span class="text-orange-400 font-bold">' + (b.prodChangePct >= 0 ? '+' : '') + b.prodChangePct.toFixed(1) + '%</span>' +
    '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
    '</div>'
).join('');

// INCREASING BLOCKS:
const increasingBlockHTML = blocks.map(b =>
    '<div class="block-item-increasing flex justify-between items-center py-2 px-3 bg-green-900/20 rounded mb-1 border border-transparent hover:border-green-500/50" data-block-code="' + b.block_code + '">' +
    '<span class="text-white font-medium">' + b.block_code + '</span>' +
    '<span class="text-green-400 font-bold">+' + b.prodChangePct.toFixed(1) + '%</span>' +
    '<span class="text-slate-400 text-sm">' + b.prod2023.toFixed(1) + ' → ' + b.prod2025.toFixed(1) + ' T/Ha</span>' +
    '</div>'
).join('');

// ───────────────────────────────────────────────────────────────
// 5. CONTAINER STYLING (max-height for scrolling)
// ───────────────────────────────────────────────────────────────
const containerHTML = `
<div id="decliningBlocksList" class="max-h-[500px] overflow-y-auto custom-scrollbar">
    <!-- Block items here -->
</div>
`;

// ───────────────────────────────────────────────────────────────
// 6. CUSTOM SCROLLBAR CSS (if not already defined)
// ───────────────────────────────────────────────────────────────
const scrollbarCSS = `
.custom-scrollbar::-webkit-scrollbar {
    width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: rgba(30, 41, 59, 0.3);
    border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(100, 116, 139, 0.5);
    border-radius: 4px;
    transition: background 0.2s;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(148, 163, 184, 0.7);
}
`;

// ───────────────────────────────────────────────────────────────
// 7. USAGE EXAMPLE - Complete Integration
// ───────────────────────────────────────────────────────────────
function showBlockBreakdownModal(divisionCode) {
    // ... your existing code ...
    
    // Populate blocks WITHOUT slice
    decliningList.innerHTML = categories.declining.map(b =>
        '<div class="block-item-declining ... " data-block-code="' + b.block_code + '">...</div>'
    ).join('');
    
    // Reset search
    const searchInput = document.getElementById('blockSearchInput');
    if (searchInput) searchInput.value = '';
    
    // Show modal
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

// ───────────────────────────────────────────────────────────────
// 8. ADVANCED: Debounced Search (Optional for better performance)
// ───────────────────────────────────────────────────────────────
let searchTimeout;
function debouncedFilterBlockLists(searchTerm) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        filterBlockLists(searchTerm);
    }, 300); // 300ms delay
}

// Usage:
// <input oninput="debouncedFilterBlockLists(this.value)" ...>

// ───────────────────────────────────────────────────────────────
// 9. ALTERNATIVE: Search with Highlighting (Advanced)
// ───────────────────────────────────────────────────────────────
function filterBlockListsWithHighlight(searchTerm) {
    const term = searchTerm.toLowerCase().trim();
    
    document.querySelectorAll('.block-item-declining, .block-item-stable, .block-item-increasing').forEach(item => {
        const blockCode = item.getAttribute('data-block-code');
        const blockCodeLower = blockCode.toLowerCase();
        
        if (term === '' || blockCodeLower.includes(term)) {
            item.style.display = 'flex';
            
            // Highlight matching text
            const codeSpan = item.querySelector('.text-white');
            if (codeSpan && term !== '') {
                const regex = new RegExp('(' + term + ')', 'gi');
                codeSpan.innerHTML = blockCode.replace(regex, '<mark class="bg-yellow-400 text-black">$1</mark>');
            } else if (codeSpan) {
                codeSpan.textContent = blockCode;
            }
        } else {
            item.style.display = 'none';
        }
    });
}

// ───────────────────────────────────────────────────────────────
// 10. EXPORT FILTERED BLOCKS (Bonus Feature)
// ───────────────────────────────────────────────────────────────
function exportFilteredBlocks() {
    const visibleBlocks = [];
    
    document.querySelectorAll('.block-item-declining:not([style*="display: none"])').forEach(item => {
        visibleBlocks.push({
            code: item.getAttribute('data-block-code'),
            category: 'declining'
        });
    });
    // ... repeat for stable and increasing
    
    // Convert to CSV
    const csv = 'Block Code,Category\n' + 
        visibleBlocks.map(b => `${b.code},${b.category}`).join('\n');
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'filtered_blocks.csv';
    a.click();
}

// ═══════════════════════════════════════════════════════════════
// END OF CODE SNIPPETS
// ═══════════════════════════════════════════════════════════════
