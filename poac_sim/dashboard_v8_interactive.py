"""
🔥 DASHBOARD PRO v8.2 (COST CONTROL EDITION)
==============================================
Features:
1. Real-time Cincin Api Recalculation (JS Engine)
2. Interactive Canvas Maps
3. Full POV 1 & 2 Analysis
4. Cost Control Integration (Ghost Trees & Treatment Sim)
"""

import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import modules
try:
    from src.ingestion import load_and_clean_data
    from config import ZSCORE_PRESETS
    from dashboard_v7_fixed import load_ame_iv_data, load_productivity_data, convert_gano_to_prod_pattern
except ImportError:
    pass

# -----------------------------------------------------------------------------
# 1. DATA PREPARATION ENGINE
# -----------------------------------------------------------------------------

def load_cost_control_data():
    """
    Load data_baru.csv for Ground Truth (Sensus) and Asset Audit (Total Pokok).
    Returns tuple: (cost_data_dict, normalization_function)
    """
    try:
        path = Path('data/input/data_baru.csv')
        if not path.exists():
            logging.warning("⚠️ Cost control data (data_baru.csv) not found.")
            return {}, None
            
        # Read header at row 4 (index 4, 0-based)
        df = pd.read_csv(path, header=4)
        
        # Clean columns: Remove unnamed, strip spaces
        df.columns = [str(c).strip() for c in df.columns]
        
        # Identify Columns
        blok_col = None
        # Heuristic: Find 'BARU' column that has block-like values
        for c in df.columns:
            if 'BARU' in c.upper() or 'BLOK' in c.upper():
                sample = df[c].dropna().astype(str).unique()
                if len(sample) > 5: 
                    valid_samples = [s for s in sample if len(s) >= 3 and len(s) <= 7]
                    if len(valid_samples) > 0:
                        blok_col = c
                        if 'BARU.2' in c: break 
        
        if not blok_col:
            if len(df.columns) > 2:
                blok_col = df.columns[2]
                logging.warning(f"⚠️ Falling back to column index 2 ('{blok_col}') for Block ID")
            else:
                logging.warning("⚠️ Could not identify Block column in data_baru.csv")
                return {}, None

        cost_data = {}
        
        # Regex to capture [Letter] + [Zeros] + [Number]
        # e.g. D001A -> D + 1, D01 -> D + 1
        blk_pattern = re.compile(r'([A-Z])0*(\d+)', re.IGNORECASE)

        def normalize_block_key(raw_name):
            """
            Normalize 'D001A' -> 'D1', 'D01' -> 'D1'
            """
            m = blk_pattern.search(str(raw_name).strip())
            if m:
                return f"{m.group(1).upper()}{m.group(2)}"
            return str(raw_name).strip().upper().replace(" ", "")
        
        for _, row in df.iterrows():
            try:
                # Get Block ID
                val = str(row[blok_col]).strip().upper()
                if not val or val == 'NAN': continue
                
                # Use Normalized Key
                norm_key = normalize_block_key(val)

                # Get Total Pokok Buku (Clean comma/dots)
                total_str = str(row.get('TOTAL PKK', 0)).replace(',', '').replace('.', '')
                try: total_pkk = int(total_str)
                except: total_pkk = 0
                
                # Get Sensus Attack Rates
                sensus = row.get('%SERANGAN', 0)
                if isinstance(sensus, str):
                    sensus = sensus.replace('%', '').replace(',', '.')
                try: sensus = float(sensus)
                except: sensus = 0.0
                
                if norm_key not in cost_data:
                    cost_data[norm_key] = {
                        'total_buku': total_pkk,
                        'sensus_pct': round(sensus, 2)
                    }
            except Exception:
                continue
                
        logging.info(f"✅ Loaded Cost Control data for {len(cost_data)} blocks. Norm Example: D001A -> {normalize_block_key('D001A')}")
        return cost_data, normalize_block_key
        
    except Exception as e:
        logging.error(f"❌ Error loading cost control data: {e}")
        return {}, None

def prepare_block_data(df, cost_data_map=None, norm_func=None):
    """
    Convert DataFrame to optimized JSON structure per block.
    """
    blocks_data = {}
    
    for blok, group in df.groupby('Blok'):
        min_x = group['N_POKOK'].min()
        min_y = group['N_BARIS'].min()
        max_x = group['N_POKOK'].max()
        max_y = group['N_BARIS'].max()
        
        if pd.isna(min_x) or pd.isna(min_y): continue
        
        mean_ndvi = group['NDRE125'].mean()
        std_ndvi = group['NDRE125'].std()
        
        # SISIP DETECTION LOGIC
        # Find majority year (Mode)
        is_sisip_available = False
        mode_year = 0
        
        # Check diverse years
        # Access Year column safely (AME II 't_tanam', AME IV 'Tahun' or 'N_BARIS' mapped)
        year_col = None
        if 't_tanam' in df.columns: year_col = 't_tanam' # AME II
        elif 'Tahun' in df.columns: year_col = 'Tahun'   # AME IV (Mapped)
        
        if year_col:
            try:
                counts = group[year_col].value_counts()
                if not counts.empty:
                    mode_year = counts.idxmax()
                    # If more than 5% trees are NOT mode year, consider variation valid
                    if len(counts) > 1:
                        is_sisip_available = True
            except: pass

        trees = [] 
        for _, row in group.iterrows():
            x = int(row['N_POKOK'] - min_x)
            y = int(row['N_BARIS'] - min_y)
            if std_ndvi > 0:
                z = (row['NDRE125'] - mean_ndvi) / std_ndvi
            else:
                z = 0
            
            # Determine Sisip Status
            is_sisip = 0
            if is_sisip_available:
                try:
                    tree_year = float(row[year_col])
                    # If tree is younger (Year > Mode) by at least 1 year
                    if tree_year > mode_year:
                        is_sisip = 1
                except: is_sisip = 0

            trees.append([x, y, round(z, 2), is_sisip])

        
        
            trees.append([x, y, round(z, 2), is_sisip])

        # --- SERVER-SIDE CINCIN API SIMULATION (Standard Preset) ---
        # To provide "Top 5 Rankings" immediately without JS crunching
        # Standard: Core -1.5, Neighbor -1.0, Min 3
        sim_z_core = -1.5
        sim_z_neighbor = -1.0
        sim_min = 3
        
        sim_tree_map = {}
        sim_trees = []
        for t in trees:
             # t = [x, y, z, is_sisip]
             node = {'x': t[0], 'y': t[1], 'z': t[2], 'status': 'HIJAU'}
             sim_trees.append(node)
             sim_tree_map[f"{t[0]},{t[1]}"] = node
             
        # Detect
        sim_reds = 0
        offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        
        for t in sim_trees:
            if t['z'] < sim_z_core:
                # Check neighbors
                neighbors = 0
                for o in offsets:
                    nk = f"{t['x']+o[0]},{t['y']+o[1]}"
                    if nk in sim_tree_map and sim_tree_map[nk]['z'] < sim_z_neighbor:
                        neighbors += 1
                
                if neighbors >= sim_min:
                    sim_reds += 1
        
        infected_pct = (sim_reds / len(trees) * 100) if trees else 0
        
        # Inject Cost Control Data (WITH NORMALIZATION)
        cost_info = {'total_buku': 0, 'sensus_pct': 0}
        
        if cost_data_map:
            # Normalize current block name (e.g. D01 -> D1)
            search_key = blok
            if norm_func:
                search_key = norm_func(blok)
            elif cost_data_map: # Try basic cleaning if norm_func missing
                 search_key = str(blok).replace(" ","").upper()
            
            if search_key in cost_data_map:
                cost_info = cost_data_map[search_key]
        
        blocks_data[blok] = {
            'width': int(max_x - min_x + 1),
            'height': int(max_y - min_y + 1),
            'min_x': int(min_x),
            'min_y': int(min_y),
            'stats': {
                'count': len(trees),
                'mean_ndvi': round(mean_ndvi, 3),
                'std_ndvi': round(std_ndvi, 3),
                'infected_pct': round(infected_pct, 2), # Initial Ranking Metric
                'total_buku': cost_info['total_buku'],
                'sensus_pct': cost_info['sensus_pct']
            },
            'trees': trees
        }
    return blocks_data

