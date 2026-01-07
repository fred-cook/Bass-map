import calendar
from datetime import datetime

import requests


def create_urls():
    """
    Create the url for the current month's master bass directory
    """
    year = datetime.now().year
    month = datetime.now().month
    for extension in ["", "-1"]:
        yield f"https://nationalbassdirectory.wordpress.com/wp-content/uploads/{year}/{month:02d}/bass-master-directory-{calendar.month_name[month].lower()}-{year}{extension}.pdf"


def download_master_bass_directory(filename: str) -> None:
    """
    Save the bass directory under the given file name
    """
    for url in create_urls():
        p = requests.get(url)

        if p.status_code == 200:
            with open(filename, "wb") as fp:
                fp.write(p.content)
            print(f"Successfully downloaded the master bass directory to {filename}")
            return
    raise RuntimeError("Could not download the master bass directory, check the URLs")
