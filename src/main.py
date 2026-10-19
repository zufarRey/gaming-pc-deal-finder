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

# test Data
data = {
    "success": True,
    "message": "Synthetic test data",
    "data": {
        "meta": {
            "page": 1,
            "size": 9,
            "total": 9
        },
        "ads": [
            {
                "ad_id": "test001",
                "title": "Gaming PC mit RTX 3070",
                "description": "Intel Core i5-12400F, 16 GB RAM und 1 TB SSD.",
                "price": {
                    "amount": 650
                },
                "location": {
                    "city": "Frankfurt am Main"
                },
                "created_at": "2026-10-19T10:00:00.000Z",
                "ad_url": "https://example.com/test001"
            },
            {
                "ad_id": "test002",
                "title": "Starker Gaming PC",
                "description": "Verbaut sind Ryzen 5 5600 und eine RX 6700 XT sowie RAM: 32 GB.",
                "price": {
                    "amount": 600
                },
                "location": {
                    "city": "Darmstadt"
                },
                "created_at": "2026-10-19T10:01:00.000Z",
                "ad_url": "https://example.com/test002"
            },
            {
                "ad_id": "test003",
                "title": "Gaming Rechner GTX-1660 Super",
                "description": "Gaming PC mit i7 10700K, 2x8 GB RAM und SSD.",
                "price": {
                    "amount": 500
                },
                "location": {
                    "city": "Mainz"
                },
                "created_at": "2026-10-19T10:02:00.000Z",
                "ad_url": "https://example.com/test003"
            },
            {
                "ad_id": "test004",
                "title": "Gaming Computer komplett",
                "description": "Leistungsstarker Rechner mit R7 5800X3D, DDR4 2x16GB und SSD.",
                "price": {
                    "amount": 700
                },
                "location": {
                    "city": "Wiesbaden"
                },
                "created_at": "2026-10-19T10:03:00.000Z",
                "ad_url": "https://example.com/test004"
            },
            {
                "ad_id": "test005",
                "title": "Gaming PC RTX 3060",
                "description": "Gaming PC in gutem Zustand mit Ryzen Prozessor und 16 GB DDR4.",
                "price": {
                    "amount": 550
                },
                "location": {
                    "city": "Offenbach"
                },
                "created_at": "2026-10-19T10:04:00.000Z",
                "ad_url": "https://example.com/test005"
            },
            {
                "ad_id": "test006",
                "title": "Gaming PC mit RX 6600",
                "description": "32 GB DDR5 5600 RAM, 1 TB NVMe SSD und Gaming Mainboard.",
                "price": {
                    "amount": 500
                },
                "location": {
                    "city": "Hanau"
                },
                "created_at": "2026-10-19T10:05:00.000Z",
                "ad_url": "https://example.com/test006"
            },
            {
                "ad_id": "test007",
                "title": "Gaming PC RTX 4060",
                "description": "AMD Ryzen 5 4600G mit DDR5 32 GB und 1 TB SSD.",
                "price": {
                    "amount": 600
                },
                "location": {
                    "city": "Bad Homburg"
                },
                "created_at": "2026-10-19T10:06:00.000Z",
                "ad_url": "https://example.com/test007"
            },
            {
                "ad_id": "test008",
                "title": "High End Gaming PC RX 6800 XT",
                "description": "Intel Core i5-12600KF mit 2 x 16 GB DDR4 und 2 TB SSD.",
                "price": {
                    "amount": 740
                },
                "location": {
                    "city": "Aschaffenburg"
                },
                "created_at": "2026-10-19T10:07:00.000Z",
                "ad_url": "https://example.com/test008"
            },
            {
                "ad_id": "test009",
                "title": "Gaming PC mit RTX 3070 8GB",
                "description": "RTX 3070 8GB GDDR6 verbaut, SSD vorhanden.",
                "price": {
                    "amount": 620
                },
                "location": {
                    "city": "Frankfurt am Main"
                },
                "created_at": "2026-10-19T10:08:00.000Z",
                "ad_url": "https://example.com/test009"
            }
        ]
    },
    "request_id": "synthetic-test"
}

# real Data
# data = respones.json()

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
# print(cleaned_ads)

price_filtered_ads = []
for x in cleaned_ads:
    if x["price"] <= 750 and x["price"] >= 250:
        price_filtered_ads.append(x)
# print("vergleich gefiltert", price_filtered_ads)

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


