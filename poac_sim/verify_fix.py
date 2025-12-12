"""Verify ground truth data is being used correctly"""
import pandas as pd

# Check Ghost Tree Audit
print("="*70)
print("VERIFICATION: Ground Truth Data")
print("="*70)

df_ghost = pd.read_csv('data/output/ghost_tree_audit/ghost_tree_audit.csv')

print("\nGhost Tree Audit - Summary per Divisi:")
for div in df_ghost['divisi'].unique():
    d = df_ghost[df_ghost['divisi']==div]
    book = d['book_count'].sum()
    drone = d['drone_count'].sum()
    ghost = d['ghost_trees'].sum()
    print(f"\n{div}:")
    print(f"  Book (Ground Truth): {book:>12,}")
    print(f"  Drone:               {drone:>12,}")
    print(f"  Selisih:             {ghost:>+12,}")
