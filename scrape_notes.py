import requests  # Imports the requests library to send HTTP requests
from bs4 import BeautifulSoup  # Imports BeautifulSoup for parsing HTML
import pandas as pd  # Imports pandas for data manipulation and storage
import time  # Imports time to add delays between requests

# Base URL for Wikipedia page, allowing substitution of the section
url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"

# Define sections from A-Z and 0-9 for navigating different pages of the category
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

# List to store all song titles and URLs
all_songs = []

# Loop through each section (A-Z and 0-9) to gather songs
for section in sections:
    # Format the URL with the current section letter/number
    url = url.format(section)
    # Make an HTTP GET request to fetch the page's HTML content
    html = requests.get(url)
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html.text, 'html.parser')

    # Find all category groups on the page (each group contains song links)
    category_groups = soup.find_all('div', class_='mw-category-group')

    # Loop through each category group to extract song links
    for group in category_groups:
        # Find all 'a' tags within the group (each represents a song link)
        songs = group.find_all('a')
        for song in songs:
            # Get song title and URL from each 'a' tag
            song_title = song.get_text()
            song_url = "https://en.wikipedia.org" + song.get('href')
            # Append the song title and URL as a tuple to all_songs
            all_songs.append((song_title, song_url))

# Print the total number of songs collected
print(f"Total songs collected: {len(all_songs)}")


# Function to extract details from an individual song page
def extract_song_details(url):
    # Send HTTP request to the song URL and parse the HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize dictionary with default fields for song details
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

    # Extract and store the song title from the page's main heading
    song_details["Title"] = soup.find('h1', {"id": "firstHeading"}).text.strip()

    # Locate the infobox on the page, which contains song metadata
    infobox = soup.find('table', class_='infobox')
    if infobox:
        # Iterate over each row in the infobox table to find metadata
        for row in infobox.find_all('tr'):
            header = row.find('th')  # Column header (e.g., Artist, Genre)
            value = row.find('td')  # Column value (e.g., artist name, genre type)

            # Check if both header and value are present in the row
            if header and value:
                header_text = header.text.strip()  # Get the text of the header

                # Store data based on header text (e.g., "Artist" -> Artist(s))
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

    # Return the collected song details as a dictionary
    return song_details

# List to store details of all songs
all_song_details = []
for title, song_url in all_songs:
    try:
        # Extract details for each song using the extract_song_details function
        song_data = extract_song_details(song_url)
        all_song_details.append(song_data)  # Append details to list
        print(f"Extracted data for: {title}")
    except Exception as e:
        # Print an error message if data extraction fails
        print(f"Failed to extract data for {title}: {e}")

    # Add a 0.5-second delay to avoid overwhelming Wikipedia's servers
    time.sleep(0.5)

# Create a pandas DataFrame from the collected song details
df = pd.DataFrame(all_song_details)
# Save the DataFrame to a CSV file
df.to_csv('billboard_hot_100_song_details.csv', index=False)
print("Data has been saved to billboard_hot_100_song_details.csv")
