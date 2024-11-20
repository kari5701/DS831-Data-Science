import requests
import urllib
from bs4 import BeautifulSoup
import os
import sys
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

    time.sleep(0.25)

#Option to name output csv
csv_name = "final_scrape3"



df = pd.DataFrame(all_song_details)
df.to_csv(f'{csv_name}.csv', index=False)
print(f"{len(df)}Datapoints has been saved to {csv_name}.csv")