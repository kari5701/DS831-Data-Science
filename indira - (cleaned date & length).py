
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime

# Base URL template for each letter section
base_url = "https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles&from={}"
sections = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

all_songs = []

# Scrape the list of songs
for section in sections:
    url = base_url.format(section)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    category_groups = soup.find_all("div", class_="mw-category-group")

    for group in category_groups:
        group_letter = group.find("h3").text.strip()
        if group_letter.startswith(section) or section == "0-9":
            links = group.find_all('a')
            for link in links:
                href = link.get('href')
                if href and link.text.startswith(section):
                    full_url = "https://en.wikipedia.org" + href
                    song_title = link.text.strip()
                    all_songs.append((song_title, full_url))

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

                if "Released" in header_text:
                    song_details["Release Date"] = value.text.strip()
                elif "Genre" in header_text:
                    song_details["Genres"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Length" in header_text:
                    song_details["Length"] = value.text.strip()
                elif "Label" in header_text:
                    song_details["Label"] = value.get_text(separator=', ').strip()
                elif "Songwriter" in header_text:
                    song_details["Songwriters"] = ', '.join(
                        part.strip() for part in value.get_text(separator=',').split(',') if part.strip())
                elif "Producer" in header_text:
                    song_details["Producers"] = ', '.join(
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

    time.sleep(0.5)

df = pd.DataFrame(all_song_details)

# Cleaning the Release Date column
def clean_date(date):
    if pd.isna(date):
        return None

    date = re.sub(r'\(.*?\)', '', date).strip()

    try:
        parsed_date = pd.to_datetime(date, errors='coerce', dayfirst=False)
        if pd.notna(parsed_date):
            return parsed_date.strftime('%B %d, %Y')  # Format: Month Day, Year
    except Exception:
        pass

    return date

df['Release Date'] = df['Release Date'].apply(clean_date)

# Cleaning the Length column
def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except Exception:
        return 0

def seconds_to_time(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"

def clean_length(length):
    if pd.isna(length):
        return None

    length = re.sub(r'\(.*?\)', '', length).strip()

    if "single version" in length.lower():
        match = re.search(r'(\d+:\d{2})', length)
        if match:
            return match.group(1)

    if '/' in length or ';' in length or 'and' in length:
        parts = re.split(r'[;/and]', length)
        total_seconds = 0
        for part in parts:
            match = re.search(r'(\d+:\d{2})', part)
            if match:
                total_seconds += time_to_seconds(match.group(1))

        if total_seconds > 0:
            return seconds_to_time(total_seconds)

    match = re.search(r'(\d+:\d{2})', length)
    if match:
        return match.group(1)

    return length

df['Length'] = df['Length'].apply(clean_length)


df.to_csv('final_scrape_cleaned.csv', index=False)
print("Data has been cleaned and saved to final_scrape_cleaned.csv")
