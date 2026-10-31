import json
import requests
import os
from pathlib import Path


def fetch_data():
    api_key = os.getenv("KLAZ_KEY")

    url = "https://api.kleinanzeigen-agent.de/api/v2/kleinanzeigen/search"
    header = {
        "klaz_key": api_key

    }
    params = {
        "q": "gaming pc",
        "size": 50,
        "min_price": 250,
        "max_price": 750,
        "category_id": "228"

    }

    response = requests.get(url, params=params, headers=header)

    # real Data
    data = response.json()

    with open("data/raw_ads.json", "w")as file:
        json.dump(data, file, indent=4)
    return data


def load_snapshot_data():
    project_root = Path(__file__).parent.parent
    data_path = project_root/"data/raw_ads.json"
    with open(data_path, "r") as file:
        snapshot_data = json.load(file)

    return snapshot_data
