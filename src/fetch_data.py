import json
import requests
import os


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
    with open("data/raw_ads.json", "r") as file:
        snapshot_data = json.load(file)

    return snapshot_data


snapshot = load_snapshot_data()
print(type(snapshot))
