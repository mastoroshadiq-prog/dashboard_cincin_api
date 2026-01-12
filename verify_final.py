#!/usr/bin/env python
# -*- coding: utf-8 -*-

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*80)
print("VERIFIKASI FINAL - BADGE PLACEMENT")
print("="*80)

# Cari phase containers
containers = {}
for i in range(1, 6):
    import re
    match = re.search(f'<div id="phase-{i}"', content)
    if match:
        containers[i] = match.start()
        # Cari end
        next_phase = i + 1
        if next_phase <= 5:
            next_match = re.search(f'<div id="phase-{next_phase}"', content)
            end = next_match.start() if next_match else len(content)
        else:
            end = content.find('</div> <!-- End tab-overview -->')
            if end == -1:
                end = len(content)
        containers[f"{i}_end"] = end

# Cari semua badges
badges = []
for match in re.finditer(r'<span class="iso-badge iso-phase-(\d)"', content):
    phase_num = int(match.group(1))
    pos = match.start()
    badges.append((phase_num, pos))

print(f"\nTotal badges: {len(badges)}")
print("\nDistribusi badges per phase container:")

for phase in range(1, 6):
    if phase not in containers:
        print(f"  Phase {phase}: CONTAINER TIDAK DITEMUKAN!")
        continue
    
    start = containers[phase]
    end = containers.get(f"{phase}_end", len(content))
    
    # Hitung badge dalam range ini
    badges_in_phase = [(p, pos) for p, pos in badges if start <= pos < end]
    
    # Kelompokkan berdasarkan badge number
    badge_counts = {}
    for badge_phase, _ in badges_in_phase:
        badge_counts[badge_phase] = badge_counts.get(badge_phase, 0) + 1
    
    print(f"\n  Phase {phase} Container (pos {start} - {end}):")
    if not badge_counts:
        print(f"    ⚠️  KOSONG - Tidak ada badge!")
    else:
        for badge_num in sorted(badge_counts.keys()):
            status = "✓ OK" if badge_num == phase else "✗ SALAH TEMPAT"
            print(f"    Badge Phase-{badge_num}: {badge_counts[badge_num]} buah [{status}]")

print("\n" + "="*80)
print("KESIMPULAN:")
print("="*80)

# Check if all badges are in correct containers
all_correct = True
for phase in range(1, 6):
    if phase not in containers:
        continue
    start = containers[phase]
    end = containers.get(f"{phase}_end", len(content))
    badges_in_phase = [(p, pos) for p, pos in badges if start <= pos < end]
    wrong_badges = [p for p, _ in badges_in_phase if p != phase]
    if wrong_badges:
        all_correct = False
        print(f"✗ Phase {phase}: Ada badge yang salah tempat!")

if all_correct:
    print("✓ SEMUA BADGE SUDAH BERADA DI CONTAINER YANG BENAR!")
    print("  Dashboard siap digunakan.")
else:
    print("✗ Masih ada badge yang salah tempat.")
    print("  Perlu perbaikan manual atau script tambahan.")
