import pandas as pd
import re

# Function to clean citation markers from text
def remove_citations(text):
    if pd.isna(text):  # Handle NaN values
        return text
    return re.sub(r'\[\d+]', '', text).strip()  # Removes [1], [2], etc.


# Function to clean citation markers from text
def remove_citationswcommas(text):
    if pd.isna(text):  # Handle NaN values
        return text
    # Match patterns like [1], [, 1, ], etc.
    return re.sub(r'\[\d+]', '', text).strip()


# Function to clean extra commas
def remove_extra_commas(text):
    if pd.isna(text):  # Handle NaN values
        return text
    # Replace consecutive commas (with optional whitespace) with a single comma
    cleaned_text = re.sub(r' ,', '', text)
    # Remove leading/trailing commas or spaces
    return cleaned_text.strip(', ')


# Function to clean the song lengths
def clean_song_lengths(df, column_name):
    def extract_single_version(length_str):
        # Ensure the value is a string
        if pd.isna(length_str):
            return length_str
        length_str = str(length_str)

        # Split the versions using regex to handle different formats without explicit delimiters
        versions = re.findall(r'\d+:\d+\s*\([^)]+\)', length_str)

        # If there are no additional versions, just return the original length
        if not versions:
            return length_str.strip()

        # Search for the "single version" in the list of versions
        for version in versions:
            if 'single version' in version.lower():
                return re.search(r'\d+:\d+', version).group()

        # If "single version" is not found, return the first version
        return re.search(r'\d+:\d+', versions[0]).group()

    # Apply the extraction function to the specified column
    df[column_name] = df[column_name].apply(extract_single_version)
    return df


# import final scrape csv as dataframe
final_scrape = pd.read_csv('html_scrape.csv', encoding='utf-8')

# Apply the function to clean the 'Release Date' column
final_scrape['Release Date'] = final_scrape['Release Date'].apply(remove_citations)

# apply the function to clean the "Genres" column
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_citationswcommas)

# Apply the function to clean the "Genres" column for extra commas
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_extra_commas)

# Clean the 'Length' column in the loaded DataFrame
final_scrape = clean_song_lengths(final_scrape, 'Length')

# Option to name output csv
csv_name = "final_scrape"

# Save the cleaned data back to a CSV file
final_scrape.to_csv(f'{csv_name}.csv', index=False)
print(f"{len(final_scrape)} Datapoints has been saved to {csv_name}.csv")
