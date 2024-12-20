import pathlib
import pandas as pd
from src.Artist_Parse_func import song_details
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
csv_path.parent.mkdir(parents=True, exist_ok=True) 
df.to_csv(csv_path, index=False)


# Filepath for the existing file
csv_path = pathlib.Path("data/html_scrape.csv")



# Import existing scrape CSV as DataFrame
df = pd.read_csv(csv_path, encoding='utf-8')

# create a backup for safe measure, and to compare under the way.
df_backup = df.copy()


### Function to remove duplicates and return string as list

def deduplicate(cell):
    """Removes duplicates from string with ', 'separators and returns string."""
    items = cell.split(", ")  # Split valid strings
    return ", ".join(dict.fromkeys(items))  # Deduplicate and rejoin as string

# Clean the 'Title' column
print('Cleaning the "Title" column:')

# Remove text within parentheses, including the parentheses
df['Title'] = df['Title'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

print(f'"{df_backup.iloc[8,0]}" cleaned to: \n"{df.iloc[8,0]}" and so on..\n')


## Clean the "Release Date" Column

print('Cleaning the "Release Date" column:')
df['Release Date'] = (df['Release Date']
                      .str.replace(r'\(US.*', '', regex=True) # Remove anything after 'US'
                      .str.replace(r'.*?UK\)', '', regex=True) # Remove anything before and including 'UK'
                      .str.replace(r'\(.*?\)|\(\)', '', regex=True).str.strip() # Removes parenthesis
                      .str.replace(r'\[.*?\]', '', regex=True) # Removes brackets
                      .str.replace(r'\([^)]*\)', '', regex=True).str.strip()
                      .str.replace(r'(?<=\d{4}}).*', '', regex=True).str.strip() # Removes anything after \d\d\d\d using positive lookbehind
                      .str.replace(r'(\d{1,2})\s([A-Za-z]+)\s(\d{4})', r'\2 \1, \3', regex=True) # Identifies strings of "date month year" and rearranges them
                      .str.replace(r'(?<=[A-Za-z]\s)(?=\d{4})', '1, ', regex=True)  # Identifies places with "month year" and inserts "15, "
                      .str.replace(r'^(?=\d{4}$)', 'June 1, ', regex=True)) #Identifies places with only "year" and inserts  "June 1, "


# Standardize all dates to ISO 8601 format with to_datetime
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce', dayfirst=True)

print(f'converting datatype of {"Release Date"} column to {df.dtypes["Release Date"]}')
print(f'"{df_backup.iloc[196,2]}" cleaned to: \n"{df.iloc[196,2]}",')

print(f'"{df_backup.iloc[14,2]}" cleaned to: \n"{df.iloc[14,2]}" and so on..\n')

## Clean song "lengths" column
print('Cleaning the "Length" column:')

# extract single version length or the first time match
df['Length'] = df['Length'].str.extract(r'(\d+:\d+)\s*\(.*?single version.*?\)', re.IGNORECASE)[0].fillna(
    df['Length'].str.extract(r'(\d+:\d+)')[0].fillna(df['Length']))


# Standardize all time to ISO 8601 format with to_datetime
df['total_seconds'] = pd.to_datetime(df['Length'], format='%M:%S', errors='coerce')

df['Minutes'] = df.total_seconds.dt.minute
df['Seconds'] = df.total_seconds.dt.second

df['total_seconds'] = df['Minutes']*60 + df['Seconds']

df = df.drop(columns=['Minutes', 'Seconds'])

print(f'"{df_backup.iloc[8,4]}" cleaned to: \n"{df.iloc[8,4]}" and so on..\n')


## Clean the "Genres" column
print('Cleaning the "Genres" column:')

df['Genres'] = (df['Genres']
                .str.replace(r'\[.*?\]', '', regex=True) # removing brackets
                .str.replace(r',\s', ',', regex=True) # removing extra commas substituting with a comma
                .str.replace(r',+', ', ', regex=True) # removing more than one comma and replacing with one comma and a space
                .str.replace(r'-,\s', '', regex=True) # remove '-, ' 
                .str.rstrip(" ") # removing trailing spaces
                .str.rstrip(",")) # removing trailing commas
                            


print(f'"{df_backup.iloc[5,3]}" cleaned to: \n"{df.iloc[5,3]}" and so on..\n')


## Clean the "Label" column
print('Cleaning the "Label" column:')


df['Label'] = (df['Label']
               .str.replace(r'\(US.*', '', regex=True) # Remove anything after 'US'
               .str.replace(r'.*?UK\)', '', regex=True) # Remove anything before and including 'UK'
               .str.replace(r'\[.*?\]', '', regex=True) # removing brackets
               .str.replace(r'\(.*?\)', '', regex=True) # Remove content in parenthesis
               .str.replace(r',\s*,+', ', ', regex=True) # Clean up extra commas and spaces
               .str.strip(',') # Remove trailing/leading commas           
               .str.strip() # Remove trailing/leading whitespace
              )

print(f'"{df_backup.iloc[492,5]}" cleaned to: \n"{df.iloc[492,5]}" and so on..\n')

## Clean the "Songwriters" column
print('Cleaning the "Songwriters" column:')

df['Songwriters'] = (df['Songwriters']
                     .str.replace(r'\[.*?\]', '', regex=True) # removing brackets
                    .str.replace(r' and,', '', regex=True) # removing ocurrences of " and,"
                    .str.replace(r' ,+', ', ', regex=True) # removing extra commas
                    .str.replace(r',\s', ',', regex=True) # removing extra commas substituting with a comma
                    .str.replace(r',+', ', ', regex=True) # removing more than one comma and replacing with one comma and a space
                    .str.replace(r'\W\W+', ', ', regex=True) # removing non word charector and more nonwordcharectorsand replacing with one comma and a space
                    .str.rstrip(" ") # removing trailing spaces
                    .str.rstrip(",")) # removing trailing commas


print(f'returning: \n"{df.iloc[147,6]}" and so on..\n')

print(f'"{df_backup.iloc[79,6]}" cleaned to: \n"{df.iloc[79,6]}" and so on..\n')


# Merge 'Lyricist(s)' and 'Composer(s)' into 'Producers' column 

print('Merging "Producers", "Lyricist(s)" and "Composer(s)" into "Producers" column:')

print(f'"{df.iloc[144,8]} "and"\n {df.iloc[144,9]}" Merged with: \n"{df.iloc[144,7]}"')

# Merge 'Lyricist(s)' and 'Composer(s)' into 'Producers' with a comma separator
df['Producers'] = (df['Producers'].fillna('') + ', ' + 
                   df['Lyricist(s)'].fillna('') + ', ' + 
                   df['Composer(s)'].fillna('')).str.strip(', ')

print(f'"resulting in:\n"{df.iloc[144,7]}"\n')

# Clean the "Producers" column
print('Cleaning the "Producers" column:')

df['Producers'] = (df['Producers']
                   .str.replace(r'\[.*?\]', '', regex=True) # Removing brackets
                   .str.replace(r'\s*,\s*', ', ', regex=True).str.strip(', ')
                   .str.replace(r'\n+', ', ', regex=True).str.strip() #replacing "\n+", with ", "
                   .str.replace(r',\s,\s', ', ', regex=True) # removing extra commas substituting with a comma
                   .str.replace(r',\s,\s', ', ', regex=True)) # removing extra commas substituting with a comma

print(f'"{df_backup.iloc[144,7]}" cleaned to: \n"{df.iloc[144,7]}" and so on..\n')

#remove duplicates from 'Producers', 'Genres' and 'Songwriter' column and return as lists
print('removing duplicates from the "Producers", "Genres" and "Songwriter" column and return as lists:')

df['Producers'] = df['Producers'].apply(deduplicate)

print(f'returning: \n"{df.iloc[144,7]}" and so on..\n')

# Drop the 'Lyricist(s)' and 'Composer(s)' columns
print('Dropping the "Lyricist(s)" and "Composer(s)" columns ')

df = df.drop(columns=['Lyricist(s)', 'Composer(s)'])


# Create filepath for saving CSV
output_csv_path = pathlib.Path("data") / "html_cleaned.csv"

# Save cleaned data to the new CSV file
df.to_csv(output_csv_path, index=False)


print(f"{len(df)} rows have been updated, cleaned, and saved to {output_csv_path}")