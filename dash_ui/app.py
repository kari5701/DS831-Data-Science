from dash import Dash, html, dcc, Input, Output
import pandas as pd
import pathlib

# Import constants
from src.const import get_constants
from src.dash1 import create_grid

# Load the CSV file into a DataFrame

csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

# Get constants from the data
constants = get_constants(cleaned_data)

# Initialize the Dash app
app = Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dash med Tailwind</title>
    <link rel="stylesheet" href="/static/css/styles.css">
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

# Define app layout, including the components from dash1
app.layout = html.Div([
    html.Div([
        html.Div(html.Img(src="./assets/Billboard_logo.png", width=150), className="w-1/6"),
        html.H1("Billboard Artist Hot 100", className="text-3xl font-bold mb-4 text-center text-gray-800"),
    ], className="flex items-center space-x-4 mb-10 bg-white p-4 rounded-lg shadow-md"),

    # Including the visualization from dash1 module
    html.Div(create_grid(cleaned_data), className="mb-10 p-4 bg-white rounded-lg shadow-md"),

    # Dropdown for Genres (for demonstration purposes)
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in cleaned_data['Genres'].dropna().unique()],
        placeholder='Select a genre',
        multi=False,
        className="mb-5 p-2 border border-gray-300 rounded w-full"
    ),

    # Wordcloud Placeholder
    dcc.Graph(id='wordcloud-graph', className="mb-5 bg-white p-4 rounded-lg shadow-md"),

    # Histogram Placeholder
    dcc.Graph(id='length-histogram', className="bg-white p-4 rounded-lg shadow-md")
], className="container mx-auto p-6 bg-gray-50")

# Define callback to link dropdown selection to data grid filtering
@app.callback(
    Output("getting-started-sort", 'rowData'),  # Output targets the AgGrid component by ID
    Input('genre-dropdown', 'value')  # Input is the genre dropdown value
)
def update_grid(selected_genre):
    if not selected_genre:
        return cleaned_data.to_dict('records')

    # Filter data based on selected genre
    filtered_data = cleaned_data[cleaned_data['Genres'].str.contains(selected_genre, case=False, na=False)]
    return filtered_data.to_dict('records')

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)