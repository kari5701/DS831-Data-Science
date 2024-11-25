import requests
from bs4 import BeautifulSoup

# Function to extract song details from individual song pages
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
            if header and 'description' in header.get('class', []) and ("Single by" in header.text or "Song by" in header.text):
                # Only get the names from <a> tags within this header, excluding "Single"
                artist_links = header.find_all('a')
                if artist_links:
                    song_details["Artist(s)"] = ', '.join(
                        artist.text for artist in artist_links if artist.text not in ["Single", "Song"])

    return song_details