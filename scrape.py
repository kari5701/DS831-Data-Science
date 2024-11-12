import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"

# Sections from A-Z and 0-9
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

all_songs = []

for section in sections:
    url = url.format(section)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Category groups
    category_groups = soup.find_all('div', class_='mw-category-group')

    # Loop through each group to find song links
    for group in category_groups:
        # Find all 'a' tags within the group, which are the song links
        songs = group.find_all('a')
        for song in songs:
            # Extract song title and URL
            song_title = song.get_text()
            song_url = "https://en.wikipedia.org" + song.get('href')
            all_songs.append((song_title, song_url))

print(f"Total songs collected: {len(all_songs)}")


# Function to extract song details from individual song pages
def extract_song_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    song_details = {
        "Title": "",
        "Artist(s)": "",
        "Release Date": "",
        "Genres": "",
        "Length": "",
        "Label": "",
        "Songwriters": "",
        "Producers": ""
    }

    song_details["Title"] = soup.find('h1', {"id": "firstHeading"}).text.strip()

    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            value = row.find('td')

            if header and value:
                header_text = header.text.strip()

                if "Artist" in header_text:
                    song_details["Artist(s)"] = value.get_text(separator=', ').strip()
                elif "Released" in header_text:
                    song_details["Release Date"] = value.text.strip()
                elif "Genre" in header_text:
                    song_details["Genres"] = value.get_text(separator=', ').strip()
                elif "Length" in header_text:
                    song_details["Length"] = value.text.strip()
                elif "Label" in header_text:
                    song_details["Label"] = value.get_text(separator=', ').strip()
                elif "Songwriter" in header_text:
                    song_details["Songwriters"] = value.get_text(separator=', ').strip()
                elif "Producer" in header_text:
                    song_details["Producers"] = value.get_text(separator=', ').strip()

    return song_details

all_song_details = []
for title, song_url in all_songs:
    try:
        song_data = extract_song_details(song_url)
        all_song_details.append(song_data)
        print(f"Extracted data for: {title}")
    except Exception as e:
        print(f"Failed to extract data for {title}: {e}")

    time.sleep(0.5)

df = pd.DataFrame(all_song_details)
df.to_csv('billboard_hot_100_song_details.csv', index=False)
print("Data has been saved to billboard_hot_100_song_details.csv")
