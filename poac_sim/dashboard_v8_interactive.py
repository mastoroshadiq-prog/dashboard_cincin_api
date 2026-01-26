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
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import logging
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure path to allow importing local modules
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import modules
from src.ingestion import load_and_clean_data
from config import ZSCORE_PRESETS
try:
    from dashboard_v7_fixed import load_ame_iv_data, load_productivity_data, convert_gano_to_prod_pattern
except ImportError:
    # If failed, try relative import if run from root
    from poac_sim.dashboard_v7_fixed import load_ame_iv_data, load_productivity_data, convert_gano_to_prod_pattern

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
if(typeof DATA === 'undefined' || !DATA) throw new Error("DATA missing");

/* State */
let currentDiv = null;
let currentBlockId = null;

let transform = new Object();
transform.x = 20; transform.y = 20; transform.k = 1;

let isDragging = false;
let startPos = new Object(); 
startPos.x = 0; startPos.y = 0;

let financial = {
    cost_per_tree: 50000,   // Biaya rawat per pohon (Rp)
    asset_value: 1500000,   // Nilai aset per pohon (Rp) - 1.5 Juta
    trench_cost: 15000      // Biaya gali parit per meter (Rp)
};

const PRESETS = {
    'konservatif': { z_core: -1.2, z_neighbor: -0.8, min: 2 },
    'standar':     { z_core: -1.5, z_neighbor: -1.0, min: 3 },
    'agresif':     { z_core: -1.8, z_neighbor: -1.2, min: 4 }
};

let currentConfig = { ...PRESETS['standar'] };
let currentBlockData = null;
let computedTrees = [];
let treeMap = new Map(); // GLOBAL NOW
let hoveredTree = null;

// VIEW STATES
let isGradientMode = false;
let isTrenchMode = false;

let blockDimensions = new Object();

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

// DEBUG: ERROR HANDLER
function showError(msg, stack) {
    const el = document.createElement('div');
    el.style.cssText = "position:fixed; top:10px; left:10px; right:10px; background:#e74c3c; color:white; padding:20px; z-index:9999; font-family:monospace; white-space:pre-wrap; border-radius:8px; box-shadow:0 5px 15px rgba(0,0,0,0.5)";
    el.innerHTML = `<h3>⚠️ DASHBOARD ERROR</h3><strong>${msg}</strong><br><br><small>${stack || ''}</small><br><button onclick="this.parentElement.remove()" style="margin-top:10px; padding:5px 10px; cursor:pointer">DISMISS</button>`;
    document.body.appendChild(el);
    console.error(msg, stack);
}

