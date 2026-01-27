import pandas as pd

df = pd.read_excel('poac_sim/data/input/data_gabungan.xlsx')
ame02 = df[df[df.columns[5]] == 'AME02']

print("Comprehensive scan for ALL production columns:")
print("="*60)

results = []
for i in range(len(df.columns)):
    try:
        total = ame02.iloc[:, i].sum()
        if 10000 < total < 20000:
            results.append((i, total))
    except:
        pass

print(f"Found {len(results)} production columns:\n")
for i, total in results:
    print(f"Index {i:3d}: {total:12,.2f} Ton")

print("\n" + "="*60)
print("CONCLUSION:")
if len(results) == 2:
    print("Only 2024 and 2025 data available")
    print(f"  2024: Index {results[0][0]} ({results[0][1]:,.2f} Ton)")
    print(f"  2025: Index {results[1][0]} ({results[1][1]:,.2f} Ton)")
elif len(results) == 3:
    print("2023, 2024, 2025 data available!")
else:
    print(f"{len(results)} years of data detected")