def analyze_divisi_interactive(df, divisi_name, prod_df, cost_data_map, norm_func=None):
    """
    Analyze division data for POV tables.
    """
    blocks_json = prepare_block_data(df, cost_data_map, norm_func)
    pov_rows = []
    
    preset = ZSCORE_PRESETS['standar']
    z_core = preset['z_threshold_core']
    
    for blok, data in blocks_json.items():
        trees = np.array(data['trees']) 
        if len(trees) == 0: continue
            
        suspect_count = np.sum(trees[:, 2] < z_core)
        attack_pct = (suspect_count / len(trees)) * 100
        
        prod_pattern = convert_gano_to_prod_pattern(blok)
        yield_matches = prod_df[prod_df['Blok_Prod'].str.contains(prod_pattern, na=False, regex=False)]
        
        if not yield_matches.empty:
            yield_matches = yield_matches[(yield_matches['Umur_Tahun'] >= 3) & (yield_matches['Umur_Tahun'] <= 25)]
            if not yield_matches.empty:
                r = yield_matches.iloc[0]
                pov_rows.append({
                    'Blok': blok,
                    'Attack_Pct': round(attack_pct, 1),
                    'Luas_Ha': r['Luas_Ha'],
                    'Produksi_Ton': r['Produksi_Ton'],
                    'Yield_TonHa': round(float(r['Yield_TonHa']), 2),
                    'Potensi_Yield': r['Potensi_Yield'],
                    'Gap_Yield': round(float(r['Gap_Yield']), 2),
                    'Umur': int(r['Umur_Tahun'])
                })
                
    return blocks_json, pov_rows


# -----------------------------------------------------------------------------
# 2. HTML GENERATOR (V8.2 Cost Control Update)
# -----------------------------------------------------------------------------

def generate_v8_dashboard(all_data):
    """
    Generate HTML with Cost Control & Info Panel
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    divisi_json_map = {}
    pov_tables_html = {}
    
    for div, data in all_data.items():
        div_key = div.replace(" ", "_")
        divisi_json_map[div_key] = data['blocks_json']
        
        rows = data['pov_data']
        if rows:
            # Initial sort by Attack Rate Descending
            rows.sort(key=lambda x: x['Attack_Pct'], reverse=True)
            tbl = "<div style='margin-bottom:10px; font-style:italic; color:#666'>💡 Tip: Click column headers to sort (e.g., 'Yield' for Best Performers). Showing all blocks.</div>"
            tbl += "<table class='pov-table' id='povAnalysisTable' style='width:100%'>"
            tbl += "<thead><tr style='background:#f0f0f0; cursor:pointer'>"
            tbl += "<th onclick='sortTable(0)'>Blok ↕</th>"
            tbl += "<th onclick='sortTable(1, true)'>Luas ↕</th>"
            tbl += "<th onclick='sortTable(2, true)'>Umur ↕</th>"
            tbl += "<th onclick='sortTable(3, true)'>Attack Rate ↕</th>"
            tbl += "<th onclick='sortTable(4, true)'>Produksi ↕</th>"
            tbl += "<th onclick='sortTable(5, true)'>Yield ↕</th>"
            tbl += "<th onclick='sortTable(6, true)'>Gap ↕</th>"
            tbl += "</tr></thead><tbody>"
            
            for r in rows:
                gap_color = "#e74c3c" if r['Gap_Yield'] < 0 else "#2ecc71"
                # Add data-value attribute for numeric sorting accuracy in JS
                tbl += f"<tr>"
                tbl += f"<td>{r['Blok']}</td>"
                tbl += f"<td data-val='{r['Luas_Ha']}'>{r['Luas_Ha']}</td>"
                tbl += f"<td data-val='{r['Umur']}'>{r['Umur']}</td>"
                tbl += f"<td data-val='{r['Attack_Pct']}'><b>{r['Attack_Pct']}%</b></td>"
                tbl += f"<td data-val='{r['Produksi_Ton']}'>{r['Produksi_Ton']}</td>"
                tbl += f"<td data-val='{r['Yield_TonHa']}'>{r['Yield_TonHa']:.2f}</td>"
                tbl += f"<td data-val='{r['Gap_Yield']}' style='color:{gap_color}; font-weight:bold'>{r['Gap_Yield']:.2f}</td>"
                tbl += "</tr>"
            tbl += "</tbody></table>"
            pov_tables_html[div_key] = tbl
        else:
            pov_tables_html[div_key] = "<div style='padding:20px; text-align:center'>No Production Data Available</div>"

    # --- JAVASCRIPT LOGIC ---
    js_logic = r"""