window.onload = () => {
    try {
        console.log("🚀 Init: Start");
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
            document.querySelector('.loading-overlay').innerHTML = "<h3>NO DATA FOUND</h3>";
        }
        setupHelpTips();
    } catch (e) {
        showError("Init Error: " + e.message, e.stack);
        document.querySelector('.loading-overlay').style.display = 'none';
    }
    
    // Check if initial load failed to render anything
    /*
    setTimeout(() => {
        if(document.querySelector('.loading-overlay').style.display !== 'none') {
             console.warn("Loading stuck?");
        }
    }, 5000);
    */
    
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
    currentBlockData = DATA[currentDiv][currentBlockId]; // Update currentBlockData
    if(!currentBlockData) return;
    
    // UPDATE BLOCK INFO OVERLAY
    document.getElementById('blockInfoOverlay').innerHTML = 
        `<h4 style="margin:0 0 5px 0; color:#2c3e50">Block ${currentBlockId}</h4>` +
        `<div style="font-size:0.85rem; color:#555">` + 
        `Trees Analysed: <b>${currentBlockData.stats.count}</b><br>` +
        `Avg NDRE: <b>${currentBlockData.stats.mean_ndvi}</b><br>` +
        `<span style="color:#888; font-size:0.8rem">Grid: ${currentBlockData.width} x ${currentBlockData.height}</span>` +
        `</div>`;
    
    blockDimensions.w = currentBlockData.width;
    blockDimensions.h = currentBlockData.height;
    
    treeMap.clear(); // Clear global map
    const trees = [];
    
    currentBlockData.trees.forEach(t => {
        const tree = { 
            x: t[0], y: t[1], z: t[2], 
            is_sisip: t[3] === 1,
            orig_x: t[0] + (currentBlockData.min_x || 0), 
            orig_y: t[1] + (currentBlockData.min_y || 0), 
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
    const totalBuku = currentBlockData.stats.total_buku || 0;
    const sensusPct = currentBlockData.stats.sensus_pct || 0;
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
    
    // DRAW TRENCH OVERLAY
    if (isTrenchMode && trenchClusters.length > 0) {
        ctx.save();
        ctx.translate(transform.x, transform.y);
        ctx.scale(transform.k, transform.k);
        
        ctx.lineWidth = 0.15;
        ctx.setLineDash([0.2, 0.2]); // Dashed line
        
        trenchClusters.forEach(c => {
             let minX=Infinity, maxX=-Infinity, minY=Infinity, maxY=-Infinity;
            c.forEach(n => {
                minX = Math.min(minX, n.x);
                maxX = Math.max(maxX, n.x);
                minY = Math.min(minY, n.y);
                maxY = Math.max(maxY, n.y);
            });
            
            // Draw Box with buffer
            // Buffer 0.6 unit around the extremes
            const bx = minX - 0.6;
            const by = minY - 0.6;
            const bw = (maxX - minX) + 1.2;
            const bh = (maxY - minY) + 1.2;
            
            // Black bg line for contrast
            ctx.strokeStyle = '#000000';
            ctx.strokeRect(bx, by, bw, bh);
            
            // Yellow fg line
            ctx.strokeStyle = '#f1c40f';
            ctx.lineDashOffset = 0.2;
            ctx.strokeRect(bx, by, bw, bh);
            
            // Label
            ctx.fillStyle = 'black';
            ctx.font = '0.3px Arial';
            ctx.fillText("TRENCH", bx, by - 0.1);
        });
        
        ctx.restore();
    }
}

function handleTooltip(e) {
    const rect = document.getElementById('mainCanvas').getBoundingClientRect();
    const worldX = (e.clientX - rect.left - transform.x) / transform.k;
    const worldY = (e.clientY - rect.top - transform.k) / transform.k;
    
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

let trenchClusters = [];

function toggleTrenchMode() {
    isTrenchMode = document.getElementById('trenchToggle').checked;
    document.getElementById('trenchStats').style.display = isTrenchMode ? 'block' : 'none';
    if (isTrenchMode) {
        calculateTrenchClusters();
    }
    drawCanvas();
}

function calculateTrenchClusters() {
    if (!currentBlockData) return;
    
    // 1. Identify Target Trees (Red/Orange/Yellow? Usually Red+Orange need isolation)
    // Let's stick to Red (Merah) and Orange (Cluster) as targets
    const targets = computedTrees.filter(t => t.status === 'MERAH' || t.status === 'ORANYE');
    
    // 2. Clustering (Connected Components using Spatial Lookup)
    // Optimized: Use treeMap for O(1) neighbor check instead of O(N^2) loop
    const visited = new Set();
    const clusters = [];
    // Neighbors: 8 directions
    const offsets = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]];
    
    targets.forEach(t => {
        if(visited.has(t)) return;
        
        const cluster = [];
        const queue = [t];
        visited.add(t);
        cluster.push(t);
        
        while(queue.length > 0) {
            const curr = queue.pop();
            
            offsets.forEach(o => {
                const nx = curr.x + o[0];
                const ny = curr.y + o[1];
                const key = nx + ',' + ny;
                const neighbor = treeMap.get(key);
                
                // If neighbor exists, is Red/Orange, and not visited
                if(neighbor && (neighbor.status === 'MERAH' || neighbor.status === 'ORANYE') && !visited.has(neighbor)) {
                    visited.add(neighbor);
                    cluster.push(neighbor);
                    queue.push(neighbor);
                }
            });
        }
        clusters.push(cluster);
    });
    
    trenchClusters = clusters;
    
    // 3. Calculate Cost
    // Assumption: Trench is a box around the cluster + 1 unit buffer
    // 1 Grid Unit approx 9 meters in real life
    const GRID_SCALE_M = 9; 
    let totalPerimeterM = 0;
    
    clusters.forEach(c => {
        let minX=Infinity, maxX=-Infinity, minY=Infinity, maxY=-Infinity;
        c.forEach(n => {
            minX = Math.min(minX, n.x);
            maxX = Math.max(maxX, n.x);
            minY = Math.min(minY, n.y);
            maxY = Math.max(maxY, n.y);
        });
        
        // Add buffer 1 unit
        const width = (maxX - minX + 2) * GRID_SCALE_M;
        const height = (maxY - minY + 2) * GRID_SCALE_M;
        
        const perimeter = 2 * (width + height);
        totalPerimeterM += perimeter;
    });
    
    const estCost = totalPerimeterM * financial.trench_cost;
    
    document.getElementById('val_trench_len').innerText = `${totalPerimeterM.toLocaleString()} m`;
    document.getElementById('val_trench_cost').innerText = `Rp ${estCost.toLocaleString('id-ID')}`;
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

    # --- WRITE HTML SAFELY (Avoid f-string for large JS/CSS blocks) ---
    try:
        # Create Output Path
        output_path = Path(f'data/output/dashboard_v8_interactive_{timestamp.replace(":", "").replace(" ", "_")}.html')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # 1. HEADER & CSS
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>POAC v8.2 Cost Control</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #f4f6f9; display: flex; flex-direction: column; height: 100vh; }}
        header {{ background: #2c3e50; color: white; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ margin: 0; font-size: 1.2rem; font-weight: 600; letter-spacing: 0.5px; }}
        .header-controls {{ display: flex; gap: 15px; align-items: center; }}
        
        /* LAYOUT */
        .main-container {{ display: flex; flex: 1; overflow: hidden; }}
        
        /* SIDEBAR (Controls) */
        .sidebar {{ width: 320px; background: white; border-right: 1px solid #ddd; display: flex; flex-direction: column; overflow-y: auto; z-index: 10; }}
        .sidebar-header {{ padding: 15px; border-bottom: 1px solid #eee; background: #f8f9fa; }}
        .sidebar-content {{ padding: 15px; flex: 1; }}
        
        .control-group {{ margin-bottom: 20px; border-bottom: 1px solid #f0f0f0; padding-bottom: 15px; }}
        .control-group:last-child {{ border-bottom: none; }}
        .control-group h3 {{ margin: 0 0 10px 0; font-size: 0.9rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }}
        
        label {{ display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: #2c3e50; }}
        select, input[type=number], input[type=range] {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 0.9rem; }}
        input[type=range] {{ margin-top: 5px; }}
        
        /* PRESET BUTTONS */
        .preset-btn-group {{ display: flex; gap: 5px; margin-bottom: 10px; flex-wrap: wrap; }}
        .preset-btn {{ flex: 1; padding: 6px 10px; border: 1px solid #3498db; background: white; color: #3498db; border-radius: 4px; cursor: pointer; font-size: 0.8rem; transition: all 0.2s; white-space: nowrap; }}
        .preset-btn:hover {{ background: #ebf5fb; }}
        .preset-btn.active {{ background: #3498db; color: white; }}
        
        /* MAP AREA */
        .map-area {{ flex: 1; position: relative; background: #eef2f7; overflow: hidden; cursor: grab; }}
        .map-area:active {{ cursor: grabbing; }}
        .canvas-container {{ width: 100%; height: 100%; }}
        
        /* OVERLAYS */
        .loading-overlay {{ position: absolute; top:0; left:0; right:0; bottom:0; background: rgba(255,255,255,0.9); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 1000; }}
        .block-info-overlay {{ position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); pointer-events: none; font-size: 0.9rem; }}
        
        /* LEGEND */
        .legend {{ position: absolute; bottom: 20px; right: 20px; background: white; padding: 10px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-size: 0.8rem; pointer-events: none; }}
        .legend-item {{ display: flex; align-items: center; margin-bottom: 4px; }}
        .legend-color {{ width: 12px; height: 12px; margin-right: 8px; border-radius: 2px; }}
        
        /* STATS BADGES */
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }}
        .stat-card {{ background: #f8f9fa; padding: 8px; border-radius: 4px; text-align: center; border: 1px solid #eee; }}
        .stat-val {{ font-size: 1.1rem; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 0.7rem; color: #7f8c8d; }}
        
        /* FINANCIAL CARDS */
        .financial-card {{ background: #fff; border: 1px solid #e0e0e0; border-left: 4px solid #3498db; padding: 10px; margin-bottom: 8px; border-radius: 0 4px 4px 0; }}
        .fin-label {{ display: block; font-size: 0.75rem; color: #7f8c8d; text-transform: uppercase; }}
        .fin-value {{ font-size: 1.0rem; font-weight: bold; color: #2c3e50; margin-top: 2px; }}
        
        /* TOOLTIPS */
        .tooltip {{ position: absolute; background: rgba(0,0,0,0.85); color: white; padding: 8px 12px; border-radius: 4px; font-size: 0.8rem; pointer-events: none; display: none; z-index: 1001; white-space: nowrap; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        
        /* POV TABLE Styles */
        .pov-table {{ width:100%; border-collapse: collapse; font-size: 0.8rem; }}
        .pov-table th {{ background: #ecf0f1; padding: 6px; text-align: left; border-bottom: 2px solid #ddd; }}
        .pov-table td {{ padding: 6px; border-bottom: 1px solid #eee; }}
        .pov-table tr:hover {{ background: #f5f6fa; }}
        
        /* TABS */
        .tab-buttons {{ display: flex; border-bottom: 1px solid #ddd; }}
        .tab-btn {{ flex: 1; padding: 10px; border: none; background: none; cursor: pointer; font-weight: 600; color: #7f8c8d; border-bottom: 3px solid transparent; }}
        .tab-btn.active {{ color: #3498db; border-bottom-color: #3498db; }}
        
        .tab-content {{ display: none; padding: 15px; overflow-y: auto; height: 100%; }}
        .tab-content.active {{ display: block; }}
        
        .val-badge {{ background:#eee; padding:2px 6px; border-radius:10px; font-size:0.75rem; font-weight:bold }}
        
        /* HELP TIP (?) */
        .help-tip {{
            display: inline-block; width: 16px; height: 16px; background: #95a5a6; color: white;
            border-radius: 50%; text-align: center; line-height: 16px; font-size: 11px;
            cursor: help; margin-left: 5px;
        }}
        .help-tip:hover {{ background: #3498db; }}
        
        #infoPanel {{ height: 150px; background: white; border-top: 1px solid #ccc; padding: 15px; font-size: 0.9rem; overflow-y: auto; line-height: 1.5; }}
        
        /* POPOVER */
        #statsPopover {{ position: absolute; display: none; background: white; border: 1px solid #ddd; padding: 0; border-radius: 8px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); z-index: 900; width: 300px; max-height: 400px; flex-direction: column; }}
        .pop-header {{ background: #f8f9fa; padding: 10px 15px; border-bottom: 1px solid #eee; font-weight: bold; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; }}
        .pop-body {{ overflow-y: auto; padding: 0; flex: 1; }}
        .pop-table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
        .pop-table th {{ position: sticky; top: 0; background: #eee; padding: 8px; text-align: left; }}
        .pop-table td {{ padding: 6px 8px; border-bottom: 1px solid #f0f0f0; }}
        .pop-table tr:hover {{ background: #f9f9f9; }}
        .pop-close {{ cursor: pointer; color: #999; }}
        .pop-close:hover {{ color: #333; }}

        /* Toggle Switch Styles */
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 40px;
            height: 20px;
        }}
        .toggle-switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}
        .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            -webkit-transition: .4s;
            transition: .4s;
        }}
        .slider:before {{
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            -webkit-transition: .4s;
            transition: .4s;
        }}
        input:checked + .slider {{
            background-color: #2196F3;
        }}
        input:focus + .slider {{
            box-shadow: 0 0 1px #2196F3;
        }}
        input:checked + .slider:before {{
            -webkit-transform: translateX(20px);
            -ms-transform: translateX(20px);
            transform: translateX(20px);
        }}
        /* Rounded sliders */
        .slider.round {{
            border-radius: 20px;
        }}
        .slider.round:before {{
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div id="loader" class="loading-overlay">
        <div style="font-size: 2rem; margin-bottom: 10px;">🤖</div>
        <div>Initializing Cincin Api Engine v8.2...</div>
        <div style="font-size:0.8rem; color:#777; margin-top:5px">Simulating Cost Control & Neural Analysis</div>
    </div>

    <!-- HEADER -->
    <header>
        <div class="header-controls">
            <h1>POAC Cincin Api v8.2</h1>
            <span style="background:rgba(255,255,255,0.2); pad:2px 8px; border-radius:4px; font-size:0.8rem">Interactive Cost Control & Audit</span>
        </div>
        <div style="font-size:0.9rem">
            <b>Divisi:</b> <select id="divSelect" style="width:150px; margin-left:10px; color:black"></select>
        </div>
    </header>

    <div class="main-container">
        <!-- SIDEBAR -->
        <div class="sidebar">
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="switchTab('controls')">Controls</button>
                <button class="tab-btn" onclick="switchTab('pov')">Production Analysis</button>
            </div>
            
            <!-- CONTROLS TAB -->
            <div id="tab-controls" class="tab-content active">
                <div class="control-group">
                    <h3>📍 Navigation</h3>
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
                    <h3>🛠️ Action Plan</h3>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px">
                        <label style="margin:0">Trench Planner</label>
                        <label class="toggle-switch">
                            <input type="checkbox" id="trenchToggle" onchange="toggleTrenchMode()">
                            <span class="slider round"></span>
                        </label>
                    </div>
                    
                    <div id="trenchStats" style="display:none; background:#eee; padding:8px; border-radius:4px; font-size:0.85rem">
                        <div style="display:flex; justify-content:space-between">
                            <span>Panjang Parit:</span>
                            <strong id="val_trench_len">0 m</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:5px">
                            <span>Est. Biaya:</span>
                            <strong id="val_trench_cost" style="color:#d35400">Rp 0</strong>
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <h3>💰 Financial Impact</h3>
                    
                    <div class="financial-card">
                        <span class="fin-label">Ghost Trees (Audit Aset)</span>
                        <div id="val_ghost" class="fin-value">-</div>
                    </div>
                    
                    <div class="financial-card">
                        <span class="fin-label">Sensus Validation</span>
                        <div id="val_sensus" class="fin-value">-</div>
                    </div>
                    
                    <div class="financial-card">
                        <span class="fin-label">Est. Treatment Cost</span>
                        <div id="val_cost" class="fin-value" style="color:#e67e22">-</div>
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
                        <span class="help-tip" data-tooltip="Z-NEIGHBOR (Syarat Tetangga)\n🏡 Fungsi: Filter noise.\nHanya jika tetangganya JUGA punya skor di bawah ini, baru dianggap valid.\nMencegah 'False Alarm' dari satu pohon aneh sendirian.">?</span>
                    </label>
                    <input type="range" id="z_neighbor" min="-3.0" max="0.0" step="0.1" value="-1.0" oninput="updateParam('z_neighbor')">
                    
                    <label>
                        Min Neighbors <span id="val_min" class="val-badge">3</span>
                        <span class="help-tip" data-tooltip="MINIMUM CLUSTER\n👨‍👩‍👧‍👦 Fungsi: Konfirmasi masa.\nBerapa banyak tetangga 'sakit' yang dibutuhkan untuk memvonis Merah?\n3 = Butuh 3 teman sakit\n1 = Sangat sensitif">?</span>
                    </label>
                    <input type="range" id="min" min="1" max="8" step="1" value="3" oninput="updateParam('min')">
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card" style="border-bottom:3px solid #e74c3c">
                        <span class="stat-val" id="cnt_red" style="color:#e74c3c">0</span>
                        <span class="stat-label">Merah</span>
                    </div>
                    <div class="stat-card" style="border-bottom:3px solid #e67e22">
                        <span class="stat-val" id="cnt_org" style="color:#e67e22">0</span>
                        <span class="stat-label">Oranye</span>
                    </div>
                    <div class="stat-card" style="border-bottom:3px solid #f1c40f">
                        <span class="stat-val" id="cnt_yell" style="color:#f1c40f">0</span>
                        <span class="stat-label">Kuning</span>
                    </div>
                    <div class="stat-card" style="border-bottom:3px solid #2ecc71">
                        <span class="stat-val" id="cnt_grn" style="color:#2ecc71">0</span>
                        <span class="stat-label">Hijau</span>
                    </div>
                </div>
                
                <div style="margin-top:10px; text-align:center; padding:10px; background:#e8f8f5; border:1px solid #d1f2eb; border-radius:4px">
                    <span style="font-size:0.8rem; color:#555">Est. Attack Rate</span>
                    <div id="attack_rate" style="font-size:1.5rem; font-weight:bold; color:#16a085">0.0%</div>
                </div>
            </div>
            
            <!-- POV TAB -->
            <div id="tab-pov" class="tab-content">
                <h3 style="margin-top:0">Production vs Health Analysis</h3>
                <div style="font-size:0.8rem; color:#666; margin-bottom:10px">
                    Comparing SPH, Yield, and Gap with Attack Rate (Cincin Api).
                </div>
                <div id="povContent">
                    Select a Division to view data.
                </div>
            </div>
            
        </div>
        
        <!-- MAP AREA -->
        <div class="map-area" id="mapArea">
            <div class="block-info-overlay" id="blockInfoOverlay">
                <!-- Info block -->
            </div>
            
            <div class="canvas-container">
                <canvas id="mainCanvas"></canvas>
            </div>
            
            <div class="legend">
                <div class="legend-item"><div class="legend-color" style="background:#e74c3c"></div><b>Merah:</b> High Confidence Infection</div>
                <div class="legend-item"><div class="legend-color" style="background:#e67e22"></div><b>Oranye:</b> Secondary Infection (Ring)</div>
                <div class="legend-item"><div class="legend-color" style="background:#f1c40f"></div><b>Kuning:</b> Early Stress / Suspect</div>
                <div class="legend-item"><div class="legend-color" style="background:#2ecc71"></div><b>Hijau:</b> Healthy</div>
                <div class="legend-item" style="margin-top:5px; border-top:1px solid #ccc; padding-top:5px">
                    <div style="width:10px; height:10px; border-radius:50%; background:white; border:2px solid #555; margin-right:8px"></div><b>Titik Putih:</b> Sisip (Replant)
                </div>
                <div class="legend-item">
                    <div style="width:15px; height:0; border-top:2px dashed #f1c40f; border-bottom:1px solid black; margin-right:5px"></div><b>Kotak Kuning:</b> Rencana Parit Isolas
                </div>
            </div>
            
            <!-- TOOLTIP -->
            <div id="tooltip" class="tooltip"></div>
            
             <!-- POPOVER STATS -->
            <div id="statsPopover">
                <div class="pop-header">
                    <span>Cluster Analysis</span>
                    <span class="pop-close" onclick="document.getElementById('statsPopover').style.display='none'">×</span>
                </div>
                <div class="pop-body">
                    <table class="pop-table" id="popTable">
                        <!-- Ajax content -->
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <!-- INFO PANEL BOTTOM -->
    <div id="infoPanel">
        <div id="infoPanelContent"></div>
    </div>

""")
            
            # 1b. INJECT ERROR HANDLER (Raw string to avoid f-string escaping issues)
            f.write(r"""
    <!-- ERROR HANDLER (Isolated to catch parse errors in main logic) -->
    <script>
    window.onerror = function(message, source, lineno, colno, error) {
        const loader = document.getElementById('loader');
        if(loader) {
            loader.innerHTML = `
                <div style="padding:20px; text-align:center; color:#c0392b; background:white; height:100vh; display:flex; flex-direction:column; justify-content:center">
                    <h2>⚠️ Dashboard Crash</h2>
                    <p style="font-size:1.2rem"><strong>${message}</strong></p>
                    <div style="background:#eee; padding:15px; text-align:left; margin:20px auto; width:80%; max-width:800px; border-radius:8px; overflow:auto; font-family:monospace">
                        <div style="margin-bottom:5px; color:#555">Location: ${source}:${lineno}:${colno}</div>
                        <pre style="margin:0; color:#c0392b">${error ? error.stack : 'No stacktrace'}</pre>
                    </div>
                </div>
            `;
            loader.style.zIndex = '99999';
        }
        console.error("FATAL:", message, error);
    };
    </script>
""")
            
            # 2. INJECT DATA (Separate Blocks)
            f.write(f"<script>const DATA = {json.dumps(divisi_json_map)};</script>\n")
            f.write(f"<script>const POV_HTML = {json.dumps(pov_tables_html)};</script>\n")
            
            # 3. WRITE MAIN JS ENGINE (Separate Block)
            f.write("<script>\n")
            f.write(js_logic)
            f.write("\n</script>\n")
            
            # 4. CLOSE HTML
            f.write("""
</body>
</html>
""")
            
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        return None

    print(f"Dashboard generated: {output_path}")
    
    return output_path



# -----------------------------------------------------------------------------
# 3. LOCAL OVERRIDES (Fixing Missing Data Issues)
# -----------------------------------------------------------------------------

def load_productivity_data():
    """
    Load productivity data from Realisasi vs Potensi PT SR.xlsx (Robust Dynamic Header Search)
    """
    candidates = [
        Path('data/input/Realisasi vs Potensi PT SR.xlsx'),
        Path('data/input/data_gabungan.xlsx')
    ]
    file_path = None
    for p in candidates:
        if p.exists():
            file_path = p
            break
            
    if not file_path:
        logging.warning("⚠️ Productivity data file not found.")
        return pd.DataFrame()
    
    print(f"   Using productivity file: {file_path}")
    
    try:
        # Read header area to find structure
        df_header = pd.read_excel(file_path, header=None, nrows=15)
        
        # 1. Find BLOK, Ha, TT (Tahun Tanam), and DIVISI (Estate) columns
        blok_col_idx = -1
        luas_col_idx = -1
        tt_col_idx = -1
        div_col_idx = -1 # Estate/Divisi
        header_row_idx = -1
        
        for r in range(len(df_header)):
            row_vals = df_header.iloc[r].astype(str).str.upper().tolist()
            if 'BLOK' in row_vals:
                header_row_idx = r
                blok_col_idx = row_vals.index('BLOK')
                
                # Find Ha
                indices = [i for i, x in enumerate(row_vals) if 'HA' == x or 'LUAS' in x]
                if indices: luas_col_idx = indices[0]
                
                # Find TT
                indices_tt = [i for i, x in enumerate(row_vals) if 'TT' == x or 'TAHUN' in x]
                if indices_tt: tt_col_idx = indices_tt[0]
                
                # Find Divisi/Estate
                indices_div = [i for i, x in enumerate(row_vals) if 'ESTATE' in x or 'KEBUN' in x or 'DIVISI' in x]
                if indices_div: div_col_idx = indices_div[0]
                else: div_col_idx = 0 # Default to 1st col if not found
                
                break
        
        if blok_col_idx == -1:
            logging.warning("⚠️ Could not find 'BLOK' column header in prod file.")
            return pd.DataFrame()

        # 2. Find Production (Ton) and Potensi (Ton) Columns
        prod_col_idx = -1
        pot_col_idx = -1
        target_year = "2023" # Default
        
        row_years = df_header.iloc[header_row_idx].astype(str).tolist()
        year_start_col = -1
        if "2024" in row_years: 
            target_year = "2024"; year_start_col = row_years.index("2024")
        elif "2023" in row_years:
            target_year = "2023"; year_start_col = row_years.index("2023")
            
        if year_start_col != -1:
             row_type = df_header.iloc[header_row_idx+1].astype(str).str.upper().tolist()
             row_unit = df_header.iloc[header_row_idx+2].astype(str).str.upper().tolist()
             
             for c in range(year_start_col, min(year_start_col+20, len(row_type))):
                typ = row_type[c]; unit = row_unit[c]
                if 'REAL' in typ and 'TON' in unit and prod_col_idx == -1: prod_col_idx = c
                if 'POTENSI' in typ and 'TON' in unit and 'REAL' not in typ and pot_col_idx == -1: pot_col_idx = c

        # 3. Load FULL Data safely
        data_start_row = header_row_idx + 3
        df = pd.read_excel(file_path, header=None, skiprows=data_start_row)
        
        extracted = pd.DataFrame()
        extracted['Blok_Prod'] = df.iloc[:, blok_col_idx]
        extracted['Divisi_Prod'] = df.iloc[:, div_col_idx] if div_col_idx != -1 else 'Unknown'
        extracted['Luas_Ha'] = df.iloc[:, luas_col_idx] if luas_col_idx != -1 else 0
        extracted['Tahun_Tanam'] = df.iloc[:, tt_col_idx] if tt_col_idx != -1 else 0
        extracted['Produksi_Ton'] = df.iloc[:, prod_col_idx] if prod_col_idx != -1 else 0
        extracted['Potensi_Prod_Ton'] = df.iloc[:, pot_col_idx] if pot_col_idx != -1 else 0
        
        df = extracted
        
        # Stringify Block for matching
        if 'Blok_Prod' in df.columns:
            df['Blok_Prod'] = df['Blok_Prod'].astype(str).str.strip().str.upper()
            # Drop invalid blocks
            df = df[df['Blok_Prod'].apply(lambda x: len(x) > 1 and x != 'NAN')]

        # Ensure numeric
        for col in ['Luas_Ha', 'Produksi_Ton', 'Potensi_Prod_Ton', 'Tahun_Tanam']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Age
        current_year = datetime.now().year
        df['Umur_Tahun'] = current_year - df['Tahun_Tanam']
        
        # Metrics
        df['Yield_Realisasi'] = df['Produksi_Ton'] / df['Luas_Ha']
        df['Potensi_Yield'] = df['Potensi_Prod_Ton'] / df['Luas_Ha']
        # Replace INF
        df['Yield_Realisasi'] = df['Yield_Realisasi'].replace([np.inf, -np.inf], 0)
        df['Potensi_Yield'] = df['Potensi_Yield'].replace([np.inf, -np.inf], 0)
        
        df['Gap_Yield'] = df['Potensi_Yield'] - df['Yield_Realisasi']
        
        # Aliases
        df['Yield_TonHa'] = df['Yield_Realisasi']

        # Filter valid
        df_clean = df[df['Luas_Ha'] > 0]
        
        return df_clean
        
    except Exception as e:
        logging.error(f"❌ Error loading productivity data: {e}")
        return pd.DataFrame()


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
