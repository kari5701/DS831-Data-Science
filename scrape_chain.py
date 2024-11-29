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

# - Remove citations (text in square brackets).
# - Remove country mentions (text in parentheses, including the parentheses).
# - Remove extra spaces and trailing commas for cleaner formatting.
df['Title'] = df['Title'].str.replace(r'\[.*?\]', '', regex=True)  # Remove citations
df['Title'] = df['Title'].str.replace(r'\([^)]*\)', '', regex=True)  # Remove country mentions
df['Title'] = df['Title'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')  # Clean commas and spaces

# Remove UK-specific date formats (extract text before "(US)")
df['Release Date'] = df['Release Date'].str.extract(r'(.*?)(?=\s*\(US\))')[0].fillna(df['Release Date'])  # Extract date before "(US)"

# Remove citations and text in parentheses
df['Release Date'] = df['Release Date'].str.replace(r'\[.*?\]', '', regex=True)  # Remove citations
df['Release Date'] = df['Release Date'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()  # Remove parentheses

# Convert to datetime and format to "Month DD, YYYY"
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')  # Convert to datetime
df['Release Date'] = df['Release Date'].dt.strftime('%B %d, %Y').fillna(df['Release Date'])  # Format date

# - Extract the length if "single version" is mentioned.
df['Length'] = df['Length'].str.extract(r'(\d+:\d+)\s*\(.*?single version.*?\)', re.IGNORECASE)[0].fillna(
    df['Length'].str.extract(r'(\d+:\d+)')[0].fillna(df['Length'])
)

# - Remove citations and clean extra spaces or commas.
df['Genres'] = df['Genres'].str.replace(r'\[.*?\]', '', regex=True)  # Remove citations
df['Genres'] = df['Genres'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')  # Clean commas and spaces

# - Remove text in parentheses to get rid of country mentions.
df['Label'] = df['Label'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# - Remove citations and clean extra spaces or commas.
df['Songwriters'] = df['Songwriters'].str.replace(r'\[.*?\]', '', regex=True)  # Remove citations
df['Songwriters'] = df['Songwriters'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')  # Clean commas and spaces

# - Remove citations, clean extra spaces, and handle multiple lines properly.
df['Producers'] = df['Producers'].str.replace(r'\[.*?\]', '', regex=True)  # Remove citations
df['Producers'] = df['Producers'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')  # Clean commas and spaces
df['Producers'] = df['Producers'].str.replace(r'\n+', '\n', regex=True).str.strip()  # Handle newlines

# - Combine the values from 'Lyricist(s)' and 'Composer(s)' into a single 'Producers' column.
df['Producers'] = df['Lyricist(s)'].fillna('') + '\n' + df['Composer(s)'].fillna('')

# - Remove 'Lyricist(s)' and 'Composer(s)' columns since they are now merged into 'Producers'.
df = df.drop(columns=['Lyricist(s)', 'Composer(s)'])
