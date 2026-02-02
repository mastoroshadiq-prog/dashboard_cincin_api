"""
Remove SPH datasets from 5-Year Trend Analysis chart
Remove both "SPH (No Treatment)" and "SPH (With Treatment)" green lines
"""

# Read file
input_file = r"f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find and mark SPH datasets for removal
# Dataset 3: SPH (No Treatment) - lines 17952-17970
# Dataset 6: SPH (With Treatment) - lines 18010-18028

# Strategy: Remove these line ranges
sph_no_treatment_start = 17952 - 1  # 0-indexed
sph_no_treatment_end = 17970        # Exclusive

sph_with_treatment_start = 18010 - 1  # 0-indexed  
sph_with_treatment_end = 18028        # Exclusive

print(f"\nRemoving SPH (No Treatment) dataset:")
print(f"  Lines {sph_no_treatment_start+1} to {sph_no_treatment_end}")
print(f"  Total: {sph_no_treatment_end - sph_no_treatment_start} lines")

print(f"\nRemoving SPH (With Treatment) dataset:")
print(f"  Lines {sph_with_treatment_start+1} to {sph_with_treatment_end}")
print(f"  Total: {sph_with_treatment_end - sph_with_treatment_start} lines")

# Build new content WITHOUT SPH datasets
# Remove second dataset first (higher line numbers) to maintain indices
new_lines = []

for i, line in enumerate(lines):
    # Skip SPH (With Treatment) lines
    if i >= sph_with_treatment_start and i < sph_with_treatment_end:
        if i == sph_with_treatment_start:
            print(f"  Skipping line {i+1}: {line[:60].strip()}...")
        continue
    
    # Skip SPH (No Treatment) lines
    if i >= sph_no_treatment_start and i < sph_no_treatment_end:
        if i == sph_no_treatment_start:
            print(f"  Skipping line {i+1}: {line[:60].strip()}...")
        continue
    
    new_lines.append(line)

print(f"\nLines before: {len(lines)}")
print(f"Lines after: {len(new_lines)}")
print(f"Removed: {len(lines) - len(new_lines)} lines")

# Write back
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nSUCCESS! SPH datasets removed from 5-Year Trend chart")
print(f"\nChart will now show only:")
print(f"  - Kerugian (No Treatment) - Red solid")
print(f"  - Ganoderma % (No Treatment) - Purple solid")
print(f"  - Kerugian (With Treatment) - Red dashed")
print(f"  - Ganoderma % (With Treatment) - Purple dashed")
print(f"\nGreen SPH lines removed!")
