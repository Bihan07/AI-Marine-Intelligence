import pandas as pd
import folium
from folium.plugins import MarkerCluster

# -----------------------------------------
# LOAD DATA
# -----------------------------------------

FILE = "data/raw/obis_fish.csv"

df = pd.read_csv(FILE)

print("Loaded:", len(df), "observations")


# -----------------------------------------
# CREATE MAP
# -----------------------------------------

center_lat = df["decimalLatitude"].mean()
center_lon = df["decimalLongitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon], zoom_start=4, tiles="CartoDB positron"
)


# -----------------------------------------
# MARKER CLUSTER
# -----------------------------------------

cluster = MarkerCluster().add_to(m)


# -----------------------------------------
# ADD OBSERVATIONS
# -----------------------------------------

for _, row in df.iterrows():
    species = row["scientificName"]

    latitude = row["decimalLatitude"]
    longitude = row["decimalLongitude"]

    popup = f"""
    <b>Species:</b> {species}<br>
    <b>Genus:</b> {row.get("genus", "Unknown")}<br>
    <b>Family:</b> {row.get("family", "Unknown")}<br>
    <b>Location:</b> {row.get("locality", "Unknown")}<br>
    <b>Date:</b> {row.get("eventDate", "Unknown")}<br>
    <b>Depth:</b> {row.get("depth", "Unknown")}
    """

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=5,
        popup=folium.Popup(popup, max_width=350),
        fill=True,
        fill_opacity=0.7,
    ).add_to(cluster)


# -----------------------------------------
# SAVE
# -----------------------------------------

output = "data/processed/obis_map.html"

m.save(output)

print("\nMap created successfully!")

print("Saved to:")
print(output)
