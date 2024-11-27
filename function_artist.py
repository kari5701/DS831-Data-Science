from bs4 import BeautifulSoup

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
            try:
                if header and value:
                    header_text = header.text.strip()

                    if "Released" in header_text:
                        song_details["Release Date"] = value.text.strip()
                    elif "Genre" in header_text:
                        song_details["Genres"] = value.text.strip()
                    elif "Length" in header_text:
                        song_details["Length"] = value.text.strip()
                    elif "Label" in header_text:
                        song_details["Label"] = value.text.strip()
                    elif "Songwriter" in header_text:
                        song_details["Songwriters"] = value.text.strip()
                    elif "Producer" in header_text:
                        song_details["Producers"] = value.text.strip()
                    elif "Lyricist" in header_text:
                        song_details["Lyricist(s)"] = value.text.strip()
                    elif "Composer" in header_text:
                        song_details["Composer(s)"] = value.text.strip()
                        
                # Extract artist(s) information
                if header and 'description' in header.get('class', []) and ("Single by" in header.text or "Song by" in header.text):
                    artist_links = header.find_all('a')
                    if artist_links:
                        song_details["Artist(s)"] = ', '.join(
                            artist.text for artist in artist_links if artist.text not in ["Single", "Song"])
            except Exception as e:
                print(f"Error: {e} for URL: {filepath}")

    return song_details

