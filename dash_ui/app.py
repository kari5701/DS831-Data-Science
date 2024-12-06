from dash import Dash, html, dcc, Input, Output
import pandas as pd
import pathlib

# Import constants
from src.const import get_constants
from src.dash1 import create_grid

# Load the CSV file into a DataFrame
csv_path = pathlib.Path("/Users/karinachristensen/Documents/GitHub/DS831-Data-Science/data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

# Get constants from the data
constants = get_constants(cleaned_data)

# Initialize the Dash app
app = Dash(__name__)

# Define app layout, including the components from dash1
app.layout = html.Div([
    html.H1("Billboard Artist Top 100"),

    # Including the visualization from dash1 module
    create_grid(cleaned_data),

    # Dropdown for Genres (for demonstration purposes)
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in cleaned_data['Genres'].dropna().unique()],
        placeholder='Select a genre',
        multi=False
    ),

    # Wordcloud Placeholder
    dcc.Graph(id='wordcloud-graph'),

    # Histogram Placeholder
    dcc.Graph(id='length-histogram')
])

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
