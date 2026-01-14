"""
Update renderPaparanRisk to support sortBy parameter
"""

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the function
old_func = "function renderPaparanRisk() {"
new_func = "function renderPaparanRisk(sortBy = 'ar') {"

content = content.replace(old_func, new_func)

# Add button state management and sorting logic after the function declaration
old_sort = """            if (!BLOCKS_DATA) return;

            const sorted = Object.entries(BLOCKS_DATA).sort((a, b) => (b[1].attack_rate || 0) - (a[1].attack_rate || 0));"""

new_sort = """            if (!BLOCKS_DATA) return;

            // Update button states
            document.getElementById('sortByAR').className = sortBy === 'ar' 
                ? 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                : 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';
            document.getElementById('sortByLoss').className = sortBy === 'loss'
                ? 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-600 text-white border border-rose-400'
                : 'px-3 py-1 rounded-lg text-xs font-bold bg-rose-900/30 text-rose-300 border border-rose-500/30';

            // Sort data
            const sorted = Object.entries(BLOCKS_DATA).sort((a, b) => {
                if (sortBy === 'ar') {
                    return (b[1].attack_rate || 0) - (a[1].attack_rate || 0);
                } else {
                    return (b[1].loss_value_juta || 0) - (a[1].loss_value_juta || 0);
                }
            });"""

content = content.replace(old_sort, new_sort)

with open('data/output/DASHBOARD_DEMO_FEATURES.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated renderPaparanRisk with sortBy parameter")
print("✅ Added button state toggle")
print("✅ Added conditional sorting (AR or Loss)")
