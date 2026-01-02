"""
Bandingkan hasil generate dengan reference F08
"""
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("📊 VISUAL COMPARISON ANALYSIS")
print("="*70)

# Load images
try:
    ref_img = Image.open('poac_sim/data/output/cincin_api/20251222_1525_multi_divisi/AME_II/cluster_map_agresif_03_F08.png')
    my_f008a = Image.open('data/output/cincin_api_map_F008A.png')
    
    print("\n✅ Images loaded successfully")
    print(f"\nReference F08:")
    print(f"  Size: {ref_img.size} (width x height)")
    print(f"  Mode: {ref_img.mode}")
    print(f"  Aspect: {ref_img.size[1]/ref_img.size[0]:.2f}")
    
    print(f"\nMy F008A:")
    print(f"  Size: {my_f008a.size} (width x height)")
    print(f"  Mode: {my_f008a.mode}")
    print(f"  Aspect: {my_f008a.size[1]/my_f008a.size[0]:.2f}")
    
    # Create side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    ax1.imshow(ref_img)
    ax1.set_title('REFERENCE: cluster_map_agresif_03_F08.png', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    ax2.imshow(my_f008a)
    ax2.set_title('MY OUTPUT: cincin_api_map_F008A.png', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('data/output/comparison_visual.png', dpi=150, bbox_inches='tight')
    print(f"\n✅ Comparison saved: data/output/comparison_visual.png")
    
    # Analyze colors
    print("\n" + "="*70)
    print("🎨 COLOR ANALYSIS")
    print("="*70)
    
    ref_array = np.array(ref_img.convert('RGB'))
    my_array = np.array(my_f008a.convert('RGB'))
    
    # Sample center area
    ref_h, ref_w = ref_array.shape[:2]
    my_h, my_w = my_array.shape[:2]
    
    # Get unique colors in center area (sample)
    ref_center = ref_array[ref_h//4:3*ref_h//4, ref_w//4:3*ref_w//4]
    my_center = my_array[my_h//4:3*my_h//4, my_w//4:3*my_w//4]
    
    from collections import Counter
    
    # Sample colors
    ref_sample = ref_center.reshape(-1, 3)[::100]  # Sample every 100th pixel
    my_sample = my_center.reshape(-1, 3)[::100]
    
    print("\nTop 5 colors in REFERENCE:")
    ref_counter = Counter([tuple(c) for c in ref_sample])
    for color, count in ref_counter.most_common(5):
        print(f"  RGB{color}: {count} occurrences")
    
    print("\nTop 5 colors in MY OUTPUT:")
    my_counter = Counter([tuple(c) for c in my_sample])
    for color, count in my_counter.most_common(5):
        print(f"  RGB{color}: {count} occurrences")
    
    # Visual characteristics check
    print("\n" + "="*70)
    print("📐 VISUAL CHARACTERISTICS CHECK")
    print("="*70)
    
    print("\nReference characteristics:")
    print("  - Tall vertical layout: ✅" if ref_img.size[1] > ref_img.size[0] else "  - Wide layout")
    print(f"  - Aspect ratio: {ref_img.size[1]/ref_img.size[0]:.1f}")
    
    print("\nMy output characteristics:")
    print("  - Tall vertical layout: ✅" if my_f008a.size[1] > my_f008a.size[0] else "  - Wide layout")
    print(f"  - Aspect ratio: {my_f008a.size[1]/my_f008a.size[0]:.1f}")
    
    # Check if overlapping (density)
    print("\n" + "="*70)
    print("🔍 OVERLAP DENSITY CHECK")
    print("="*70)
    
    # Count non-white pixels
    ref_non_white = np.sum(np.all(ref_array < 250, axis=2))
    my_non_white = np.sum(np.all(my_array < 250, axis=2))
    
    ref_total = ref_array.shape[0] * ref_array.shape[1]
    my_total = my_array.shape[0] * my_array.shape[1]
    
    ref_coverage = (ref_non_white / ref_total) * 100
    my_coverage = (my_non_white / my_total) * 100
    
    print(f"\nReference coverage: {ref_coverage:.1f}%")
    print(f"My output coverage: {my_coverage:.1f}%")
    
    coverage_diff = abs(ref_coverage - my_coverage)
    if coverage_diff < 5:
        print("✅ Coverage similar (difference < 5%)")
    elif coverage_diff < 10:
        print("⚠️  Coverage somewhat different (difference < 10%)")
    else:
        print(f"❌ Coverage very different (difference: {coverage_diff:.1f}%)")
    
    print("\n" + "="*70)
    print("📊 FINAL ASSESSMENT")
    print("="*70)
    
    issues = []
    matches = []
    
    # Check aspect ratio
    ref_aspect = ref_img.size[1]/ref_img.size[0]
    my_aspect = my_f008a.size[1]/my_f008a.size[0]
    if abs(ref_aspect - my_aspect) < 0.2:
        matches.append("✅ Aspect ratio similar")
    else:
        issues.append(f"❌ Aspect ratio different (ref: {ref_aspect:.1f}, mine: {my_aspect:.1f})")
    
    # Check coverage
    if coverage_diff < 10:
        matches.append("✅ Overlap density similar")
    else:
        issues.append(f"❌ Overlap density different ({coverage_diff:.1f}% difference)")
    
    # Check orientation
    if ref_img.size[1] > ref_img.size[0] and my_f008a.size[1] > my_f008a.size[0]:
        matches.append("✅ Both vertical/tall orientation")
    else:
        issues.append("❌ Orientation mismatch")
    
    print("\n✅ MATCHES:")
    for m in matches:
        print(f"  {m}")
    
    if issues:
        print("\n❌ ISSUES TO FIX:")
        for i in issues:
            print(f"  {i}")
    else:
        print("\n🎉 All checks passed!")
    
    print("\n💡 RECOMMENDATION:")
    if len(issues) == 0:
        print("  Maps look good! Ready to use.")
    elif len(issues) <= 2:
        print("  Minor adjustments needed. Check the issues above.")
    else:
        print("  Significant differences. Need major style revision.")
    
except FileNotFoundError as e:
    print(f"\n❌ Error: {e}")
    print("   Make sure both images exist!")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*70)
