from dash import html
import dash_ag_grid as dag
import pandas as pd
import pathlib

# Load the dataset
csv_path = pathlib.Path("../data/html_cleaned.csv")
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
    "filter": True,
    "floatingFilter": True,
    "sortable": True,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
    "initialWidth": True,
    "resizable": True,
}

# Function to create a grid layout
def create_grid(data):
    grid = dag.AgGrid(
        id="getting-started-sort",
        rowData=data.to_dict("records"),
        columnDefs=columnDefs,
        defaultColDef=defaultColDef,
        dashGridOptions={'pagination': True,
                         'paginationPageSize': 10
        },
    )
    return html.Div(
        [grid],
        className="p-4 sm:p-2 md:p-6 bg-gray-100 flex flex-col items-center"
    )
