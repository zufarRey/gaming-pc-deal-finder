import requests

import os


api_key = os.getenv("KLAZ_KEY")
url = "https://api.kleinanzeigen-agent.de/api/v2/kleinanzeigen/search"
header = {
    "klaz_key": api_key

}
params = {
    "q": "gaming pc",
    "size": 5,
    "max_price": 750
}

respones = requests.get(url, params=params, headers=header)

print(respones)
