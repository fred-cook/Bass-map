from pathlib import Path

from bass_map.get_coordinates import get_coords
from bass_map.get_pdf import download_master_bass_directory
from bass_map.parse_bass_directory import get_tables

filename = "bass_directory.pdf"

download_master_bass_directory(filename=filename)
bass_df = get_tables(filename=filename)

permanent_bass_df = get_coords(bass_df[bass_df["status"] == "Perm"])
guest_bass_df = get_coords(bass_df[bass_df["status"] == "Guest"])

out_dir = Path("outputs")
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Saving permanent Bass locations to {str(out_dir)}")
permanent_bass_df.to_csv(out_dir / "permanent_locations.csv", index=False)
print(f"Saving guest Bass locations to {str(out_dir)}")
guest_bass_df.to_csv(out_dir / "guest_locations.csv", index=False)

for f in Path(out_dir).iterdir():
    print(f.absolute())