// GLOBAL ERROR HANDLER
window.onerror = function(message, source, lineno, colno, error) {
    const loader = document.getElementById('loader');
    if(loader) {
        loader.innerHTML = `
            <div style="padding:20px; text-align:center; color:#c0392b">
                <h2>⚠️ System Error</h2>
                <p><strong>${message}</strong></p>
                <code style="background:#eee; padding:5px; display:block; margin:10px auto; max-width:800px; text-align:left">
                    Line: ${lineno}:${colno}<br>
                    ${error ? error.stack : ''}
                </code>
            </div>
        `;
        loader.style.background = '#fff';
    }
};

if(typeof DATA === 'undefined' || !DATA) throw new Error("DATA missing");

/* State */
let currentDiv = null;
let currentBlockId = null;

let currentConfig = new Object();
currentConfig.z_core = -1.5;
currentConfig.z_neighbor = -1.0;
currentConfig.min = 3;

// Financial Config
let financial = {
    cost_per_tree: 50000,
    asset_value: 1000000
};

let transform = new Object();
transform.x = 20; transform.y = 20; transform.k = 1;

let isDragging = false;
let startPos = new Object(); 
startPos.x = 0; startPos.y = 0;

let computedTrees = [];
let blockDimensions = new Object();
let hoveredTree = null;

const PRESETS = new Object();
PRESETS['konservatif'] = { z_core: -1.2, z_neighbor: -0.8, min: 2 };
PRESETS['standar'] = { z_core: -1.5, z_neighbor: -1.0, min: 3 };
PRESETS['agresif'] = { z_core: -1.8, z_neighbor: -1.2, min: 4 };

/* HELP TIPS LOGIC */
function setupHelpTips() {
    const panel = document.getElementById('infoPanelContent');
    const defaultText = "<div style='color:#999; text-align:center; padding-top:40px; font-style:italic'>Hover over any <b>(?)</b> icon regarding presets or parameters to see detailed explanation here.</div>";
    
    document.querySelectorAll('.help-tip').forEach(tip => {
        tip.addEventListener('mouseenter', () => {
            let text = tip.getAttribute('data-tooltip');
            text = text.replace(/\\n/g, "<br>");
            const parts = text.split("<br>");
            if(parts.length > 0) {
                parts[0] = `<div style='color:#2c3e50; font-size:1.1rem; font-weight:bold; margin-bottom:10px; border-bottom:2px solid #3498db; padding-bottom:5px'>${parts[0]}</div>`;
            }
            panel.innerHTML = parts.join("<br>");
        });
        
        tip.addEventListener('mouseleave', () => {
            panel.innerHTML = defaultText;
        });
    });
    
    panel.innerHTML = defaultText;
}

window.onload = () => {
    // Populate Division
    const divSelect = document.getElementById('divSelect');
    divSelect.innerHTML = '';
    const divKeys = Object.keys(DATA);
    
    if(divKeys.length > 0) {
        divKeys.forEach(key => {
            const opt = document.createElement('option');
            opt.value = key;
            opt.textContent = key.replace(/_/g, " ");
            divSelect.appendChild(opt);
        });
        divSelect.value = divKeys[0];
        loadDivision();
    } else {
        alert("No Data Found");
    }
    
    setupHelpTips();
    
    // Events
    const canvas = document.getElementById('mainCanvas');
    const container = document.querySelector('.canvas-container');
    
    canvas.addEventListener('mousedown', e => {
        isDragging = true;
        startPos.x = e.clientX - transform.x;
        startPos.y = e.clientY - transform.y;
        canvas.style.cursor = 'grabbing';
    });
    
    window.addEventListener('mousemove', e => {
        if(isDragging) {
            e.preventDefault();
            transform.x = e.clientX - startPos.x;
            transform.y = e.clientY - startPos.y;
            drawCanvas(); 
        } else {
            handleTooltip(e);
        }
    });
    
    window.addEventListener('mouseup', () => {
        isDragging = false;
        canvas.style.cursor = 'crosshair';
    });
    
    container.addEventListener('wheel', e => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        adjustZoom(delta);
    });
    
    setTimeout(() => document.getElementById('loader').style.display = 'none', 800);
};

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    if(tab === 'map') {
        document.getElementById('mapView').style.display = 'flex';
        document.getElementById('povView').style.display = 'none';
        setTimeout(resetView, 100);
    } else {
        document.getElementById('mapView').style.display = 'none';
        document.getElementById('povView').style.display = 'block';
    }
}

function loadDivision() {
    currentDiv = document.getElementById('divSelect').value;
    const blocks = DATA[currentDiv];
    const select = document.getElementById('blockSelect');
    
    select.innerHTML = '';
    const sortedBlocks = Object.keys(blocks).sort();
    
    sortedBlocks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b;
        opt.textContent = b + ' (' + blocks[b].stats.count + ')';
        select.appendChild(opt);
    });
    
    document.getElementById('povContent').innerHTML = POV_HTML[currentDiv] || 'No Data';
    
    // BUILD TOP 5 RANKING
    const ranking = [];
    Object.keys(blocks).forEach(k => {
        ranking.push({
            id: k,
            rate: blocks[k].stats.infected_pct || 0
        });
    });
    
    // Sort Descending
    ranking.sort((a,b) => b.rate - a.rate);
    const top5 = ranking.slice(0, 5);
    
    let html = '';
    top5.forEach((r, idx) => {
        if(r.rate > 0) {
            html += `<div style="cursor:pointer; padding:3px 0; border-bottom:1px dashed #eee; display:flex; justify-content:space-between" onclick="loadBlock('${r.id}')">`;
            html += `<span>${idx+1}. <b>${r.id}</b></span>`;
            html += `<span style="color:#c0392b; font-weight:bold">${r.rate}%</span></div>`;
        }
    });

    if(html === '') html = '<div style="color:#7f8c8d; font-style:italic">No critical blocks found yet.</div>';
    document.getElementById('top5List').innerHTML = html;

    if(sortedBlocks.length > 0) {
        currentBlockId = sortedBlocks[0];
        calculateAlgorithm(); 
        resetView();
    }
}

function loadBlock(blkId) {
    document.getElementById('blockSelect').value = blkId;
    currentBlockId = blkId;
    resetView();
    calculateAlgorithm();
}

