import requests
import pandas as pd
from pathlib import Path

OBIS_API = "https://api.obis.org/v3"


def get_occurrences(scientific_name=None, limit=100):

    url = f"{OBIS_API}/occurrence"

    params = {"scientificname": scientific_name, "size": limit}

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def save_occurrences(data):

    records = data["results"]

    df = pd.DataFrame(records)

    output_path = Path("data/raw/obis")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "occurrences.csv"

    df.to_csv(file_path, index=False)

    print(f"Saved {len(df)} records to:")
    print(file_path)


if __name__ == "__main__":
    data = get_occurrences(scientific_name="Thunnus", limit=100)

    save_occurrences(data)
