import urllib.request
import time
from bs4 import BeautifulSoup
import pathlib

# Base URL template for each letter section
base_url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from="
sections = ["0"] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# User-Agent Header
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
headers = {'User-Agent': user_agent}

# Directory to save the HTML files
directory = pathlib.Path('billboard_articles')

directory.mkdir(parents=True, exist_ok=True)
print(f'directory created at{directory}')

# Collect all song links
all_songs = []

# Iterate over sections to scrape URLs
for section in sections:
    url = base_url + section
    try:
        # Request the page with the custom User-Agent
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.read(), "html.parser")

        # Find all category groups
        category_groups = soup.find_all("div", {"class": "mw-category-group"})
        if category_groups:
            for group in category_groups:
                links = group.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href:  # Only process if href exists
                        full_url = "https://en.wikipedia.org" + href
                        song_title = link.text.strip()
                        all_songs.append((song_title, full_url))
                        print(f"{song_title} appended to list")

        else:
            print(f"No category groups found for URL: {url}")

        time.sleep(0.25)

    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for URL: {url}")
    except Exception as e:
        print(f"Error: {e} for URL: {url}")

# Save HTML for each song
for song_title, song_url in all_songs:
    try:
        request = urllib.request.Request(song_url, headers=headers)
        response = urllib.request.urlopen(request)
        if response.status == 200:
            # Create a safe filename
            safe_title = "".join(c if c.isalnum() else "_" for c in song_title)
            filename = directory / f"{safe_title}.html"

            # Write the HTML content to a file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.read().decode('utf-8'))
            print(f"Saved: {song_title}")

    except Exception as e:
        print(f"Failed to save {song_title}: {e}")

print(f"Total songs collected: {len(all_songs)}")