function applyPreset(name) {
    const p = PRESETS[name];
    currentConfig.z_core = p.z_core;
    currentConfig.z_neighbor = p.z_neighbor;
    currentConfig.min = p.min;
    
    document.getElementById('z_core').value = p.z_core;
    document.getElementById('z_neighbor').value = p.z_neighbor;
    document.getElementById('min').value = p.min;
    
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    
    updateDisplayValues();
    calculateAlgorithm();
}

function updateParam(id) {
    currentConfig[id] = parseFloat(document.getElementById(id).value);
    // document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active')); 
    // Keep button active distinctness logic separate if needed
    updateDisplayValues();
    calculateAlgorithm();
}

function updateFinancial(id) {
    financial[id] = parseFloat(document.getElementById(id).value);
    calculateAlgorithm(); // Re-calculate stats
}

function updateDisplayValues() {
    document.getElementById('val_z_core').textContent = currentConfig.z_core.toFixed(1);
    document.getElementById('val_z_neighbor').textContent = currentConfig.z_neighbor.toFixed(1);
    document.getElementById('val_min').textContent = currentConfig.min;
}

function resetView() {
    currentBlockId = document.getElementById('blockSelect').value;
    if(!currentBlockId || !DATA[currentDiv]) return;
    const blockData = DATA[currentDiv][currentBlockId];
    if(!blockData) return;
    
    const container = document.querySelector('.canvas-container');
    const scaleX = (container.clientWidth - 100) / blockData.width;
    const scaleY = (container.clientHeight - 100) / blockData.height;
    transform.k = Math.min(scaleX, scaleY, 15);
    if(transform.k < 1) transform.k = 1;
    
    transform.x = (container.clientWidth - blockData.width * transform.k) / 2;
    transform.y = (container.clientHeight - blockData.height * transform.k) / 2;
    
    drawCanvas();
}

function adjustZoom(factor) {
    transform.k *= factor;
    if(transform.k < 0.5) transform.k = 0.5;
    if(transform.k > 50) transform.k = 50;
    drawCanvas();
}

function calculateAlgorithm() {
    currentBlockId = document.getElementById('blockSelect').value;
    const blockData = DATA[currentDiv][currentBlockId];
    if(!blockData) return;
    
    // UPDATE BLOCK INFO OVERLAY
    document.getElementById('blockInfoOverlay').innerHTML = 
        `<h4 style="margin:0 0 5px 0; color:#2c3e50">Block ${currentBlockId}</h4>` +
        `<div style="font-size:0.85rem; color:#555">` + 
        `Trees Analysed: <b>${blockData.stats.count}</b><br>` +
        `Avg NDRE: <b>${blockData.stats.mean_ndvi}</b><br>` +
        `<span style="color:#888; font-size:0.8rem">Grid: ${blockData.width} x ${blockData.height}</span>` +
        `</div>`;
    
    blockDimensions.w = blockData.width;
    blockDimensions.h = blockData.height;
    
    const treeMap = new Map();
    const trees = [];
    
    blockData.trees.forEach(t => {
        const tree = { 
            x: t[0], y: t[1], z: t[2], 
            is_sisip: t[3] === 1,
            orig_x: t[0] + (blockData.min_x || 0), 
            orig_y: t[1] + (blockData.min_y || 0), 
            status: 'HIJAU' 
        };
        const key = t[0] + ',' + t[1];
        treeMap.set(key, tree);
        trees.push(tree);
    });
    
    // Logic: Identify Suspects
    const suspects = [];
    trees.forEach(t => {
        if (t.z < currentConfig.z_core) {
            t.status = 'SUSPECT';
            suspects.push(t);
        }
    });
    
    // Logic: Neighbors
    const offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]];
    const clusters = [];
    let red_count = 0;
    
    suspects.forEach(t => {
        let stressed_neighbors = 0;
        offsets.forEach(o => {
            const nb = treeMap.get((t.x + o[0]) + ',' + (t.y + o[1]));
            if (nb && nb.z < currentConfig.z_neighbor) {
                stressed_neighbors++;
            }
        });
        
        if (stressed_neighbors >= currentConfig.min) {
            t.status = 'MERAH';
            clusters.push(t);
            red_count++;
        } else {
            t.status = 'KUNING';
        }
    });
    
    // logic Ring
    let orange_count = 0;
    clusters.forEach(c => {
        offsets.forEach(o => {
            const nb = treeMap.get((c.x + o[0]) + ',' + (c.y + o[1]));
            if (nb && nb.status !== 'MERAH') {
                if (nb.status !== 'ORANYE') orange_count++;
                nb.status = 'ORANYE';
            }
        });
    });
    
    let yellow_count = 0, green_count = 0;
    trees.forEach(t => {
        if(t.status === 'KUNING') yellow_count++;
        else if(t.status === 'HIJAU') green_count++;
    });
    
    // UPDATE UI STATS
    document.getElementById('cnt_red').innerText = red_count;
    document.getElementById('cnt_org').innerText = orange_count;
    document.getElementById('cnt_yell').innerText = yellow_count;
    document.getElementById('cnt_grn').innerText = green_count;
    
    const attack_rate = ((red_count + orange_count) / trees.length * 100).toFixed(1);
    document.getElementById('attack_rate').innerText = attack_rate + '%';
    
    // --- FINANCIAL INSIGHTS LOGIC ---
    const totalBuku = blockData.stats.total_buku || 0;
    const sensusPct = blockData.stats.sensus_pct || 0;
    const totalDrone = trees.length;
    
    // 1. Ghost Trees (Asset Audit)
    let ghostTrees = 0;
    let assetLoss = 0;
    let ghostHtml = '';
    
    if(totalBuku > 0) {
        ghostTrees = totalBuku - totalDrone;
        if(ghostTrees < 0) ghostTrees = 0; // Drone count > Buku? anomaly but ignore for loss calc
        assetLoss = ghostTrees * financial.asset_value;
        
        const lossFormatted = (assetLoss / 1000000).toFixed(1) + ' Juta';
        ghostHtml = `<span style="color:${ghostTrees > 50 ? '#e74c3c' : '#f39c12'}">⚠️ ${ghostTrees} Trees (${lossFormatted})</span>`;
    } else {
        ghostHtml = '<span style="color:#ccc">Data N/A</span>';
    }
    
    // 2. Sensus Comparison (Validity)
    let sensusHtml = '';
    if(sensusPct > 0) {
        const diff = parseFloat(attack_rate) - sensusPct;
        sensusHtml = `<b>${sensusPct}%</b> (Manual) vs <b>${attack_rate}%</b> (AI)<br>`;
        if(diff > 5) sensusHtml += `<span style="color:#2ecc71; font-size:0.8rem">💡 Found ${diff.toFixed(1)}% new potential infections</span>`;
        if(diff > 25) sensusHtml += `<br><span style="color:#e74c3c; font-size:0.8rem">⚠️ Large discrepancy! Check Field.</span>`;
        if(diff < -2) sensusHtml += `<span style="color:#e74c3c; font-size:0.8rem">⚠️ Under-detection by ${Math.abs(diff).toFixed(1)}%</span>`;
        else if(Math.abs(diff) <= 5) sensusHtml += `<span style="color:#3498db; font-size:0.8rem">✅ Validated (High Match)</span>`;
    } else {
         sensusHtml = '<span style="color:#ccc">No Census Data</span>';
    }
    
    // 3. Treatment Cost
    const infectedTotal = red_count + orange_count + yellow_count; // Assume treating all suspects
    const estCost = infectedTotal * financial.cost_per_tree;
    const costFormatted = "Rp " + estCost.toLocaleString('id-ID');
    
    // Update Financial Panel UI
    document.getElementById('val_ghost').innerHTML = ghostHtml;
    document.getElementById('val_sensus').innerHTML = sensusHtml;
    document.getElementById('val_cost').innerText = costFormatted;
    
    computedTrees = trees;
    drawCanvas();
}

