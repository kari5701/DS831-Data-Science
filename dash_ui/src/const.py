import pandas as pd
import pathlib

def get_constants(df):
    num_of_songs = df.shape[0]

    genres = df['Genres'].str.split(',').explode().value_counts().index
    num_of_genres = len(genres)

    artists = df['Artist(s)'].str.split(',').explode().value_counts().index
    num_of_artists = len(artists)

    length = df['total_seconds']
    num_of_length = len(artists)

    producers = df['Producers'].str.split(',').explode().value_counts().index
    num_of_producers = len(producers)

    songwriters = df['Songwriters'].str.split(',').explode().value_counts().index
    num_of_songwriters = len(songwriters)

    return {
        "num_of_songs": num_of_songs,
        "num_of_genres": num_of_genres,
        "num_of_artists": num_of_artists,
        "num_of_length": num_of_length,
        "num_of_producers": num_of_producers,
        "num_of_songwriters": num_of_songwriters,
        "genres": genres,  # Bruges til wordcloud
        "artists": artists,  # Bruges til browsing
        "producers": producers,  # Bruges til browsing
        "songwriters": songwriters  # Bruges til browsing
    }

# Load the cleaned dataset
csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

constants = get_constants(cleaned_data)

# Eksempel på brug af konstanter
def print_constants(constants):
    print(f"Antal sange: {constants['num_of_songs']}")
    print(f"Antal genrer: {constants['num_of_genres']}")
    print(f"Antal artister: {constants['num_of_artists']}")
    print(f"Antal producenter: {constants['num_of_producers']}")
    print(f"Antal sangskrivere: {constants['num_of_songwriters']}")

# print_constants(constants)
