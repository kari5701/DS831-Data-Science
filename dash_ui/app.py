from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import pathlib

from src.const import clean_genres, KEYWORDS
from src.dash1 import create_grid
from src.dash2 import create_histogram, create_genre_histogram
from src.dash3 import create_wordcloud

# Load the CSV file into a DataFrame
csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)
cleaned_data['Genres'] = cleaned_data['Genres'].fillna("")

# Genre List
GENRES = clean_genres(cleaned_data, KEYWORDS)


# Initialize the Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div(html.Img(src="./assets/Billboard_logo.png", width=150), className="w-1/6"),
        html.H1(style={'color': 'white', 'textAlign': 'center'}, children='Billboard Analysis'),
    ]),
    # Grid Component
    html.Div(create_grid(cleaned_data)),

    # Dropdown for Genres
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in GENRES],
        placeholder='Select a genre',
        multi=True,
        ),

    # Length histogram Component
    html.Div(create_histogram(
        cleaned_data['total_seconds']), 
        id='length-histogram',
        ),

    # Genre histogram Component
    html.Div(create_genre_histogram(
        cleaned_data, KEYWORDS),
        id='genre-histogram', 
        ),

    # WordCloud Component
    html.Div(create_wordcloud(cleaned_data, KEYWORDS), 
        id='wordcloud-graph',
        )

])

# define callback functions:

#  allback to update AgGrid based on dropdown or WordCloud click
@callback(
    Output("getting-started-sort", 'rowData'),
    [Input('genre-dropdown', 'value'),
     Input("wordcloud-graph", "clickData")]
)
def update_grid(selected_genre, clickData):
    filtered_data = cleaned_data

    # Filter by dropdown selection
    if selected_genre:
        regex_pattern = '|'.join(selected_genre)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]

    # Filter by WordCloud click
    if clickData and 'points' in clickData:
        selected_word = clickData['points'][0].get('text', '')
        if selected_word:
            filtered_data = filtered_data[filtered_data['Genres'].str.contains(selected_word, case=False, na=False)]

    # NaN values
    if filtered_data.empty:
        return []

    return filtered_data.to_dict('records')


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
