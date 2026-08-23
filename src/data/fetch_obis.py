import requests
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

OUTPUT = Path("data/raw/obis_fish.csv")

# Indian Ocean / Indian subcontinent region
MIN_LAT = 0
MAX_LAT = 25
MIN_LON = 65
MAX_LON = 95

TARGET_RECORDS = 1000

# OBIS API
URL = "https://api.obis.org/v3/occurrence"


# --------------------------------------------------
# FETCH DATA
# --------------------------------------------------

params = {
    "scientificname": "Actinopterygii",
    "geometry": f"POLYGON(({MIN_LON} {MIN_LAT},"
    f"{MAX_LON} {MIN_LAT},"
    f"{MAX_LON} {MAX_LAT},"
    f"{MIN_LON} {MAX_LAT},"
    f"{MIN_LON} {MIN_LAT}))",
    "size": TARGET_RECORDS,
}

print("Fetching OBIS data...")
print("Region: Indian Ocean / Indian subcontinent")
print(f"Target records: {TARGET_RECORDS}")

response = requests.get(URL, params=params, timeout=60)

response.raise_for_status()

data = response.json()

print("Total records available:", data.get("total"))


# --------------------------------------------------
# CONVERT TO DATAFRAME
# --------------------------------------------------

records = data.get("results", [])

df = pd.DataFrame(records)

print("Records downloaded:", len(df))


# --------------------------------------------------
# KEEP USEFUL COLUMNS
# --------------------------------------------------

wanted_columns = [
    "id",
    "scientificName",
    "species",
    "genus",
    "family",
    "phylum",
    "class",
    "eventDate",
    "decimalLatitude",
    "decimalLongitude",
    "depth",
    "minimumDepthInMeters",
    "maximumDepthInMeters",
    "country",
    "locality",
    "marine",
    "basisOfRecord",
]

existing_columns = [col for col in wanted_columns if col in df.columns]

df = df[existing_columns]


# --------------------------------------------------
# CLEAN COORDINATES
# --------------------------------------------------

df["decimalLatitude"] = pd.to_numeric(df["decimalLatitude"], errors="coerce")

df["decimalLongitude"] = pd.to_numeric(df["decimalLongitude"], errors="coerce")


# --------------------------------------------------
# REMOVE INVALID RECORDS
# --------------------------------------------------

df = df.dropna(subset=["scientificName", "decimalLatitude", "decimalLongitude"])

df = df.drop_duplicates(subset=["id"])


# --------------------------------------------------
# SAVE
# --------------------------------------------------

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT, index=False)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n================================")
print("OBIS DATASET CREATED")
print("================================")

print("Records:", len(df))

print("Unique species:", df["scientificName"].nunique())

print("\nTop species:")

print(df["scientificName"].value_counts().head(10))

print("\nSaved to:")

print(OUTPUT)
