from bass_map.get_coordinates import get_coords
from bass_map.get_pdf import download_master_bass_directory
from bass_map.parse_bass_directory import get_tables

filename = "bass_directory.pdf"

download_master_bass_directory(filename=filename)
bass_df = get_tables(filename=filename)

permanent_bass_df = get_coords(bass_df[bass_df["status"] == "Perm"])
guest_bass_df = get_coords(bass_df[bass_df["status"] == "Guest"])

print("Saving permanent Bass locations")
permanent_bass_df.to_csv("permanent_locations.csv", index=False)
print("Saving guest Bass locations")
guest_bass_df.to_csv("guest_locations.csv", index=False)