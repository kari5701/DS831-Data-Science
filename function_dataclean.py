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
df =  pd.read_csv(csv_path, encoding='utf-8')

# Clean the 'Release Date' column
df['Release Date'] = df['Release Date'].apply(remove_citations)

# Clean the 'Genres' column
df['Genres'] = df['Genres'].apply(remove_citationswcommas) 

# clean the "Genres" column for extra commas
df['Genres'] = df['Genres'].apply(remove_extra_commas)

# Clean the 'Length' column
df['length'] = df['length'].apply(clean_song_lengths)

#Option to name output csv
output_csv_name = "final_scrape"

output_csv_path = pathlib.Path("data") / output_csv_name


# Save the cleaned data to a new CSV file
df.to_csv(f'{output_csv_path}', index=False)

print(f"{len(df)} rows has been cleaned and saved to {output_csv_path}.csv")


