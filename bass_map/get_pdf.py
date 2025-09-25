import calendar
from datetime import datetime

import requests


def create_url() -> str:
    """
    Create the url for the current month's master bass directory
    """
    year = datetime.now().year
    month = datetime.now().month
    return f"https://nationalbassdirectory.wordpress.com/wp-content/uploads/{year}/{month:02d}/bass-master-directory-{calendar.month_name[month].lower()}-{year}.pdf"


def download_master_bass_directory(filename: str) -> None:
    """
    Save the bass directory under the given file name
    """
    p = requests.get(create_url())

    if p.status_code == 200:
        with open(filename, "wb") as fp:
            fp.write(p.content)
        print(f"Successfully downloaded the master bass directory to {filename}")
    else:
        p.raise_for_status()
