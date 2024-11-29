from bs4 import BeautifulSoup


def song_details(filepath):
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
        song_details["Title"] = title_element.get_text(strip=True)

    # Defining the infobox
    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            value = row.find('td')
            try:
                if header and value:
                    header_text = header.text.strip()
                    try:
                        if "Released" in header_text:
                            song_details["Release Date"] = value.get_text(strip=True)
                        elif "Genre" in header_text:
                            song_details["Genres"] = value.get_text(separator=', ', strip = True)
                        elif "Length" in header_text:
                            song_details["Length"] = value.get_text(strip = True)
                        elif "Label" in header_text:
                            song_details["Label"] = value.get_text(separator=', ', strip = True)
                        elif "Songwriter" in header_text:
                            song_details["Songwriters"] = value.get_text(separator=', ', strip = True)
                        elif "Producer" in header_text:
                            song_details["Producers"] = value.get_text(separator=', ', strip = True)
                        elif "Lyricist" in header_text:
                            song_details["Lyricist(s)"] = value.get_text(separator=', ', strip = True)
                        elif "Composer" in header_text:
                            song_details["Composer(s)"] = value.get_text(separator=', ', strip = True)
                    except Exception as e:
                        print(f"Error: {e} for URL: {filepath}")
                
                if header and 'description' in header.get('class', []) and (
                        "Single by" in header.text or "Song by" in header.text):
                    artist_links = header.find_all('a')
                    if artist_links:
                        artist_names = []
                        for artist in artist_links:
                            if artist.text not in ["Single", "Song"]:
                                artist_names.append(artist.text)
                        song_details["Artist(s)"] = ', '.join(artist_names)
            except Exception as e:
                print(f"Error: {e} for URL: {filepath}")

    return song_details

# Testbench:
# print(song_details('billboard_articles/7_Rings.html'))