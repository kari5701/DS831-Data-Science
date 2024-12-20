import pandas as pd

csv_path = pd.read_csv("data/html_cleaned.csv")

KEYWORDS = ['pop', 'r&b', 'rock', 'soul', 'hip hop', 'disco', 'funk',
            'country', 'electro', 'trap', 'blues', 'folk', 'metal',
            'gospel', 'dance', 'jazz', 'house', 'New Jack Swing', 
            'Garage', 'Psychedelic', 'Reggae', 'synth', 'new wave' ]

# Define column definitions based on your dataset
columnDefs = [
    {'field': 'Title', 'headerName': 'Song Title'},
    {'field': 'Artist(s)', 'headerName': 'Artists'},
    {'field': 'Release Date', 'headerName': 'Release Date'},
    {'field': 'Genres', 'headerName': 'Genres'},
    {'field': 'Length', 'headerName': 'Song Length'},
    {'field': 'Label', 'headerName': 'Label'},
    {'field': 'Songwriters', 'headerName': 'Songwriters'},
    {'field': 'Producers', 'headerName': 'Producers'},
]

def clean_genres(df, keywords):

    genres = set()
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.add(keyword.capitalize())
    return sorted(genres)
