
import os

html_path = r'data\output\DASHBOARD_DEMO_FEATURES.html'
new_modal_path = r'data\output\modal_breakdown_v2.html'
json_path = r'data\output\block_breakdown_v2.json'

# Baca HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Baca Modal Baru
with open(new_modal_path, 'r', encoding='utf-8') as f:
    new_modal_content = f.read()

# 1. REPLACE MODAL HTML
# Cari marker modal lama
start_marker = '<!-- ====== BLOCK BREAKDOWN MODAL ======'
end_marker = '<!-- BLOCK DETAIL PANEL (Hidden by default) -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    print(f"Mengganti Modal Breakdown dari index {start_idx} sampai {end_idx}")
    # Replace content, keep end marker
    html = html[:start_idx] + new_modal_content + '\n\n' + html[end_idx:]
else:
    print("WARNING: Modal Breakdown marker tidak ditemukan. Cek HTML.")

# 2. INJECT VARIABLE JSON DATA BARU
# Kita harus membaca file JSON v2 dan menginjectnya ke variabel JS global
import json
with open(json_path, 'r') as f:
    breakdown_data = json.load(f)

json_script = f"""
<script>
    const BLOCK_BREAKDOWN_DATA_V2 = {json.dumps(breakdown_data)};
    console.log("BLOCK BREAKDOWN V2 LOADED", BLOCK_BREAKDOWN_DATA_V2.summary.empty.count + " empty blocks");
</script>
"""
html = html.replace('</body>', json_script + '</body>')


# 3. UPDATE FUNGSI JS openBlockBreakdownModal
# Kita akan override fungsi lama dengan fungsi baru yang handle 5 kategori.
# Karena fungsi lama ada di dalam script tag acak, kita append override function di akhir body (setelah load json)

new_js_logic = """
<script>
    // OVERRIDE FUNCTION FOR V2
    function openBlockBreakdownModal() {
        // Gunakan Data V2
        const data = typeof BLOCK_BREAKDOWN_DATA_V2 !== 'undefined' ? BLOCK_BREAKDOWN_DATA_V2 : null;
        
        if (!data) {
            alert('Data analisis belum siap.');
            return;
        }

        const cats = data.categories;
        const stats = data.summary;

        // 1. Update Counts (Big Numbers)
        document.getElementById('categoryCount_declining').textContent = stats.declining.count;
        document.getElementById('categoryCount_stable').textContent = stats.stable.count;
        document.getElementById('categoryCount_increasing').textContent = stats.increasing.count;
        document.getElementById('categoryCount_tbm').textContent = stats.tbm.count;
        document.getElementById('categoryCount_empty').textContent = stats.empty.count;

        // 2. Update Counts (Small Badges)
        document.getElementById('decliningCount').textContent = stats.declining.count;
        document.getElementById('stableCount').textContent = stats.stable.count;
        document.getElementById('increasingCount').textContent = stats.increasing.count;
        document.getElementById('tbmCount').textContent = stats.tbm.count;
        document.getElementById('emptyCount').textContent = stats.empty.count;

        // 3. Update Analysis Footer
        document.getElementById('avgChange_declining').textContent = stats.declining.avg_change + '%';
        document.getElementById('totalArea_declining').textContent = stats.declining.total_area + ' Ha';
        document.getElementById('totalArea_empty').textContent = stats.empty.total_area + ' Ha';

        // 4. Render Lists
        renderBlockList('decliningBlocksList', cats.declining, 'text-red-400');
        renderBlockList('stableBlocksList', cats.stable, 'text-orange-400');
        renderBlockList('increasingBlocksList', cats.increasing, 'text-green-400');
        renderBlockList('tbmBlocksList', cats.tbm, 'text-emerald-400');
        renderEmptyBlockList('emptyBlocksList', cats.empty);

        // Show Modal
        document.getElementById('blockBreakdownModal').classList.remove('hidden');
    }

    // Helper render list standard
    function renderBlockList(containerId, blocks, colorClass) {
        const container = document.getElementById(containerId);
        if(!container) return;
        container.innerHTML = '';
        
        blocks.forEach(block => {
            const div = document.createElement('div');
            // Add block-item class for search filtering
            div.className = 'flex justify-between items-center p-2 bg-slate-800/30 rounded hover:bg-slate-700/50 cursor-pointer block-item';
            div.setAttribute('data-block', block.block_code.toLowerCase());
            div.onclick = function() { showBlockDetail(block.block_code); };
            div.innerHTML = `
                <span class="font-bold text-slate-200 text-xs">${block.block_code}</span>
                <span class="text-[10px] ${colorClass}">${block.desc || block.val + '%'}</span>
            `;
            container.appendChild(div);
        });
    }

    // Helper render empty list
    function renderEmptyBlockList(containerId, blocks) {
        const container = document.getElementById(containerId);
        if(!container) return;
        container.innerHTML = '';
        
        blocks.slice(0, 100).forEach(block => { // Limit render agar tidak berat (500 blok!)
            const div = document.createElement('div');
            div.className = 'flex justify-between items-center p-2 bg-slate-800/30 rounded hover:bg-slate-700/50 cursor-pointer block-item';
            div.setAttribute('data-block', block.block_code.toLowerCase());
            // Empty block still opens detail (standard popup)
            div.onclick = function() { showBlockDetail(block.block_code); };
            div.innerHTML = `
                <span class="font-bold text-slate-400 text-xs">${block.block_code}</span>
                <span class="text-[9px] text-slate-600 italic">No Data</span>
            `;
            container.appendChild(div);
        });
        
        if(blocks.length > 100) {
            const more = document.createElement('div');
            more.className = 'text-center text-[9px] text-slate-600 py-2';
            more.textContent = `... dan ${blocks.length - 100} blok lainnya`;
            container.appendChild(more);
        }
    }
    
    // Search Filter Logic
    function filterBlockLists(query) {
       query = query.toLowerCase();
       const allItems = document.querySelectorAll('.block-item');
       
       allItems.forEach(item => {
           const code = item.getAttribute('data-block');
           if(code.includes(query)) {
               item.style.display = 'flex';
           } else {
               item.style.display = 'none';
           }
       });
    }

</script>
"""

html = html.replace('</body>', new_js_logic + '</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Berhasil mengupdate HTML Modal Breakdown V2 dan JS Logic.")
