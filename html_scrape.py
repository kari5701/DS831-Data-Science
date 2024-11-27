import os
import pandas as pd

from function_artist import extract_song_details_from_file

# HTML Directory
# Test test test test
directory_path = 'billboard_articles'

# Collect all song details
all_song_details = []
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        filepath = os.path.join(directory_path, filename)
        details = extract_song_details_from_file(filepath)
        all_song_details.append(details)
        print(f"Extracted data for: {filename}")

# Save results to a CSV file
csv_name = "html_scrape"

df = pd.DataFrame(all_song_details)
df.to_csv(f'{csv_name}.csv', index=False)
print(f"{len(df)}Datapoints has been saved to {csv_name}.csv")

from functions import remove_citations, remove_citationswcommas, remove_extra_commas, clean_song_lengths