function drawCanvas() {
    const canvas = document.getElementById('mainCanvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.canvas-container');
    
    if(canvas.width !== container.clientWidth || canvas.height !== container.clientHeight) {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    ctx.save();
    ctx.translate(transform.x, transform.y);
    ctx.scale(transform.k, transform.k);
    
    computedTrees.forEach(t => {
        ctx.beginPath();
        if (t.status === 'MERAH') ctx.fillStyle = '#e74c3c';
        else if (t.status === 'ORANYE') ctx.fillStyle = '#e67e22';
        else if (t.status === 'KUNING') ctx.fillStyle = '#f1c40f';
        else ctx.fillStyle = '#2ecc71';
        
        ctx.fillRect(t.x, t.y, 0.8, 0.8); 
        
        // DRAW SISIP MARKER (White Dot)
        if(t.is_sisip) {
            ctx.fillStyle = 'rgba(255,255,255,0.7)';
            ctx.beginPath();
            ctx.arc(t.x + 0.4, t.y + 0.4, 0.2, 0, 2 * Math.PI);
            ctx.fill();
        }
    });
    
    if(hoveredTree) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 0.1; 
        ctx.strokeRect(hoveredTree.x - 0.1, hoveredTree.y - 0.1, 1.0, 1.0);
    }
    
    ctx.restore();
}

function handleTooltip(e) {
    const rect = document.getElementById('mainCanvas').getBoundingClientRect();
    const worldX = (e.clientX - rect.left - transform.x) / transform.k;
    const worldY = (e.clientY - rect.top - transform.y) / transform.k;
    
    const gridX = Math.floor(worldX);
    const gridY = Math.floor(worldY);
    const offsetX = worldX - gridX;
    const offsetY = worldY - gridY;
    
    const inBox = offsetX >= 0 && offsetX <= 0.8 && offsetY >= 0 && offsetY <= 0.8;
    
    let tree = null;
    if (inBox) {
        tree = computedTrees.find(t => t.x === gridX && t.y === gridY);
    }
    
    if (tree !== hoveredTree) {
        hoveredTree = tree;
        drawCanvas();
    }
    
    const tooltip = document.getElementById('tooltip');
    
    if (tree) {
        const currentBlock = DATA[currentDiv][currentBlockId];
        const ndre = (tree.z * currentBlock.stats.std_ndvi + currentBlock.stats.mean_ndvi).toFixed(3);
        
        let statusIcon = '🟢';
        let statusText = 'HIJAU';
        
        if(tree.status === 'MERAH') { statusIcon = '🔴'; statusText = 'MERAH'; }
        else if(tree.status === 'ORANYE') { statusIcon = '🟠'; statusText = 'ORANYE'; }
        else if(tree.status === 'KUNING') { statusIcon = '🟡'; statusText = 'KUNING'; }
        else if(tree.status === 'SUSPECT') { statusIcon = '🟡'; statusText = 'SUSPECT'; }
        
        let sisipBadge = '';
        if(tree.is_sisip) {
            sisipBadge = '<div style="background:#555; color:white; padding:2px 5px; border-radius:4px; font-size:0.75rem; margin-top:5px; display:inline-block">🌱 SISIP / REPLANT</div>';
        }
        
        const canvas = document.getElementById('mainCanvas');
        canvas.style.cursor = 'pointer';

        tooltip.innerHTML = `
            <div style="margin-bottom:5px"><strong>${statusIcon} ${statusText}</strong></div>
            <div style="display:grid; grid-template-columns: 80px auto; gap:2px; font-family:monospace">
                <span>N_POKOK:</span> <b>${tree.orig_x}</b>
                <span>N_BARIS:</span> <b>${tree.orig_y}</b>
                <span>NDRE:</span> <b>${ndre}</b>
                <span>Z-Score:</span> <b>${tree.z}</b>
            </div>
            ${sisipBadge}
        `;
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 15) + 'px';
        tooltip.style.top = (e.clientY + 15) + 'px';
    } else {
        const canvas = document.getElementById('mainCanvas');
        if(!isDragging) canvas.style.cursor = 'crosshair';
        tooltip.style.display = 'none';
    }
}

