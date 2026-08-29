import xml.etree.ElementTree as ET

tree = ET.parse('LDS Data 2025-2026/artists.xml')
root = tree.getroot()

missing_counts = {}

for record in root:
    for elem in record:
        key = elem.tag
        value = elem.text.strip() if elem.text else None

        if key not in missing_counts:
            missing_counts[key] = 0

        if value in [None, '', 'null', 'NULL', '\\N']:
            missing_counts[key] += 1

print("Missing values per field:")
for field, count in missing_counts.items():
    print(f"{field}: {count}")

