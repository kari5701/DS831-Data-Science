import pathlib
import pandas as pd
from function_artist import song_details

# HTML Directory
directory_path = pathlib.Path('billboard_articles')

# Collect all song details
all_song_details = []
for filepath in directory_path.glob('*.html'):
    details = song_details(filepath)
    all_song_details.append(details)
    print(f"Extracted data for: {filepath.name}")

# Option to name output CSV with an extension
csv_name = "html_scrape.csv"

# Create filepath for saving CSV
csv_path = pathlib.Path("data") / csv_name

# Save results to a CSV file in the correct directory
df = pd.DataFrame(all_song_details)
csv_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure 'data' directory exists
df.to_csv(csv_path, index=False)

print(f"{len(df)} rows of info has been saved to {csv_path}")

from function_dataclean import remove_citations, remove_citationswcommas, remove_extra_commas, clean_song_lengths