
import re

file_path = 'dashboard-cincin-api/data/output/DASHBOARD_DEMO_FEATURES.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

modals = re.findall(r'id=["\']\w*Modal["\']', content)
print("Found Modals:", modals)

# Also look for the probable target Modal for `openPaparanRisikoModal`
# Maybe "riskModal" or "paparanModal"?
