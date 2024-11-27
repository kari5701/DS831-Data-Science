import os
import pandas as pd
from function_artist import extract_song_details_from_file

# HTML Directory
# Test test test test
directory_path = os.path.normpath('billboard_articles')

# Collect all song details
all_song_details = []
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        filepath = os.path.normpath(os.path.join(directory_path, filename))
        details = extract_song_details_from_file(filepath)
        all_song_details.append(details)
        print(f"Extracted data for: {filename}")

# Save results to a CSV file
csv_name = "html_scrape_edited_artist_function"

csv_path = os.path.normpath(os.path.join('data', f'{csv_name}.csv'))

df = pd.DataFrame(all_song_details)
df.to_csv(os.path.normpath(f'{csv_path}.csv'), index=False)

print(f"{len(df)} rows of info has been saved to {csv_path}.csv")
