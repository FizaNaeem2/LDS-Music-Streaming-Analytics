"""
**Conversion to CSV File**
"""

import xml.etree.ElementTree as ET
import csv

tree = ET.parse('LDS Data 2025-2026/artists.xml')
root = tree.getroot()

with open('LDS Data 2025-2026/artists.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id_author', 'name', 'gender', 'birth_date', 'birth_place', 'nationality', 'description',
                  'active_start', 'active_end', 'province', 'region', 'country', 'latitude', 'longitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in root.findall('row'):
        artist_data = {
            'id_author': row.find('id_author').text,
            'name': row.find('name').text,
            'gender': row.find('gender').text,
            'birth_date': row.find('birth_date').text if row.find('birth_date') is not None else '',
            'birth_place': row.find('birth_place').text if row.find('birth_place') is not None else '',
            'nationality': row.find('nationality').text if row.find('nationality') is not None else '',
            'description': row.find('description').text if row.find('description') is not None else '',
            'active_start': row.find('active_start').text if row.find('active_start') is not None else '',
            'active_end': row.find('active_end').text if row.find('active_end') is not None else '',
            'province': row.find('province').text if row.find('province') is not None else '',
            'region': row.find('region').text if row.find('region') is not None else '',
            'country': row.find('country').text if row.find('country') is not None else '',
            'latitude': row.find('latitude').text if row.find('latitude') is not None else '',
            'longitude': row.find('longitude').text if row.find('longitude') is not None else ''
        }
        writer.writerow(artist_data)

"""**1. Load CSV file into a list of dictionaries**"""

import csv

file_path = "LDS Data 2025-2026/artists.csv"

df_artists = []

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        df_artists.append(row)

"""**2. active_end**"""

for r in df_artists:
    r.pop("active_end", None)

"""**3. latitude and longitude, region, country, birthplace, region, province**"""

from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="artists_unified_geocoder")

def norm(s):
    return (s or "").strip()

def missing(v):
    v = norm(v).lower()
    return v == "" or v in {"na", "n/a", "null", "none", "nan", "-"}

for r in df_artists:
    has_birth = not missing(r.get("birth_place"))
    has_latlon = (not missing(r.get("latitude"))) and (not missing(r.get("longitude")))

    if not (
        missing(r.get("latitude")) or
        missing(r.get("longitude")) or
        missing(r.get("region")) or
        missing(r.get("country")) or
        missing(r.get("province")) or
        (missing(r.get("birth_place")) and has_latlon)
    ):
        continue

    try:
        loc = None

        if missing(r.get("birth_place")) and has_latlon:
            loc = geolocator.reverse(
                (float(norm(r.get("latitude"))), float(norm(r.get("longitude")))),
                addressdetails=True,
                timeout=10
            )
        else:
            city = norm(r.get("birth_place"))
            if city == "":
                continue
            country_existing = norm(r.get("country"))
            query = f"{city}, {country_existing or 'Italy'}"
            loc = geolocator.geocode(query, addressdetails=True, timeout=10)

        if not loc:
            continue

        addr = loc.raw.get("address", {})

        if missing(r.get("latitude")) and hasattr(loc, "latitude") and loc.latitude is not None:
            r["latitude"] = str(loc.latitude)

        if missing(r.get("longitude")) and hasattr(loc, "longitude") and loc.longitude is not None:
            r["longitude"] = str(loc.longitude)

        if missing(r.get("country")):
            val = addr.get("country")
            if val:
                r["country"] = val

        if missing(r.get("region")):
            val = addr.get("state") or addr.get("region")
            if val:
                r["region"] = val

        if missing(r.get("province")):
            val = addr.get("province") or addr.get("state_district") or addr.get("county")
            if val:
                r["province"] = val

        if missing(r.get("birth_place")):
            val = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality")
            if val:
                r["birth_place"] = val

    except:
        pass

    sleep(1)

"""**4. nationality**"""

def norm(s):
    return (s or "").strip()

def missing(v):
    v = norm(v).lower()
    return v == "" or v in {"na", "n/a", "null", "none", "nan", "-"}

for r in df_artists:
    if missing(r.get("nationality")) and not missing(r.get("country")):
        r["nationality"] = norm(r.get("country"))

"""**5. h5_index**"""

!pip install geopy

import h3
from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="dss_project_group_05")

def get_lat_lon(place_name):
    try:
        if not place_name or place_name.lower() in ['unknown', 'none', '']:
            return None, None
        location = geolocator.geocode(place_name)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None

for r in df_artists:
    lat = r.get('latitude')
    lon = r.get('longitude')

    if missing(lat) or missing(lon) or str(lat) == 'None' or str(lon) == 'None':
        place = r.get('birth_place') or r.get('country')
        if place:
            new_lat, new_lon = get_lat_lon(place)
            if new_lat:
                lat, lon = new_lat, new_lon
                r['latitude'] = lat
                r['longitude'] = lon
                print(f"Recovered coords for {r.get('name')}: {place}")
                sleep(1)

    if lat and lon and str(lat) != 'None':
        try:
            r['h3_index'] = h3.latlng_to_cell(float(lat), float(lon), 4)
        except ValueError:
            r['h3_index'] = None
    else:
        r['h3_index'] = None

"""**6. Final Dataset**"""

import csv

out_path = "LDS Data 2025-2026/Cleaned_Artists.csv"
fieldnames = list(df_artists[0].keys())

with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(df_artists)