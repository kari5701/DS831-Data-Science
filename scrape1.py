import pathlib
import pandas as pd
from function_artist import song_details
import re

# HTML Directory
directory_path = pathlib.Path('billboard_articles')

# Collect all song details
all_song_details = []
for filepath in directory_path.glob('*.html'):
    details = song_details(filepath)
    all_song_details.append(details)
    print(f"Extracted data for: {filepath.name}")

# Option to name output CSV with an extension
csv_name = "html_scrape.csv"

# Create filepath for saving CSV
csv_path = pathlib.Path("data") / csv_name

# Save results to a CSV file in the correct directory
df = pd.DataFrame(all_song_details)
csv_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure 'data' directory exists
df.to_csv(csv_path, index=False)

# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")

# Import existing scrape CSV as DataFrame
df = pd.read_csv(csv_path, encoding='utf-8')

# Apply your chainable `.str` operations

# Remove citations and brackets in 'Title' column
df['Title'] = df['Title'].str.replace(r'\[.*?\]', '', regex=True)

# Remove country mentions (text within parentheses, including the parentheses)
df['Title'] = df['Title'].str.replace(r'\([^)]*\)', '', regex=True)

# Remove extra commas in 'Title' column
df['Title'] = df['Title'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')

# Clean the 'Release Date' column
df['Release Date'] = df['Release Date'].str.extract(r'(.*?)(?=\s*\(US\))')[0].fillna(df['Release Date'])
df['Release Date'] = df['Release Date'].str.replace(r'\(.*?\)|\(\)', '', regex=True).str.strip()
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce').dt.strftime('%B %d, %Y').fillna(df['Release Date'])

# Clean song lengths to extract single version length or the first time match
df['Length'] = df['Length'].str.extract(r'(\d+:\d+)\s*\(.*?single version.*?\)', re.IGNORECASE)[0].fillna(
    df['Length'].str.extract(r'(\d+:\d+)')[0].fillna(df['Length']))

# Clean the "Release Date" column
df['Release Date'] = df['Release Date'].str.replace(r'\[.*?\]', '', regex=True)
df['Release Date'] = df['Release Date'].str.extract(r'(.*?)(?=\s*\(US\))')[0].fillna(df['Release Date'])
df['Release Date'] = df['Release Date'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# Clean the 'Genres' column
df['Genres'] = df['Genres'].str.replace(r'\[.*?\]', '', regex=True)
df['Genres'] = df['Genres'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')

# Clean the "Label" column to remove country mentions
df['Label'] = df['Label'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# Clean the "Songwriters" column
df['Songwriters'] = df['Songwriters'].str.replace(r'\[.*?\]', '', regex=True).str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')

# Clean the "Producers" column
df['Producers'] = df['Producers'].str.replace(r'\[.*?\]', '', regex=True).str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')
df['Producers'] = df['Producers'].str.replace(r'\n+', '\n', regex=True).str.strip()

# Merge "Composer(s)" and "Lyricist(s)" into "Producers"
df['Producers'] = df[df.columns[7:]].apply(
    lambda x: ', '.join(x.dropna().astype(str)), 
    axis=1
)

df = df.drop(columns=[df.columns[8], df.columns[9]])


# Save cleaned data to the same CSV file
df.to_csv(csv_path, index=False)

print(f"{len(df)} Datapoints have been updated, cleaned, and saved to {csv_path}")