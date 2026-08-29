import json

with open('LDS Data 2025-2026/tracks.json', 'r', encoding='utf-8') as jsonfile:
    tracks_data = json.load(jsonfile)

missing_counts = {}

for track in tracks_data:
    for key, value in track.items():
        if value in [None, '', 'null', 'NULL', '\\N']:
            if key not in missing_counts:
                missing_counts[key] = 0
            missing_counts[key] += 1
        if key not in missing_counts:
            missing_counts[key] = 0

print("Missing values per field:")
for field, count in missing_counts.items():
    print(f"{field}: {count}")