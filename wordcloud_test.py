import pandas as pd
import base64
import io
from dash import Dash, html, dcc, Input, Output
from wordcloud import WordCloud
import plotly.express as px
import pathlib

# Import constants
from src.const import get_constants
from src.dash1 import create_grid

# ---------------------------
# 1. Load and Preprocess Data
# ---------------------------
csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

# Preprocess Genres: Handle missing genres and explode comma-separated values
cleaned_data['Genres'] = cleaned_data['Genres'].fillna('Unknown')  # Fill NaN
all_genres = cleaned_data['Genres'].str.split(',').explode()  # Flatten genre lists
genre_counts = all_genres.value_counts()  # Count genres

# ---------------------------
# 2. Word Cloud Generator Function
# ---------------------------
def generate_wordcloud(frequencies):
    """Generate a Word Cloud and return as base64-encoded PNG image."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    return "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())

# ---------------------------
# 3. Dash App Initialization
# ---------------------------
app = Dash(__name__)

# Add Tailwind styling
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dash with Tailwind</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body class="bg-gray-100 font-sans">
    <div id="react-entry-point">{%app_entry%}</div>
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
'''

# ---------------------------
# 4. App Layout
# ---------------------------
app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div(html.Img(src="./assets/Billboard_logo.png", width=150), className="w-1/6"),
        html.H1("Billboard Artist Hot 100", className="text-3xl font-bold mb-4 text-center text-gray-800"),
    ], className="flex items-center space-x-4 mb-10 bg-white p-4 rounded-lg shadow-md"),

    # Data Grid Component (from dash1)
    html.Div(create_grid(cleaned_data), className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    # Dropdown for filtering Word Cloud
    html.Div([
        html.H3("Filter by Genre", className="text-xl font-semibold text-center mb-4"),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in all_genres.unique()],
            placeholder="Select a genre",
            multi=False,
            className="mb-5 p-2 border border-gray-300 rounded w-1/2 mx-auto"
        ),
    ]),

    # Word Cloud Visualization
    html.Div([
        html.H3("Word Cloud", className="text-xl font-semibold text-center"),
        html.Img(id="wordcloud-image", src=generate_wordcloud(genre_counts), style={'width': '100%', 'height': 'auto'}),
    ], className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    # Histogram Placeholder (You can fill this later)
    dcc.Graph(id='length-histogram', className="bg-white p-4 rounded-lg shadow-md")
], className="container mx-auto p-6 bg-gray-50")

# ---------------------------
# 5. Callbacks for Word Cloud
# ---------------------------
@app.callback(
    Output('wordcloud-image', 'src'),  # Output: Update Word Cloud image
    Input('genre-dropdown', 'value')   # Input: Dropdown value
)
def update_wordcloud(selected_genre):
    """Update Word Cloud based on the selected genre."""
    if selected_genre:  # Filter data based on selected genre
        filtered_genres = cleaned_data[cleaned_data['Genres'].str.contains(selected_genre, case=False, na=False)]
        filtered_counts = filtered_genres['Genres'].str.split(',').explode().value_counts()
        return generate_wordcloud(filtered_counts)
    # Return overall Word Cloud if no filter is selected
    return generate_wordcloud(genre_counts)

# ---------------------------
# 6. Run the App
# ---------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
