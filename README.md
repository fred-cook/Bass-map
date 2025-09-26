# Bass-map
A small script that reads from the [National Bass Directory](https://nationalbassdirectory.wordpress.com/), uses Google maps' API to find the pubs coordinates and outputs a CSV that can be uploaded to a personal Google map

## Running

The script is set up to run in Github workflows at 1pm on the first of every month. This should automatically update the `permanent_locations.csv` and `guest_locations.csv` in the root of the repository. However you can also run it locally by following these steps:

1. Make sure you have UV installed, this can be achieved with `pip install uv` if you already have python, or by following the instructions [here](https://docs.astral.sh/uv/getting-started/installation/)
2. Create a google maps API key for youself