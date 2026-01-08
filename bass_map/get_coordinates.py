import os
from pathlib import Path
import time

from dotenv import load_dotenv
import pandas as pd
import requests
from tqdm import tqdm

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
SEARCH_URL = "https://api.geoapify.com/v1/geocode/search"

MAX_REQUESTS_PER_SECOND = 5
MIN_REQUEST_INTERVAL = 1.0 / MAX_REQUESTS_PER_SECOND

if not GEOAPIFY_API_KEY:
    raise RuntimeError("GEOAPIFY_API_KEY is missing! Set it in .env or GitHub Secrets.")


def create_query(row: pd.Series) -> str:
    """
    Create a text query based on the pub's name, town and region
    """
    return f"{row['name']} pub, {row['place']}, {row['region']}, UK"


def get_coords(
    bass_df: pd.DataFrame, cache: dict[str, dict[str, float]] | None = None
) -> pd.DataFrame:
    """
    Query Geoapify Place Search API to get pub coordinates.
    Rate-limited to 5 requests / second.
    """
    lats: list[float] = []
    lngs: list[float] = []

    last_request_time = 0.0

    for _, row in tqdm(
        bass_df.iterrows(),
        total=len(bass_df),
        desc=f"Fetching pub coords: {bass_df['status'].unique()}",
    ):
        query = create_query(row)

        if cache is not None and (cached := cache.get(query)) is not None:
            lat = cached["lat"]
            lng = cached["lng"]

        else:
            # ---- rate limiting ----
            now = time.monotonic()
            elapsed = now - last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - elapsed)

            last_request_time = time.monotonic()

            params = {
                "text": query,
                "format": "json",
                "apiKey": GEOAPIFY_API_KEY,
                "filter": "countrycode:gb",
                "limit": 1,
            }

            r = requests.get(SEARCH_URL, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()

            if not data.get("results"):
                print(f"{row['name']} pub had no results")
                lat, lng = float("nan"), float("nan")
            else:
                result = data["results"][0]
                lat, lng = result["lat"], result["lon"]

        lats.append(lat)
        lngs.append(lng)

    bass_df["latitude"] = lats
    bass_df["longitude"] = lngs
    return bass_df


def create_cache() -> dict[str, dict[str, float]] | None:
    """
    If pub locations have been run before create a lookup
    dictionary of the query to find that pub and its coords
    """
    existing_csvs: list[pd.DataFrame] = []
    if (existing_data_path := Path("./pub_locations")).exists():
        for file in [f for f in existing_data_path.iterdir() if f.suffix == ".csv"]:
            existing_csvs.append(pd.read_csv(file))
    if len(existing_csvs):
        cache = {}
        df = pd.concat(existing_csvs)
        for _, row in df.iterrows():
            query = create_query(row)
            cache[query] = {"lat": row["latitude"], "lng": row["longitude"]}
        return cache
