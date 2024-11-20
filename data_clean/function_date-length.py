import pandas as pd
import re


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
