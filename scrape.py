import pathlib
import pandas as pd
from function_artist import song_details
import re
from datetime import datetime

'''Comment out from here to test second part'''

# # HTML Directory
# directory_path = pathlib.Path('billboard_articles')

# # Collect all song details
# all_song_details = []
# for filepath in directory_path.glob('*.html'):
#     details = song_details(filepath)
#     all_song_details.append(details)
#     print(f"Extracted data for: {filepath.name}")

# # Option to name output CSV with an extension
# csv_name = "html_scrape.csv"

# # Create filepath for saving CSV
# csv_path = pathlib.Path("data") / csv_name

# # Save results to a CSV file in the correct directory
# df = pd.DataFrame(all_song_details)
# csv_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure 'data' directory exists
# df.to_csv(csv_path, index=False)



'''Comment out to here to test second part''' 



# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")

# Import existing scrape CSV as DataFrame
df = pd.read_csv(csv_path, encoding='utf-8')

# create a backup for safe measure, and to compare under the way.
df_backup = df.copy()

# Clean the 'Title' column
print('Cleaning the "Title" column:')

# Remove text within parentheses, including the parentheses
df['Title'] = df['Title'].str.replace(r'\([^)]*\)', '', regex=True)

print(f'"{df_backup.iloc[8,0]}" cleaned to: \n"{df.iloc[8,0]}" and so on..\n')

# Clean the 'Release Date' column #
df['Release Date'] = df['Release Date'].str.extract(r'(.*?)(?=\s*\(US\))')[0].fillna(df['Release Date'])
df['Release Date'] = df['Release Date'].str.replace(r'\(.*?\)|\(\)', '', regex=True).str.strip()
df['Release Date'] = df['Release Date'].str.replace(r'\[.*?\]', '', regex=True)
df['Release Date'] = df['Release Date'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce').dt.strftime('%Y %M, %D').fillna(df['Release Date'])

# Standardize all dates to ISO 8601 format with to_datetime
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce', dayfirst=True)

print(df.dtypes)

print(df.iloc[14,7:])

print(f'"{df_backup.iloc[14,2]}" cleaned to: \n"{df.iloc[14,2]}" and so on..\n')

# Clean song lengths to
print('Cleaning the "Length" column:')

# extract single version length or the first time match
df['Length'] = df['Length'].str.extract(r'(\d+:\d+)\s*\(.*?single version.*?\)', re.IGNORECASE)[0].fillna(
    df['Length'].str.extract(r'(\d+:\d+)')[0].fillna(df['Length']))

print(f'"{df_backup.iloc[8,4]}" cleaned to: \n"{df.iloc[8,4]}" and so on..\n')


# Clean the "Genres" column
print('Cleaning the "Genres" column:')

df['Genres'] = df['Genres'].str.replace(r'\[.*?\]', '', regex=True) # removing brackets
df['Genres'] = df['Genres'].str.replace(r',\s', ',', regex=True) # removing extra commas substituting with a comma
df['Genres'] = df['Genres'].str.replace(r',+', ', ', regex=True) # removing more than one comma and replacing with one comma and a space
df['Genres'] = df['Genres'].str.rstrip(" ") # removing trailing spaces
df['Genres'] = df['Genres'].str.rstrip(",") # removing trailing commas

print(f'"{df_backup.iloc[5,3]}" cleaned to: \n"{df.iloc[5,3]}" and so on..\n')


# Clean the "Label" column
print('Cleaning the "Label" column:')

df['Label'] = df['Label'].str.replace(r'\[.*?\]', '', regex=True) # removing brackets
df['Label'] = df['Label'].str.replace(r',\s*,+', ', ', regex=True) # removing extra commas

print(f'"{df_backup.iloc[30,5]}" cleaned to: \n"{df.iloc[30,5]}" and so on..\n')

# Clean the "Songwriters" column
print('Cleaning the "Songwriters" column:')

df['Songwriters'] = df['Songwriters'].str.replace(r'\[.*?\]', '', regex=True) # removing brackets
df['Songwriters'] = df['Songwriters'].str.replace(r' and,', '', regex=True) # removing ocurrences of " and,"
df['Songwriters'] = df['Songwriters'].str.replace(r' ,+', ', ', regex=True) # removing extra commas
df['Songwriters'] = df['Songwriters'].str.replace(r',\s', ',', regex=True) # removing extra commas substituting with a comma
df['Songwriters'] = df['Songwriters'].str.replace(r',+', ', ', regex=True) # removing more than one comma and replacing with one comma and a space
df['Songwriters'] = df['Songwriters'].str.replace(r'\W\W+', ', ', regex=True) # removing non word charector and more nonwordcharectorsand replacing with one comma and a space
df['Songwriters'] = df['Songwriters'].str.rstrip(" ") # removing trailing spaces
df['Songwriters'] = df['Songwriters'].str.rstrip(",") # removing trailing commas

print(f'"{df_backup.iloc[79,6]}" cleaned to: \n"{df.iloc[79,6]}" and so on..\n')


# Clean the "Producers" column
print('Cleaning the "Producers" column:')

df['Producers'] = df['Producers'].str.replace(r'\[.*?\]', '', regex=True)
df['Producers'] = df['Producers'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')
df['Producers'] = df['Producers'].str.replace(r'\n+', '\n', regex=True).str.strip()

print(f'"{df_backup.iloc[72,7]}" cleaned to: \n"{df.iloc[72,7]}" and so on..\n')


# Merge 'Lyricist(s)' and 'Composer(s)' into 'Producers' column with linebreaks
print('Merging "Lyricist(s)" and "Composer(s)" into "Producers" column:')

df['Producers'] = df['Lyricist(s)'].fillna('') + '\n' + df['Composer(s)'].fillna('')

print(f'"{df_backup.iloc[68,8]} "and"\n {df_backup.iloc[68,9]}" Merged to: \n"{df.iloc[68,7]}" and so on..\n')


print('Dropping the "Lyricist(s)" and "Composer(s)" columns ')
# Drop the 'Lyricist(s)' and 'Composer(s)' columns
df = df.drop(columns=['Lyricist(s)', 'Composer(s)'])


# Create filepath for saving CSV
output_csv_path = pathlib.Path("data") / "html_cleaned.csv"

# Save cleaned data to the new CSV file
df.to_csv(output_csv_path, index=False)


print(f"{len(df)} rows have been updated, cleaned, and saved to {output_csv_path}")
