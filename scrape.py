import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL with placeholder for the section
base_url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"

# Sections from A-Z and 0-9
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

# List to store all song URLs and titles
all_songs = []

# Step 1: Scrape all song links from the category page
for section in sections:
    url = base_url.format(section)  # Format URL with the section
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Find the category groups containing song links
    category_groups = soup.find_all("div", class_="mw-category-group")

    # Loop through each group to find song links
    for group in category_groups:
        # Each category group has a heading (h3) that indicates the letter
        group_letter = group.find("h3").text.strip()

        # Only process links starting with the current section letter
        if not group_letter.startswith(section) and section != "0-9":
            # Stop processing further if songs don't match the intended letter
            break

        links = group.find_all('a')
        for link in links:
            href = link.get('href')
            if href and link.text.startswith(section):  # Only process songs starting with the section letter
                full_url = "https://en.wikipedia.org" + href
                song_title = link.text.strip()
                all_songs.append((song_title, full_url))  # Store title and URL as tuple

print(f"Total songs collected: {len(all_songs)}")


def extract_song_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a dictionary to store song details
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

    # Title from the page header
    song_details["Title"] = soup.find('h1', {"id": "firstHeading"}).text.strip()

    # Locate the infobox
    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            value = row.find('td')

            # Primary infobox rows (e.g., Genre, Length, Label, Songwriters, Producers)
            if header and value:
                header_text = header.text.strip()

                if "Released" in header_text:
                    song_details["Release Date"] = value.text.strip()
                elif "Genre" in header_text:
                    song_details["Genres"] = ', '.join(part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Length" in header_text:
                    song_details["Length"] = value.text.strip()
                elif "Label" in header_text:
                    song_details["Label"] = value.get_text(separator=', ').strip()
                elif "Songwriter" in header_text:
                    song_details["Songwriters"] = ', '.join(part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Producer" in header_text:
                    song_details["Producers"] = ', '.join(part.strip() for part in value.get_text(separator=',').split(',') if part.strip())

            # Look for artist information in the header with keywords indicating it's a single by certain artists
            if header and 'description' in header.get('class', []) and "Single by" in header.text:
                # Only get the names from <a> tags within this header, excluding "Single"
                artist_links = header.find_all('a')
                if artist_links:
                    song_details["Artist(s)"] = ', '.join(artist.text for artist in artist_links if artist.text != "Single")

    return song_details


# Step 2: Visit each song's page and collect detailed data
all_song_details = []
for song_title, song_url in all_songs:
    try:
        song_data = extract_song_details(song_url)
        all_song_details.append(song_data)
        print(f"Extracted data for: {song_title}")
    except Exception as e:
        print(f"Failed to extract data for {song_title}: {e}")

    time.sleep(0.5)  # Delay to avoid overloading the server

# Step 3: Save the collected data to a CSV file
df = pd.DataFrame(all_song_details)
df.to_csv('billboard_hot_100_song_details_2.csv', index=False)
print("Data has been saved to billboard_hot_100_song_details.csv")