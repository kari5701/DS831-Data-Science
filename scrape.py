import requests
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL template for each letter section
base_url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from="
sections = ["0"]+[chr(i) for i in range(ord('A'), ord('Z') + 1)]


# Creating empty list to hold urls to scrape:
urlList = list()

all_songs = []

# Appending suffixes to URLs:
for item in sections:
    urlList.append(base_url + str(item))

# Setup user-agent header for making requests
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
headers = {'User-Agent': user_agent}

# Inroduce empty list to append scraped urls to
all_songs =[]

# Iterate over the generated URLs in urlList
for url in urlList:
    try:
        # Make the request with the custom User-Agent header
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.read(), "lxml")

        # Find the first category group containing the links
        category_group = soup.find("div", {"class": "mw-category-group"})

        # If the category group is found, process the links
        if category_group:
            links = category_group.find_all('a')
            for link in links:
                href = link.get('href')
                if href:  # Only process if href exists
                    full_url = "https://en.wikipedia.org" + href
                    song_title = link.text.strip()
                    all_songs.append((song_title, full_url))
                    print(f"{song_title} appended to list")
        else:
            print(f"Category group not found for URL: {url}")

        # Wait to avoid karma issues
        time.sleep(0.5)

    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for URL: {url}")


print(f"Total song links collected: {len(all_songs)}")


# Function to extract song details from individual song pages
def extract_song_details(url):
    """Takes url to wikipage and extracts song details: Title, Artist, Release Date, Genre, Length, Label, Songwriters, Producers, Composers, Lyricists """
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
        "Producers": "",
        "Composers": "",
        "Lyricists": ""
    }

    song_details["Title"] = soup.find('h1', {"id": "firstHeading"}).text.strip()
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
                    song_details["Genres"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Length" in header_text:
                    song_details["Length"] = value.text.strip()
                elif "Label" in header_text:
                    song_details["Label"] = value.get_text(separator=', ').strip()
                elif "Songwriter(s)" in header_text:
                    song_details["Songwriters"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Producer(s)" in header_text:
                    song_details["Producers"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Composer(s)" in header_text:
                    song_details["Composers"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Lyricist(s)" in header_text:
                    song_details["Lyricists"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())

            if header and 'description' in header.get('class', []) and ("Single by" in header.text or "Song by" in header.text):
                artist_links = header.find_all('a')
                if artist_links:
                    song_details["Artist(s)"] = ', '.join(
                        artist.text for artist in artist_links if artist.text not in ["Single", "Song"])
    return song_details


all_song_details = []
for song_title, song_url in all_songs:
    try:
        song_data = extract_song_details(song_url)
        all_song_details.append(song_data)
        print(f"Extracted data for: {song_title}")
    except Exception as e:
        print(f"Failed to extract data for {song_title}: {e}")

    time.sleep(0.25)

#Option to name output csv
csv_name = "final_scrape3"



df = pd.DataFrame(all_song_details)
df.to_csv(f'{csv_name}.csv', index=False)
print(f"{len(df)}Datapoints has been saved to {csv_name}.csv")