pattern_gpu = r"(RTX|GTX|RX)[-\s]*\d{4}[-\s]*(TI|Super|XTX|XT)?"
# Zur errinenrung (||) kann wörter unterscheiden und als option sehen
# [] kann nur ein einziges zeichen als option sehen
pattern_cpu_intel = r"(Intel Core)?\s?i[3579][-\s]*\d{4,5}(KF|F|K|T)?"
pattern_cpu_ryzen = r"\b(Ryzen|R)\s?[3579][-\s]*\d{4}(x3d|xt|x|g)?"
pattern_ram = r"(\d{1,2}\s*GB\s*(RAM|ARBEITSSPEICHER)|(RAM|ARBEITSSPEICHER):?\s*\d{1,2}\s*GB)|(\d{1,2}\s*GB\s*DDR[45])|(DDR[45][-\s]*\d{1,2}\s*GB)|(\d\s*x\s*\d{1,2}\s*GB\s*(ARBEITSSPEICHER|RAM|DDR[45])|DDR[45]\s*\d\s*x\s*\d{1,2}\s*GB)"

gpu_scores = {
    "RTX2060SUPER": 60,
    "RTX2070": 60,
    "RTX2070SUPER": 65,
    "RTX2080": 70,
    "RTX2080SUPER": 75,
    "RTX2080TI": 80,

    "RTX3060TI": 75,
    "RTX3070": 80,
    "RTX3070TI": 80,
    "RTX3080TI": 95,
    "RTX4070": 95,
    "RTX4060": 70,
    "RTX5060": 80,

    "GTX1050": 10,
    "GTX1050TI": 20,
    "GTX1060": 30,
    "GTX1070": 40,
    "GTX1070TI": 45,
    "GTX1080": 45,
    "GTX1080TI": 55,
    "GTX1630": 10,
    "GTX1650": 25,
    "GTX1650SUPER": 35,
    "GTX1660": 40,
    "GTX1660SUPER": 45,
    "GTX1660TI": 45,

    "RX5500XT": 35,
    "RX5600XT": 50,
    "RX5700": 55,
    "RX5700XT": 60,
    "RX6400": 20,
    "RX6500XT": 25,
    "RX6600": 60,
    "RX6600XT": 70,
    "RX6650XT": 70,
    "RX6700": 75,
    "RX6700XT": 80,
    "RX6750XT": 85,
    "RX6800": 90,
    "RX6800XT": 95,
    "RX6900XT": 100,
    "RX6950XT": 100,
    "RX7600": 70,
    "RX7600XT": 75,
    "RX7700XT": 90,
    "RX7800XT": 100
}

cpu_scores = {
    # AMD Ryzen 2000
    "RYZEN52600": 45,
    "RYZEN52600X": 47,
    "RYZEN72700": 50,
    "RYZEN72700X": 52,

    # AMD Ryzen 3000
    "RYZEN33100": 45,
    "RYZEN33300X": 55,
    "RYZEN53600": 60,
    "RYZEN53600X": 62,
    "RYZEN53600XT": 63,
    "RYZEN73700X": 65,
    "RYZEN73800X": 67,
    "RYZEN73800XT": 68,
    "RYZEN93900X": 70,
    "RYZEN93950X": 72,

    # AMD Ryzen 4000 / 5000
    "RYZEN54500": 52,
    "RYZEN55500": 62,
    "RYZEN55600G": 65,
    "RYZEN55600": 75,
    "RYZEN55600X": 77,

    "RYZEN75700G": 68,
    "RYZEN75700X": 80,
    "RYZEN75800X": 82,
    "RYZEN75800X3D": 95,

    "RYZEN95900X": 84,
    "RYZEN95950X": 85,

    # AMD Ryzen 7000
    "RYZEN57600": 90,
    "RYZEN57600X": 92,
    "RYZEN77700": 94,
    "RYZEN77700X": 95,
    "RYZEN77800X3D": 100,

    # Intel 9th Gen
    "I59400F": 42,
    "I59600K": 50,
    "I79700": 55,
    "I79700K": 58,
    "I99900K": 65,

    # Intel 10th Gen
    "I310100F": 45,
    "I510400": 60,
    "I510400F": 60,
    "I510600K": 65,
    "I510600KF": 65,
    "I710700": 70,
    "I710700F": 70,
    "I710700K": 72,
    "I710700KF": 72,
    "I910900K": 76,

    # Intel 11th Gen
    "I511400": 65,
    "I511400F": 65,
    "I511600K": 70,
    "I511600KF": 70,
    "I711700": 72,
    "I711700F": 72,
    "I711700K": 74,
    "I711700KF": 74,

    # Intel 12th Gen
    "I312100F": 70,
    "I512400": 80,
    "I512400F": 80,
    "I512600K": 88,
    "I512600KF": 88,
    "I712700": 90,
    "I712700F": 90,
    "I712700K": 92,
    "I712700KF": 92,

    # Intel 13th Gen
    "I313100F": 75,
    "I513400": 85,
    "I513400F": 85,
    "I513600K": 95,
    "I513600KF": 95,
    "I713700K": 98,
    "I713700KF": 98,

    # Intel 14th Gen
    "I514400": 86,
    "I514400F": 86,
    "I514600K": 97,
    "I514600KF": 97,
    "I714700K": 100,
    "I714700KF": 100
}

