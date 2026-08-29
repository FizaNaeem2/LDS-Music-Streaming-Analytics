"""**Assignment No 3**"""

import csv
import statistics

file_path = "LDS Data 2025-2026/Cleaned_Tracks.csv"
output_path = "LDS Data 2025-2026/Cleaned_Tracks(with_categories).csv"

rows = []
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

def to_float(x):
    try:
        return float(x)
    except:
        return None

def percentile(vals, p):
    k = (len(vals)-1) * p
    f = int(k)
    c = min(f+1, len(vals)-1)
    if f == c:
        return vals[f]
    return vals[f] + (vals[c]-vals[f]) * (k-f)

bpm_vals = sorted([to_float(r["bpm"]) for r in rows if to_float(r["bpm"]) is not None])
rms_vals = sorted([to_float(r["rms"]) for r in rows if to_float(r["rms"]) is not None])
roll_vals = sorted([to_float(r["rolloff"]) for r in rows if to_float(r["rolloff"]) is not None])
loud_vals = sorted([to_float(r["loudness"]) for r in rows if to_float(r["loudness"]) is not None])

bpm_p40 = percentile(bpm_vals, 0.40)
bpm_p60 = percentile(bpm_vals, 0.60)
rms_p40 = percentile(rms_vals, 0.40)
rms_p60 = percentile(rms_vals, 0.60)
roll_p40 = percentile(roll_vals, 0.40)
roll_p60 = percentile(roll_vals, 0.60)
loud_p40 = percentile(loud_vals, 0.40)
loud_p60 = percentile(loud_vals, 0.60)

def category(t):
    bpm = to_float(t["bpm"])
    rms = to_float(t["rms"])
    roll = to_float(t["rolloff"])
    loud = to_float(t["loudness"])
    if bpm is None or rms is None or roll is None or loud is None:
        return "Unknown"
    if bpm > bpm_p60 or rms > rms_p60:
        energy = "high"
    elif bpm < bpm_p40 and rms < rms_p40:
        energy = "low"
    else:
        energy = "mid"
    if roll > roll_p60 or loud > loud_p60:
        bright = "bright"
    elif roll < roll_p40 and loud < loud_p40:
        bright = "calm"
    else:
        bright = "neutral"
    if energy == "high" and bright == "bright":
        return "Energetic/Party"
    if energy == "high":
        return "Energetic/Emotional"
    if energy == "low" and bright == "calm":
        return "Soft/Chill"
    return "Mellow/Bright"

for r in rows:
    r["song_category"] = category(r)

fields = list(rows[0].keys())
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows(rows)

print("Saved:", output_path)