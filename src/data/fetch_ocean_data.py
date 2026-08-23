import requests
import pandas as pd
from pathlib import Path
from io import StringIO

# ==========================================
# SETTINGS
# ==========================================

OUTPUT = Path("data/raw/ocean_data.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Indian Ocean region
MIN_LAT = 0
MAX_LAT = 25

MIN_LON = 65
MAX_LON = 95


# ==========================================
# NOAA ERDDAP DATASET
# ==========================================

BASE_URL = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41.csv"

# MUR SST:
# time, latitude, longitude, sea surface temperature


# ==========================================
# REQUEST
# ==========================================

print("Downloading NOAA ocean temperature data...")
print("Region:")
print(f"Latitude: {MIN_LAT} to {MAX_LAT}")
print(f"Longitude: {MIN_LON} to {MAX_LON}")


params = {
    "time>=": "2024-01-01T00:00:00Z",
    "time<=": "2024-01-07T00:00:00Z",
    "latitude>=": MIN_LAT,
    "latitude<=": MAX_LAT,
    "longitude>=": MIN_LON,
    "longitude<=": MAX_LON,
}


response = requests.get(BASE_URL, params=params, timeout=120)


print("Status:", response.status_code)

response.raise_for_status()


# ==========================================
# READ CSV
# ==========================================

df = pd.read_csv(StringIO(response.text))


print("\nData downloaded!")

print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# SAVE
# ==========================================

df.to_csv(OUTPUT, index=False)


print("\n================================")
print("OCEAN DATA CREATED")
print("================================")

print("Saved to:")
print(OUTPUT)

print("\nFirst 5 rows:")
print(df.head())
