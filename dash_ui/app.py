from dash import Dash, html, dcc, Input, Output
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

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>Billboard Hot 100</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500;700&family=Syne:wght@400..800&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div id="react-entry-point">
        {%app_entry%}
    </div>
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# Define app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div(html.Img(src="./assets/Billboard_logo.png", width=150), className="w-1/6"),
        html.H1("Billboard Artist Hot 100", className="text-3xl font-bold mb-4 text-center text-gray-800"),
    ], className="flex items-center space-x-4 mb-10 bg-white p-4 rounded-lg shadow-md"),

    # Grid Component
    html.Div(create_grid(cleaned_data), className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    # Dropdown for Genres
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in GENRES],
        placeholder='Select a genre',
        multi=True,
        className="mb-5 p-2 border border-gray-300 rounded w-full",
    ),

    html.Div(create_histogram(cleaned_data['total_seconds']), className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    html.Div(create_genre_histogram(cleaned_data, KEYWORDS), className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    # WordCloud Component
    html.Div(create_wordcloud(cleaned_data, KEYWORDS), className="mb-10 p-4 bg-white rounded-lg shadow-md")

], className="container mx-auto p-6 bg-gray-50")

# Define callback to update AgGrid based on dropdown or WordCloud click
@app.callback(
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
    app.run_server(debug=True)
