from bs4 import BeautifulSoup
import os
import sys
import pandas as pd

# Add functions directory
sys.path.append(os.path.join(os.path.dirname(__file__), "scrape"))
sys.path.append(os.path.join(os.path.dirname(__file__), "data_clean"))

def extract_song_details_from_file(filepath):

    # Read the local HTML file
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Initialize a dictionary to store song details
    song_details = {
        "Title": "",
        "Artist(s)": "",
        "Release Date": "",
        "Genres": "",
        "Length": "",
        "Label": "",
        "Songwriters": "",
        "Producers": "",
        "Lyricist(s)": "",
        "Composer(s)": "",
    }

    # Extract the title
    title_element = soup.find('h1', {"id": "firstHeading"})
    if title_element:
        song_details["Title"] = title_element.text.strip()

    # Defining the infobox
    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            value = row.find('td')

            if header and value:
                header_text = header.text.strip()

                if "Released" in header_text:
                    song_details["Release Date"] = value.text.strip()
                elif "Genre" in header_text:
                    song_details["Genres"] = value.text.strip()
                elif "Length" in header_text:
                    song_details["Length"] = value.text.strip()
                elif "Label" in header_text:
                    song_details["Label"] = value.get_text(separator=', ').strip()
                elif "Songwriter" in header_text:
                    song_details["Songwriters"] = value.text.strip()
                elif "Producer" in header_text:
                    song_details["Producers"] = value.text.strip()
                elif "Lyricist" in header_text:
                    song_details["Lyricist"] = value.text.strip()
                elif "Composer" in header_text:
                    song_details["Composer"] = value.text.strip()

            # Extract artist(s) information
            if header and 'description' in header.get('class', []) and ("Single by" in header.text or "Song by" in header.text):
                artist_links = header.find_all('a')
                if artist_links:
                    song_details["Artist(s)"] = ', '.join(
                        artist.text for artist in artist_links if artist.text not in ["Single", "Song"])

    return song_details

# HTML Directory
directory_path = '/billboard_articles/'

# Collect all song details
all_song_details = []
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        filepath = os.path.join(directory_path, filename)
        details = extract_song_details_from_file(filepath)
        all_song_details.append(details)


# Option to name output CSV
CSV_name = 'song_details_with_artists.csv'

# Save results to a CSV file
df = pd.DataFrame(all_song_details)
output_csv_path = '/data/{CSV_name}'
df.to_csv(output_csv_path, index=False)

print(f"Data extraction complete. Saved to {output_csv_path}")

