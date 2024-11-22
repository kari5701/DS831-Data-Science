import os
import time
import pandas as pd
from bs4 import BeautifulSoup

# Directory containing HTML files
html_dir = "/Users/karinachristensen/Documents/GitHub/DS831-Data-Science/billboard_articles"

# Import the custom function to extract song details from HTML
from function_artist import extract_song_details

# List to hold extracted song details
all_song_details = []

# Iterate over the local HTML files
for file_name in os.listdir(html_dir):
    try:
        # Construct file path
        file_path = os.path.join(html_dir, file_name)

        # Open and parse the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, "lxml")

        # Extract song data using the custom function
        song_data = extract_song_details(soup)  # Pass the BeautifulSoup object
        all_song_details.append(song_data)

        print(f"Extracted data for: {file_name.replace('.html', '').replace('_', ' ')}")

    except Exception as e:
        print(f"Failed to extract data for {file_name}: {e}")

    # Optional delay to mimic scraping behavior
    time.sleep(0.25)

# Save the extracted data to a CSV
csv_name = "final_scrape_from_html"
df = pd.DataFrame(all_song_details)
df.to_csv(f"{csv_name}.csv", index=False)
print(f"{len(df)} data points have been saved to {csv_name}.csv")

# Import cleaning functions and clean the data
from datacleanfunctions import remove_citations, remove_citationswcommas, remove_extra_commas

# Apply cleaning functions
df_cleaned = df.copy()
df_cleaned = df_cleaned.applymap(remove_citations)  # Remove citations
df_cleaned = df_cleaned.applymap(remove_extra_commas)  # Remove extra commas

# Save cleaned data
cleaned_csv_name = "cleaned_final_scrape_from_html"
df_cleaned.to_csv(f"{cleaned_csv_name}.csv", index=False)
print(f"Cleaned data has been saved to {cleaned_csv_name}.csv")
