import pathlib
import pandas as pd
import re

# Remove citations and brackets
def remove_citations(text):
    if pd.isna(text):
        return text
    return re.sub(r'\[.*?]', '', text).strip()

# Remove extra commas
def remove_extra_commas(text):
    if pd.isna(text):
        return text
    return re.sub(r'\s*,\s*', ', ', text).strip(', ')

def remove_country_mentions(text):
    if pd.isna(text):
        return text
    # Remove text within parentheses, including the parentheses
    return re.sub(r'\([^)]*\)', '', text).strip()

# Clean the Release Date column
def clean_date(date):
    if pd.isna(date):
        return None
    date = re.sub(r'\(.*?\)|\(\)', '', date).strip()
    try:
        parsed_date = pd.to_datetime(date, errors='coerce')
        if pd.notna(parsed_date):
            return parsed_date.strftime('%B %d, %Y')
    except Exception:
        pass
    return date

# Clean song lengths
def clean_song_lengths(df, column_name):
    def extract_single_version(length_str):
        if pd.isna(length_str):
            return length_str
        length_str = str(length_str)
        versions = re.findall(r'(\d+:\d+)\s*\(.*?single version.*?\)', length_str, re.IGNORECASE)
        if versions:
            return versions[0]
        time_match = re.search(r'\d+:\d+', length_str)
        return time_match.group() if time_match else length_str.strip()

    df[column_name] = df[column_name].apply(extract_single_version)
    return df

# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")

# Import existing scrape CSV as DataFrame
df = pd.read_csv(csv_path, encoding='utf-8')

# Clean the 'Release Date' column
df['Release Date'] = df['Release Date'].apply(remove_citations)
df['Release Date'] = df['Release Date'].apply(remove_country_mentions)

# Clean the 'Genres' column
df['Genres'] = df['Genres'].apply(remove_citations)
df['Genres'] = df['Genres'].apply(remove_extra_commas)

# Clean the 'Length' column
df = clean_song_lengths(df, 'Length')

# Clean the "Label" column
df['Label'] = df['Label'].apply(remove_country_mentions)

# Overwrite the same file with cleaned data
df.to_csv(csv_path, index=False)

print(f"{len(df)} Datapoints have been updated, cleaned and saved to {csv_path}")
