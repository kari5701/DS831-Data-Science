import pathlib

KEYWORDS = ['pop', 'r&b', 'rock', 'soul', 'hip hop', 'disco', 'funk',
            'country', 'electro', 'trap', 'blues', 'folk', 'metal',
            'gospel', 'dance', 'jazz', 'house']

CSV_PATH = pathlib.Path("data/html_cleaned.csv")

def clean_genres(df, keywords):

    genres = set()
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.add(keyword.capitalize())
    return sorted(genres)
