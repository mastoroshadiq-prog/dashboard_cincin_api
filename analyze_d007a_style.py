from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load D007A reference map
img = Image.open('data/output/cincin_api_map_D007A.png')

print("="*70)
print("📊 ANALYZING D007A MAP STYLE")
print("="*70)

print(f"\nImage Properties:")
print(f"  Size: {img.size} (width x height)")
print(f"  Mode: {img.mode}")
print(f"  Aspect ratio: {img.size[1]/img.size[0]:.2f} (height/width)")

# Convert to RGB for analysis
img_rgb = img.convert('RGB')
img_array = np.array(img_rgb)

print(f"\nArray shape: {img_array.shape}")

# Sample colors from different regions
print(f"\nSampling colors:")
# Sample from top-left (likely background or title)
top_sample = img_array[100, 100]
print(f"  Top area: RGB{tuple(top_sample)}")

# Sample from middle areas
mid_sample = img_array[img.size[1]//2, img.size[0]//2]
print(f"  Middle area: RGB{tuple(mid_sample)}")

# Find unique colors (simplified)
unique_colors = set()
for i in range(0, img.size[1], 50):
    for j in range(0, img.size[0], 50):
        unique_colors.add(tuple(img_array[i, j]))

print(f"\nTotal unique sampled colors: {len(unique_colors)}")

# Common colors in the image
from collections import Counter
# Sample every 10th pixel for performance
sampled_pixels = []
for i in range(0, img.size[1], 10):
    for j in range(0, img.size[0], 10):
        sampled_pixels.append(tuple(img_array[i, j]))

color_counts = Counter(sampled_pixels)
print(f"\nTop 10 most common colors:")
for color, count in color_counts.most_common(10):
    print(f"  RGB{color}: {count} pixels")

# Save a visualization
fig, ax = plt.subplots(1, 1, figsize=(8, 16))
ax.imshow(img)
ax.set_title('D007A Reference Map', fontsize=14, pad=10)
ax.axis('off')
plt.tight_layout()
plt.savefig('data/output/d007a_reference_view.png', dpi=100, bbox_inches='tight')
print(f"\n✅ Saved reference view to: data/output/d007a_reference_view.png")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
