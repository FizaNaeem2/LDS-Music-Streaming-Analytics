import csv
import os
from datetime import datetime

# --- CONFIGURATION ---
input_tracks = "LDS Data 2025-2026/Cleaned_Tracks(with_categories).csv"
input_artists = "LDS Data 2025-2026/Cleaned_Artists.csv"
output_dir = "LDS Data 2025-2026/DW_Import/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_season(month):
    m = int(month)
    if m in [12, 1, 2]: return 'Winter'
    if m in [3, 4, 5]: return 'Spring'
    if m in [6, 7, 8]: return 'Summer'
    return 'Autumn'

def get_quarter(month):
    return (int(month) - 1) // 3 + 1

def clean_int(val):
    try:
        return int(float(val)) if val else 0
    except ValueError:
        return 0

print("Loading Artists...")
valid_artist_ids = set()
dim_artist_rows = []

with open(input_artists, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        valid_artist_ids.add(row['id_author'])

        dim_artist_rows.append({
            'id_artist': row['id_author'],
            'name': row['name'],
            'gender': row['gender'],
            'birth_place': row['birth_place'],
            'country': row['country'],
            'region': row['region'],
            'h3_index': row['h3_index'],
            'latitude': row['latitude'],
            'longitude': row['longitude']
        })

with open(f"{output_dir}Dim_Artist.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=dim_artist_rows[0].keys())
    writer.writeheader()
    writer.writerows(dim_artist_rows)

print("Processing Tracks, Time, and Facts...")

dim_track_rows = []
dim_time_rows = {} 
fact_rows = []

seen_track_ids = set()
seen_fact_keys = set() 

with open(input_tracks, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 1. Dim_Track
        if row['id'] not in seen_track_ids:
            dim_track_rows.append({
                'id_track': row['id'],
                'title': row['title'],
                'song_category': row.get('song_category', 'Unknown'),
                'featured_artists': row['featured_artists'],
                'explicit': row['explicit'],
                'duration_ms': clean_int(row['duration_ms']),
                'bpm': row['bpm'],
                'n_tokens': row['n_tokens'],      
                'language': row['language'],
                'n_sentences': row['n_sentences'],
                'char_per_tok': row['char_per_tok'],
                'avg_token_per_clause': row['avg_token_per_clause'],
                'swear_IT':row['swear_IT'],
                'swear_EN':row['swear_EN']
            })
            seen_track_ids.add(row['id'])

        # 2. Dim_Time
        try:
            y = int(float(row['year'])) if row['year'] else 0
            m = int(float(row['month'])) if row['month'] else 1
            d = int(float(row['day'])) if row['day'] else 1
        except ValueError:
            y, m, d = 0, 1, 1
            
        id_time = int(f"{y}{m:02d}{d:02d}")
        
        if id_time not in dim_time_rows:
            dim_time_rows[id_time] = {
                'id_time': id_time,
                'year': y,
                'month': m,
                'day': d,
                'quarter': get_quarter(m),
                'season': get_season(m)
            }

        # 3. Fact_Streams
        fact_key = (row['id'], row['id_artist'], id_time) 

        # INTEGRITY CHECK: 
        # 1. Artist must exist in Dim_Artist
        # 2. This exact combination of (Track, Artist, Time) must not have been added yet
        if row['id_artist'] in valid_artist_ids and fact_key not in seen_fact_keys:
            
            fact_rows.append({
                'id_track': row['id'],
                'id_artist': row['id_artist'],
                'id_time': id_time,
                'streams': row['streams@1month'],
                'popularity': clean_int(row['popularity'])
            })
            
            seen_fact_keys.add(fact_key)

# Write Dim_Track
with open(f"{output_dir}Dim_Track.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id_track', 'title', 'song_category', 'featured_artists', 'explicit', 
               'duration_ms', 'bpm', 'n_tokens', 'language', 
               'n_sentences', 'char_per_tok', 'avg_token_per_clause', 'swear_IT', 'swear_EN'])
    writer.writeheader()
    writer.writerows(dim_track_rows)

# Write Dim_Time
with open(f"{output_dir}Dim_Time.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id_time', 'year', 'month', 'day', 'quarter', 'season'])
    writer.writeheader()
    writer.writerows(list(dim_time_rows.values()))

# Write Fact_Streams
with open(f"{output_dir}Fact_Streams.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id_track', 'id_artist', 'id_time', 'streams', 'popularity'])
    writer.writeheader()
    writer.writerows(fact_rows)

print("Files saved to DW_Import.")