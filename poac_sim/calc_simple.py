
# ... (Previous constants)
import pandas as pd

HARGA_TBS = 1500000 

blocks = {
    'D006A': {
        'ha': 23.0, 'trees': 2382, 'sph': 104,
        'gap_ton_ha': 16.51, 'core': 37, 'ring': 80, 'suspect': 244
    },
    'D007A': {
        'ha': 24.7, 'trees': 2586, 'sph': 105,
        'gap_ton_ha': 17.23, 'core': 57, 'ring': 107, 'suspect': 200
    }
}

total_loss_divisi = 0
total_ha_divisi = 0

for name, data in blocks.items():
    loss_per_ha = data['gap_ton_ha'] * HARGA_TBS
    loss_total_block = loss_per_ha * data['ha']
    total_loss_divisi += loss_total_block
    total_ha_divisi += data['ha']
    
    # Calc Cost per Tree for Risk Scenarios
    # Loss per tree (approx based on potential gap)
    gap_value_per_ha = data['gap_ton_ha'] * HARGA_TBS
    val_per_tree = gap_value_per_ha / data['sph'] # Valuasi kasar per pohon hilang
    
    cost_std = data['ring'] * val_per_tree
    cost_agg = (data['ring'] + data['suspect']) * val_per_tree

    print(f"BLOCK_{name}_DATA:")
    print(f"  LossTotal: {loss_total_block}")
    print(f"  RiskStd: {cost_std}")
    print(f"  RiskAgg: {cost_agg}")
    
print(f"TOTAL_DIVISI: {total_loss_divisi}")
