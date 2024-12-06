from dash import html
import dash_ag_grid as dag
import pandas as pd
import pathlib

# Load the dataset
csv_path = pathlib.Path("/Users/karinachristensen/Documents/GitHub/DS831-Data-Science/data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

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

# Default column definition for common properties
defaultColDef = {
    "filter": True,  # Enables filtering for all columns
    "floatingFilter": True,  # Adds a quick filter bar below the header
    "sortable": True,  # Enables sorting for all columns
    "wrapHeaderText": True,  # Wraps header text if it's too long
    "autoHeaderHeight": True,  # Automatically adjusts header height
    "initialWidth": 125,  # Sets the initial width of the columns
}

# Function to create a grid layout
def create_grid(data):
    grid = dag.AgGrid(
        id="getting-started-sort",
        rowData=data.to_dict("records"),  # Convert DataFrame to list of dictionaries
        columnDefs=columnDefs,  # Use the updated column definitions
        defaultColDef=defaultColDef,  # Apply the default column settings
        dashGridOptions={'pagination': True},
    )
    return html.Div([grid])