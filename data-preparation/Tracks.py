"""
**Conversion to CSV File**
"""

import json
import csv

with open('LDS Data 2025-2026/tracks.json', 'r', encoding='utf-8') as jsonfile:
    tracks_data = json.load(jsonfile)

with open('LDS Data 2025-2026/tracks.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'id_artist', 'title', 'featured_artists', 'primary_artist', 'language', 'album',
                  'swear_IT', 'swear_EN', 'swear_IT_words', 'swear_EN_words', 'year', 'month', 'day',
                  'n_sentences', 'n_tokens', 'char_per_tok', 'avg_token_per_clause', 'bpm', 'rolloff',
                  'flux', 'rms', 'flatness', 'spectral_complexity', 'pitch', 'loudness', 'album_name',
                  'album_release_date', 'album_type', 'disc_number', 'track_number', 'duration_ms',
                  'explicit', 'popularity', 'id_album', 'lyrics', 'streams@1month']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for track in tracks_data:
        track_data = {
            'id': track.get('id', ''),
            'id_artist': track.get('id_artist', ''),
            'title': track.get('title', ''),
            'featured_artists': track.get('featured_artists', ''),
            'primary_artist': track.get('primary_artist', ''),
            'language': track.get('language', ''),
            'album': track.get('album', ''),
            'swear_IT': track.get('swear_IT', ''),
            'swear_EN': track.get('swear_EN', ''),
            'swear_IT_words': track.get('swear_IT_words', ''),
            'swear_EN_words': track.get('swear_EN_words', ''),
            'year': track.get('year', ''),
            'month': track.get('month', ''),
            'day': track.get('day', ''),
            'n_sentences': track.get('n_sentences', ''),
            'n_tokens': track.get('n_tokens', ''),
            'char_per_tok': track.get('char_per_tok', ''),
            'avg_token_per_clause': track.get('avg_token_per_clause', ''),
            'bpm': track.get('bpm', ''),
            'rolloff': track.get('rolloff', ''),
            'flux': track.get('flux', ''),
            'rms': track.get('rms', ''),
            'flatness': track.get('flatness', ''),
            'spectral_complexity': track.get('spectral_complexity', ''),
            'pitch': track.get('pitch', ''),
            'loudness': track.get('loudness', ''),
            'album_name': track.get('album_name', ''),
            'album_release_date': track.get('album_release_date', ''),
            'album_type': track.get('album_type', ''),
            'disc_number': track.get('disc_number', ''),
            'track_number': track.get('track_number', ''),
            'duration_ms': track.get('duration_ms', ''),
            'explicit': track.get('explicit', ''),
            'popularity': track.get('popularity', ''),
            'id_album': track.get('id_album', ''),
            'lyrics': track.get('lyrics', ''),
            'streams@1month': track.get('streams@1month', '')
        }
        writer.writerow(track_data)

"""**1. Load CSV file into a list of dictionaries**"""

!pip install langdetect

# !pip install langdetect spotipy

import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from langdetect import detect
import re
from datetime import datetime

file_path = "LDS Data 2025-2026/tracks.csv"
df_tracks = []

with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        df_tracks.append(row)
import os

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

"""**3. Define Function to Fetch Track Info from Spotify**"""

def get_track(title, artist):
    q = f"{title} {artist}"
    result = sp.search(q=q, type="track", limit=1)
    try:
        return result["tracks"]["items"][0]
    except:
        return None

"""**4. Define Function to Extract Track Information and Filling Missing Values in the Dataset**"""

def extract_track_info(t):
    artist_names = [artist['name'] for artist in t.get('artists', [])]

    return {
        "album_name": t["album"]["name"],
        "album_type": t["album"]["album_type"],
        "album_release_date": t["album"]["release_date"],
        "disc_number": t["disc_number"],
        "track_number": t["track_number"],
        "duration_ms": t["duration_ms"],
        "explicit": t["explicit"],
        "popularity": t["popularity"],
        "album": t["album"]["name"],
        "artists": ', '.join(artist_names)
    }

for idx, row in enumerate(df_tracks):

    if row.get("featured_artists") in [None, 'null', 'NULL', '\\N', '']:

        track = get_track(
            row.get("title", ""),
            row.get("primary_artist", "")
        )

        if track:
            info = extract_track_info(track)

            for col in [
                "album_name", "album_type", "album_release_date",
                "disc_number", "track_number", "duration_ms",
                "explicit", "popularity", "album"
            ]:
                if row.get(col) in [None, 'null', 'NULL', '\\N', ''] and info.get(col) is not None:
                    row[col] = info[col]

            artist_names = info["artists"].split(', ')
            featured = [a for a in artist_names if a != row.get("primary_artist")]

            if featured:
                row["featured_artists"] = ', '.join(featured)

"""**5. bpm, rolloff, flux, rms, flatness, spectral_complexity, pitch, loudness**"""

def missing_count_per_field(data, fields):
    missing_counts = {field: 0 for field in fields}
    for row in data:
        for field in fields:
            if not row.get(field):
                missing_counts[field] += 1
    return missing_counts

