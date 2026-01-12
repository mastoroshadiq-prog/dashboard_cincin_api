import re
from collections import defaultdict

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'
OUTPUT = r'data/output/dashboard_cincin_api_ISO_TABBED_v10_FIXED.html'

def analyze_and_fix():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 80)
    print("ANALISIS STRUKTUR DASHBOARD ISO 31000")
    print("=" * 80)
    
    # 1. IDENTIFIKASI SEMUA PHASE CONTAINERS
    phase_containers = {}
    for i in range(1, 6):
        pattern = f'<div id="phase-{i}"[^>]*>'
        match = re.search(pattern, content)
        if match:
            phase_containers[i] = match.start()
            print(f"✓ Phase {i} container ditemukan di posisi {match.start()}")
        else:
            print(f"✗ Phase {i} container TIDAK DITEMUKAN!")
    
    print("\n" + "=" * 80)
    print("ANALISIS KOMPONEN BERDASARKAN BADGE")
    print("=" * 80)
    
    # 2. TEMUKAN SEMUA KOMPONEN DENGAN BADGE
    badge_pattern = r'<span class="iso-badge iso-phase-(\d)"[^>]*>([^<]+)</span>'
    badges = list(re.finditer(badge_pattern, content))
    
    print(f"\nTotal badge ditemukan: {len(badges)}")
    
    # 3. ANALISIS POSISI SETIAP BADGE RELATIF TERHADAP CONTAINER
    misplaced = defaultdict(list)
    correct = defaultdict(list)
    
    for badge_match in badges:
        badge_phase = int(badge_match.group(1))
        badge_text = badge_match.group(2).strip()
        badge_pos = badge_match.start()
        
        # Cari komponen parent (div terdekat sebelum badge)
        # Cari backward untuk menemukan opening div tag
        search_start = max(0, badge_pos - 500)
        component_snippet = content[search_start:badge_pos + 100]
        
        # Tentukan di phase container mana badge ini berada
        current_phase = None
        for phase_num in sorted(phase_containers.keys()):
            phase_start = phase_containers[phase_num]
            # Cari phase berikutnya untuk menentukan batas
            next_phase_start = float('inf')
            for next_num in range(phase_num + 1, 6):
                if next_num in phase_containers:
                    next_phase_start = phase_containers[next_num]
                    break
            
            if phase_start <= badge_pos < next_phase_start:
                current_phase = phase_num
                break
        
        # Bandingkan badge phase dengan container phase
        if current_phase == badge_phase:
            correct[badge_phase].append(badge_text)
            print(f"  ✓ [{badge_text}] - Benar di Phase {current_phase}")
        else:
            misplaced[badge_phase].append({
                'text': badge_text,
                'should_be': badge_phase,
                'currently_in': current_phase,
                'position': badge_pos
            })
            print(f"  ✗ [{badge_text}] - SALAH! Badge Phase {badge_phase} tapi ada di Container Phase {current_phase}")
    
    print("\n" + "=" * 80)
    print("RINGKASAN ANALISIS")
    print("=" * 80)
    
    for phase in range(1, 6):
        print(f"\nPhase {phase}:")
        if phase in correct and correct[phase]:
            print(f"  ✓ Komponen benar: {len(correct[phase])}")
            for comp in correct[phase]:
                print(f"    - {comp}")
        
        if phase in misplaced and misplaced[phase]:
            print(f"  ✗ Komponen salah tempat: {len(misplaced[phase])}")
            for comp in misplaced[phase]:
                print(f"    - {comp['text']} (seharusnya di Phase {comp['should_be']}, tapi ada di Phase {comp['currently_in']})")
    
    # 4. PERBAIKAN OTOMATIS
    if any(misplaced.values()):
        print("\n" + "=" * 80)
        print("MELAKUKAN PERBAIKAN OTOMATIS...")
        print("=" * 80)
        
        # Strategi: Ekstrak setiap komponen yang salah tempat dan pindahkan
        # Ini kompleks, jadi kita akan menggunakan pendekatan rebuild
        
        # Untuk sekarang, laporkan saja apa yang perlu diperbaiki
        print("\nKomponen yang perlu dipindahkan:")
        for phase, items in misplaced.items():
            for item in items:
                print(f"  - Pindahkan '{item['text']}' dari Phase {item['currently_in']} ke Phase {item['should_be']}")
        
        print("\n⚠️  Perbaikan manual diperlukan karena kompleksitas struktur HTML")
        print("    Gunakan informasi di atas untuk memindahkan komponen secara manual")
    else:
        print("\n✓ SEMUA KOMPONEN SUDAH BERADA DI TEMPAT YANG BENAR!")
    
    return misplaced

if __name__ == "__main__":
    analyze_and_fix()