function showDrilldown(status) {
    const list = computedTrees.filter(t => t.status === status);
    const table = document.getElementById('popTable');
    const title = document.getElementById('popTitle');
    const currentBlock = DATA[currentDiv][currentBlockId];
    
    title.innerText = `${status} (${list.length})`;
    if(status === 'MERAH') title.style.color = '#e74c3c';
    else if(status === 'ORANYE') title.style.color = '#e67e22';
    else if(status === 'KUNING') title.style.color = '#f1c40f';
    else title.style.color = '#2ecc71';
    
    list.sort((a,b) => (a.orig_y - b.orig_y) || (a.orig_x - b.orig_x));
    
    let html = '<thead><tr><th>Baris</th><th>Pokok</th><th>NDRE</th><th>Z-Score</th></tr></thead><tbody>';
    
    const showList = list.slice(0, 500);
    
    showList.forEach(t => {
        const ndre = (t.z * currentBlock.stats.std_ndvi + currentBlock.stats.mean_ndvi).toFixed(3);
        html += `<tr><td>${t.orig_y}</td><td>${t.orig_x}</td><td>${ndre}</td><td>${t.z}</td></tr>`;
    });
    
    if(list.length > 500) {
        html += `<tr><td colspan="4" style="text-align:center; color:#999">... and ${list.length - 500} more ...</td></tr>`;
    }
    
    if(list.length === 0) {
        html += `<tr><td colspan="4" style="text-align:center; padding:20px">No matching trees</td></tr>`;
    }
    
    html += '</tbody>';
    table.innerHTML = html;
    
    const pop = document.getElementById('statsPopover');
    pop.style.display = 'flex';
    pop.style.top = '100px';
    pop.style.right = '340px'; 
}

