#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Cari semua badge dan posisinya
badges = []
for match in re.finditer(r'<span class="iso-badge iso-phase-(\d)"', content):
    phase_num = int(match.group(1))
    pos = match.start()
    badges.append((phase_num, pos))

print(f"Total badges found: {len(badges)}")
print("\nBadge distribution:")
for i in range(1, 6):
    count = sum(1 for p, _ in badges if p == i)
    print(f"  Phase {i}: {count} badges")

# Cari phase containers
containers = {}
for i in range(1, 6):
    match = re.search(f'<div id="phase-{i}"', content)
    if match:
        containers[i] = match.start()
        print(f"\nPhase {i} container at position: {match.start()}")

# Check each badge
print("\n" + "="*60)
print("CHECKING BADGE POSITIONS:")
print("="*60)

for badge_phase, badge_pos in badges:
    # Find which container this badge is in
    current_container = None
    for phase_num in sorted(containers.keys()):
        start = containers[phase_num]
        end = containers.get(phase_num + 1, len(content))
        if start <= badge_pos < end:
            current_container = phase_num
            break
    
    status = "OK" if current_container == badge_phase else "WRONG"
    print(f"Badge Phase-{badge_phase} at pos {badge_pos}: in container Phase-{current_container} [{status}]")
