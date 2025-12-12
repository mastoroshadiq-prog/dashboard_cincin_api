"""Quick check for AME IV data discrepancy"""
from src.cost_control_loader import load_cost_control_data, get_book_count_dict, normalize_block
from src.ingestion import load_ame_iv_data
from pathlib import Path

# Load data
df_cost = load_cost_control_data(Path('data/input/data_baru.csv'))
df_ame4_book = df_cost[df_cost['DIVISI'] == 'AME004']
book_dict = get_book_count_dict(df_ame4_book)

df_drone = load_ame_iv_data(Path('data/input/AME_IV.csv'))
drone_bloks = df_drone['Blok'].apply(normalize_block).unique()

print('=== AME IV Analysis ===')
print(f"Book total (TOTAL_PKK): {df_ame4_book['TOTAL_PKK'].sum():,.0f}")
print(f"Book blok count: {len(book_dict)}")
print(f"Drone total: {len(df_drone):,}")
print(f"Drone blok count: {len(drone_bloks)}")
print()
print("Book bloks:", sorted(book_dict.keys())[:10], "...")
print("Drone bloks:", sorted(drone_bloks)[:10], "...")
print()

# Check matched vs unmatched
matched = set(book_dict.keys()) & set(drone_bloks)
book_only = set(book_dict.keys()) - set(drone_bloks)
drone_only = set(drone_bloks) - set(book_dict.keys())

print(f"Matched bloks: {len(matched)}")
book_only_sum = sum(book_dict[b] for b in book_only)
print(f"Book only (tidak ada di drone): {len(book_only)} blok - {book_only_sum:,} pohon")
print(f"Book only list: {sorted(book_only)}")
print()
print(f"Drone only (tidak ada di buku): {len(drone_only)} blok")
print(f"Drone only list: {sorted(drone_only)}")

# Sum matched
matched_book_sum = sum(book_dict[b] for b in matched)
print()
print(f"Matched book sum: {matched_book_sum:,} pohon")
