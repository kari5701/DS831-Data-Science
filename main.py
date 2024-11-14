import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"

# Sections from A-Z and 0-9
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

all_songs = []

# Loop through each section
for section in sections:
    url = url.format(section)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    category_groups = soup.find_all('div', class_='mw-category-group')

    # Loop
    for group in category_groups:
        # Find all 'a' tags
        songs = group.find_all('a')
        for song in songs:
            # Extract song title and URL
            song_title = song.get_text()
            song_url = "https://en.wikipedia.org" + song.get('href')
            all_songs.append((song_title, song_url))
            print(f"Title: {song_title}, URL: {song_url}")

import pandas as pd

df = pd.DataFrame(all_songs, columns=['Title', 'URL'])
df.to_csv('billboard_hot_100_songs.csv', index=False)
