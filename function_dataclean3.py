import pathlib
import pandas as pd
import re

# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")

# Import existing scrape CSV as DataFrame
df = pd.read_csv(csv_path, encoding='utf-8')

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

# Function to remove country mentions such as (US) and (UK)
def remove_country_mentions(text):
    if pd.isna(text):
        return text
    return re.sub(r'\([^)]*\)', '', text).strip()

# Function to add a comma+space after a lowercase letter followed by an uppercase letter
def comma_and_space(text):
    if pd.isna(text):
        return text
    return re.sub(r'([a-z\d])([A-Z])', r'\1, \2', text)

# Function to remove text like [4] and [5]
def squarebracket_number(text):
    if pd.isna(text):
        return text
    return re.sub(r'\[\d+\]', '', text).strip()

# Function to handle UK dates
def ditch_UK_date(text):
    if pd.isna(text):
        return text
    match = re.search(r'(.*?)(?=\s*\(US\))', text)
    if match:
        return match.group(1).strip()
    return text

# Clean the 'Release Date' column
df['Release Date'] = df['Release Date'].apply(remove_citations)

# Clean the 'Genres' column
df['Genres'] = df['Genres'].apply(remove_citationswcommas)
df['Genres'] = df['Genres'].apply(remove_extra_commas)

# Format 'Songwriters' column
df['Songwriters'] = df['Songwriters'].apply(comma_and_space)

# Ditch UK date format
df['Release Date'] = df['Release Date'].apply(ditch_UK_date)

# Remove country mentions
df['Release Date'] = df['Release Date'].apply(remove_country_mentions)

# Remove square bracket numbers
df['Release Date'] = df['Release Date'].apply(squarebracket_number)

# Clean the 'Length' column
df = clean_song_lengths(df, 'Length')

# Merge 'Lyricist(s)' and 'Composer(s)' into 'Producers' column with linebreaks
df['Producers'] = df['Lyricist(s)'].fillna('') + '\n' + df['Composer(s)'].fillna('')

# Clean up to avoid unintended formatting issues:
# Remove any extra spaces, commas, or newlines at the beginning or end of the string
df['Producers'] = df['Producers'].str.replace(r'\n+', '\n', regex=True).str.strip()

# Drop the 'Lyricist(s)' and 'Composer(s)' columns
df = df.drop(columns=['Lyricist(s)', 'Composer(s)'])


# Save the cleaned data
output_csv_name = "final_scrape22.csv"
output_csv_path = pathlib.Path("data") / output_csv_name

df.to_csv(output_csv_path, index=False)

print(f"{len(df)} rows have been cleaned and saved to {output_csv_path}")
