import requests
from bs4 import BeautifulSoup
import sys
import os
import pandas as pd
import time

# Base URL template for each letter section
base_url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

all_songs = []

for section in sections:
    url = base_url.format(section)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    category_groups = soup.find_all("div", class_="mw-category-group")

    for group in category_groups:
        group_letter = group.find("h3").text.strip()
        # adding songs if group_letter starts with the category letter
        if group_letter.startswith(section) or section == "0-9":
            links = group.find_all('a')
            for link in links:
                href = link.get('href')
                if href and link.text.startswith(section):
                    full_url = "https://en.wikipedia.org" + href
                    song_title = link.text.strip()
                    all_songs.append((song_title, full_url))

print(f"Total songs collected: {len(all_songs)}")

# Add functions directory
sys.path.append(os.path.join(os.path.dirname(__file__), "scrape"))

# Import the function
from function_artist import extract_song_details

all_song_details = []
for song_title, song_url in all_songs:
    try:
        song_data = extract_song_details(song_url)
        all_song_details.append(song_data)
        print(f"Extracted data for: {song_title}")
    except Exception as e:
        print(f"Failed to extract data for {song_title}: {e}")

    time.sleep(0.5)

df = pd.DataFrame(all_song_details)
df.to_csv('final_scrape.csv', index=False)
print("Data has been saved to final_scrape.csv")