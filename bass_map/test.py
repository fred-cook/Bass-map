from pathlib import Path

import pandas as pd

# create a random df and save it to output.csv
out_dir = Path("outputs")
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Saving test.csv to {str(out_dir)}")
df = pd.DataFrame({"a": range(10), "b": list("abcdefghij")})
df.to_csv(out_dir / "test.csv", index=False)

for f in Path(out_dir).iterdir():
    print(f.absolute())