def fill_audio_features_with_artist_mean(data):
    missing_count = 0
    audio_fields = ['bpm', 'rolloff', 'flux', 'rms', 'flatness', 'spectral_complexity', 'pitch', 'loudness']

    artist_means = {}
    for row in data:
        artist = row['primary_artist']
        if artist not in artist_means:
            artist_means[artist] = {field: [] for field in audio_fields}

    for row in data:
        artist = row['primary_artist']
        for field in audio_fields:
            if row.get(field):
                artist_means[artist][field].append(float(row[field]))

    for artist, fields in artist_means.items():
        for field, values in fields.items():
            if values:
                artist_means[artist][field] = sum(values) / len(values)

    print("Missing counts before filling:")
    initial_missing_counts = missing_count_per_field(data, audio_fields)
    for field, count in initial_missing_counts.items():
        print(f"{field}: {count}")

    for row in data:
        for field in audio_fields:
            if not row.get(field):
                artist = row['primary_artist']
                if artist in artist_means and field in artist_means[artist]:
                    row[field] = artist_means[artist][field]
                    missing_count += 1

    print("\nMissing counts after filling:")
    final_missing_counts = missing_count_per_field(data, audio_fields)
    for field, count in final_missing_counts.items():
        print(f"{field}: {count}")

    return missing_count

missing_count = fill_audio_features_with_artist_mean(df_tracks)
print(f"\nTotal missing values filled: {missing_count}")

"""**6. n_sentences, n_tokens, char_per_tok, avg_token_per_clause**"""

def count_sentences(text):
    return len(re.split(r'[.!?]', text)) - 1

def count_tokens(text):
    return len(text.split())

def count_chars_per_token(text):
    tokens = text.split()
    return sum(len(token) for token in tokens) / len(tokens) if tokens else 0

def count_avg_token_per_clause(text):
    clauses = re.split(r'[,.]', text)
    token_counts = [len(clause.split()) for clause in clauses if clause.strip()]
    return sum(token_counts) / len(token_counts) if token_counts else 0

def fill_nlp_metrics(data):
    missing_sentences = missing_tokens = missing_char_per_tok = missing_avg_token_per_clause = 0

    for row in data:
        lyrics = row.get('lyrics')
        if not lyrics:
            continue

        if not row.get('n_sentences'):
            row['n_sentences'] = count_sentences(lyrics)
            missing_sentences += 1
        if not row.get('n_tokens'):
            row['n_tokens'] = count_tokens(lyrics)
            missing_tokens += 1
        if not row.get('char_per_tok'):
            row['char_per_tok'] = count_chars_per_token(lyrics)
            missing_char_per_tok += 1
        if not row.get('avg_token_per_clause'):
            row['avg_token_per_clause'] = count_avg_token_per_clause(lyrics)
            missing_avg_token_per_clause += 1

    return missing_sentences, missing_tokens, missing_char_per_tok, missing_avg_token_per_clause

missing_sentences, missing_tokens, missing_char_per_tok, missing_avg_token_per_clause = fill_nlp_metrics(df_tracks)

print(f"Filled {missing_sentences} 'n_sentences' using lyrics.")
print(f"Filled {missing_tokens} 'n_tokens' using lyrics.")
print(f"Filled {missing_char_per_tok} 'char_per_tok' using lyrics.")
print(f"Filled {missing_avg_token_per_clause} 'avg_token_per_clause' using lyrics.")

"""**7. langauge**"""

missing_values = {'None', 'null', 'NULL', '\\N', ''}

def detect_language_from_lyrics(lyrics):
    try:
        return detect(lyrics)
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None

def fill_language(data):
    missing_count = 0

    for row in data:
        if row['language'] in missing_values and row.get('lyrics'):
            detected_lang = detect_language_from_lyrics(row['lyrics'])
            if detected_lang:
                row['language'] = detected_lang
                missing_count += 1

    print(f"Filled {missing_count} 'language' values using lyrics detection.")

    missing_after_lyrics = sum(1 for row in data if row['language'] in missing_values)
    print(f"Missing 'language' after lyrics detection: {missing_after_lyrics}")

    return missing_count

missing_count = fill_language(df_tracks)

"""**8. year, month, day**"""

def missing(v):
    return v in [None, '', 'null', 'NULL', '\\N', 'Unknown']

def report(step):
    y = m = d = 0
    for r in df_tracks:
        if missing(r['year']): y += 1
        if missing(r['month']): m += 1
        if missing(r['day']): d += 1
    print(f"{step}:")
    print("Missing YEAR :", y)
    print("Missing MONTH:", m)
    print("Missing DAY  :", d)
    return y, m, d

report("Before Filling Missing Values")

for row in df_tracks:
    if not missing(row['album_release_date']):
        try:
            release_date = row['album_release_date'].strip()
            if len(release_date) == 10:
                d = datetime.strptime(release_date, "%Y-%m-%d")
            elif len(release_date) == 7:
                d = datetime.strptime(release_date, "%Y-%m")
                row['day'] = 1
            row['year'], row['month'], row['day'] = d.year, d.month, d.day
        except Exception as e:
            pass

report("After Filling Missing Values")

"""**10. Final Dataset**"""

output_path = "LDS Data 2025-2026/Cleaned_Tracks.csv"

with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=df_tracks[0].keys())
    writer.writeheader()
    writer.writerows(df_tracks)

print("Final dataset saved at:", output_path)