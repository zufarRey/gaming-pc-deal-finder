

import re

import pandas as pd
import fetch_data as fd
from pathlib import Path
import config as cfg
import hardware_scores as hs
import regex_patterns as rp


def clean_ads(raw_Data):
    cleaned_ads = []
    for x in raw_Data["data"]["ads"]:
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
    return cleaned_ads


def filter_ads_by_price(not_priced_filtered_ads):
    temp_price_filtered_ads = []
    for x in not_priced_filtered_ads:
        if x["price"] <= cfg.MAX_PRICE and x["price"] >= cfg.MIN_PRICE:
            temp_price_filtered_ads.append(x)
    return temp_price_filtered_ads


def filter_text_ads(unfiltered_text_ads):
    filtered_ads = []
    text_filter_criteria = ["defekt", "bastler", "ersatzteil", "teileträger",
                            "ohne funktion", "funktioniert nicht", "ohne grafikkarte", "ohne gpu", "nur gehäuse"]

    for x in unfiltered_text_ads:
        bad_ads = False
        title = x["title"].lower()
        description = x["description"].lower()
        for exclusion__keyword in text_filter_criteria:
            if exclusion__keyword in title or exclusion__keyword in description:
                bad_ads = True
                break
        if bad_ads is False:
            filtered_ads.append(x)
    return filtered_ads


def extract_gpu_data(ads):
    for x in ads:
        unnormed_gpu = re.search(
            rp.PATTERN_GPU, x["description"], re.IGNORECASE)
        if unnormed_gpu is not None:
            unnormed_gpu = unnormed_gpu.group()
        if unnormed_gpu is None:
            unnormed_gpu = re.search(rp.PATTERN_GPU, x["title"], re.IGNORECASE)
            if unnormed_gpu is not None:
                unnormed_gpu = unnormed_gpu.group()

        normed_gpu = None

        if unnormed_gpu is not None:
            unnormed_gpu = re.sub(r"\s", "", unnormed_gpu)
            unnormed_gpu = re.sub("-", "", unnormed_gpu)
            normed_gpu = unnormed_gpu.upper()

        x["gpu"] = normed_gpu
        x["gpu_score"] = hs.GPU_SCORES.get(x["gpu"])
    return ads


def extract_cpu_data(ads):

    for x in ads:

        normed_cpu = None
        unnormed_cpu_intel = re.search(
            rp.PATTERN_CPU_INTEL, x["description"], re.IGNORECASE)
        if unnormed_cpu_intel is None:
            unnormed_cpu_intel = re.search(
                rp.PATTERN_CPU_INTEL, x["title"], re.IGNORECASE)

        if unnormed_cpu_intel is not None:
            unnormed_cpu_intel = unnormed_cpu_intel.group()
            unnormed_cpu_intel = unnormed_cpu_intel.upper()
            unnormed_cpu_intel = re.sub(r"INTEL CORE", "", unnormed_cpu_intel)
            unnormed_cpu_intel = re.sub(r"-", "", unnormed_cpu_intel)
            unnormed_cpu_intel = re.sub(r"\s", "", unnormed_cpu_intel)

            normed_cpu = unnormed_cpu_intel

        if normed_cpu is None:
            unnormed_cpu_ryzen = re.search(
                rp.PATTERN_CPU_RYZEN, x["description"], re.IGNORECASE)
            if unnormed_cpu_ryzen is None:
                unnormed_cpu_ryzen = re.search(
                    rp.PATTERN_CPU_RYZEN, x["title"], re.IGNORECASE)
            if unnormed_cpu_ryzen is not None:
                unnormed_cpu_ryzen = unnormed_cpu_ryzen.group()
                unnormed_cpu_ryzen = unnormed_cpu_ryzen.upper()
                unnormed_cpu_ryzen = re.sub(
                    r"^R([3579])", r"RYZEN\1", unnormed_cpu_ryzen)
                unnormed_cpu_ryzen = re.sub(r"\s", "", unnormed_cpu_ryzen)
                unnormed_cpu_ryzen = re.sub(r"-", "", unnormed_cpu_ryzen)
                normed_cpu = unnormed_cpu_ryzen
        x["cpu"] = normed_cpu
        x["cpu_score"] = hs.CPU_SCORES.get(x["cpu"])
    return ads


def extract_ram_data(ads):
    for x in ads:
        normed_ram = None

        unnormed_ram = re.search(
            rp.PATTERN_RAM, x["description"], re.IGNORECASE)
        if unnormed_ram is None:
            unnormed_ram = re.search(rp.PATTERN_RAM, x["title"], re.IGNORECASE)

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
    return ads


# print(text_filtered_ads)


def filter_candidates(df):
    candidate_df = df[(df["gpu_score"] >= cfg.MIN_GPU_SCORE)
                      | (df["gpu_score"].isna())]
    candidate_df = candidate_df[(candidate_df["cpu_score"] >= cfg.MIN_CPU_SCORE) | (
        candidate_df["cpu_score"].isna())]
    return candidate_df


def sort_candidates(df):
    sorted_df = df.sort_values(
        ["gpu_score", "cpu_score", "price"], ascending=[False, False, True])
    return sorted_df


def export_candidates_to_csv(df):
    project_root = Path(__file__).parent.parent
    output_path = project_root / "output"/"candidate.csv"
    df.to_csv(output_path, index=False)


def main():

    data = fd.load_snapshot_data()
    # data = fd.fetch_data()
    cleaned_ads = clean_ads(data)
    price_filtered_ads = filter_ads_by_price(cleaned_ads)
    defect_filtered_ads = filter_text_ads(price_filtered_ads)
    gpu_enriched_ads = extract_gpu_data(defect_filtered_ads)
    cpu_enriched_ads = extract_cpu_data(gpu_enriched_ads)
    ram_enriched_ads = extract_ram_data(cpu_enriched_ads)
    df = pd.DataFrame(ram_enriched_ads)
    filtered_candidates = filter_candidates(df)
    sorted_df = sort_candidates(filtered_candidates)

    print(sorted_df[["price", "gpu", "gpu_score",
          "cpu", "cpu_score", "ram_gb"]])
    export_candidates_to_csv(sorted_df)


if __name__ == "__main__":
    main()
