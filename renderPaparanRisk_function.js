function renderPaparanRisk(sortBy = 'ar', divisionCode = null) {
                if (!BLOCKS_DATA) return;

                console.log(`[PHASE 3] Rendering Paparan Resiko - Sort: ${sortBy}, Division: ${divisionCode || 'ALL'}`);

                // Update button states
                document.getElementById('sortByAR').className = sortBy === 'ar'
                    ? 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                    : 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';
                document.getElementById('sortByLoss').className = sortBy === 'loss'
                    ? 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                    : 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';


                // FIX BUG #2: Use COMPLETE_BLOCKS_DATA and stadium-based filtering
                // OPTION B: Show critical blocks filtered by selected division

                // Constants for loss calculation
                const FFB_PRICE_PER_TON_JUTA = 2.5;

                // Helper: Get stadium classification
                