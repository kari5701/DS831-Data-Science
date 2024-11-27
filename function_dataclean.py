import pathlib
import pandas as pd
import re

# Function to clean citation markers from text
def remove_citations(text):
    if pd.isna(text):
        return text
    return re.sub(r'\[\d+]', '', text).strip()

# Function to clean citation markers with commas
def remove_citationswcommas(text):
    if pd.isna(text):
        return text
    return re.sub(r'\[\d+]', '', text).strip()

# Function to clean extra commas
def remove_extra_commas(text):
    if pd.isna(text):
        return text
    cleaned_text = re.sub(r' ,', '', text)
    return cleaned_text.strip(', ')

# Function to clean the song lengths
def clean_song_lengths(df, column_name):
    def extract_single_version(length_str):
        if pd.isna(length_str):
            return length_str
        length_str = str(length_str)
        versions = re.findall(r'\d+:\d+\s*\([^)]+\)', length_str)
        if not versions:
            return length_str.strip()
        for version in versions:
            if 'single version' in version.lower():
                return re.search(r'\d+:\d+', version).group()
        return re.search(r'\d+:\d+', versions[0]).group()

    df[column_name] = df[column_name].apply(extract_single_version)
    return df

# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")

# Import existing scrape CSV as DataFrame
final_scrape = pd.read_csv(csv_path, encoding='utf-8')

# Clean the 'Release Date' column
final_scrape['Release Date'] = final_scrape['Release Date'].apply(remove_citations)

# Clean the 'Genres' column
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_citationswcommas)
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_extra_commas)

# Clean the 'Length' column
final_scrape = clean_song_lengths(final_scrape, 'Length')

# Overwrite the same file with cleaned data
final_scrape.to_csv(csv_path, index=False)

print(f"{len(final_scrape)} Datapoints have been updated, cleaned and saved to {csv_path}")
