import os
import pandas as pd

from function_artist import extract_song_details_from_file

# HTML Directory
directory_path = 'billboard_articles'

# Collect all song details
all_song_details = []
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        filepath = os.path.join(directory_path, filename)
        details = extract_song_details_from_file(filepath)
        all_song_details.append(details)

from datacleanfunctions import remove_citations, remove_citationswcommas, remove_extra_commas

# Save results to a CSV file
df = pd.DataFrame(all_song_details)
output_csv_path = 'song_details_with_artists1.csv'
df.to_csv(output_csv_path, index=False)

print(f"Data extraction complete. Saved to {output_csv_path}")

