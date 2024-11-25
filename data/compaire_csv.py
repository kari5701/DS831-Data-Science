import pandas as pd

# Load the datasets
final_scrape_path = 'final_scrape.csv'
song_details_with_artists_path = 'song_details_with_artists.csv'

final_scrape_df = pd.read_csv(final_scrape_path)
song_details_with_artists_df = pd.read_csv(song_details_with_artists_path)

# Extract the Title columns from both datasets
titles_in_final_scrape = set(final_scrape_df['Title'].dropna())
titles_in_song_details = set(song_details_with_artists_df['Title'].dropna())

# Find common titles
common_titles = titles_in_final_scrape.intersection(titles_in_song_details)

# Find unique titles in each dataset
unique_to_final_scrape = titles_in_final_scrape - titles_in_song_details
unique_to_song_details = titles_in_song_details - titles_in_final_scrape

# Summary of comparison
comparison_summary = {
    "Total Titles in final_scrape": len(titles_in_final_scrape),
    "Total Titles in song_details_with_artists": len(titles_in_song_details),
    "Common Titles": len(common_titles),
    "Unique to final_scrape": len(unique_to_final_scrape),
    "Unique to song_details_with_artists": len(unique_to_song_details)
}

# Display comparison summary
print(comparison_summary)

# Save all unique titles from song_details_with_artists
unique_titles_list = list(unique_to_song_details)

# Display the list
unique_titles_df = pd.DataFrame(unique_titles_list, columns=["Unique Titles"])
print(unique_titles_df)
