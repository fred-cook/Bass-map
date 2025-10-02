import re

import camelot
import pandas as pd


HEADERS = [
    "region",
    "name",
    "place",
    "status",
    "last_sighted",
    "method",
    "notes",
]

mapper = {i: name for i, name in enumerate(HEADERS)}

methods = {
    "B": "Banked",
    "H": "Handpump",
    "G": "Gravity",
    "J": "Jug",
    "E": "Electric",
    "P": "Powered pump",
}


def get_tables(filename: str) -> pd.DataFrame:
    """
    Read the tables in the bass directory, convert the
    columns to have the correct headers, expand the pour
    methods and assign the region to all rows
    """
    print("Parsing bass directory into dataframe")
    tables = camelot.read_pdf(filename, pages="all")
    combined: list[pd.DataFrame] = []

    for table in tables:
        df = table.df
        # Removed pubs table either has that as first row, or has
        # year/month style values for first column.
        if df.iloc[0][0] == "Removed pubs" or re.fullmatch(
            "^\d{4}/(0[1-9]|1[0-2])$", df.iloc[0][0]
        ):
            break
        combined.append(df)

    bass_df = pd.concat(combined)
    bass_df = bass_df.rename(columns=mapper)

    # Add region to all columns
    bass_df.loc[bass_df["region"] == "", "region"] = float("nan")
    bass_df["region"] = bass_df["region"].ffill()
    # Expand the pour methods from initials
    bass_df["method"] = bass_df["method"].map(methods)

    return bass_df[bass_df["name"] != ""]