for x in text_filtered_ads:
    unnormed_gpu = re.search(pattern_gpu, x["description"], re.IGNORECASE)
    if unnormed_gpu is not None:
        unnormed_gpu = unnormed_gpu.group()
    if unnormed_gpu is None:
        unnormed_gpu = re.search(pattern_gpu, x["title"], re.IGNORECASE)
        if unnormed_gpu is not None:
            unnormed_gpu = unnormed_gpu.group()

    normed_gpu = None

    if unnormed_gpu is not None:
        unnormed_gpu = re.sub(r"\s", "", unnormed_gpu)
        unnormed_gpu = re.sub("-", "", unnormed_gpu)
        normed_gpu = unnormed_gpu.upper()

    x["gpu"] = normed_gpu
    x["gpu_score"] = gpu_scores.get(x["gpu"])

    normed_cpu = None
    unnormed_cpu_intel = re.search(
        pattern_cpu_intel, x["description"], re.IGNORECASE)
    if unnormed_cpu_intel is None:
        unnormed_cpu_intel = re.search(
            pattern_cpu_intel, x["title"], re.IGNORECASE)

    if unnormed_cpu_intel is not None:
        unnormed_cpu_intel = unnormed_cpu_intel.group()
        unnormed_cpu_intel = unnormed_cpu_intel.upper()
        unnormed_cpu_intel = re.sub(r"INTEL CORE", "", unnormed_cpu_intel)
        unnormed_cpu_intel = re.sub(r"-", "", unnormed_cpu_intel)
        unnormed_cpu_intel = re.sub(r"\s", "", unnormed_cpu_intel)

        normed_cpu = unnormed_cpu_intel

    if normed_cpu is None:
        unnormed_cpu_ryzen = re.search(
            pattern_cpu_ryzen, x["description"], re.IGNORECASE)
        if unnormed_cpu_ryzen is None:
            unnormed_cpu_ryzen = re.search(
                pattern_cpu_ryzen, x["title"], re.IGNORECASE)
        if unnormed_cpu_ryzen is not None:
            unnormed_cpu_ryzen = unnormed_cpu_ryzen.group()
            unnormed_cpu_ryzen = unnormed_cpu_ryzen.upper()
            unnormed_cpu_ryzen = re.sub(
                r"^R([3579])", r"RYZEN\1", unnormed_cpu_ryzen)
            unnormed_cpu_ryzen = re.sub(r"\s", "", unnormed_cpu_ryzen)
            unnormed_cpu_ryzen = re.sub(r"-", "", unnormed_cpu_ryzen)
            normed_cpu = unnormed_cpu_ryzen
    x["cpu"] = normed_cpu
    x["cpu_score"] = cpu_scores.get(x["cpu"])

    normed_ram = None

    unnormed_ram = re.search(pattern_ram, x["description"], re.IGNORECASE)
    if unnormed_ram is None:
        unnormed_ram = re.search(pattern_ram, x["title"], re.IGNORECASE)

    if unnormed_ram is not None:
        unnormed_ram = unnormed_ram.group()
        unnormed_ram = unnormed_ram.upper()
        unnormed_ram = re.sub(r"DDR[45]", "", unnormed_ram)
        ram_number = re.findall(r"\d+", unnormed_ram)

        if "X" in unnormed_ram:
            normed_ram = int(ram_number[0]) * int(ram_number[1])

        else:
            normed_ram = int(ram_number[0])
    x["ram_gb"] = normed_ram


print(text_filtered_ads)
