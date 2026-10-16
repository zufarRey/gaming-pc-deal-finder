import requests

import os

import re

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

data = respones.json()

# print(data['success'])
# print(data['error_code'])
# print(data['message'])
# print(data["data"]['ads'])
# print(data['request_id'])
# print(data)

# title price city url
cleaned_ads = []
for x in data["data"]["ads"]:
    temp_dict = {
        "title": x["title"],
        "price": x["price"]["amount"],
        "city": x["location"]["city"],
        "url": x["ad_url"],
        "ad_id": x["ad_id"],
        "description": x["description"],
        "created_at": x["created_at"]

    }
    cleaned_ads.append(temp_dict)
print(cleaned_ads)

price_filtered_ads = []
for x in cleaned_ads:
    if x["price"] <= 750 and x["price"] >= 250:
        price_filtered_ads.append(x)
print("vergleich gefiltert", price_filtered_ads)

text_filtered_ads = []
text_filter_criteria = ["defekt", "bastler", "ersatzteil", "teileträger",
                        "ohne funktion", "funktioniert nicht", "ohne grafikkarte", "ohne gpu", "nur gehäuse"]
for x in price_filtered_ads:
    bad_ads = False
    title = x["title"].lower()
    description = x["description"].lower()
    for exclusion__keyword in text_filter_criteria:
        if exclusion__keyword in title or exclusion__keyword in description:
            bad_ads = True
            break
    if bad_ads is False:
        text_filtered_ads.append(x)

pattern = r"(RTX|GTX|RX)[-\s]*\d{4}[-\s]*(TI|Super|XTX|XT)?"