/* SORT TABLE LOGIC */
function sortTable(n, isNumeric=false) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("povAnalysisTable");
  switching = true;
  dir = "asc"; 
  
  while (switching) {
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      
      let xVal = x.getAttribute('data-val') || x.innerHTML.toLowerCase();
      let yVal = y.getAttribute('data-val') || y.innerHTML.toLowerCase();
      
      if(isNumeric) {
          xVal = parseFloat(xVal);
          yVal = parseFloat(yVal);
      }
      
      if (dir == "asc") {
        if (xVal > yVal) { shouldSwitch = true; break; }
      } else if (dir == "desc") {
        if (xVal < yVal) { shouldSwitch = true; break; }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
"""

    # --- MAIN HTML FOO---
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>POAC v8.2 Cost Control</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #f4f6f9; display: flex; flex-direction: column; height: 100vh; }}
        header {{ background: #2c3e50; color: white; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .header-title {{ font-size: 1.2rem; font-weight: 500; display:flex; align-items:center; gap:10px; }}
        
        .layout {{ display: flex; flex: 1; overflow: hidden; }}
        
        .sidebar {{ width: 340px; background: white; border-right: 1px solid #ddd; display: flex; flex-direction: column; z-index:10; box-shadow: 2px 0 5px rgba(0,0,0,0.05); }}
        .sidebar-scroll {{ flex:1; overflow-y:auto; }}
        
        .control-group {{ padding: 20px; border-bottom: 1px solid #eee; }}
        .control-group h3 {{ margin: 0 0 15px 0; font-size: 0.9rem; text-transform: uppercase; color: #888; letter-spacing: 1px; }}
        
        /* Financial Panel Style */
        .financial-card {{ background: #fdfefe; border: 1px solid #e1e8ed; border-radius: 6px; padding: 10px; margin-bottom: 5px; }}
        .fin-label {{ font-size: 0.8rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; display:block; }}
        .fin-value {{ font-size: 1.0rem; font-weight: 600; color: #2c3e50; }}
        
        input[type=number] {{ width: 100%; box-sizing: border-box; padding: 6px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.9rem; margin-top: 2px; }}

        /* INFO PANEL */
        .info-panel {{ height: 260px; border-top: 2px solid #3498db; background: #f8f9fa; padding: 20px; overflow-y: auto; font-size: 0.85rem; line-height: 1.5; color: #444; box-shadow: inset 0 3px 6px rgba(0,0,0,0.05); }}
        
        select, input[type=range] {{ width: 100%; box-sizing: border-box; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.9rem; margin-bottom: 5px; }}
        label {{ display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px; color: #555; }}
        .val-badge {{ background: #eee; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #333; }}
        
        .preset-btn-group {{ display: flex; gap: 5px; margin-bottom: 20px; }}
        .preset-btn {{ flex: 1; padding: 8px 4px; border: 1px solid #ddd; background: #f9f9f9; cursor: pointer; border-radius: 4px; font-size: 0.8rem; transition: all 0.2s; }}
        .preset-btn.active {{ background: #3498db; color: white; border-color: #2980b9; }}
        
        .tabs {{ display: flex; gap: 20px; }}
        .tab {{ cursor: pointer; padding: 5px 10px; opacity: 0.7; transition: 0.2s; border-bottom: 2px solid transparent; }}
        .tab:hover {{ opacity: 1; }}
        .tab.active {{ opacity: 1; border-bottom-color: #3498db; font-weight: bold; }}
        
        .main-view {{ flex: 1; position: relative; display: flex; flex-direction: column; background: #eef2f5; }}
        .canvas-container {{ flex: 1; background: #222; position: relative; cursor: crosshair; overflow: hidden; }}
        #mainCanvas {{ display: block; }}
        
        /* OVERLAYS */
        .live-stats {{ position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.95); padding: 15px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); width: 220px; backdrop-filter: blur(5px); font-size:0.9rem; z-index: 50; }}
        
        .block-info-overlay {{ position: absolute; top: 250px; right: 20px; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 220px; backdrop-filter: blur(5px); font-size:0.9rem; z-index: 50; border-left: 5px solid #3498db; }}
        
        .stat-row {{ display: flex; justify-content: space-between; margin-bottom: 5px; cursor: pointer; padding:2px; }}
        .stat-row:hover {{ background: rgba(0,0,0,0.05); border-radius: 4px; }}
        .dot {{ width: 10px; height: 10px; display: inline-block; border-radius: 50%; margin-right: 8px; }}
        
        .pov-section {{ padding: 0; background: white; flex: 1; overflow-y: auto; display: none; }}
        .pov-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .pov-table th {{ background: #2c3e50; color: white; padding: 10px; text-align: left; position: sticky; top: 0; }}
        .pov-table td {{ padding: 8px 10px; border-bottom: 1px solid #eee; }}
        .pov-table tr:hover {{ background: #f9f9f9; }}
        
        #loader {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .spinner {{ width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        
        .map-controls {{ position: absolute; bottom: 20px; right: 20px; display: flex; flex-direction: column; gap: 5px; }}
        .map-btn {{ width: 36px; height: 36px; background: white; border: none; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; color: #555; }}
        .map-btn:hover {{ background: #f0f0f0; }}
        
        #tooltip {{ position: absolute; pointer-events: none; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-radius: 4px; font-size: 0.8rem; display: none; z-index: 100; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid #444; }}

        .help-tip {{ display: inline-block; cursor: help; margin-left: 5px; color: #3498db; font-weight:bold; width:20px; height:20px; text-align:center; line-height:20px; border-radius:50%; background:#eef6fc; border:1px solid #d6eaf8; font-size:12px; }}
        .help-tip:hover {{ background:#3498db; color:white; transform:scale(1.1); transition:0.2s; }}
        
        #statsPopover {{ position: absolute; display: none; background: white; border: 1px solid #ddd; padding: 0; border-radius: 8px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); z-index: 900; width: 300px; max-height: 400px; flex-direction: column; }}
        .pop-header {{ background: #f8f9fa; padding: 10px 15px; border-bottom: 1px solid #eee; font-weight: bold; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; }}
        .pop-body {{ overflow-y: auto; padding: 0; flex: 1; }}
        .pop-table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
        .pop-table th {{ position: sticky; top: 0; background: #eee; padding: 8px; text-align: left; }}
        .pop-table td {{ padding: 6px 8px; border-bottom: 1px solid #f0f0f0; }}
        .pop-table tr:hover {{ background: #f9f9f9; }}
        .pop-close {{ cursor: pointer; color: #999; }}
        .pop-close:hover {{ color: #333; }}
    </style>
</head>
<body>

<div id="loader">
    <div class="spinner"></div>
    <h3 style="margin-top:15px; color:#555">Initialising Engine...</h3>
</div>

<div id="tooltip"></div>
<div id="statsPopover">
    <div class="pop-header">
        <span id="popTitle">Title</span>
        <span class="pop-close" onclick="document.getElementById('statsPopover').style.display='none'">✖</span>
    </div>
    <div class="pop-body">
        <table class="pop-table" id="popTable"></table>
    </div>
</div>

<header>
    <div class="header-title">
        <span>🌳</span> Simulation Engine v8.2
        <span style="font-size:0.8rem; opacity:0.6; font-weight:normal; margin-left:10px">Generated: {timestamp}</span>
    </div>
    <div class="tabs">
        <div class="tab active" onclick="switchTab('map')">🗺️ Interactive Map</div>
        <div class="tab" onclick="switchTab('pov')">📊 Production Analysis</div>
    </div>
</header>

<div class="layout">
    <aside class="sidebar">
        <div class="sidebar-scroll">
            <div class="control-group">
                <h3>📍 Location</h3>
                <label>Division</label>
                <select id="divSelect" onchange="loadDivision()">
                    <!-- Dyn -->
                </select>
                
                <label>Block ID</label>
                <select id="blockSelect" onchange="resetView(); calculateAlgorithm()">
                    <!-- Dyn -->
                </select>
                
                <!-- NEW: TOP 5 RANKINGS -->
                <div id="top5Ranking" style="margin-top:10px; background:#fff5f5; border:1px solid #ffcccc; border-radius:4px; padding:8px;">
                     <h4 style="margin:0 0 5px 0; font-size:0.8rem; color:#c0392b">🚨 Top 5 Critical Hotspots</h4>
                     <div id="top5List" style="font-size:0.8rem"></div>
                </div>
            </div>
            
            <div class="control-group">
                <h3>💰 Financial & Audit</h3>
                
                <div class="financial-card">
                     <span class="fin-label">Ghost Trees (Audit Aset)</span>
                     <div id="val_ghost" class="fin-value">-</div>
                     <span class="help-tip" style="float:right; margin-top:-20px" data-tooltip="GHOST TREES (Hilang)\\n👻 Selisih antara Data Buku vs Deteksi Drone.\\n📉 Total Kerugian Aset = (Buku - Drone) x Nilai per Pokok.">?</span>
                </div>
                
                <div class="financial-card">
                     <span class="fin-label">Sensus Validation</span>
                     <div id="val_sensus" class="fin-value" style="font-size:0.9rem">-</div>
                     <span class="help-tip" style="float:right; margin-top:-20px" data-tooltip="COMPARISON\\n⚖️ Membandingkan % Serangan Sensus Manual vs AI.\\n✅ Hijau: AI Valid / Menemukan infeksi baru.\\n⚠️ Merah: AI Under-detection.">?</span>
                </div>
                
                <div class="financial-card">
                     <span class="fin-label">Est. Treatment Cost</span>
                     <div id="val_cost" class="fin-value" style="color:#e74c3c">-</div>
                </div>

                <div style="display:flex; gap:10px; margin-top:10px">
                    <div style="flex:1">
                        <label style="font-size:0.7rem">Cost/Tree</label>
                        <input type="number" id="cost_per_tree" value="50000" oninput="updateFinancial('cost_per_tree')">
                    </div>
                    <div style="flex:1">
                        <label style="font-size:0.7rem">Asset Val</label>
                        <input type="number" id="asset_value" value="1000000" oninput="updateFinancial('asset_value')">
                    </div>
                </div>
            </div>
            
            <div class="control-group">
                <h3>🎛️ Algorithm Presets</h3>
                <div class="preset-btn-group">
                    <button class="preset-btn" onclick="applyPreset('konservatif')" title="Konservatif">Konservatif</button>
                    <span class="help-tip" data-tooltip="PRESET KONSERVATIF (Si 'Paranoid')\n🛡️ Filosofi: 'Lebih baik salah rawat daripada kecolongan.'\n📉 Ambang Batas: -1.2 (Sangat Sensitif)\n💡 Konsekuensi: Biaya Treatment TINGGI, tapi Aset AMAN. Cocok untuk pembibitan.">?</span>
                    
                    <button class="preset-btn active" onclick="applyPreset('standar')" title="Standar">Standar</button>
                    <span class="help-tip" data-tooltip="PRESET STANDAR (The Elbow)\n⚖️ Filosofi: 'Sesuai Kaidah Statistik.'\n📉 Ambang Batas: -1.5 (Titik Siku)\n💡 Konsekuensi: Memisahkan variasi alami vs penyakit secara matematis. Keseimbangan terbaik.">?</span>

                    <button class="preset-btn" onclick="applyPreset('agresif')" title="Agresif">Agresif</button>
                    <span class="help-tip" data-tooltip="PRESET AGRESIF (Si 'Hemat Biaya')\n💰 Filosofi: 'Hanya rawat yang parah.'\n📉 Ambang Batas: -1.8 (Toleransi Tinggi)\n💡 Konsekuensi: Biaya MURAH, tapi Risiko Penularan TINGGI. Cocok untuk tanaman tua siap replanting.">?</span>
                </div>
            </div>

            <div class="control-group">
                <h3>⚙️ Fine Tuning</h3>
                
                <label>
                    Z-Score Core <span id="val_z_core" class="val-badge">-1.5</span>
                    <span class="help-tip" data-tooltip="Z-SCORE (Skor Penyimpangan)\n📊 Definisi: Seberapa 'aneh' pohon ini dibanding rata-rata blok.\n0 = Normal\n-1 = Agak Stress\n-3 = Sakit Parah\n\nSemakin negatif angka Z-Core, semakin parah syarat untuk dianggap 'Suspect'.">?</span>
                </label>
                <input type="range" id="z_core" min="-3.0" max="0.0" step="0.1" value="-1.5" oninput="updateParam('z_core')">
                
                <label>
                    Z-Score Neighbor <span id="val_z_neighbor" class="val-badge">-1.0</span>
                     <span class="help-tip" data-tooltip="THRESHOLD NEIGHBOR (Penularan)\\n🎛 Fungsi: Batas toleransi pohon tetangga untuk dianggap 'tertular'.\\n💡 Makna: Digunakan untuk memvalidasi apakah ada cluster serangan.\\n⚠️ Jika tetangga < Z-Neighbor, dia dianggap mendukung status MERAH pohon tengah.">?</span>
                </label>
                <input type="range" id="z_neighbor" min="-3.0" max="0.0" step="0.1" value="-1.0" oninput="updateParam('z_neighbor')">
                
                <label>
                    Min Neighbors <span id="val_min" class="val-badge">3</span>
                     <span class="help-tip" data-tooltip="SENSITIVITAS KLUSTER\\n🎛 Fungsi: Jumlah minimal tetangga sakit.\\n💡 Makna: Validasi spasial Cincin Api.\\n🔢 1-2: Mudah jadi Merah\\n🔢 4-6: Susah jadi Merah (butuh bukti kuat)">?</span>
                </label>
                <input type="range" id="min" min="1" max="6" step="1" value="3" oninput="updateParam('min')">
            </div>
        </div>
        
        <!-- INFO PANEL (Fixed Bottom) -->
        <div class="info-panel">
            <h4 style="margin:0 0 10px 0; color:#2980b9; border-bottom:1px solid #ddd; padding-bottom:5px">ℹ️ Explanation Panel</h4>
            <div id="infoPanelContent"></div>
        </div>
    </aside>

    <main class="main-view">
        <div id="mapView" style="display:flex; flex:1; position:relative; overflow:hidden;">
            <div class="canvas-container">
                <canvas id="mainCanvas"></canvas>
            </div>
            
            <div class="map-controls">
                <button class="map-btn" onclick="adjustZoom(1.2)">➕</button>
                <button class="map-btn" onclick="adjustZoom(0.8)">➖</button>
                <button class="map-btn" onclick="resetView()">🏠</button>
            </div>
            
            <!-- Live Stats -->
            <div class="live-stats">
                <h4 style="margin:0 0 10px 0; border-bottom:1px solid #eee; padding-bottom:5px">Live Detection</h4>
                <div class="stat-row" onclick="showDrilldown('MERAH')"><span><span class="dot" style="background:#e74c3c"></span>Merah</span> <strong id="cnt_red">0</strong></div>
                <div class="stat-row" onclick="showDrilldown('ORANYE')"><span><span class="dot" style="background:#e67e22"></span>Oranye</span> <strong id="cnt_org">0</strong></div>
                <div class="stat-row" onclick="showDrilldown('KUNING')"><span><span class="dot" style="background:#f1c40f"></span>Kuning</span> <strong id="cnt_yell">0</strong></div>
                <div class="stat-row" onclick="showDrilldown('HIJAU')"><span><span class="dot" style="background:#2ecc71"></span>Hijau</span> <strong id="cnt_grn">0</strong></div>
                <div style="margin-top:10px; pt-10; border-top:1px solid #eee; font-size:0.8rem; text-align:right">
                    Attack Rate: <strong id="attack_rate" style="color:#e74c3c">0%</strong>
                </div>
                <div style="font-size:0.7rem; color:#999; margin-top:5px; text-align:center">Click rows for details</div>
            </div>
            
            <!-- NEW BLOCK INFO OVERLAY -->
            <div id="blockInfoOverlay" class="block-info-overlay">
                Select a block...
            </div>
        </div>
        
        <!-- POV View -->
        <div id="povView" class="pov-section">
            <div id="povContent">Select a division...</div>
        </div>
    </main>
</div>

<!-- DATA SCRIPT -->
<script>
const DATA = {json.dumps(divisi_json_map)};
const POV_HTML = {json.dumps(pov_tables_html)};
</script>

<!-- LOGIC SCRIPT -->
<script>
{js_logic}
</script>
</body>
</html>
"""
    
    output_path = Path(f'data/output/dashboard_v8_interactive_{timestamp.replace(":", "").replace(" ", "_")}.html')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    return output_path

def main():
    print("🚀 STARTED: Dashboard v8.2 Generation (Cost Control)")
    
    # 0. Load Cost Control Data
    print("   Loading Cost Control Data (Sensus & Assets)...")
    cost_map, norm_func = load_cost_control_data()
    
    # 1. Load Productivity Data
    print("   Loading Productivity Data...")
    prod_df = load_productivity_data()
    
    all_data = {}
    
    # AME II
    print("   Processing AME II...")
    df_ii = load_and_clean_data(Path('data/input/tabelNDREnew.csv'))
    # Pass norm_func
    blocks_ii, pov_ii = analyze_divisi_interactive(df_ii, "AME II", prod_df, cost_map, norm_func)
    all_data["AME II"] = {'blocks_json': blocks_ii, 'pov_data': pov_ii}
    
    # AME IV
    print("   Processing AME IV...")
    df_iv = load_ame_iv_data(Path('data/input/AME_IV.csv'))
    # Pass norm_func
    blocks_iv, pov_iv = analyze_divisi_interactive(df_iv, "AME IV", prod_df, cost_map, norm_func)
    all_data["AME IV"] = {'blocks_json': blocks_iv, 'pov_data': pov_iv}
    
    # Generate HTML
    print("   Generating HTML & JS Engine...")
    path = generate_v8_dashboard(all_data)
    
    print(f"\\n✅ SUCCESS: Dashboard v8.2 created at:\\n   {path}")

if __name__ == '__main__':
    main()
