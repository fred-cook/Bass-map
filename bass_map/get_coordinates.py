import os
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import requests
from tqdm import tqdm

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API")
PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API is missing! Set it in .env or GitHub Secrets.")


def create_query(row: pd.Series) -> str:
    """
    Create a query from the pub information to pass
    in to the Google maps API
    """
    if (pub_name := row['name']) == "Navigation":
        # the Google api tries to start navigation and returns
        # the wrong result
        pub_name = "Navig"
    return f"{pub_name} pub, {row['place']}, {row['region']}"


def get_coords(bass_df: pd.DataFrame) -> pd.DataFrame:
    """
    Query the google maps API to get the coords of every pub
    in bass_df. Add latitude and longitude columns
    """
    lats: list[float] = []
    lngs: list[float] = []
    for _, row in tqdm(
        bass_df.iterrows(), total=len(bass_df), desc=f"Fetching pub coords: {bass_df['status'].unique()}"
    ):
        params = {"query": create_query(row), "key": GOOGLE_API_KEY}
        r = requests.get(PLACES_URL, params=params).json()

        if r["status"] == "OK" and len(r["results"]):
            pub = r["results"][0]
            lat = pub["geometry"]["location"]["lat"]
            lng = pub["geometry"]["location"]["lng"]
        else:
            print(f"{row['name']} pub had no results")
            lat, lng = float("nan"), float("nan")
        lats.append(lat)
        lngs.append(lng)
    bass_df["latitude"] = lats
    bass_df["longitude"] = lngs
    return bass_df

def create_cache() -> dict[str, dict[str, float]]:
    """
    If pub locations have been run before create a lookup
    dictionary of the query to find that pub and its coords
    """
    existing_csvs: list[pd.DataFrame] = []
    if (existing_data_path := Path("pub_locations")).exists():
        for file in [f for f in existing_data_path.iterdir() if f.stem == ".csv"]:
            existing_csvs.append(pd.read_csv(file))
    if len(existing_csvs):
        cache = {}
        df = pd.concat(existing_csvs)
        for _, row in df.iterrows():
            query = create_query(row)
            cache[query] = {"lat": row["latitude"], "lng": row["longitude"]}
            
