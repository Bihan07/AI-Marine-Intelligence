import pandas as pd

FILE = "data/raw/obis_fish.csv"

print("Loading OBIS data...")

df = pd.read_csv(FILE)

print("\n==============================")
print("OBIS DATA CHECK")
print("==============================")

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique species:")
print(df["scientificName"].nunique())

print("\nTop 20 species:")
print(df["scientificName"].value_counts().head(20))

print("\nCoordinate range:")

print("Latitude:", df["decimalLatitude"].min(), "to", df["decimalLatitude"].max())

print("Longitude:", df["decimalLongitude"].min(), "to", df["decimalLongitude"].max())

print("\nMarine records:")

if "marine" in df.columns:
    print(df["marine"].value_counts())

print("\nDataset looks ready for the next step.")
