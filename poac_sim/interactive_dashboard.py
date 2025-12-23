"""
Interactive Z-Score + Cincin Api Dashboard
Real-time recalculation using HTML5 Canvas & JavaScript
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import sys

# Import loading function from fixed v7 dashboard
sys.path.insert(0, '.')
from dashboard_v7_fixed import load_ame_iv_data, load_and_clean_data

def prepare_interactive_data(df, divisi_name):
    """
    Convert DataFrame to optimized JSON structure for JavaScript.
    Structure: { block_id: { width: w, height: h, trees: [x, y, ndvi] } }
    """
    blocks = {}
    
    # Group by block
    for blok, group in df.groupby('Blok'):
        # Normalize coordinates to 0-based for canvas
        min_x = group['N_POKOK'].min()
        min_y = group['N_BARIS'].min()
        max_x = group['N_POKOK'].max()
        max_y = group['N_BARIS'].max()
        
        width = int(max_x - min_x + 1)
        height = int(max_y - min_y + 1)
        
        # Calculate block stats
        mean_ndvi = group['NDRE125'].mean()
        std_ndvi = group['NDRE125'].std()
        
        # Parse tree data: [x, y, ndvi]
        # Store as simple array to save space
        trees = []
        for _, row in group.iterrows():
            x = int(row['N_POKOK'] - min_x)
            y = int(row['N_BARIS'] - min_y)
            ndvi = round(row['NDRE125'], 3)
            # Pre-calculate z-score (based on static mean) 
            # OR pass raw NDVI and calculate dynamic mean/std in JS?
            # Let's pass pre-calculated Z-Score to keep consistent with Python logic
            z_score = round((ndvi - mean_ndvi) / std_ndvi, 2) if std_ndvi > 0 else 0
            
            trees.append([x, y, z_score])
            
        blocks[blok] = {
            'width': width,
            'height': height,
            'stats': {
                'count': len(trees),
                'mean_ndvi': round(mean_ndvi, 3),
                'std_ndvi': round(std_ndvi, 3)
            },
            'trees': trees
        }
        
    return blocks

def generate_interactive_dashboard():
    # Load AME IV Data (Corrected)
    print("Loading AME IV Data...")
    df = load_ame_iv_data(Path('data/input/AME_IV.csv'))
    
    # Prepare data
    print("Preparing JSON data...")
    block_data = prepare_interactive_data(df, 'AME_IV')
    
    # HTML Template
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Cincin Api Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
        .container {{ display: flex; gap: 20px; }}
        .sidebar {{ width: 300px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: fit-content; }}
        .main-content {{ flex: 1; }}
        
        .control-group {{ margin-bottom: 20px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; color: #555; }}
        input[type=range] {{ width: 100%; }}
        .val-display {{ float: right; color: #2980b9; font-weight: bold; }}
        
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        
        canvas {{ background: #f9f9f9; border: 1px solid #eee; border-radius: 4px; cursor: crosshair; }}
        
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; margin-top: 10px; }}
        .stat-box {{ padding: 10px; border-radius: 8px; font-weight: bold; color: white; }}
        .stat-red {{ background: #e74c3c; }}
        .stat-orange {{ background: #e67e22; }}
        .stat-yellow {{ background: #f1c40f; color: #333; }}
        .stat-green {{ background: #27ae60; }}
        
        select {{ width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 10px; }}
        
        .loading {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.8); display: flex; align-items: center; justify-content: center; z-index: 1000; }}
    </style>
</head>
<body>

<div id="loading" class="loading">Loading Data...</div>

<div class="container">
    <div class="sidebar">
        <h2>🛠️ Controls</h2>
        
        <div class="control-group">
            <label>Select Block</label>
            <select id="blockSelect" onchange="renderBlock()"></select>
        </div>
        
        <div class="control-group">
            <label>Preset Strategy</label>
            <select id="presetSelect" onchange="applyPreset()">
                <option value="custom">Custom</option>
                <option value="konservatif">Konservatif</option>
                <option value="standar" selected>Standar</option>
                <option value="agresif">Agresif</option>
            </select>
        </div>

        <hr>

        <div class="control-group">
            <label>Z-Score Core <span id="val_z_core" class="val-display">-1.5</span></label>
            <input type="range" id="z_core" min="-3.0" max="0.0" step="0.1" value="-1.5" oninput="updateConfig()">
            <small>Threshold for initial suspect detection</small>
        </div>

        <div class="control-group">
            <label>Z-Score Neighbor <span id="val_z_neighbor" class="val-display">-1.0</span></label>
            <input type="range" id="z_neighbor" min="-3.0" max="0.0" step="0.1" value="-1.0" oninput="updateConfig()">
            <small>Threshold for infected neighbors</small>
        </div>

        <div class="control-group">
            <label>Min Neighbors <span id="val_min_neighbor" class="val-display">3</span></label>
            <input type="range" id="min_neighbor" min="1" max="6" step="1" value="3" oninput="updateConfig()">
            <small>Min infected neighbors to form Red cluster</small>
        </div>
        
        <div class="card">
            <h3>📊 Block Stats</h3>
            <div id="blockStatsInfo">Select a block</div>
        </div>
    </div>

    <div class="main-content">
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 id="chartTitle">Cluster Map</h2>
                <div id="processTime" style="color:#999; font-size:12px;"></div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-box stat-red">🔴 <span id="count_red">0</span></div>
                <div class="stat-box stat-orange">🟠 <span id="count_orange">0</span></div>
                <div class="stat-box stat-yellow">🟡 <span id="count_yellow">0</span></div>
                <div class="stat-box stat-green">🟢 <span id="count_green">0</span></div>
            </div>
            
            <div style="margin-top: 20px; overflow: auto; text-align: center;">
                <canvas id="clusterMap"></canvas>
            </div>
        </div>
    </div>
</div>

<script>
    // Embedded Data
    const BLOCKS = {json.dumps(block_data)};
    
    // Presets Config
    const PRESETS = {{
        'konservatif': {{ z_core: -1.2, z_neighbor: -0.8, min: 2 }},
        'standar': {{ z_core: -1.5, z_neighbor: -1.0, min: 3 }},
        'agresif': {{ z_core: -1.8, z_neighbor: -1.2, min: 4 }}
    }};

    // Current Config
    let config = {{ z_core: -1.5, z_neighbor: -1.0, min: 3 }};
    let currentBlockId = null;

    // Initialize
    window.onload = function() {{
        const select = document.getElementById('blockSelect');
        const blockIds = Object.keys(BLOCKS).sort();
        
        blockIds.forEach(id => {{
            const opt = document.createElement('option');
            opt.value = id;
            opt.textContent = id + ' (' + BLOCKS[id].stats.count + ' trees)';
            select.appendChild(opt);
        }});
        
        // Select first block
        if(blockIds.length > 0) {{
            select.value = blockIds[0];
        }}
        
        document.getElementById('loading').style.display = 'none';
        applyPreset(); // Initial render
    }};

    function applyPreset() {{
        const p = document.getElementById('presetSelect').value;
        if(p !== 'custom') {{
            const c = PRESETS[p];
            document.getElementById('z_core').value = c.z_core;
            document.getElementById('z_neighbor').value = c.z_neighbor;
            document.getElementById('min_neighbor').value = c.min;
            updateConfig();
        }}
    }}

    function updateConfig() {{
        config.z_core = parseFloat(document.getElementById('z_core').value);
        config.z_neighbor = parseFloat(document.getElementById('z_neighbor').value);
        config.min = parseInt(document.getElementById('min_neighbor').value);
        
        document.getElementById('val_z_core').textContent = config.z_core.toFixed(1);
        document.getElementById('val_z_neighbor').textContent = config.z_neighbor.toFixed(1);
        document.getElementById('val_min_neighbor').textContent = config.min;
        
        // Check if matches preset
        let match = 'custom';
        for(const k in PRESETS) {{
            const p = PRESETS[k];
            if(p.z_core === config.z_core && p.z_neighbor === config.z_neighbor && p.min === config.min) {{
                match = k;
            }}
        }}
        document.getElementById('presetSelect').value = match;
        
        renderBlock();
    }}

    function renderBlock() {{
        const t0 = performance.now();
        currentBlockId = document.getElementById('blockSelect').value;
        const blockData = BLOCKS[currentBlockId];
        if(!blockData) return;
        
        const canvas = document.getElementById('clusterMap');
        const ctx = canvas.getContext('2d');
        
        // Setup Canvas Size
        // Scale factor for visibility
        const SCALE = 7; 
        canvas.width = blockData.width * SCALE;
        canvas.height = blockData.height * SCALE;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 1. Process Data (Algorithm Logic)
        const treeMap = new Map(); // Key: "x,y", Value: tree object
        const trees = [];
        
        // Step 1: Initialize trees and map
        blockData.trees.forEach(t => {{
            const tree = {{
                x: t[0],
                y: t[1],
                z: t[2],
                status: 'HIJAU', // Default
                neighbors_score: 0
            }};
            trees.push(tree);
            treeMap.set(tree.x + "," + tree.y, tree);
        }});
        
        // Step 2: Identify Initial Suspects
        const suspects = [];
        trees.forEach(tree => {{
            if (tree.z < config.z_core) {{
                tree.status = 'SUSPECT';
                suspects.push(tree);
            }}
        }});
        
        // Step 3 & 4: Check Neighbors & Classify Clusters
        const clusters = []; // List of RED trees
        
        suspects.forEach(tree => {{
            let stressed_neighbors = 0;
            // Check 6 directions (hexagonal approximation or simply grid 8-neighbors)
            // Cincin api logic uses specific neighbor coordinates.
            // Simplified: Within radius 1.5
            
            // Standard Mata Lima / Hex neighbors offsets
            // Assuming simplified grid check for interactive demo speed
            const offsets = [
                [0,1], [0,-1], [1,0], [-1,0],
                [1,1], [1,-1], [-1,1], [-1,-1]
            ];
            
            offsets.forEach(off => {{
                const nx = tree.x + off[0];
                const ny = tree.y + off[1];
                const neighbor = treeMap.get(nx + "," + ny);
                
                if (neighbor && neighbor.z < config.z_neighbor) {{
                    stressed_neighbors++;
                }}
            }});
            
            if (stressed_neighbors >= config.min) {{
                tree.status = 'MERAH';
                clusters.push(tree);
            }} else {{
                tree.status = 'KUNING';
            }}
        }});
        
        // Step 5: Ring of Fire (Oranye)
        clusters.forEach(center => {{
            const offsets = [
                [0,1], [0,-1], [1,0], [-1,0],
                [1,1], [1,-1], [-1,1], [-1,-1]
            ];
            
            offsets.forEach(off => {{
                const nx = center.x + off[0];
                const ny = center.y + off[1];
                const neighbor = treeMap.get(nx + "," + ny);
                
                if (neighbor && neighbor.status !== 'MERAH') {{
                    neighbor.status = 'ORANYE';
                }}
            }});
        }});
        
        // 2. Render to Canvas
        let counts = {{ MERAH: 0, ORANYE: 0, KUNING: 0, HIJAU: 0 }};
        
        trees.forEach(tree => {{
            counts[tree.status]++;
            
            const px = tree.x * SCALE + (SCALE/2);
            const py = tree.y * SCALE + (SCALE/2);
            
            ctx.beginPath();
            ctx.arc(px, py, SCALE/2.5, 0, 2 * Math.PI);
            
            if (tree.status === 'MERAH') ctx.fillStyle = '#e74c3c';
            else if (tree.status === 'ORANYE') ctx.fillStyle = '#e67e22';
            else if (tree.status === 'KUNING') ctx.fillStyle = '#f1c40f';
            else ctx.fillStyle = '#2ecc71'; // Hijau
            
            ctx.fill();
        }});
        
        // 3. Update Stats
        document.getElementById('count_red').textContent = counts.MERAH;
        document.getElementById('count_orange').textContent = counts.ORANYE;
        document.getElementById('count_yellow').textContent = counts.KUNING;
        document.getElementById('count_green').textContent = counts.HIJAU;
        
        document.getElementById('blockStatsInfo').innerHTML = 
            'Total Trees: ' + trees.length + '<br>' +
            'Avg NDRE: ' + blockData.stats.mean_ndvi + '<br>' +
            'Attack Rate: ' + ((counts.MERAH + counts.ORANYE)/trees.length*100).toFixed(1) + '%';
            
        document.getElementById('chartTitle').textContent = 'Cluster Map: ' + currentBlockId;
        
        const t1 = performance.now();
        document.getElementById('processTime').textContent = 'Processed in ' + (t1 - t0).toFixed(1) + 'ms';
    }}
</script>

</body>
</html>
    '''
    
    # Save output
    output_path = Path('data/output/interactive_dashboard.html')
    output_path = output_path.resolve()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"✅ Dashboard generated at: {output_path}")
    return output_path

if __name__ == '__main__':
    generate_interactive_dashboard()
